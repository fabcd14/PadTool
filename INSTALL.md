PadTool installation procedure
==============================

Required dependencies
=====================
* Python 3+, PadTool is not compatible with Python 2 instances
* PIP3 in order to install dependencies
* Chrome Driver with Chrome/Chromium (ensure to have the same version of these two softwares)
* Pillow PIL fork lib
* Selenium lib
* ImgKit lib
* CoverPy lib

Installation
============

Dependencies
------------

In order to install all the necessary tools, please run the following commands :   
For Ubuntu and other Linux distributions (usage of Chromium which is Open Source)   

    $ sudo apt install python3 python3-pip chromium-browser chromium-chromedriver
    $ pip3 install selenium
    $ pip3 install imgkit
    $ pip3 install pillow
    $ pip3 install coverpy
    $ pip3 install discogs_client
   
Tip : On Debian distributions, packages for chromium-brower and chromium-chromedriver are named respectively `chromium` and `chromium-driver`

These commands works properly on Ubuntu 18.04, the package names may differ if you are using a different distribution

For Windows

* Download Python 3 and install it from the official Python website : https://www.python.org/downloads/
* Download Chrome Driver from the official Chrome website : https://chromedriver.chromium.org/downloads (take care to use the same version of your Chrome/Chromium instance)
* Extract the Chrome Driver executable on the same folder than PadTool (or a folder in the PATH environment variable)
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

    $ ./padtool.py -c <your_configuration_file.ini>

For PadTool usage, see `USAGE`

Using Supervisor
----------------

If you plan to execute PadTool within a Supervisor task, you might encounter errors on Python packages.   
In this case, install the pip3 packages as `sudo` :

    $ sudo pip3 install selenium
    $ sudo pip3 install imgkit
    $ sudo pip3 install pillow
    $ sudo pip3 install coverpy
    $ sudo pip3 install discogs_client

Here is an example of a supervisor config file :

    [program:padtool-grrif]
    directory=/home/your_user/PadTool/
    command=python3 padtool.py -c examples-config/config-grrif.ini
    user=your_user
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/supervisor/padtool-grrif.err.log
    stdout_logfile=/var/log/supervisor/padtool-grrif.out.log

Tip : Replace the content of the `directory` parameter to your PadTool path
