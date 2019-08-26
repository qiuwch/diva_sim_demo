from unrealcv import client
from unrealcv.util import read_png, read_npy
import argparse
import imageio
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-n', type=int, help='Number of iterations')
parser.add_argument('--cam_id', type=int, help='Camera id for data capture')
args = parser.parse_args()

client.connect()

if args.cam_id:
    cam_ids = [args.cam_id]
else:
    cams = client.request('vget /cameras').strip().split(' ')
    print(cams)
    cam_ids = range(len(cams))

for i in range(args.n):
    for cam_id in cam_ids:
        res = client.request('vget /camera/{cam_id}/lit png'.format(**locals()))
        imageio.imsave('tmp/lit_{cam_id}.png'.format(**locals()), read_png(res))
        # client.request('vget /camera/{cam_id}/depth npy'.format(**locals()))
        # np.save('tmp/depth_{cam_id}.npy'.format(**locals()), read_npy(res))
        res = client.request('vget /camera/{cam_id}/object_mask png'.format(**locals()))
        imageio.imsave('tmp/seg_{cam_id}.png'.format(**locals()), read_png(res))
