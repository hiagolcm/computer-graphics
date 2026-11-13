import glfw
import glm
import moderngl
import numpy as np

glfw.init()

window = glfw.create_window(800, 800, "rotation", None, None)

glfw.make_context_current(window)

ctx = moderngl.create_context()

vertex_shader = """
#version 400

in vec2 in_position;
uniform mat4 m;

void main() {
    gl_Position = m * vec4 (in_position.x, in_position.y, 0, 1);
}
"""

fragment_shader = """
#version 400

out vec4 fragColor;

void main() {
    fragColor = vec4(1,0,0,1);
}
"""

program = ctx.program(vertex_shader, fragment_shader)
vertices = np.array([0, 0, 0, 0.5, 0.5, 0, 0.5, 0.5], dtype="f4")
indices = np.array([[0, 1, 2, 1, 3, 2]], dtype="u4")
vbo = ctx.buffer(vertices.tobytes())
ebo = ctx.buffer(indices.tobytes())
vba = ctx.vertex_array(program, [(vbo, "2f", "in_position")], index_buffer=ebo)

T = glm.translate(glm.mat4(1.0), glm.vec3(0.25, 0.25, 0))
T2 = glm.translate(glm.mat4(1.0), glm.vec3(-0.25, -0.25, 0))

while not glfw.window_should_close(window):
    ctx.clear(0.1, 0.1, 0.1, 1)
    R = glm.rotate(glm.mat4(1.0), glm.radians(glfw.get_time() * 50), glm.vec3(0, 0, 1))
    M = T  * R * T2
    program["m"].write(M.to_bytes())
    vba.render(mode=moderngl.TRIANGLES)
    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
