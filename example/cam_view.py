from unrealcv import client
from unrealcv_util import UnrealcvUtil
import ipynb_util

client.connect()
util = UnrealcvUtil(client)
util.DEBUG = False
util.clear()
util.make_demo_car('demo_car')

ims = []
for az in range(0, 360, 60):
    util.cam_track_obj('demo_car', az, 30, 500)
    ims.append(util.get_im())
for el in range(30, 60, 10):
    util.cam_track_obj('demo_car', 0, el, 500)
    ims.append(util.get_im())

fig = ipynb_util.imshow_grid(ims, 3)
fig.savefig('cam_view.png')
