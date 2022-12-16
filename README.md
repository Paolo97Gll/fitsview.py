# fitsview.py

A simple FITS viewer in python.

## Instructions

Clone the repository:

```
git clone --depth 1 https://github.com/Paolo97Gll/fitsview.py.git
```

You can also download the zip or the tarball in the [latest release](https://github.com/Paolo97Gll/fitsview.py/releases/latest) and uncompress it.

Install the dependencies and install the program on system:

```
pip install astropy matplotlib pillow auto-stretch
sudo ln -s $(readlink -f fitsview.py/fitsview.py) /usr/local/bin
```

**Note.** Since this program is intended to be global, you need to use the system `pip` (as user is ok) to install the dependencies. It would be better to implement it as a PyPI package, but now I do not have time to do that.

To uninstall, simply remove the symlink and the downloaded repository or archive.

## Usage

```
usage: fitsview.py [-h] [-c CMAP] [-r] [-t TABLE] [--convert] [--block] [-s] [--version] images [images ...]

FitsView: apply auto-stretch and show all the valid tables of FITS image(s).

positional arguments:
  images                path to the image(s) to be opened

optional arguments:
  -h, --help            show this help message and exit
  -c CMAP, --cmap CMAP  matplotlib cmap (https://matplotlib.org/stable/tutorials/colors/colormaps.html)
  -r, --reverse         reverse cmap
  -t TABLE, --table TABLE
                        number of the table to be shown; default to all (-1)
  --convert             save stretched image as jpg in the current folder, do not show
  --block               block until each window is closed
  -s, --single-thread   single thread computing
  --version             show program's version number and exit
```
