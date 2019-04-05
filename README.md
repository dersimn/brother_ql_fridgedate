This whole project is still kinda sketchy. Goal is to receive an MQTT message and then print the current date onto a label.  
Why? To stick it on food in your fridge. Ever lived in a shared appartment?

## Install

    cd /opt
    git clone <this url> labelprinter

Install requirements (maybe one of them are redundant - I lost track during development):

    apt-get install libjpeg-dev zlib1g-dev python3-setuptools python3-pip libopenjp2-7-dev libtiff5 git fontconfig python3-rpi.gpio build-essentials
    pip3 install --upgrade brother_ql

Copy Unit file to `/lib/systemd/system/labelprinter.service`, then

    systemctl daemon-reload
    systemctl enable labelprinter.service
    systemctl start labelprinter.service

    