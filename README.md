Mirror Control
==============

[![Join the chat at https://gitter.im/jreyes/mirror-sidekick](https://badges.gitter.im/jreyes/mirror.svg)](https://gitter.im/jreyes/mirror-sidekick?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
![](https://img.shields.io/badge/Licence-Apache%20v2-green.svg)

This is a companion application for the [Another Smart Mirror](https://github.com/jreyes/mirror) application.

This application runs in a Raspberry PI and adds the ability to control the mirror with a Wiimote or a Lirc supported 
device like the Amazon Fire TV Stick remote. 

## Installation

Easy to use installation, from your Raspberry PI, run the following commands:

    git clone https://github.com/jreyes/mirror-control.git
    cd mirror-control
    sudo scripts/install.sh

When asked enter your Artik **DEVICE ID** and **DEVICE TOKEN**

After it finishes the installation, pair your bluetooth device to Raspberry PI, this is the only time where you would 
need to do this to trust the device. 