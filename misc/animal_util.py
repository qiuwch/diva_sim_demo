# pip install unrealcv before runing this script
from unrealcv import client
from unrealcv.util import read_png, read_npy
import json
import matplotlib.pyplot as plt
import re
import d3
import numpy as np

client.connect()

mesh_paths = [
    "SkeletalMesh'/Game/Animal_pack_ultra_2/Meshes/Tiger/SK_tiger.SK_tiger'",
    # "SkeletalMesh'/Game/Animal_pack_ultra_2/Meshes/Zebra/SK_zebra.SK_zebra'",
    # "SkeletalMesh'/Game/Animal_pack_ultra_2/Meshes/Horse/SK_horse_skeleton.SK_horse_skeleton'",
]

# # tiger paths
anim_paths = [
    "AnimSequence'/Game/Animal_pack_ultra_2/Animations/tiger_attackA_anim.tiger_attackA_anim'",
    "AnimSequence'/Game/Animal_pack_ultra_2/Animations/tiger_attackB_anim.tiger_attackB_anim'",
    "AnimSequence'/Game/Animal_pack_ultra_2/Animations/tiger_death_anim.tiger_death_anim'",
    "AnimSequence'/Game/Animal_pack_ultra_2/Animations/tiger_eat_anim.tiger_eat_anim'",
    "AnimSequence'/Game/Animal_pack_ultra_2/Animations/tiger_idleA_anim.tiger_idleA_anim'",
    "AnimSequence'/Game/Animal_pack_ultra_2/Animations/tiger_idleB_anim.tiger_idleB_anim'",
    "AnimSequence'/Game/Animal_pack_ultra_2/Animations/tiger_roar_anim.tiger_roar_anim'",
    "AnimSequence'/Game/Animal_pack_ultra_2/Animations/tiger_run_anim.tiger_run_anim'",
    "AnimSequence'/Game/Animal_pack_ultra_2/Animations/tiger_walk_anim.tiger_walk_anim'",
]

# horse paths
# anim_paths = [
#     "AnimSequence'/Game/Animal_pack_ultra_2/Animations/horse_death_anim.horse_death_anim'",
#     "AnimSequence'/Game/Animal_pack_ultra_2/Animations/horse_eat_anim.horse_eat_anim'",
#     "AnimSequence'/Game/Animal_pack_ultra_2/Animations/horse_idleA_anim.horse_idleA_anim'",
#     "AnimSequence'/Game/Animal_pack_ultra_2/Animations/horse_idleB_anim.horse_idleB_anim'",
#     "AnimSequence'/Game/Animal_pack_ultra_2/Animations/horse_jump_anim.horse_jump_anim'",
#     "AnimSequence'/Game/Animal_pack_ultra_2/Animations/horse_run_anim.horse_run_anim'",
#     "AnimSequence'/Game/Animal_pack_ultra_2/Animations/horse_turn_left_anim.horse_turn_left_anim'",
#     "AnimSequence'/Game/Animal_pack_ultra_2/Animations/horse_turn_right_anim.horse_turn_right_anim'",
#     "AnimSequence'/Game/Animal_pack_ultra_2/Animations/horse_walk_anim.horse_walk_anim'",
# ]

def set_animation(obj, mesh, anim, ratio):
    client.request('vset /animal/{obj}/mesh {mesh}'.format(**locals()))
    client.request('vset /animal/{obj}/animation/ratio {anim} {ratio}'.format(**locals()))

def set_env(floor, sky):
    client.request('vset /env/floor/texture {floor}'.format(**locals()))
    client.request('vset /env/sky/texture {sky}'.format(**locals()))
    client.request('vset /env/light/random')

def get_image(obj, dist, az, el):
    client.request('vset /animal/{obj}/camera {dist} {az} {el}'.format(**locals()))
    lit = client.request('vget /animal/{obj}/image'.format(**locals()))
    seg = client.request('vget /animal/{obj}/seg'.format(**locals()))
    depth = client.request('vget /animal/{obj}/depth'.format(**locals()))
    lit = read_png(lit)
    seg = read_png(seg)
    depth = read_npy(depth)

    return lit, seg, depth

