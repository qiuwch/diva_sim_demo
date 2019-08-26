import unrealcv
from unrealcv_util import UnrealcvUtil
import ipynb_util
import numpy as np

client = unrealcv.Client(('localhost', 9000))
client.connect()
util = UnrealcvUtil(client)

util.DEBUG = False
util.clear()

obj_id = 'character0'
mesh_path = ["SkeletalMesh'/Game/Girl_01/meshes/girl_01_a.girl_01_a'"]
anim_path = ["AnimSequence'/Game/Mocap/skel_girl/girl_CloseTrunk_Char00.girl_CloseTrunk_Char00'"]
ratios = np.arange(0, 1, 0.1)

ims = util.sample_anim_frames(obj_id, mesh_path, anim_path, ratios)

fig = ipynb_util.imshow_grid(ims, 3)
fig.savefig('human_anim.png')