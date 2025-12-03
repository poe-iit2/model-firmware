Model Firmware
==============

Controls GPIO pins and communicates with server.

ESP32 version at: [e30970e](https://github.com/poe-iit2/model-firmware/tree/e30970e3f5a5cb8ed6094ce418c3b56f8ea07421)

Installation Instructions for Pi
--------------------------------

As superuser (`sudo -i`):

```sh
apt install python3-dev git
mkdir -p /opt
cd /opt
git clone https://github.com/poe-iit2/model-firmware.git
cd model-firmware
python3 -m venv venv
. ./venv/bin/activate
pip3 install -r requirements.txt
mkdir -p /usr/local/lib/systemd/system
cp model-firmware.service /usr/local/lib/systemd/system
```
