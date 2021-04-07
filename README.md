# circum-kinect

![build](https://travis-ci.com/LumineerLabs/circum-kinect.svg?branch=master) ![PyPI](https://img.shields.io/pypi/v/circum-kinect)

Kinect sensor plugin for [circum](https://github.com/LumineerLabs/circum).

## Install

### Kinect V2

Install the PyKinect2 prerequisites described on the [PyKinect2 GitHub](https://github.com/LumineerLabs/PyKinect2), but do not install the package from pypi.

```bash
pip3 install circum-kinect[pykinect2]
```

### Kinect V1

WARNING: This version has not been tested without hardware. It has been installed and run to the point of creating the NUI runtime. Beyond that, all bets are off.

WARNING: This is more complicated and brittle than installing the Kinect V2 options. If at all possible, we recommend updating to and using the Kinect V2.

* Install the WDK using the directions [here](https://docs.microsoft.com/en-us/windows-hardware/drivers/download-the-wdk)
* Install any 1.x version of the Kinect for Windows SDK.
* Install the [Build Tools for Visual Studio](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019), ensure that the ATL features are selected.

```bash
pip3 install circum-kinect[pykinect]
```

### Both

Install all the prerequesites described above and use the following pip command:

```bash
pip3 install circum-kinect[pykinect, pykinect2]
```

## Usage

```bash
Usage: circum-endpoint kinect [OPTIONS]

Options:
  --version [1|2]  PyKinect version to use.
  --help           Show this message and exit.
```
