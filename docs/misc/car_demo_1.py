from unrealcv import client; client.connect()
from unrealcv.util import read_png
import imageio

client.request('vset /car/0/mesh/id suv')
# The id can be selected from 
# [suv, sedan2door, sedan4door, hybrid, hatchback]
client.request('vset /car/0/door/angles 30 30 30 30 30 30')
# The six values are associated to fl (front left), fr, bl, br, hood, trunk
img = read_png(client.request('vget /car/0/image'))
imageio.imwrite('car.png', img)