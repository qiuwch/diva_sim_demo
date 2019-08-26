## Unrealcv Basic


| Command                | Comment                                  |
|------------------------|------------------------------------------|
| vget /unreacv/status   | Get the simulator status                 |
| vget /camera/{cam_id}/lit png | Return image from the camera as a binary |

## Object Manipulation

| command                                             | comment                            |
|-----------------------------------------------------|------------------------------------|
| vget /objects                                       | List existing objects in the scene |
| vset /objects/spawn {obj_type} {obj_id}             | spawn an object to the scene       |
| vset /object/{obj_id}/location {x} {y} {z}          | set obj location                   |
| vset /object/{obj_id}/rotation {pitch} {yaw} {roll} | set obj rotation                   |
| vget /object/{obj_id}/location                      | get obj location                   |
| vget /object/{obj_id}/rotation                      | get obj rotation                   |

## Ground Truth

| Command                        | Comment               |
|--------------------------------|-----------------------|
| vget /camera/{cam_id}/lit png         | Get image             |
| vget /camera/{cam_id}/object_mask png | Get segmentation mask |
| vget /camera/{cam_id}/depth npy       | Get depth             |

## Car


| Command                                                       | Comment                      |
|---------------------------------------------------------------|------------------------------|
| vset /car/{id}/mesh/id {mesh_id}                              | Set the mesh id of the car   |
| vset /car/{id}/door/angles {fl} {fr} {bl} {br} {hood} {trunk} | Set door angles              |
| vset /car/{id}/annotation/obj {r} {g} {b}                     | Set car annotation color     |

## Advanced Car

| Command                                                                 | Comment                   |
|-------------------------------------------------------------------------|---------------------------|
| vset /car/{obj_id}/annotation/parts {fl} {fr} {bl} {br} {hood} {trunk} | Set part annotation color |
| vset /car/{obj_id}/mesh/texture {texture_filename}                     | Control car texture       |
| -                      | Control texture of each car part       |
| -                                                                       | Get car keypoint          |

## Shapenet Car

| Command        | Comment                            |
|----------------|------------------------------------|
| vset /car/{obj_id}/mesh/folder {mesh_folder} {meta_folder} | Set where shapenet models are stored |
| vset /car/{obj_id}/mesh/id {mesh_id} | See reference.md to see available mesh id |


## Human

| Command                                              | Comment                                          |
|------------------------------------------------------|--------------------------------------------------|
| vset /human/{id}/mesh {mesh_path}                    | Set the appearance of a human                    |
| vset /human/{id}/animation/ratio {anim_path} {ratio} | Set the pose of a human using recorded animation |
| vset /human/{id}/texture | Control texture of the human | 
| vget /human/{id}/keypoint | Get keypoint |
| vget /human/{id}/3d_keypoint | Get 3D keypoint |
| vget /human/{id}/vertex | Get 3D keypoint |



## Environment

|              Command              |         Comment          |
|:---------------------------------:|:------------------------:|
| vset /env/floor/texture {texture} | Set texture of the floor |
|  vset /env/sky/texture {texture}  | Set texture for the sky  |
|  vset /env/light/random |     Random lighting      |