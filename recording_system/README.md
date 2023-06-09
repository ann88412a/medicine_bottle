```./darknet detector demo /home/medical/medicine_bottle/pill/yolov4/jetson_obj.data /home/medical/medicine_bottle/pill/yolov4/yolov4_tiny_pill.cfg /home/medical/medicine_bottle/pill/yolov4/yolov4_tiny_pill_final.weights -c 0```

```./darknet detector test /home/medical/medicine_bottle/pill/yolov4/jetson_obj.data /home/medical/medicine_bottle/pill/yolov4/yolov4_tiny_pill.cfg /home/medical/medicine_bottle/pill/yolov4/yolov4_tiny_pill_final.weights```


open the label server
```npx light-server -s . -p1526```
