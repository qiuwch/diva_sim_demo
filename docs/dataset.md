---
title: "Generated Synthetic Dataset"
toc: true
---

This page shows generated images from the dataset.

## Pilot Synthetic Image Dataset

We use our simulation tool to generate a dataset similar to DIVA setup. What TK sent is a binary that can be used to produce images and ground truth and this dataset is what we have generated using it. If you have time, welcome to take a look and give some feedback about improving it or how it might be helpful to your research. 

Here's the Dropbox link for the synthetic dataset: https://www.dropbox.com/s/e69zzs9r1n798qw/synthetic_DIVA_v1.1.zip?dl=0

This is a preliminary version. There are four virtual scenes with cameras in different positions. We have annotations for object bounding boxes and four activities (Entering, Exiting, OpenTrunk, CloseTrunk).

The structure of the dataset is as follows:

TODO: Show images here.

```bash
├── scene
│   ├── cam
│   │   └── FusionCameraSensor
│   │       ├── bb
│   │       ├── caminfo
│   │       └── lit
```

Please feel free to contact Zihao Xiao (a904794043@gmail.com) or Weichao (qiuwch@gmail.com) for this section!
