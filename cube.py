import taichi as ti
ti.init()
def draw_bounds(x_min=0, y_min=0, z_min=0, x_max=1, y_max=1, z_max=1):
    box_anchors = ti.Vector.field(3, dtype=ti.f32, shape = 8)
    box_anchors[0] = ti.Vector([x_min, y_min, z_min])
    box_anchors[1] = ti.Vector([x_min, y_max, z_min])
    box_anchors[2] = ti.Vector([x_max, y_min, z_min])
    box_anchors[3] = ti.Vector([x_max, y_max, z_min])
    box_anchors[4] = ti.Vector([x_min, y_min, z_max])
    box_anchors[5] = ti.Vector([x_min, y_max, z_max])
    box_anchors[6] = ti.Vector([x_max, y_min, z_max])
    box_anchors[7] = ti.Vector([x_max, y_max, z_max])

    box_lines_indices = ti.field(int, shape=(2 * 12))
    for i, val in enumerate([0, 1, 0, 2, 1, 3, 2, 3, 4, 5, 4, 6, 5, 7, 6, 7, 0, 4, 1, 5, 2, 6, 3, 7]):
        box_lines_indices[i] = val
    return box_anchors, box_lines_indices


window = ti.ui.Window("visualizer", (1080, 720), vsync=True)
camera = ti.ui.Camera()
camera.position(5,5,5)
camera.lookat(0,0,-1)
camera.fov(45) 
canvas = window.get_canvas()
canvas.set_background_color((1,1,1))
scene = ti.ui.Scene()

box_anchors, box_lines_indices = draw_bounds(x_min=0, y_min=0, z_min=0, x_max=1, y_max=1, z_max=1)

while window.running:
    camera.track_user_inputs(window, movement_speed=0.03, hold_key=ti.ui.RMB)
    scene.set_camera(camera)
    scene.point_light(pos=(0, 1, 2), color=(1, 1, 1))
    scene.ambient_light((0.5, 0.5, 0.5))
    scene.lines(box_anchors, indices=box_lines_indices, color = (0.99, 0.68, 0.28), width = 2.0)

    canvas.scene(scene)
    window.show()
