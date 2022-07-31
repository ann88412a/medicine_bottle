
# medicine_bottle   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

The plan of using real-time video and the other method to Identifying medicines.

This project is using Jetson Nano with camera to predicted the medicine bottle label, pill shape and the dosage of drugs.







## To-Do List

- [x]  1. Setup the Jetson Nano

- [x]  2. Meeting with the customer

- [x]  3. Setup the camera environment

- [x]  4. Design the hardware without sensors Ver. 1

- [x]  5. Identifying the medicine bottls label by using 1D/2D Barcode scanner

- [ ]  6. Identifying the dosage of drugs(syringe scale) by using Image recognition

- [ ]  7. Identifying pill shape and dosage(using yolo)

- [ ]  8. Design the hardware without sensors Ver. 2

- [ ]  9. Design the Main GUI

- [ ] 10. Undecided ...





----------------------------------------
<!--
30day token 10/5

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
-->



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