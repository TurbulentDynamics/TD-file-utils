# TD-file-utils
Some utilities for handling plot files and massive amounts of files.

Linux command line arguments are limited to a certain size so passing many thousands of files into some basic utilities can fail.  To see this limit run ```getconf ARG_MAX # Get argument limit in bytes``` although ```xargs``` can be used to get around this limit.  However, these utilities are specifically designed to work with files and directories with format ```^.*step_[0-9]+.*$```

## Install
```pip install --user git+https://github.com/TurbulentDynamics/TD-file-utils.git```


## rmglob
Removes all files and dirs matching the glob.
```rmglob "plot_*" #Quotes are necessary```

## llglob
Should list files and dirs in some simple summary, eg head or tail.
```llglob "plot_*"  #Quotes are necessary```

## cpglob
Copies all files or dirs into new_dir
```cpglob "plot_*" new_dir #Quotes are necessary```

## mvglob
Moves all files/dirs into a new_dir
```mvglob "plot_*" new_dir #Quotes are necessary```

## check_step_integrity
Checks the sequence of steps and reports if any files are missing.
```check_step_integrity "plot_*"```

```
Batch «plot_axis__Q4_step_*»:
Gap size      : 20
Files present : [200000,200040-222800]
Files missing : [200020]
```

## break_step
Breaks a long range of files/dirs into blocks by moving the files into subdirectories
```break_step "plot_XY*" 20 #Quotes are necessary```
Before
```
.
├── plot_XY_step_1000
├── plot_XY_step_1010
├── plot_XY_step_1020
├── plot_XY_step_1030
```
After
```
├── plot_XY_1000_1010
│   ├── plot_XY_1000
│   └── plot_XY_1010
├── plot_XY_1020_1030
│   ├── plot_XY_1020
│   └── plot_XY_1030
```




