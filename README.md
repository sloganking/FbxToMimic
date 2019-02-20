# FbxToMimic [Not Yet Working]

## Goal

The [DeepMimic project](https://github.com/xbpeng/DeepMimic) currently offers no way to import custom reference motions.

This project aims to transfer animation data from .FBX files into DeepMimic Motion files. Motion files can then be used to Train DeepMimic skills.



## Progress

- FBX files (v6.1.0) are converted to fbx.JSON
- fbx.JSON files are converted to DeepMimic Motion files

![FbxToMimic_Progress](./Assets/FbxToMimic_Progress.gif)


## Need to complete

- Fix Euler to quaternions angle conversion
