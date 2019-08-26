import unrealcv
from unrealcv_util import UnrealcvUtil
import ipynb_util

client = unrealcv.Client(('localhost', 9000))
client.connect()
util = UnrealcvUtil(client)

util.DEBUG = False
util.clear()

ims = []
obj_id = 'demo_car'
util.make_demo_car(obj_id)
client.request('vset /object/{obj_id}/location 0 0 60'.format(**locals()))

for mesh_id in ['suv', 'hybrid', 'hatchback', 'sedan2door', 'sedan4door']:
    client.request('vset /car/{obj_id}/mesh/id {mesh_id}'.format(**locals()))
    ims.append(util.get_im())

fig = ipynb_util.imshow_grid(ims, 3)
fig.savefig('car_ue.png')