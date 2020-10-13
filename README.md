PadTool
=======
[![Build Status](https://travis-ci.com/fabcd14/PadTool.svg?branch=master)](https://travis-ci.com/fabcd14/PadTool)
[![Maintenance](https://img.shields.io/badge/Maintained-yes-green.svg)](https://github.com/fabcd14/PadTool/graphs/commit-activity)
[![GitHub version](https://badge.fury.io/gh/fabcd14%2FPadTool.svg)](https://github.com/fabcd14/PadTool)
[![Lines of Code](https://tokei.rs/b1/github/fabcd14/PadTool)](https://github.com/fabcd14/PadTool)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Python versioning](https://img.shields.io/badge/python-%3E=3.5-blue.svg)](https://github.com/fabcd14/PadTool)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)

![Screenshot of a logo slide](https://raw.githubusercontent.com/fabcd14/PadTool/master/img/padtool_logo.png)   
   
PadTool is a MOT SLS and DLS generator for PAD encoders such as ODR-PadEnc.

PadTool is able to read JSON, XML, text or HTML files and outputs DLS+ text
from these information and generates nice SLS with personnalized templates

PadTool is better to use with the ODR-mmbTools tool set, especially with ODR-PadEnc. 
More information about the ODR-mmbTools can be found in the *guide*, available on the
[Opendigitalradio mmbTools page](http://www.opendigitalradio.org/mmbtools).

Features of PadTool:

- Reads JSON, XML or text files containing live information of your radio station
- Outputs DLS+ files compatible with ODR-PadEnc
- Outputs DAB compliant slides, JPG format with 320x240px resolution, and no more than 16kB sized files
- Windows and latest Linux versions fully compatible (tested with Ubuntu 20.04 and Windows 10)
- Easy personnalized DLS text with predefined tags
- Possible generation of a logo station slide
- Possible generation of ATC slide (Artist, Title & Cover)
- Compatible with other plugins (see [www.rplusd.io](https://www.rplusd.io/PadTool).)
- Automatic cover art seeking thanks to CoverPy and Sacad (iTunes, Amazon, last.fm and many more...)
- Colors and themes fully personnalisable via CSS and HTML templates

Output example slides :  

![Screenshot of a logo slide](https://raw.githubusercontent.com/fabcd14/PadTool/master/img/example_logo.jpg)   
![Screenshot of a ATC slide](https://raw.githubusercontent.com/fabcd14/PadTool/master/img/example_music.jpg)   

Install
=======

See `INSTALL` file for installation instructions.

Usage after installation
========================

See `USAGE` to see examples and best practices

License
=======

See the files `LICENSE`, `COPYING` files

Contributions and Contact
=========================

Contributions to this tool are welcome, you can contact me at any time via my e-mail
address below.   
   
There is a bunch of ideas and thoughts about new possible features and improvements
in the `TODO` file.   
   
Developed by:   
Fabien Cuny *fabien.cuny7 [at] orange [dot] fr*   
aka `fabcd14`, admin of the `DAB Radio Normandie` Facebook Page   

If you like my work, and want to support it, grab me a coffee or a beer here : https://www.buymeacoffee.com/fabcd14   
   
Thanks by advance :-)
