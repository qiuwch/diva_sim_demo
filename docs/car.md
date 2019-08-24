---
permalink: /docs/shapenet
toc: true
---

This page describes how to generate a dataset with a single deformable car and the door configuration being set to different angles. The python script for this tutorial can be found in `shapenet_car.py` and `car_util.py`.

Shapenet deformable car dataset.

In order to support diverse car data generation, we provide following commands.

An executable python script looks like this

Control door angle and generate images.


Images of car can be found [here](https://drive.google.com/open?id=1dTC7eRrADMw2_s3_nm4z8OkTpvHL72iO).

# Reference

- Control Mesh
    - `vset /car/{id}/mesh/folder {mesh_folder} {meta_folder}`
    - `vset /car/{id}/mesh/id {mesh_id}`
- Control door angle
    - `vset /car/{id}/door/angles {fl} {fr} {bl} {br} {hood} {trunk}`


Currently we have five car models from `Vehicle_Vol1` purchased from Unreal Engine marketplace. We working on importing Shapenet objects into UE4.