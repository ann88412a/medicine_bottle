
# medicine_bottle   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

The plan of using real-time video and the other method to Identifying medicines.

This project is using Jetson Nano with camera to predicted the medicine bottle label, pill shape and the dosage of drugs.



----------------------------------------

## file structure
    .
    ├── .git
    ├── Arduino_code (arduino relate file)
    ├── bottle (bottle function file)
    ├── camera_test (camera test and setting file )
    ├── deploy_nano (for yang ming nano exec file)
        ├── lesson_plan_4 (each lesson plan)
    ├── document (plan relate file)
    ├── GUI
    ├── pictures 
    ├── pill (pill detection relate file)
        ├── folder (each darknet training file)
        ├── others (traditional image processing)
    ├── Platform_System (IoTtalk web page and device)
        ├── medical_control_page (user control web page)
        ├── medical_show_page (feedback web page)
        ├── medical_device (yang ming nano IoTtalk device)
    ├── recording_system (yang ming recording data device)
    ├── .vscode
    ├── .gitignore
    ├── LICENSE
    └── README.md

## How to upgrade the opencv to 4.7.0：
uninstall the old opencv version. 
```shell
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo sudo apt-get purge *libopencv*
```
Enlarge memory swap.
```shell
$ sudo apt-get update
$ sudo apt-get upgrade
## install dphys-swapfile
$ sudo apt-get install dphys-swapfile
## enlarge the boundary (set CONF_MAXSWAP=4096)
$ sudo vim /sbin/dphys-swapfile
## give the required memory size (set CONF_SWAPSIZE=4096)
$ sudo vim /etc/dphys-swapfile
## reboot afterwards
$ sudo reboot.
```
Installation script with the 4.7.0 version.
```shell
$ wget https://github.com/Qengineering/Install-OpenCV-Jetson-Nano/raw/main/OpenCV-4-7-0.sh
$ sudo chmod 755 ./OpenCV-4-7-0.sh
$ ./OpenCV-4-7-0.sh
## The installation is considered complete only when "Congratulations" appears.
```
Remove the dphys-swapfile
```shell
$ sudo /etc/init.d/dphys-swapfile stop
$ sudo apt-get remove --purge dphys-swapfile
```

## How to install Arduino IDE(AARCH64) in Jetson Nano
*Install the Arduino IDE (AARCH64 Ver.1.8.10).*
```shell
# Download-> https://downloads.arduino.cc/arduino-1.8.10-linuxaarch64.tar.xz
# Move to ~/下載/arduino-1.8.10-linuxaarch64/arduino-1.8.10/
$ sudo ./install.sh
$ cd ~/Desktop/
# Change owner
$ chown medical arduino-arduinoide.desktop 
# Click the new shortcut on Desktop, and select trust.
# This will reset after reboot -> sudo chmod 777 /dev/ttyUSB*
# So, had to use the next command
$ sudo adduser medical dialout
```


## How to install the WiFi USB dongle driver
*Install the WiFi USB dongle Dlink DWA-121(based on the rtl8188eu) driver.*
```shell
$ sudo apt-get install git dkms
$ git clone https://github.com/jeremyb31/rtl8188eu.git
$ sudo dkms add ./rtl8188eu
$ sudo dkms install 8188eu/1.0
```

## How to write/BackUp the system image in windows
*Use "USB Image Tool" BackUp: https://www.alexpage.de/usb-image-tool/download/*
```
Mode: Device Mode
BackUp: clone the system image
```
*Use balenaEtcher write: https://www.balena.io/etcher/*
```
Select image: Choose the system image which you want to use.
Select drive: Choose the SD card or USB device which you want to write.(It will be format) 
```
*If you want to boot from USB device*
```shell
# Use the same mrthod(SD card) to write the USB device.
$ sudo mount /dev/sda1 /mnt
# open /mnt/boot/extlinux/extlinux.conf
# change root=/dev/mmcblk0p1 to root=/dev/sda1 and save it.
# Shutdown and remove the SD card.(Keep the USB device)
# Boot will load from USB device.
```

*Nano cant not Boot (Black screen)*
```shell
# Download NVIDIA SDK Manager (.deb)
# https://developer.nvidia.com/nvidia-sdk-manager
# ref: https://juejin.cn/post/7099653549713260575
$ sudo apt install ./{sdkmanger_file}
$ sdkmanger
```

*Yang ming deployment operation video*
https://drive.google.com/file/d/1Kk4vD4NKLuZSDS1dN5Uc6jvUK7NtrUn_/view?usp=sharing

