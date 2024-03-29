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

update the config to point to your sam.py and your python instance

```
{
     "script":"C:\\github\\gimp-segment-anything\\sam.py",
    "python":"C:\\Users\\<YOUR USER HERE>\\AppData\\Local\\Microsoft\\WindowsApps\\python3.11.exe"
}
```



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

If it doesn't work that is the first place to start looking.

if you change the file rerun the copy pluggin.

Depending on Windows vs Linux you might need different error handling. In the future if there is interest I might code it, but if not anyone can just fork the repo and do it themselves.

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

### Doesn't work

on linux fix the permisions
try moving the pluginrc so it 

pyenv install 2.7.18

```
# Load pyenv automatically by appending
# the following to 
~/.bash_profile if it exists, otherwise ~/.profile (for login shells)
and ~/.bashrc (for interactive shells) :

export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```