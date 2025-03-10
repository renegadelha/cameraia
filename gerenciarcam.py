from flask import *
import cv2

app = Flask(__name__)

url = "http://192.168.0.102:8080/video"

camera = cv2.VideoCapture(url)

def generate_frames():
    #foto_ref = cv2.imread("imgs/pessoa1_1.jpg")
    #foto_ref = cv2.cvtColor(foto_ref, cv2.COLOR_BGR2RGB)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def showcam():
    return render_template('video.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
