import unrealcv
from unrealcv_util import UnrealcvUtil
import ipynb_util
import os
from tqdm import tqdm
import imageio

data_dir = './example/'
if not os.path.isdir(data_dir): data_dir = './'

def list_mesh_id():
    with open(data_dir + 'selected.txt') as f:
        shapenet_selected = [l.strip() for l in f.readlines()]
    with open(data_dir + 'manual.txt') as f:
        shapenet_manual = [l.strip() for l in f.readlines()]
    preset_id = ['suv', 'hybrid', 'hatchback', 'sedan2door', 'sedan4door']
    # mesh_ids = shapenet_id + preset_id
    # mesh_ids = shapenet_id
    mesh_ids = shapenet_selected
    return mesh_ids

def main():
    client = unrealcv.Client(('localhost', 9000))
    client.connect()
    util = UnrealcvUtil(client)

    util.DEBUG=False
    util.clear()
    mesh_folder = "/Game/ShapenetManual/" # need to end with /
    meta_folder = os.path.abspath(data_dir + 'ShapenetManual_metadata/')

    mesh_ids = list_mesh_id()
    ims = []
    segs = []
    for mesh_id in tqdm(mesh_ids):
        util.clear()
        obj_id = 'demo_car'
        util.make_demo_car(obj_id)
        util.request('vset /car/{obj_id}/mesh/folder {mesh_folder} {meta_folder}'.format(**locals()))
        util.request('vset /car/{obj_id}/mesh/id {mesh_id}'.format(**locals()))
        util.request('vset /car/{obj_id}/door/angles 30 30 30 30 30 30'.format(**locals()))
        util.request('vset /object/{obj_id}/location 0 0 130'.format(**locals()))
        util.set_car_part_seg_color(obj_id, 
            [0, 0, 0], [0, 0, 128],  # fl, fr
            [0, 128, 0], [0, 128, 128], # bl, br 
            [128, 0, 0], [128, 0, 128], # hood, trunk
            [128, 128, 0]  # body
        )    
        util.cam_track_obj(obj_id, 45 + 180, 45, 300)

        ims.append(util.get_im())
        segs.append(util.get_seg())
        # imageio.imwrite(mesh_id + '_im.png', util.get_im())
        # imageio.imwrite(mesh_id + '_seg.png', util.get_seg())
    
    fig = ipynb_util.imshow_grid(ims, 3)
    fig.savefig('car_shapenet_im.png')
    fig = ipynb_util.imshow_grid(segs, 3)
    fig.savefig('car_shapenet_seg.png')

if __name__ == '__main__':
    main()