from flask import Flask,redirect, url_for,request,render_template
import os
import subprocess
import re
import json
import math
app = Flask(__name__)
import pymongo
import requests

motorcntrl="192.168.240.168"
mong="192.168.240.95"



@app.route('/dashbd/<name>')
def dash(name):
   
  client = pymongo.MongoClient("mongodb://jawa:password@"+mong+":27017/?authMechanism=DEFAULT")
  db = client["docker"]
   # Collection Name
  col = db["users"]
  x = col.find_one({
     "username": name
  })
  return render_template('web.html',data={"title":"Dashboadsss","id":x['dockeripaddress'],"port":x['port'],"sship":x['sship'] })

# templates------------------

@app.route('/')
def hello_():
   return render_template('login.html')

@app.route('/regis')
def reg():
   return render_template('register.html')




# logics--------------------------

@app.route('/login',methods=['POST'])
def login(): 
  if 'username' in request.form and 'password' in request.form:
    username = request.form['username']
    password = request.form['password']

    client = pymongo.MongoClient("mongodb://jawa:password@"+mong+":27017/?authMechanism=DEFAULT")
    db = client["docker"]

    col = db["users"]

    result=col.find_one({
            "username": username
        })
    if result:
            if result['password']==password:
                return redirect(url_for('dash',name=username))
            else:
               raise Exception("incorrect password")
    return 
  
  else:
    return {
            "message": "Not enough parameters",
            "authenticated": False
         }, 400



@app.route('/register',methods=['POST'])
def register(): 
  if 'username' in request.form and 'password' in request.form and 'email' in request.form:
    username = request.form['username']
    password = request.form['password']
    email =request.form['email']

    client = pymongo.MongoClient("mongodb://jawa:password@"+mong+":27017/?authMechanism=DEFAULT")
    db = client["docker"]

    col = db["users"]

    id=col.insert_one({
            "username":username,
            "password":password,
            "email":email,
        })
    if id:
      #docker assign and ip finding update on db
      docker_logic(username)
      return redirect(url_for('hello_'))
       


def docker_logic(username):
   myclient = pymongo.MongoClient("mongodb://jawa:password@"+mong+":27017/?authMechanism=DEFAULT")
   db=myclient["docker"]
   user3=db.users
   mydoc = user3.find().sort("port", -1).limit(1)
   for x in mydoc:
      portnum=x['port']+1
   
   os.system("sudo docker run --name "+username+" -p "+str(portnum)+":22 -dit --restart unless-stopped ssh_con:v1")
   a=subprocess.check_output(["sudo", "docker", "inspect","--format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'",username])
   
   ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', str(a))
   ipaddres=ip[0]

   myclient = pymongo.MongoClient("mongodb://jawa:password@"+mong+":27017/?authMechanism=DEFAULT")
   db=myclient["docker"]
   user2=db.users
   filter = { 'username': username }
 
   newvalues = { "$set": {
            "dockeripaddress":ipaddres,
            "sship":mong,
            "port":portnum
            
        } }
    
   id2=user2.update_one(filter, newvalues)
  
   

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=1134,debug=True)   # 0000 acept all public and localhost also