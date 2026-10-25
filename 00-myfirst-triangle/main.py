
import glfw
import moderngl
import numpy as np

# Criar janela e contexto OpenGL
if not glfw.init():
    raise RuntimeError("Falha ao inicializar GLFW")

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

window = glfw.create_window(800, 600, "Meu primeiro triangulo", None, None)

if not window:
    glfw.terminate()
    raise RuntimeError("Falha ao criar janela")

glfw.make_context_current(window)
ctx = moderngl.create_context()

# Shaders
vertex_shader = """
#version 330

in vec2 in_position;

void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
}
"""

fragment_shader = """
#version 330

out vec4 fragColor;

void main() {
    fragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
"""

program = ctx.program(
    vertex_shader=vertex_shader,
    fragment_shader=fragment_shader,
)

# Geometria
vertices = np.array([
     0.0,  0.5,
    -0.5, -0.5,
     0.5, -0.5,
], dtype="f4")

vbo = ctx.buffer(vertices.tobytes())

vao = ctx.vertex_array(
    program,
    [(vbo, "2f", "in_position")]
)

# Loop de renderização
while not glfw.window_should_close(window):
    width, height = glfw.get_framebuffer_size(window)
    ctx.viewport = (0, 0, width, height)

    ctx.clear(0.1, 0.1, 0.1, 1.0)
    vao.render(mode=moderngl.TRIANGLES)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
