# Created by Sourim Das, School of Computing, Clemson University

from bottle import route, run, error
from docker import Client, errors

class DockerClient:
	client = Client(base_url = 'unix://var/run/docker.sock', version = 'auto')
	def __init__(self):
		pass

@route('/get-images')
def get_images():
	c = DockerClient.client
	images = {}
	images['images'] = c.images(all=False)	
	return str(images)

@route('/get-images-by-name/<image_name>')
def get_images_by_id(image_name):
	c = DockerClient.client
	images = {}
	images['images'] = c.images(name=image_name)	
	return str(images)

# This may lead to two types of error, HTTP/WebServer specific errors and/or Docker daemon specific errors
# HTTP/WebServer specific errors does not necessarily imply failure in image removal. So if such an error
# occurs do not jump into any conclusion. Hang-on till you get Docker daemon specific response. If the
# latter response turns out to be an error then there is indeed an error in image removal.
@route('/remove-image/<image_name>/<tag>')
def remove_image(image_name, tag):
	c = DockerClient.client
	response = {}
	try:
		c.remove_image(image_name+":"+str(tag) )
		response["status"] = "success"
		response["message"] = image_name+":"+str(tag)+" successfully removed"
		return str(response)
	except errors.APIError as e:
		response["status"] = "fail"
		response["message"] = e.explanation
		return str(response)
	except:
		response["status"] = "fail"
		response["message"] = "unknown"
		return str(response)

@route('/inspect-image/<image_id>')
def inspect_image(image_id):
	c = DockerClient.client
	try:
		response = c.inspect_image(str(image_id) )
		return str(response)
	except errors.APIError as e:
		fail_response = {}
		fail_response["status"] = "fail"
		fail_response["message"] = e.explanation
		return str(fail_response)
	except:
		fail_response = {}
		fail_response["status"] = "fail"
		fail_response["message"] = "unknown"
		return str(fail_response)

@route('/search/<query>')
def search(query):
	c = DockerClient.client
	response = {}
	response['images'] = c.search(str(query))
	return str(response)

@route('/pull/<repository>/<tag>')
def pull(repository, tag):
	c = DockerClient.client
	try:
		response = {}
		c.pull( str(repository), str(tag) )
		response['status'] = "success"
		response['message'] = "pull successful"
		return str(response)
	except errors.APIError as e:
		fail_response = {}
		fail_response["status"] = "fail"
		fail_response["message"] = e.explanation
		return str(fail_response)
	except:
		fail_response = {}
		fail_response["status"] = "fail"
		fail_response["message"] = "unknown"
		return str(fail_response)

run(host='localhost', port=8080, debug=True)