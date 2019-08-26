# Weichao Qiu @ 2019
# Script to show all car appearance
import unrealcv
from unrealcv.util import read_png, read_npy
from unrealcv_util import request, clear, get_im, show_im
import imageio
from tqdm import tqdm
import os, sys

client = unrealcv.Client(('localhost', 9000))
client.connect()

def set_angle(fl, fr, bl, br, hood, trunk):
    client.request('vset /car/0/door/angles {fl} {fr} {bl} {br} {hood} {trunk}'.format(**locals()))

def set_mesh_id(mesh_id):
    # The mesh_dir needs to end with /
    client.request('vset /car/0/mesh/id {mesh_id}'.format(**locals()))

def get_image(dist, az, el):
    client.request('vset /car/0/camera {dist} {az} {el}'.format(**locals()))
    lit = client.request('vget /car/0/image'.format(**locals()))
    lit = read_png(lit)
    return lit

def get_seg():
    seg = client.request('vget /car/0/seg'.format(**locals()))
    seg = read_png(seg)
    return seg

def str_color(color):
    return '%d %d %d' % (color[0], color[1], color[2])

def set_car_seg_color(color):
    color = str_color(color)
    client.request('vset /car/0/annotation/obj {color}'.format(**locals()))

def set_part_seg_color(fl, fr, bl, br, hood, trunk, body):
    fl = str_color(fl); fr = str_color(fr)
    bl = str_color(bl); br = str_color(br)
    hood = str_color(hood); trunk = str_color(trunk)
    body = str_color(body)
    client.request('vset /car/0/annotation/parts {fl} {fr} {bl} {br} {hood} {trunk} {body}'.format(**locals()))

def set_mesh_texture(texture_filename):
    client.request('vset /car/0/mesh/texture {texture_filename}'.format(**locals()))

def make_filename(mesh_id, fl, fr, bl, br, trunk, dist, az, el):
    template = '{mesh_id}_{fl}_{fr}_{bl}_{br}_{trunk}_{dist}_{az}_{el}.png'
    filename = template.format(**locals())
    return filename

def main():
    with open('manual.txt') as f:
        shapenet_id = [l.strip() for l in f.readlines()]
    preset_id = ['suv', 'hybrid', 'hatchback', 'sedan2door', 'sedan4door']
    mesh_ids = shapenet_id + preset_id

    mesh_folder = "/Game/ShapenetManual/"
    meta_folder = os.path.abspath('ShapenetManual_metadata/')
    fl = 30; fr = 30; bl = 30; br = 30; trunk = 30; 
    dist = 300; az = 0; el = 30
    
    client.request('vset /car/0/mesh/folder {mesh_folder} {meta_folder}'.format(**locals()))
    for mesh_id in mesh_ids:
        filename = make_filename(mesh_id, fl, fr, bl, br, trunk, dist, az, el)

        set_mesh_id(mesh_id)
        set_mesh_texture(texture_filename)
        set_angle(fl, fr, bl, br, 0, trunk)
        lit = get_image(dist, az, el)
        imageio.imwrite(filename, lit)
        set_car_seg_color([128, 0, 0])
        seg = get_seg()
        imageio.imwrite(filename + '_full_seg.png', seg)
        set_part_seg_color(
            [0, 0, 0], [0, 0, 128],  # fl, fr
            [0, 128, 0], [0, 128, 128], # bl, br 
            [128, 0, 0], [128, 0, 128], # hood, trunk
            [128, 128, 0]  # body
        )
        seg = get_seg()
        imageio.imwrite(filename + '_part_seg.png', seg)
        lit = get_image(dist, az, el)
        imageio.imwrite(filename, lit)

if __name__ == '__main__':
    main()