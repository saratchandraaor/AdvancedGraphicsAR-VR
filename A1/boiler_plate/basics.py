from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import glm
import trimesh
import moderngl
import numpy as np
import moderngl_window
from pathlib import Path


class basics(moderngl_window.WindowConfig):
    resizable = False
    window_size = [1024, 1024]
    aspect_ratio = window_size[0] / window_size[1]
    gl_version = [4, 6]
    resource_dir = Path('.').absolute()
    title = 'basics'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        mesh_model = trimesh.load('data/models/monkey.obj')

        self.program = self.ctx.program(vertex_shader=open('data/shaders/basics.vert.glsl').read(),
                                        fragment_shader=open('data/shaders/basics.frag.glsl').read())
        
        v, n, uv = mesh_model.vertices, mesh_model.vertex_normals, mesh_model.visual.uv
        faces = mesh_model.faces

        # Convert to byte data while getting buffers --> tobytes()
        vbo = self.ctx.buffer(np.array(v).astype('float32').tobytes())  # Vertices are float32/f4
        nbo = self.ctx.buffer(np.array(n).astype('float32').tobytes())  # Vertex Normals are float32/f4
        uvbo = self.ctx.buffer(np.array(uv).astype('float32').tobytes()) # UV are float32/f4

        fbo = self.ctx.buffer(np.array(faces).astype('uint32').tobytes()) # faces are unsigned int

        # defined contents of vao - Vertex array object which sends the buffer objects into shader phase
        vao_content = [
            (vbo, '3f', 'in_vertex'),
            (nbo, '3f', 'in_normal'),
            (uvbo, '2f', 'in_uv')
        ]
        # load a texture
        texture = self.load_texture_2d('data/textures/uv_tex.jpg')
        texture.use(0)  # 0 tell which sampler2D this texture needs to be linked with (use number 1 if you are using 2nd texture)

        # index element size of is 4 because of the unsinged int we have used in face data
        self.vao = self.ctx.vertex_array(self.program, vao_content, fbo, index_element_size=4)

        model_matrix = glm.mat4(1.)      # use glm.translate glm.scale glm.rotate based on the requirement
        view_matrix = glm.lookAt(
            glm.vec3(10., 10., 10.),      # location of camera in world space
            glm.vec3(0, 0, 0.),           # location where camera needs to see
            glm.vec3(0., 1., 0.)          # orientation of camera      
        )
        projection_matrix = glm.perspective(glm.radians(60),    # field of View
                                            self.aspect_ratio,  # aspect ratio
                                            0.1,                # near plane 
                                            100.                # far plane
                                            )

        self.program['model'].write(model_matrix)
        self.program['view'].write(view_matrix)
        self.program['projection'].write(projection_matrix)

    
    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys
        if action == keys.ACTION_PRESS:
            if key == keys.W:
                pass            # handling event when 'w' is pressed # alter according to your logic
                print('Key W pressed')
    
    def render(self, time, frame_time):
        self.ctx.clear(1., 1., 1.)  # clear screen buffer
        self.ctx.enable(moderngl.DEPTH_TEST)
        
        # dynamically altering camera location
        view = glm.lookAt(
                            5 * glm.vec3(glm.sin(glm.radians(time)), 0, glm.cos(glm.radians(time))), 
                            glm.vec3(0., 0., 0.),
                            glm.vec3(0, 1, 0))
        self.program['view'].write(view)

        self.vao.render()   # renders the buffer based on the vertex array content sent
    

    @classmethod
    def run(cls):
        moderngl_window.run_window_config(cls)


basics.run()