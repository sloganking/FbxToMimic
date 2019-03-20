# FbxToMimic [Not Yet Working]

## Notice
- Documentation quality needs to be increased for easier group work
- This project is being developed in Ubuntu 18.04.2 LTS

## Goal

The [DeepMimic project](https://github.com/xbpeng/DeepMimic) currently offers no way to import custom reference motions. This is shown in [DeepMimic issue #23](https://github.com/xbpeng/DeepMimic/issues/23). This project aims to transfer animation data from .FBX files into DeepMimic Motion files. Motion files can then be used to Train DeepMimic skills.

## Progress

- FBX files (v6.1.0)(ASCII) are converted to fbx.JSON
- fbx.JSON files are converted to DeepMimic Motion files

![FbxToMimic_Progress](./Assets/FbxToMimic_Progress.gif)
![ChickenMimic](./Assets/ChickenMimic.gif)

## Prepairing your .fbx files

JsonToMimic.py is not currently able to work with rotation data unless there is a return character after every ",L,".
This means the euler rotation data for animations inside .fbx files must be formatted as shown.

![Correct Format](https://i.imgur.com/WcOOPNS.png)


If your files are not formatted as shown above, they can be fixed with [Blender](https://www.blender.org/)
### fixing your .fbx files

- Import your file into Blender
- Export as .fbx

![export](https://i.imgur.com/4EdWW0u.png)

- In the bottom left, make sure you export as FBX 6.1 ASCII

![6.1](https://i.imgur.com/DnOk7Oh.png)

## Running the project

```Bash
python FbxToMimic.py
```

Will convert all .fbx files located in ./InputFbx/ into Mimic Motion files, located in ./OutputMimic/
