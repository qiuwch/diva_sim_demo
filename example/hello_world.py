from unrealcv import clientt
from unrealcv.util import read_png
import imageio
client.connect()

im = read_png(client.request('vget /camera/0/lit png'))
imageio.imwrite('hello_world.png', im)