---
permalink: /
toc: true
---

This document covers how to run the simulator and generate data from the binary. It demonstrates how to manipulate a virtual scene with python API and generate images and ground truth.

## Simulation Binary

The binary supports Ubuntu 16.04 by default, but it can be compiled to support windows and other linux distributions.

Here is a simple demo python code (synthesis_demo.py) to help get you started: the demo includes actor generation, vehicle part manipulation, camera manipulation and image generation from python.
I have also included the binary in zip format here:https://www.dropbox.com/s/4hv7qx6b6igg0sq/EmptyPlaneBinary.zip?dl=0. The source code can be found in `https://github.com/qiuwch/CarAct.git`.
 
## Scene Manipulation with Python

Also, I attached the requirements.txt of my pip env so that things can be run in a more or less consistent environment. I am in conda python 3.6.7.
 
To execute:

```bash
unzip EmptyPlaneBinary.zip
./EmptyPlaneBinary/LinuxNoEditor/CarAct.sh EmptyPlane
python synthesis_demo.py
```
 
The demo generates a girl character and a SUV with rear_right and front_left doors opened. 
 
What is more to come:
- Lighting control in python
- Background textures in python

sysnthesis.py and requirements.txt can be found in this gist: https://gist.github.com/qiuwch/b4eb4fe3964d44257a9b17c85d6789e9

Please feel free to contact Tae Soo Kim (tkim60@jhu.edu) or Weichao (qiuwch@gmail.com) for this section!

## Trouble shooting

If saw any issue, please email `qiuwch@gmail.com`. 

Here are some examples of the system. The list of all features can be found in [the feature description](/docs/feature/)
