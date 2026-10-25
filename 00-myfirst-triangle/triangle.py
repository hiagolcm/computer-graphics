import glfw
import moderngl
import numpy as np

glfw.init();
window = glfw.create_window(800, 600, "Triangulo", None, None);
glfw.make_context_current(window);

ctx = moderngl.create_context()

verts = np.array([
     0.0,  0.5,
    -1, -0.5,
     1, -0.5,
], dtype="f4")

vertex_shader = """
#version 400

in vec2 in_position;

void main() {
    gl_Position = vec4(in_position.x + 0.5, in_position.y, 0, 1);
}

"""

fragment_shader = """
#version 400

out vec4 fragColor;

void main() {
    fragColor = vec4(0.0, 1.0, 0.0, 1.0);
}
"""

program = ctx.program(vertex_shader, fragment_shader)

vbo = ctx.buffer(verts.tobytes())

vao = ctx.vertex_array(program, [(vbo, '2f', 'in_position')])


while not glfw.window_should_close(window):
    width, height = glfw.get_framebuffer_size(window)
    ctx.viewport = (0, 0, width, height)

    ctx.clear(0.1, 0.1, 0.1, 1.0)
    vao.render(mode=moderngl.TRIANGLES)

    glfw.swap_buffers(window)
    glfw.poll_events()
glfw.terminate();