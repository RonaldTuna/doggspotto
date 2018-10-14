# Pip install the client:
# pip install clarifai

from clarifai.rest import ClarifaiApp, Concept
from clarifai.rest import Image as ClImage

# Create your API key in your account's `Manage your API keys` page:
# https://clarifai.com/developer/account/keys

app = ClarifaiApp(api_key='d4e760d1e96940fb9a371f79f3249bc5')

def get_label(image_url):
	model = app.models.get('doggospotto')
	image = ClImage(url=image_url)
	response_data = model.predict([image])

	print("You have uploaded a: ")
	return response_data['outputs'][0]['data']['concepts'][0]['name']

output = get_label('https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11/12225627/Pomeranian-On-White-01.jpg')

print(output)
# You can also create an environment variable called `CLARIFAI_API_KEY` 
# and set its value to your API key.
# In this case, the construction of the object requires no `api_key` argument.

# app = ClarifaiApp()

# print('n'.join(get_relevant_tags('https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11/12225627/Pomeranian-On-White-01.jpg')))

# def get_relevant_tags(image_url):
#     response_data = app.tag_urls([image_url])
 
#     tag_urls = []
#     for concept in response_data['outputs'][0]['data']['concepts']:
#         tag_urls.append(concept['name'])
 
#     return tag_urls