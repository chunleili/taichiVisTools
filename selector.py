import taichi as ti
import numpy as np
import trimesh

ti.init()

mesh = trimesh.load("data/model/bunny.obj")
particles = ti.Vector.field(3, dtype=ti.f32, shape=mesh.vertices.shape[0])
particles.from_numpy(mesh.vertices)
rect_verts = ti.Vector.field(2, dtype=ti.f32, shape=8)
per_vertex_color = ti.Vector.field(3, dtype=ti.f32, shape=particles.shape[0])
per_vertex_color.fill([0.1229,0.2254,0.7207])
screen_pos = ti.Vector.field(2, shape=particles.shape[0], dtype=float)
is_in_rect = ti.field(dtype=ti.i32, shape=particles.shape[0])

def select_particles(world_pos, proj, view, start, end, per_vertex_color):
    view_ti = ti.math.mat4(view)
    proj_ti = ti.math.mat4(proj)
    leftbottom = [min(start[0], end[0]), min(start[1], end[1])]
    righttop   = [max(start[0], end[0]), max(start[1], end[1])]

    @ti.kernel
    def world_to_screen_kernel(world_pos:ti.template()):
        for i in range(world_pos.shape[0]):
            pos_homo = ti.math.vec4([world_pos[i][0], world_pos[i][1], world_pos[i][2], 1.0])
            ndc = pos_homo @ view_ti @ proj_ti #CAUTION: right multiply
            ndc /= ndc[3]

            screen_pos[i][0] = ndc[0]
            screen_pos[i][1] = ndc[1]
            #from [-1,1] scale to [0,1]
            screen_pos[i][0] = (screen_pos[i][0] + 1) /2
            screen_pos[i][1] = (screen_pos[i][1] + 1) /2
        
    @ti.kernel
    def judge_point_in_rect_kernel():
        for i in range(screen_pos.shape[0]):
            if  screen_pos[i][0] > leftbottom[0] and\
                screen_pos[i][0] < righttop[0] and\
                screen_pos[i][1] > leftbottom[1] and\
                screen_pos[i][1] < righttop[1]:
                is_in_rect[i] = True
                per_vertex_color[i] = [1,0,0]
    
    world_to_screen_kernel(world_pos)
    judge_point_in_rect_kernel()


def rect(x_min, y_min, x_max, y_max):
    rect_verts[0] = [x_min, y_min]
    rect_verts[1] = [x_max, y_min]
    rect_verts[2] = [x_min, y_max]
    rect_verts[3] = [x_max, y_max]
    rect_verts[4] = [x_min, y_min]
    rect_verts[5] = [x_min, y_max]
    rect_verts[6] = [x_max, y_min]
    rect_verts[7] = [x_max, y_max]


def visualize(particle_pos):
    window = ti.ui.Window("visualizer", (1080, 720), vsync=True)
    camera = ti.ui.Camera()
    camera.position(0,0,0)
    camera.lookat(0,0,-1)
    camera.fov(45) 
    canvas = window.get_canvas()
    canvas.set_background_color((1,1,1))
    scene = ti.ui.Scene()
    
    viewport_width, viewport_hight = window.get_window_shape()
    start = (-1e5,-1e5)
    end   = (1e5,1e5)

    while window.running:
        camera.track_user_inputs(window, movement_speed=0.03, hold_key=ti.ui.RMB)
        scene.set_camera(camera)
        scene.point_light(pos=(0, 1, 2), color=(1, 1, 1))
        scene.ambient_light((0.5, 0.5, 0.5))
        scene.particles(particle_pos, radius=0.01, per_vertex_color=per_vertex_color)

        if window.is_pressed(ti.ui.LMB):
            per_vertex_color.fill([0.1229,0.2254,0.7207])
            start = window.get_cursor_pos()
            if window.get_event(ti.ui.RELEASE):
                end = window.get_cursor_pos()
            rect(start[0], start[1], end[0], end[1])
            canvas.lines(vertices=rect_verts, color=(1,0,0), width=0.005)

            proj = camera.get_projection_matrix(viewport_width/viewport_hight)
            view = camera.get_view_matrix()
            select_particles(particle_pos, proj, view, start, end, per_vertex_color)
        canvas.scene(scene)
        window.show()


visualize(particles)