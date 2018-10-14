# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
import os
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES

from clarifai.rest import ClarifaiApp, Concept
from clarifai.rest import Image as ClImage

#clarigaiApp key given in account
app_c = ClarifaiApp(api_key='d4e760d1e96940fb9a371f79f3249bc5')

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

def get_label(image_url):
	model = app_c.models.get('doggospotto')
	#image = ClImage(url=image_url)
	full_name = os.path.join(os.path.dirname(__file__), 'static', 'img', image_url)
	image = ClImage(file_obj=open(full_name, 'rb'))	
	response_data = model.predict([image])

	print("You have uploaded a: ")
	return response_data['outputs'][0]['data']['concepts'][0]['name']

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/uploaded', methods = ['GET', 'POST'])
def uploaded():	
	if request.method == 'POST' and 'photo' in request.files:
		filename = photos.save(request.files['photo'])
		print("waiting for clarifai")
		output = get_label(filename)
		# return filename

		return render_template('photo_uploaded.html', img = filename, category = output)

#{{ url_for('hello') }}
if __name__ == '__main__':
	# This is used when running locally only. When deploying to Google App
	# Engine, a webserver process such as Gunicorn will serve the app. This
	# can be configured by adding an `entrypoint` to app.yaml.
	app.run(host='127.0.0.1', port=5000, debug=True)
# [END gae_python37_app]

