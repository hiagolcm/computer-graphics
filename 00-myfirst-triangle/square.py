import glfw
import moderngl
import numpy as np

glfw.init()
window = glfw.create_window(600, 600, "My firstsquare", None, None)

if not window:
    raise RuntimeError("window failed")
    glfw.terminate()


glfw.make_context_current(window)
ctx = moderngl.create_context()

vertices = np.array(
    [0, 0, 0, 0.5, 0.5, 0, 0.5, 0.5], dtype="f4"
)

indieces = np.array([[0, 1, 2, 1, 3, 2]], dtype ="u4")


vertex_shader = """
#version 400

in vec2 in_position;

void main() {
    gl_Position = vec4 (in_position.x, in_position.y, 0, 1);
}
"""

fragment_shader = """
#version 400

out vec4 fragColor;

void main() {
    fragColor = vec4 (1,0,0,1);
}
"""

program = ctx.program(vertex_shader, fragment_shader)
vbo = ctx.buffer(vertices.tobytes())
ebo = ctx.buffer(indieces.tobytes())
vba = ctx.vertex_array(program, [(vbo, "2f", "in_position")], index_buffer = ebo)

while not glfw.window_should_close(window):
    ctx.clear(0.1, 0.1, 0.1, 1.0)
    vba.render(mode=moderngl.TRIANGLES)
    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
