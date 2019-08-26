from unrealcv import client
from tqdm import tqdm
client.connect()

iters = range(100000)

for i in tqdm(iters):
    # client.request('vget /unrealcv/status')
    # client.request('vget')
    client.request('vget /camera/0/lit png')
