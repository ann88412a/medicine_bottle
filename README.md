
# medicine_bottle   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

The plan of using real-time video and the other method to Identifying medicines.

This project is using Jetson Nano with camera to predicted the medicine bottle label, pill shape and the dosage of drugs.


<!--
30day token 10/5

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
-->

## How to install the WiFi USB dongle driver
Install the WiFi USB dongle Dlink DWA-121(based on the rtl8188eu) driver
```
$ sudo apt-get install git dkms
$ git clone https://github.com/jeremyb31/rtl8188eu.git
$ sudo dkms add ./rtl8188eu
$ sudo dkms install 8188eu/1.0
```
## How to use the USB webcam with Jetson Nano
Using usb webcam on Jetson Nano had to install opencv with apt-get
```
$ sudo apt-get update
$ sudo apt-get upgrade -y
$ sudo apt-get install build-essential nano
$ sudo apt-get install python3-opencv
```




## To-Do List

- [x] 1. Setup the Jetson Nano

- [x] 2. Meeting with the customer

- [x] 3. Setup the camera environment

- [ ] 4. Design the hardware without sensors

- [ ] 5. Identifying the medicine bottls label (which method?)

- [ ] 6. Identifying the dosage of drugs (which method?)

- [ ] 7. Identifying pill shape (Using cv hough transform to find circle square)

- [ ] 8. Undecided ...
