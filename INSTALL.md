PadTool installation procedure
==============================

Required dependencies
=====================
* Python 3+, PadTool is not compatible with Python 2 instances
* PIP3 in order to install dependencies
* PhantomJS instance
* Pillow PIL fork lib
* Selenium lib
* ImgKit lib

Installation
============

Dependencies
------------

In order to install all the necessary tools, please run the following commands :   
For Ubuntu and other Linux distributions   

    $ sudo apt install python3 python3-pip phantomjs
    $ pip3 install selenium
    $ pip3 install imgkit
    $ pip3 install pillow

These commands works properly on Ubuntu 18.04, the package names may differ if you are using a different distribution

For Windows

* Download Python 3 and install it from the official Python website : https://www.python.org/downloads/
* Download PhantomJS from the official PhantomJS website : https://phantomjs.org/download.html
* Extract the PhantomJS executable on the same folder than PadTool (or a folder in the PATH environment variable)
* Install from PIP3 located in the Python the following libraries : selenium, imgkit and pillow

PadTool installation
--------------------

To get the lastest version of PadTool, and execute it :

    $ git clone https://github.com/fabcd14/PadTool
    $ cd PadTool
    $ chmod +x padtool.py
    $ ./padtool.py

PadTool will run with the `config.ini` file by default.   
In order to use a different configuration file, type :
    $ ./padtool.py -c <your_configuration_file.py>

For PadTool usage, see `USAGE`
