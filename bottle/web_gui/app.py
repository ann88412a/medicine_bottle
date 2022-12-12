from flask import Flask, render_template, request, url_for, redirect, Response
import time
try:
    # fix opencv open webcam slowly bug in WIN10
    import os
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
    # call cv2 in WIN10
    from cv2 import cv2
except:
    # call cv2 in jetson nano
    import cv2

class VideoCamera(object):
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def __del__(self):
        self.cam.release()

    def get_frame(self):
        ret, frame = self.cam.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

stream_camera = VideoCamera()
def gen_stream(camera=stream_camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n' 
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen_scale_stream(camera=stream_camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n' 
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


app = Flask(__name__)

@app.route('/')
def index():
    return render_template(r"index.html")

@app.route('/syringe/')
def syringe():
    return redirect(url_for(r'barcode'))

@app.route('/syringe/barcode/', methods=['POST','GET'])
def barcode():
    if request.method == 'POST':
        # if request.values['send'] == 'next':
        barcode_id = request.values['barcode']
        print("barcode_id:", barcode_id)
        return render_template(r'syringe/barcode.html', barcode_id=barcode_id)
    return render_template(r'syringe/barcode.html', barcode_id="")

@app.route('/syringe/diluent/')
def diluent():
    return render_template(r'syringe/diluent.html')

@app.route('/syringe/scale/', methods=['POST','GET'])
def scale():
    if request.method == 'POST':
        # if request.values['send'] == 'next':
        syringe_type = request.values['syringe_type']
        print("syringe_type:", syringe_type)
        return render_template(r'syringe/scale.html', syringe_type=syringe_type)
    return render_template(r'syringe/scale.html', syringe_type="")

@app.route('/video_stream')
def video_stream():
    return Response(gen_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/scale_stream')
def scale_stream():
    return Response(gen_scale_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5001", debug=True)