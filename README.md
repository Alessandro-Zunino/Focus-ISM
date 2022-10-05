# Focus-ISM

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-green.svg)](https://github.com/Alessandro-Zunino/Focus-ISM/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-ISM.svg?color=green)](https://python.org)

A toolbox for analysing Image Scanning Microscopy (ISM) datasets. It contains libraries for:

* Adaptive Pixel Reassignment (https://doi.org/10.1364/JOSAA.37.000154)
* Focus-ISM (https://doi.org/10.1101/2022.04.28.489892 )

----------------------------------

## System requirements

The code has been tested on a Windows 10 machine, using Python Python 3.10.2 on Spyder IDE 5.2.2

The following Python packages are required:

	numpy
	scipy
	matplotlib
	scikit-image
	scikit-learn

## Installation guide

The libraries can be used simply by downloading and importing them in any Python script.
The download is expect to last less than a minute.

## Demo

The repository contains a sample ISM dataset, "demo_img.npy", and a demonstration script, "demo.py".
The demo can be executed simply by running the script. The software will ask the user to select a region of the sample containing mostly in-focus emitters, to perform the calibration procedure.
The result will be a panel with four images, namely (1) closed pinhole, (2) open pinhole, (3) ISM reconstruction, (4) Focus-ISM reconstruction.
The execution time is expected to be less than 10 minutes on a modern computer.

## Instructions for use

The libraries can be used with any data, following the same steps shown in the demo script.
The user should simply read the desired ISM dataset and use it as the input of the focusISM function.

## License

Distributed under the terms of the [GNU GPL v3.0] license,
"Focus-ISM" is free and open source software

[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt

[file an issue]: https://github.com/VicidominiLab/ISM-processing/issues

[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/

