---
toc: true
---

The simulation system enables fine control of attributes in the scene, then generate images and ground truth. It can be used for offline data generation or be connected to pytorch for RL learning. It enables some tasks which is hard for real data, such as disentabled learning, or rich intermediate supervision, but also face challenges such as domain adaptation.

The system is designed to be easy to use and extend. It utilizes a python interface to control the scene. In order to use it, the steps are: download a game binary (source code available), run a short python example, modify the python example for your data generation purpose. The learning procedure will take about less than 30 minutes.

The fine control of the scene includes: car and human appearance, car door angles (five doors), car color and texture for domain randomization, car and human 3D relationship, human pose, camera parameters, etc.


In terms of ground truth, currently we have 

- part / object segmentation
- human / car keypoints
- dense keypoints (CAD model vertices)
- all 3D information (camera, object loc/rotation, etc.) 

For demo of these features, please see [feature page](/docs/feature/)

If you need more features, probably we have it but not documented here, please let us know.

## Ground Truth

Use following commands to generate ground truth.