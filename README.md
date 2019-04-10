# FbxToMimic

## Goal

The [DeepMimic project](https://github.com/xbpeng/DeepMimic) currently offers no way to import custom reference motions. This is shown in [DeepMimic issue #23](https://github.com/xbpeng/DeepMimic/issues/23). This project aims to transfer animation data from .FBX files into DeepMimic Motion files. Motion files can then be used to Train DeepMimic skills.

## Progress so far

![FbxToMimic_Progress](./Assets/FbxToMimic_Progress.gif)
![ChickenMimic](./Assets/ChickenMimic.gif)

## Process

- User puts desired .fbx files in [./InputFbx/](InputFbx)
- User manually creates humanoid rig from .fbx bone names.
- User calls [FbxToMimic.py](./FbxToMimic.py) to start conversion.
	- All files in "./OutputMimic" are removed
- [FbxToJson.py](./Utils/FbxToJson.py) converts .fbx files (v6.1.0)(ASCII) into fbx.JSON in "/Utils/Temp/"
	- All old files in "./Utils/Temp/" are removed
- JsonToMimic.py converts fbx.JSON to DeepMimic Motion files. Saved in /OutputMimic/

## Prepairing your .fbx files

JsonToMimic.py is not currently able to work with rotation data unless there is a return character after every ",L,".
This means the euler rotation data for animations inside .fbx files must be formatted as shown.

![Correct Format](https://i.imgur.com/WcOOPNS.png)


If your files are not formatted as shown above, they can be fixed with [Blender](https://www.blender.org/)
### Fixing your .fbx files with Blender

- Import your file into Blender
- Export as .fbx

![export](https://i.imgur.com/DmCfaoh.png)

- In the bottom left, make sure you export as "FBX 6.1 ASCII"

![6.1](https://i.imgur.com/DnOk7Oh.png)

## Creating a humanoid rig

Currently joints in .fbx files have to be manually assigned by name to the corresponding joints in the Mimic Motion humanoid rig. Right now this is done by putting the json property names of your bones into the "animated" list, located in [./Utils/JsonToMimic.py](./Utils/JsonToMimic.py) in order with the Mimic joints listed below.

```
[
	duration of frame in seconds (1D),
	root position (3D),
	root rotation (4D),
	chest rotation (4D),
	neck rotation (4D),
	right hip rotation (4D),
	right knee rotation (1D),
	right ankle rotation (4D),
	right shoulder rotation (4D),
	right elbow rotation (1D),
	left hip rotation (4D),
	left knee rotation (1D),
	left ankle rotation (4D),
	left shoulder rotation (4D),
	left elbow rotation (1D)
]
```

The "animated" list is currently assigned with the bone name properties of all .fbx files located in the [Huge FBX Mocap Library part 1](https://assetstore.unity.com/packages/3d/animations/huge-fbx-mocap-library-part-1-19991) asset found on the Unity asset store.

The current method of creating a humanoid rig just described is not intuative and sloppy at best. It is planned to be replaced by having users assign their .fbx model's bone names into a .json file before conversion. I am currently unaware of how to create or use any algorithms that know how to automatically generate a humanoid rig (similar to how unity can), but am open to using them upon finding one.

## Running the project

```Bash
python FbxToMimic.py
```

Will convert all .fbx files located in ./InputFbx/ into Mimic Motion files, located in ./OutputMimic/
