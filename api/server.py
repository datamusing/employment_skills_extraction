import os
import json
import string
from bottle import route, run, request, abort
from urllib2 import urlopen
import socket

import process_request
pr = process_request.process_request()

@route('/post', method='POST')
def post_data():

    # Collect json post data
    data = ""
    for line in request.body:
        data += line.strip()

    # Exit if post does not contain data
    if not data or data == "":
        abort(400, 'No data received')

    # Process post data
    response = pr.process(data)

    return response


if __name__ == '__main__':

    # Local Version
    # -------------
    thisURL = "localhost"
    run(host=thisURL, port=8080)

    # AWS Version
    # -------------
    #thisURL = "http://169.254.169.254/latest/meta-data/public-hostname"
    #publicURL = urlopen(thisURL).read()
    #HOSTNAME = socket.gethostname()
    #run(host=HOSTNAME, port=8080)
