from unrealcv.util import read_png, read_npy
import numpy as np
import itertools
from tqdm import tqdm
# import imageio # super slow in windows

class UnrealcvUtil:
    def __init__(self, client):
        self.client = client
        self.DEBUG = False

    def request(self, req): 
        res = self.client.request(req)
        if self.DEBUG:
            print('Request: ', req)
            print('Response: ', res[:100])
        return res

    def clear(self, map_name='EmptyPlane'):
        res = self.request('vset /action/game/level {map_name}'.format(**locals()))
        # Set the default camera location
        cmd = [
            'vset /camera/0/location -600 0 300', 
            'vset /camera/0/rotation -10 0 0'
        ]
        self.request(cmd)

    def imshow(self, im):
        import matplotlib.pyplot as plt
        plt.imshow(im)
        plt.axis('off')
        plt.show()

    def set_env(self, floor, sky):
        self.request('vset /env/floor/texture {floor}'.format(**locals()))
        self.request('vset /env/sky/texture {sky}'.format(**locals()))
        self.request('vset /env/light/random')

    def get_im(self):
        res = self.request('vget /camera/0/lit png')
        return read_png(res)

    def get_seg(self):
        res = self.request('vget /camera/0/object_mask png')
        return read_png(res)

    def get_depth(self):
        res = self.request('vget /camera/0/depth npy')
        depth = read_npy(res)
        depth[depth>5000] = 0; # cut-off for better visualization
        return depth

    def show_im(self): self.imshow(self.get_im())
    def show_seg(self): self.imshow(self.get_seg())
    def show_depth(self): self.imshow(self.get_depth())

    def make_obj(self, obj_type, obj_id, loc=[0,0,0], rot=[0,0,0]):
        x,y,z = loc
        pitch, yaw, roll = rot
        self.request([
            'vset /objects/spawn {obj_type} {obj_id}'.format(**locals()),
            'vset /object/{obj_id}/location {x} {y} {z}'.format(**locals()),
            'vset /object/{obj_id}/rotation {pitch} {yaw} {roll}'.format(**locals()),
        ])

    def make_demo_car(self, obj_id, mesh_id='suv'):
        self.make_obj('CvShapenetCar', obj_id)
        self.request([
            'vset /car/{obj_id}/mesh/id {mesh_id}'.format(**locals()),
            'vset /car/{obj_id}/annotation/obj 128 0 0'.format(**locals()),
            'vset /object/{obj_id}/location 0 0 60'.format(**locals())
        ])
        # self.request('vset /car/{obj_id}/door/angles -30 30 -30 30 30 30'.format(**locals()))
        self.cam_track_obj(obj_id, 45, 30, 500)

    def make_demo_human(self, obj_id):
        mesh_path = "SkeletalMesh'/Game/Girl_01/meshes/girl_01_a.girl_01_a'"
        anim_path = "AnimSequence'/Game/Mocap/skel_girl/girl_CloseTrunk_Char00.girl_CloseTrunk_Char00'"
        ratio = 0
        self.make_obj('CvCharacter', obj_id)
        self.request('vset /human/{obj_id}/mesh {mesh_path}'.format(**locals()))
        self.request('vset /human/{obj_id}/animation/ratio {anim_path} {ratio}'.format(**locals()))

    def cam_track_obj(self, obj_id, az, el, dist):
        # Compute camera loc and rot
        if obj_id:
            obj_loc = self.request('vget /object/{obj_id}/location'.format(**locals()))
            obj_loc = np.array([float(v) for v in obj_loc.split(' ')]) # convert str to np array
        else:
            obj_loc = np.array([0, 0, 0])
        cam_z = dist * np.sin(el * np.pi / 180.)
        cam_xy = dist * np.cos(el * np.pi / 180.)
        cam_delta = np.array([cam_xy * np.cos(az * np.pi / 180.), 
                            cam_xy * np.sin(az * np.pi / 180.), cam_z])
        cam_loc = obj_loc + cam_delta + np.array([0, 0, 0]) # add an offset
        x, y, z = list(cam_loc)
        yaw = -180 + az; roll = 0; pitch = -el
        self.request([
            'vset /camera/0/location {x:.2f} {y:.2f} {z:.2f}'.format(**locals()),
            'vset /camera/0/rotation {pitch} {yaw} {roll}'.format(**locals())
        ])

    def str_color(self, color):
        return '%d %d %d' % (color[0], color[1], color[2])

    def set_car_part_seg_color(self, obj_id, fl, fr, bl, br, hood, trunk, body):
        fl = self.str_color(fl); fr = self.str_color(fr)
        bl = self.str_color(bl); br = self.str_color(br)
        hood = self.str_color(hood); trunk = self.str_color(trunk)
        body = self.str_color(body)
        cmd = 'vset /car/{obj_id}/annotation/parts {fl} {fr} {bl} {br} {hood} {trunk} {body}'.format(**locals())
        self.request(cmd)

    def sample_anim_frames(self, obj_id, mesh_paths, anim_paths, ratios):
        # Render images using cartesian product of parameters
        self.make_obj('CvCharacter', obj_id, [0, 0, 138])
        self.cam_track_obj(obj_id, 0, 30, 200)
        ims = []
        params = list(itertools.product(mesh_paths, anim_paths, ratios))
        for param in tqdm(params):
            mesh_path, anim_path, ratio = param
            self.request('vset /human/{obj_id}/mesh {mesh_path}'.format(**locals()))
            self.request('vset /human/{obj_id}/animation/ratio {anim_path} {ratio}'.format(**locals()))
            res = self.request('vget /camera/0/lit png')
            im = read_png(res)
            ims.append(im)
        return ims