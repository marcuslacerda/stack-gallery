from stack import app
from stack.security import login_authorized

import requests
from flask import request, session

def get_technology(id, oauth_token):
  url = 'https://tech-gallery.appspot.com/_ah/api/rest/v1/technology/%s' % id
  headers = {'Authorization': oauth_token}
  response = requests.get(url=url, headers= headers)

  return response.text

@app.route('/technology/<id>')
@login_authorized
def list_technology(userid, id):
  print ('user - %s' % userid)
  #print (request.headers)
  url = 'https://tech-gallery.appspot.com/_ah/api/rest/v1/technology/%s' % id
  response = requests.get(url=url)

  return response.text

@app.route('/technologies')
def technologies():
  access_token = session.get('access_token')  
  url = 'https://tech-gallery.appspot.com/_ah/api/rest/v1/technology'

  oauth_token = 'OAuth ' + access_token[0]
  headers = {'Authorization': oauth_token}
  print('==> %s' % headers)
  response = requests.get(url=url, headers= headers)

  return response.text