def get_kp(obj):
    res = client.request('vget /animal/{obj}/3d_keypoint'.format(**locals())) 
    kp_3d = json.loads(res)
    res = client.request('vget /animal/{obj}/keypoint'.format(**locals())) 
    kp = json.loads(res)

    return kp, kp_3d


def capture(obj, mesh, anim, ratio, dist, az, el):
    set_animation(obj, mesh, anim, ratio)
    lit, seg, depth = get_image(obj, dist, az, el)
    kp, kp_3d = get_kp(obj)

    return lit, seg, depth, kp, kp_3d


def plot_kp(im, kp):
    plt.imshow(im)
    for i in range(len(kp)):
        plt.plot(kp[i]['KpScreen']['X'], kp[i]['KpScreen']['Y'], 'bo')



def make_filename(mesh, anim, time, dist, az, el):
    mesh_name = get_mesh_name(mesh)
    anim_name = get_anim_name(anim)
    template = '{mesh_name}_{anim_name}_{time:.2f}_{dist:.2f}_{az:.2f}_{el:.2f}.png'
    filename = template.format(**locals())
    return filename

# The animal name can set configured in the editor

re_mesh = re.compile("SkeletalMesh'.*/(.*)\.(.*)'")
re_anim = re.compile("AnimSequence'.*/(.*)\.(.*)'")

def get_mesh_name(mesh_path):
    match = re_mesh.match(mesh_path)
    return match.group(1)

def get_anim_name(anim_path):
    match = re_anim.match(anim_path)
    return match.group(1)

def get_camera_params():
    cam_loc = client.request('vget /camera/1/location'.format(**locals()))
    cam_rot = client.request('vget /camera/1/rotation'.format(**locals()))
    return cam_loc, cam_rot

def transform_kpts(cam_loc, cam_rot, kpts_3d, depth_img):
    # x, y, z = # Get camera location in world coordinate
    # pitch, yaw, roll, # camera rotation
    # width, height =  # image width 
    # f  = width / 2 # FOV = 90
    width = 640
    height = 480
    x, y, z = cam_loc
    pitch, yaw, roll = cam_rot
    cam_pose = d3.CameraPose(x, y, z, pitch, yaw, roll, width, height, width / 2)

    # points_2d = cam_pose.project_to_2d(points_3d)  # list of 2d point, x, y
    points_3d_cam = cam_pose.project_to_cam_space(kpts_3d)
    # x, y, z # z means distance to image plane.
    depth = depth_img # Get depth image from the simulator. w x h x 1 float array.
    epsilon = 15
    kpts_2d = points_3d_cam[:,:2]

    vis = np.zeros((kpts_3d.shape[0], 1))
    for i, (x, y, z) in enumerate(points_3d_cam):
        x = int(x)
        y = int(y)
        if y<0 or y>=480 or x<0 or x>=640:
            vis[i] = 0
        else:
            real_z = depth[y][x]
            if abs(real_z - z) < epsilon:
                # print(abs(real_z - z))
                vis[i] = 1
            else:
                # print(abs(real_z - z))
                vis[i] = 0 

    # points_3d = # read 3D keypoint from AnimalParsing
    kpts = np.hstack((kpts_2d, vis))
    return kpts 


def test():
    match = re_mesh.match(mesh_paths[0])
    print(match.group(1))
    match = re_anim.match(anim_paths[0])
    print(match.group(1))

if __name__ == '__main__':
    # test()
    time = 1
    mesh = mesh_paths[0]
    anim = anim_paths[0]
    obj = 'tiger1'
    # capture(mesh, anim, time, 200, 0, 30)
    client.request('vset /animal/{obj}/mesh {mesh}'.format(**locals()))
    client.request('vset /animal/{obj}/animation {anim} {time}'.format(**locals()))
    # client.request('vset /animal/tiger/camera {dist} {az} {el}'.format(**locals()))