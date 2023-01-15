
# medicine_bottle   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

The plan of using real-time video and the other method to Identifying medicines.

This project is using Jetson Nano with camera to predicted the medicine bottle label, pill shape and the dosage of drugs.


##給藥方式說明:
IVA需要一個agent，通常是精密輸液套
每次給藥就對一些輸液
用滴數控制給藥時間

IVD是直接加在點滴袋(瓶)中
比如說KCl，不可能15、30分鐘內給完，會GG
而是加在bag中慢慢滴

IV是緩推
抽完藥後直接逗在IV cath上推注
通常仿單中會告訴你要推幾分鐘
大部分可IV的藥物也都可IVA
注意勿將IV與IVP混淆

IVP是快速推注
除非急救，否則由醫師執行

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

