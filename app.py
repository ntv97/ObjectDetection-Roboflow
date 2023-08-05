from flask import Flask, render_template, request, Response
#from werkzeug import secure_filename
from objectdetection.dogs import *
from objectdetection.people import *
from objectdetection.goose import *
from objectdetection.car import *
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/')
def upload_file():
   return render_template('upload.html')
	
@app.route('/upload', methods = ['GET', 'POST'])
def upload():
   global filename
   if request.method == 'POST':
      f = request.files['file']
      filename = f.filename
      if filename != "dogs.mp4" and filename != "people.mp4" and filename != "goose.mp4" and filename != "car.mp4":
          print(filename)
          return render_template('404.html')
      path = os.path.join("uploads", f.filename)
      print(path)
      data_json = request.form.get("file")
      print(data_json)
      f.save(path)
      print(f.filename)
      if filename == "dogs.mp4":
        return render_template('dogs.html')
      elif filename == "people.mp4":
        return render_template('people.html')
      elif filename == "goose.mp4":
          return render_template('goose.html')
      elif filename =="car.mp4":
          return render_template('cars.html')
      return render_template('404.html')


@app.route('/DogVideo')
def DogVideo():
    return Response(ShowDogVideo(filename), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/PeopleVideo')
def PeopleVideo():
    return Response(ShowPeopleVideo(filename), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/GooseVideo')
def GooseVideo():
    return Response(ShowGooseVideo(filename), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/CarsVideo')
def CarsVideo():
    return Response(ShowCarVideo(filename), mimetype='multipart/x-mixed-replace; boundary=frame')

		
if __name__ == '__main__':
   #app.run(debug = True)
   app.run(port=5003, debug=True)
