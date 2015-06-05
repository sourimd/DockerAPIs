# Created by Sourim Das, School of Computing, Clemson University

from bottle import route, run, error
from docker import Client, errors
import sys

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
		response["message"] = str( sys.exc_info())
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
		fail_response["message"] = str( sys.exc_info())
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
		fail_response["message"] = str( sys.exc_info())
		return str(fail_response)

@route('/get-all-containers')
def get_all_containers():
	c = DockerClient.client;
	try:
		response = {}
		response['containers'] = c.containers(all=True)
		return str(response)
	except errors.APIError as e:
		fail_response = {}
		fail_response["status"] = "fail"
		fail_response["message"] = e.explanation
		return str(fail_response)
	except:
		fail_response = {}
		fail_response["status"] = "fail"
		fail_response["message"] = str( sys.exc_info())
		return str(fail_response)

@route('/get-running-containers')
def get_running_containers():
	c = DockerClient.client;
	try:
		response = {}
		response['containers'] = c.containers()
		return str(response)
	except errors.APIError as e:
		fail_response = {}
		fail_response["status"] = "fail"
		fail_response["message"] = e.explanation
		return str(fail_response)
	except:
		fail_response = {}
		fail_response["status"] = "fail"
		fail_response["message"] = str( sys.exc_info())
		return str(fail_response)

@route('/kill-container/<container>')
def kill_container( container):
	try:
		c = DockerClient.client
		c.kill(container)
		response={}
		response["status"] = "success"
		response["message"] = container + " killed successfully"
		return str(response)
	except errors.APIError as e:
		response = {}
		response["status"] = "fail"
		response["message"] = e.explanation
		return str(fail_response)
	except:
		response = {}
		response["status"] = "fail"
		response["message"] = str( sys.exc_info())
		return str(response)

@route('/remove-container/<container>')
def remove_container(container):
	try:
		c = DockerClient.client
		c.remove_container(container)
		response={}
		response["status"] = "success"
		response["message"] = container + " killed successfully"
		return str(response)
	except errors.APIError as e:
		response = {}
		response["status"] = "fail"
		response["message"] = e.explanation
		return str(response)
	except:
		response = {}
		response["status"] = "fail"
		response["message"] = str( sys.exc_info())
		return str(response)

@route('/create-container/<image>/<tag>/<container_name>')
def create_container(image, tag, container_name):
	c = DockerClient.client
	full_image = str(image)+":"+str(tag)
	try:
		container = c.create_container(image=full_image, command='/bin/bash', name=container_name,\
										tty=True, stdin_open=True)
		return str(container)
	except errors.APIError as e:
		response = {}
		response["status"] = "fail"
		response["message"] = e.explanation
		return str(response)
	except:
		response = {}
		response["status"] = "fail"
		response["message"] = str( sys.exc_info())
		return str(response)

@route('/start-container/<container>')
def start_container(container):
	c = DockerClient.client
	try:
		response = c.start(container)
		return str(response)
	except errors.APIError as e:
		response = {}
		response["status"] = "fail"
		response["message"] = e.explanation
		return str(response)
	except:
		response = {}
		response["status"] = "fail"
		response["message"] = str( sys.exc_info())
		return str(response)

@route('/restart-container/<container>')
def restart_container(container):
	c = DockerClient.client
	try:
		response = c.restart(container)
		return str(response)
	except errors.APIError as e:
		response = {}
		response["status"] = "fail"
		response["message"] = e.explanation
		return str(response)
	except:
		response = {}
		response["status"] = "fail"
		response["message"] = str( sys.exc_info())
		return str(response)

@route('/stop-container/<container>')
def stop_container(container):
	c = DockerClient.client
	try:
		response = c.stop(container)
		return str(response)
	except errors.APIError as e:
		response = {}
		response["status"] = "fail"
		response["message"] = e.explanation
		return str(response)
	except:
		response = {}
		response["status"] = "fail"
		response["message"] = str( sys.exc_info())
		return str(response)

@route('/pause-container/<container>')
def stop_container(container):
	c = DockerClient.client
	try:
		response = c.pause(container)
		return str(response)
	except errors.APIError as e:
		response = {}
		response["status"] = "fail"
		response["message"] = e.explanation
		return str(response)
	except:
		response = {}
		response["status"] = "fail"
		response["message"] = str( sys.exc_info())
		return str(response)

#show container logs with or without timestamp
@route('/show-logs/<container>/<ts>')
def show_logs(container, ts):
	c = DockerClient.client
	try:
		response = c.logs(container=container, timestamps=ts)
		return str(response)
	except errors.APIError as e:
		response = {}
		response["status"] = "fail"
		response["message"] = e.explanation
		return str(response)
	except:
		response = {}
		response["status"] = "fail"
		response["message"] = str( sys.exc_info())
		return str(response)

@route('/rename-container/<container>/<new_name>')
def rename_container(container, new_name):
	c = DockerClient.client
	try:
		c.rename(container, new_name)
		response = {}
		response['status'] = success
		response['message'] = str(container)+" renamed to "+ str(new_name)
		return str(response)
	except errors.APIError as e:
		response = {}
		response["status"] = "fail"
		response["message"] = e.explanation
		return str(response)
	except:
		response = {}
		response["status"] = "fail"
		response["message"] = str( sys.exc_info())
		return str(response)

run(host='localhost', port=8080, debug=True)