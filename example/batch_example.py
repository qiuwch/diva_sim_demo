# Simple snippet to generate a car image dataset
import itertools
from tqdm import tqdm

preset_id = ['suv', 'hybrid', 'hatchback', 'sedan2door', 'sedan4door']
opt = dict(
    # mesh_id = shapenet_id,
    mesh_id = preset_id,
    fl = [-30],
    fr = [30],
    bl = [-30],
    br = [30],
    trunk = [30], 
    az = [0, 90, 180, 270],
    el = [30],
    dist = [400],
)
render_params = itertools.product(opt['mesh_id'], 
    opt['fl'], opt['fr'], opt['bl'], opt['br'], opt['trunk'],
    opt['dist'], opt['az'], opt['el'])
render_params = list(render_params)

def make_filename():
    pass

def capture_frame(param):
    mesh_id, fl, fr, bl, br, trunk, dist, az, el = param
    filename = make_filename(mesh_id, fl, fr, bl, br, trunk, dist, az, el)

    set_mesh_id(mesh_id)
    # set_mesh_texture(texture_filename)
    # Change the texture image of the car
    # If you don't this, comment this line.
    set_angle(fl, fr, bl, br, 0, trunk)

    lit = get_image(dist, az, el)
    imageio.imwrite(filename, lit)

    set_car_seg_color([128, 0, 0])
    # seg = get_seg()
    # imageio.imwrite(filename + '_full_seg.png', seg)

    set_part_seg_color(
        [0, 0, 0], [0, 0, 128],  # fl, fr
        [0, 128, 0], [0, 128, 128], # bl, br 
        [128, 0, 0], [128, 0, 128], # hood, trunk
        [128, 128, 0]  # body
    )
    # seg = get_seg()
    # imageio.imwrite(filename + '_part_seg.png', seg)
    # lit = get_image(dist, az, el)
    # imageio.imwrite(filename, lit)
    
# for param in tqdm(render_params):
#     capture_frame(param)