
import glfw
import moderngl
import numpy as np

# Criar janela e contexto OpenGL
if not glfw.init():
    raise RuntimeError("Falha ao inicializar GLFW")

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.SRGB_CAPABLE, True)
GL_FRAMEBUFFER_SRGB = 0x8DB9

window = glfw.create_window(800, 400, "Meu primeiro triangulo", None, None)

largura, altura = glfw.get_framebuffer_size(window)
metade = largura // 2

if not window:
    glfw.terminate()
    raise RuntimeError("Falha ao criar janela")

glfw.make_context_current(window)
ctx = moderngl.create_context()

# Shaders
vertex_shader = """
#version 330

in vec2 in_position;
in vec3 in_color;

out vec3 color;

void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
    color = in_color;
}
"""

fragment_shader = """
#version 330

in vec3 color;

out vec4 fragColor;

void main() {
    fragColor = vec4(color, 1.0);
}
"""

program = ctx.program(
    vertex_shader=vertex_shader,
    fragment_shader=fragment_shader,
)

# Geometria
vertices = np.array([
    # posição       # cor RGB
    -0.5, -0.5,     0.0, 1.0, 0.0,  # verde
     0.5, -0.5,     0.0, 0.0, 1.0,  # azul
     0.0,  0.5,     1.0, 0.0, 0.0,  # vermelho
], dtype='f4')

vbo = ctx.buffer(vertices.tobytes())

vao = ctx.vertex_array(
    program,
    [(vbo, "2f 3f", "in_position", "in_color")]
)

# Loop de renderização
while not glfw.window_should_close(window):
    ctx.clear(0.1, 0.1, 0.1, 1.0)

    ctx.disable_direct(GL_FRAMEBUFFER_SRGB)
    ctx.viewport = (0, 0, metade, altura)
    vao.render(mode=moderngl.TRIANGLES)

    ctx.enable_direct(GL_FRAMEBUFFER_SRGB)
    ctx.viewport = (metade, 0, metade, altura)
    vao.render(mode=moderngl.TRIANGLES)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()

ctx.finish()

quadro = np.frombuffer(
    ctx.screen.read(components=3),
    dtype='u1'
)

print(quadro)