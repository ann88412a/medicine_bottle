
# medicine_bottle   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

The plan of using real-time video and the other method to Identifying medicines.

This project is using Jetson Nano with camera to predicted the medicine bottle label, pill shape and the dosage of drugs.







## To-Do List

- [x] 1. Setup the Jetson Nano

- [x] 2. Meeting with the customer

- [x] 3. Setup the camera environment

- [ ] 4. Design the hardware without sensors

- [ ] 5. Identifying the medicine bottls label (which method?)

- [ ] 6. Identifying the dosage of drugs (which method?)

- [ ] 7. Identifying pill shape (Using cv hough transform to find circle square)

- [ ] 8. Undecided ...





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

## How to upgrade the opencv to 4.5.4
<!--
#delete opencv 3.3
https://forums.developer.nvidia.com/t/how-can-i-remove-the-opencv-3-3-that-comes-with-the-jetpack/112932
#install opencv 4.5.4
https://qengineering.eu/install-opencv-4.5-on-jetson-nano.html
-->
*uninstall the old opencv version.*
```shell
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo sudo apt-get purge *libopencv*
```
*Enlarge memory swap.*
```shell
$ sudo apt-get update
$ sudo apt-get upgrade
## install nano
$ sudo apt-get install nano
## install dphys-swapfile
$ sudo apt-get install dphys-swapfile
## enlarge the boundary (set CONF_MAXSWAP=4096)
$ sudo nano /sbin/dphys-swapfile
## give the required memory size (set CONF_SWAPSIZE=4096)
$ sudo nano /etc/dphys-swapfile
## reboot afterwards
$ sudo reboot.
```
*Installation script with the 4.5.4 version.*
```shell
$ wget https://github.com/Qengineering/Install-OpenCV-Jetson-Nano/raw/main/OpenCV-4-5-4.sh
$ sudo chmod 755 ./OpenCV-4-5-4.sh
$ ./OpenCV-4-5-4.sh
## once the installation is done...
$ rm OpenCV-4-5-4.sh
## remove the dphys-swapfile now
$ sudo /etc/init.d/dphys-swapfile stop
$ sudo apt-get remove --purge dphys-swapfile
## just a tip to save an additional 275 MB
$ sudo rm -rf ~/opencv
$ sudo rm -rf ~/opencv_contrib
```
*After a successful compilation, install all newly generated packages in the database of your system with the following commands.*
```shell
$ sudo make install
$ sudo ldconfig
$ make clean
$ sudo apt-get update
```

## How to install the pylibdmtx library
*Install the pylibdmtx(data matrix detector library)*
```shell
$ sudo apt-get install libdmtx0a
$ pip3 install pylibdmtx
```

