# Tae Soo Kim, Weichao Qiu @ 2019
# Simple demo code to get started with UE+UnrealCV Binary
from unrealcv import client
from unrealcv.util import read_png, read_npy
from actor_utils import *
import matplotlib.pyplot as plt
import pickle

modality = 'rgb'

client.connect()
execute = client.request
created_cameras = []
objects = [
    {
        'location': [-230,-290,120],
        'rotation': [0,90,0],
        'type': 'GirlHumanCharacter'
    },
    {
        'location': [-180, -10, 20],
        'rotation': [0, 0, 0],
        'type': 'DefSUV'
    },

]
created_objects = {}

scene = {
  'cameras': created_cameras,
  'objects': created_objects,
}

class Scene:
  def __init__(self):
    self.objects = []

  def get_objects(self):
    res = client.request('vget /objects')
    self.objects = res.split(' ')
    return self.objects

  def create_object(self, json_obj):
    ''' Take a json object and set the scene accordingly '''
    obj_type = json_obj['type']
    tmp_name = client.request('vset /objects/spawn {obj_type}'.format(**locals()))
    x, y, z = json_obj['location']
    pitch, yaw, roll = json_obj['rotation']
    client.request('vset /object/{tmp_name}/location {x} {y} {z}'.format(**locals()))
    client.request('vset /object/{tmp_name}/rotation {pitch} {yaw} {roll}'.format(**locals()))
    return tmp_name


  def create_cameras(self):
    ## Create one default cam
    obj_type = 'FusionCameraActor'
    cam_name = 'cam0'
    x,y,z = [-620.077, 161.458, 594.571 ]
    pitch, yaw, roll = [-53.786, -23.13, 0.0]
    tmp_name = client.request('vset /objects/spawn {obj_type}'.format(**locals()))
    client.request('vset /object/{tmp_name}/name {cam_name}'.format(**locals()))
    client.request('vset /object/{cam_name}/location {x} {y} {z}'.format(**locals()))
    client.request('vset /object/{cam_name}/rotation {pitch} {yaw} {roll}'.format(**locals()))
    created_cameras.append({
      'name': cam_name,
      'location': [x, y, z],
      'rotation': [pitch, yaw, roll],
      'type': obj_type
    })

  def set_car_part_angles(self, actor_name, frontleft, frontright, rearleft, rearright, hood, trunk):
    # FrontLeft, FrontRight, RearLeft, RearRight, Hood, Trunk
    client.request(
      'vset /car/{actor_name}/door/angles {frontleft} {frontright} {rearleft} {rearright} {hood} {trunk}'.format(
        **locals()))

  def get_camera_info(self, cam_ind=0):
    res = client.request('vget /camera/{:d}/location'.format(cam_ind))
    x, y, z = [float(item) for item in res.split(' ')]
    res = client.request('vget /camera/{:d}/rotation'.format(cam_ind))
    rx, ry, rz = [float(item) for item in res.split(' ')]
    return x, y, z, rx, ry, rz


def get_rgb(cam_ind=0):
  res = client.request('vget /camera/{:d}/lit png'.format(cam_ind))
  img = read_png(res)
  return img

def get_mask(cam_ind=0):
  ## TODO: 052319, Currently not working.
  res = client.request('vget /camera/{cam_ind}/object_mask png'.format(**locals()))
  object_mask = read_png(res)
  return object_mask


def main():
  ## CREATE ACTORS
  scene = Scene()
  for json_obj in objects:
    name = scene.create_object(json_obj)
    created_objects[name] = json_obj
  scene.objects = scene.get_objects()

  ## CREATE CAMERAS
  scene.create_cameras()
  print("TOTAL OF: {} CAMERAS".format(len(created_cameras)))



  num_anims = 10
  for iter in range(0,num_anims):
    # Left vehicle parts range from 0 ~ 90
    frontleft = 30
    rearleft = 0

    ## Right vehicle parts range from -90 ~ 0
    frontright = 0
    rearright = -70

    ## Range from 0 ~ 90
    hood = 0
    trunk = 0

    scene.set_car_part_angles('DefSUV_0', frontleft, frontright, rearleft, rearright, hood, trunk)
    img = get_rgb()
    plt.imshow(img)
    plt.show()


if __name__ == '__main__':
  main()