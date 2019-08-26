import matplotlib.pyplot as plt
import itertools
from tqdm import tqdm
import imageio
import numpy as np
from unrealcv import client
import os
import PIL
from PIL import Image

client.connect()

texture_img = 'C:/qiuwch/code/AnimalParsing/animal_dev/google.png'
opt = dict(
    # mesh = animal_util.mesh_paths,
    mesh = [animal_util.mesh_paths[0]],
    anim = [animal_util.anim_paths[0]],
    ratio = np.arange(0, 1, 0.1),
    # ratio = [0],
    dist = [300],
    az = [0],
    el = [30],
    texture = [texture_img],
)

def parse_kpts(filename):
    obj_filename = 'animal_obj'+filename.replace('.png', '.obj')
    client.request('vget /animal/tiger/vertex {obj_filename}'.format(**locals()))
    obj_path = '/media/jm/000C65DB000784DF/unreal_engine/UnrealEngine/Engine/Binaries/Linux/'
    kpts_3d_array = np.zeros((3299, 3))

    # with open(obj_path+obj_filename, 'r') as f:
    #     data = f.readlines() 
    #     for i, line in enumerate(data):
    #         _, x, y, z = line.split(' ')
    #         kpts_3d_array[i] = float(x), float(y), float(z)+138.17-80
    return kpts_3d_array

# Need to be abspath
floor = '/media/jm/000C65DB000784DF/unreal_engine/AnimalParsing/animal_dev/synthetic_data/grass1.jpg'
# sky = '/media/jm/000C65DB000784DF/unreal_engine/AnimalParsing/animal_dev/sky1.jpg'
# floor = 'C:/qiuwch/code/AnimalParsing/animal_dev/google.png'
# sky = os.path.abspath('google.png')
sky = floor

render_params = itertools.product(opt['mesh'], opt['anim'], opt['ratio'],
    opt['dist'], opt['az'], opt['el'], opt['texture'])
render_params = list(render_params)

def set_texture(obj, texture):
    client.request('vset /animal/{obj}/texture {texture}'.format(**locals()))

obj = 'tiger'
num_imgs = 0
for param in tqdm(render_params):
    mesh, anim, ratio, dist, az, el, texture = param
    filename = animal_util.make_filename(mesh, anim, ratio,
        dist, az, el)
    # im, seg, depth, kp, kp_3d = animal_util.capture('human', mesh_path, anim_path, ratio, dist, az, el)
    animal_util.set_animation(obj, mesh, anim, ratio)
    animal_util.set_env(floor, sky)
    set_texture(obj, texture)

    lit, seg, depth = animal_util.get_image(obj, dist, az, el)
    cam_loc, cam_rot = animal_util.get_camera_params()


    # ## get kp_3d_array with the shape [num_kpts,3]
    # kp, kp_3d = animal_util.get_kp(obj) # get kpts from skeleton
    # kp_3d_array = np.zeros((len(kp_3d), 3))
    # for i in range(len(kp_3d)):
    #     kp_3d_array[i][0] = kp_3d[i]['KpWorld']['X']
    #     kp_3d_array[i][1] = kp_3d[i]['KpWorld']['Y']
    #     kp_3d_array[i][2] = kp_3d[i]['KpWorld']['Z']
    
    ## get cam_loc and cam_rot
    cam_loc, cam_rot = animal_util.get_camera_params()
    cam_loc = [float(item) for item in cam_loc.split(' ')]
    cam_rot = [float(item) for item in cam_rot.split(' ')]
    
    ## transform keypoints
    kp_3d_array = parse_kpts(filename)
    kpts = animal_util.transform_kpts(cam_loc, cam_rot, kp_3d_array, depth)    

    ## transform images and kpts
    img = Image.fromarray(lit[:,:,:3])
    seg = Image.fromarray(seg[:,:,:3]).convert('L')
    seg=np.asarray(seg.getdata(),dtype=np.uint8).reshape((seg.size[1],seg.size[0]))
    seg[seg!=52] = 0 # tiger/horse
    seg[seg==52] = 255 # tiger/horse

    ## save images and keypoints
    imageio.imwrite('./synthetic_data/'+filename + '_img.png', lit)
    imageio.imwrite('./synthetic_data/'+filename + '_seg.png', seg)
    np.save('./synthetic_data/'+filename + '_depth.npy', depth)
    np.save('./synthetic_data/'+filename + '_kpts.npy', kpts)

    num_imgs += 1
    if num_imgs>20:
        break