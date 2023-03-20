run onnx yolov6
`cd yolov6 `

`python3 export_onnx.py --weights ./yolov6n.pt --grid --simplify --topk-all 100 --iou-thres 0.65 --conf-thres 0.35 --img-size 640 640 --max-wh 640 --end2end `

test yolov6 onnx
`cd ..`

`python3 onnx_run.py --weights ./yolov6/yolov6n.onnx --source ./test.png`

val onnx yolov6
`cd yolov6`

`python3 export_onnx.py --weights yolov6n.pt --simplify`

`cd .. `

`python3 val.py --weights ./yolov6/yolov6n.onnx`


run onnx yolov7
`cd yolov7 `

`python3 export.py --weights ./yolov7-tiny.pt --grid --end2end --simplify --topk-all 100 --iou-thres 0.65 --conf-thres 0.35 --img-size 640 640 --max-wh 640 `

test yolov7 onnx
`cd ..`

`python3 onnx_run.py --weights ./yolov7/yolov7-tiny.onnx --source ./test.png`

val onnx yolov7
`cd yolov7`

`python3 export.py --weights ./yolov7-tiny.pt --grid --simplify --topk-all 100 --iou-thres 0.65 --conf-thres 0.35 --img-size 640 640 --max-wh 640 `

`cd ..`

`python3 val.py --weights ./yolov7/yolov7-tiny.onnx `


Reference:
val: https://github.com/ultralytics/yolov5
yolov6: https://github.com/meituan/YOLOv6
yolov7: https://github.com/WongKinYiu/yolov7
