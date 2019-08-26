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
mesh_paths = [
    "SkeletalMesh'/Game/RP_Character/rp_alison_rigged_001_ue4/rp_alison_rigged_001_ue4.rp_alison_rigged_001_ue4'",
    "SkeletalMesh'/Game/RP_Character/rp_carla_rigged_001_UE4/rp_carla_rigged_001_ue4.rp_carla_rigged_001_ue4'",
    "SkeletalMesh'/Game/RP_Character/rp_claudia_rigged_002_UE4/rp_claudia_rigged_002_ue4.rp_claudia_rigged_002_ue4'",
    "SkeletalMesh'/Game/RP_Character/rp_eric_rigged_001_UE4/rp_eric_rigged_001_ue4.rp_eric_rigged_001_ue4'",
]
anim_paths = ["AnimSequence'/Game/Mocap/skel_rp/rp_girl_CloseTrunk_Char00.rp_girl_CloseTrunk_Char00'"]
ratios = [0.5]

ims = util.sample_anim_frames(obj_id, mesh_paths, anim_paths, ratios)

fig = ipynb_util.imshow_grid(ims, 2)
fig.savefig('human_mesh.png')