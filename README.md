# gimp-plugin-segment-anything
a mvp for creating a gimp plugin

Instructions
* Install gimp
* Install latest python3
* Install gimp dev tools

install python from the windows store

install
```
pip install torch torchvision
```


Install the segment anything module
```
pip install git+https://github.com/facebookresearch/segment-anything.git
```

Install the optional deps
```
pip install opencv-python pycocotools matplotlib onnxruntime onnx
```

## LONG PATH NAMES:

* Click Win+R
* Type regedit and press Enter
* Go to Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem
* Edit or create a key named LongPathsEnabled (type: REG_DWORD)
* Enter 1 as its value and press OK.
* Restart


Install a checkpoint
```
https://github.com/facebookresearch/segment-anything#model-checkpoints
```

In my case I put it here:
```
C:\MLModels\SegmentAnything
```

I also put my OPEN_CV models here:
```
C:\MLModels\OPEN_CV
```


update the sam.py with the path to checkpoint.


create a pluggin like the hello_world.py provided.

copy the pluggin to the gimp plugins directory

```ps
cp -r .\plugin\split-to-layers\ "C:\Users\$env:USERNAME\AppData\Local\Programs\GIMP 2\lib\gimp\2.0\plug-ins\"
```


running gimp in verbose mode to get the logs
```ps
."C:\Users\$env:USERNAME\AppData\Local\Programs\GIMP 2\bin\gimp-2.10.exe" --verbose
```

There is a config.json that has the python location, and the script location.


The split-to-layers.py is python 2 7 and calls out to the sam.py python3 which calls the facebook meta ai segment anything model

Citing SAM or SA-1B
```BibTeX 
@article{kirillov2023segany,
  title={Segment Anything},
  author={Kirillov, Alexander and Mintun, Eric and Ravi, Nikhila and Mao, Hanzi and Rolland, Chloe and Gustafson, Laura and Xiao, Tete and Whitehead, Spencer and Berg, Alexander C. and Lo, Wan-Yen and Doll{\'a}r, Piotr and Girshick, Ross},
  journal={arXiv:2304.02643},
  year={2023}
}
```