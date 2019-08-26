# Make a simple car grid
from unrealcv import client
from unrealcv.util import read_png
import imageio

client.connect()

with open('./docs/shapenet_manual_id.txt') as f:
    ids = f.readlines()
    
car_h, car_w = 200, 50
for i, (x, y) in enumerate(zip(range(-10, 10), range(-10, 10))):
    mesh_id = '1a64bf1e658652ddb11647ffa4306609'
    client.request('vset /objects/spawn CvShapenetCar {i}'.format(**locals()))
    client.request('vset /car/{i}/mesh/folder /Game/ShapenetManual/ x'.format(**locals()))
    client.request('vset /car/{i}/mesh/id {mesh_id}'.format(**locals()))

png = read_png(client.request('vget /camera/0/lit png'))
imageio.imwrite('example/car_grid.png', png)
