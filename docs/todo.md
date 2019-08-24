
The ground truth includes are 2D keypoint, 3D keypoint and vertex points, see the [feature page](/docs/feature/) for the full list of features.

TODO: Write examples to generate a dataset.

TODO: Test the program with Linux.

## Run the binary

If the machine has UI, then run the binary will give an window like this. If the machine has no GUI, such as a linux server. Start the binary using `DISPLAY= ./LinuxNoEditor/xx`.

```python
from unrealcv import client
client.connect()
res = client.request('vget /camera/0/lit png')
```

## Put objects in the virtual scene

unrealcv supports putting objects into the scene and manipulate objects through python.

Use include for example snippets, the snippet can run on its own.

Useful objects in the scene are DefSUV, GirlHuman.

Here an example showing put two objects in the scene. The human animation can be controlled with the python API.

## Complex scene

If you want more complex 3D scenes.

Start the binary with a different map.

For example `./unrealcv_binary/`

## Appendix

Generic commands provided by `unrealcv`.

List of commands in the project

TODO: I have many projects, how to sync code between these projects.
TODO: Benchmark speed.

## Demo scripts

Run example scripts and generate data as below.