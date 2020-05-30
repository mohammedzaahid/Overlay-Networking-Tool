import os
import sys
import subprocess
from subprocess import Popen
from flask import Flask
import threading
from threading import Thread
from influxdb import InfluxDBClient
from flask import abort
from functools import wraps
from flask import request, Response, make_response


stark = Flask(__name__)

# Now if necessary I can modify this........

eth_val = "eth_value"
influx_db = "Use your database"
user_name = "stark"
pass_word = "stark"
host_ip ="localhost"



#This is for security 
def check_access(username, password):
	return username == user_name and password == pass_word
#This you can change the security access for the curl requests



def authenticate():
	"""Sends a 401 response that enables basic auth"""
	return Response(
	'\n\nCould not verify your access level for that URL.\n\n'
	'\n\nYou have to login with proper credentials\n\n', 401,
	{'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_login(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_access(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated

# This is for Influxdb to store the data of bitrate and timestamps with dynamic tag values
def influx(str,stream):
	counter=8
	linenum=1
	client=InfluxDBClient(host_ip,8086,user_name,pass_word,database=influx_db)
	for line in iter(str.readline,''):
		line=line.rstrip()
		if(line == ''):
			pass
		elif(linenum > counter):		
			lines=line.split()
			time=lines[0]
			bit_rate=lines[1].split('.')
			json_body=[ 
        	      {
        	       "measurement": "bitrate",
        	       "tags": {                   
				"Dynamic_tag": "{0}".format(stream),    
        	        },
        	       "fields": {
        	            "value": bit_rate[0],
			    "timestamp": time
        	        }
        	      }
		     ]
	
		        client.write_points(json_body)		
		linenum = linenum+1


# This starts the process of dpmi_streams to start the process
@stark.route('/run/<stream>', methods=['GET'])
@requires_login
def run(stream):
	global gstream
	if not gen_stream:
		gen_stream.append(stream) 
		gstream=gstream+gen_stream 
		bitrate_thread(stream)
		return '\n...Consumer-Bitrate Stream %s Has Started...\n\n' %stream

	if stream in gstream:
			return '\n... bitrate stream %s is already running...\n\n' %stream
	else:

		return '\n...I can\'t run %s stream here, use add to run another...\n\n'%stream


global gstream
gstream=[]


# This is used to stop Bitrates
@stark.route('/stop', methods=['GET'])
@requires_login
def stop():
	os.system("sudo pkill bitrate")
	del (gstream[:],gen_stream[:])
	return "\n...DPMI Bitrate Stopped!!!!!!!!...\n\n"


#This is used to Show the status of running streams
@stark.route('/show', methods=['GET'])
@requires_login
def show():
	if gstream >= [1]:
		show=" ".join(str(R) for R in gstream)
		return '\n... %s, These streams are Present...\n\n' %show
	else:
		return ' \n\n No streams are running to show \n\n'
	
#This is used to add streams 
@stark.route('/add/<add>', methods=['GET'])
@requires_login
def add(add):
	global gstream
	if add in gstream:
		return'\n\n This already exists please add another \n\n'
	else:	
		addstream=add.split(',')
		new=[]
		new=list(set(addstream))
		strnew=" ".join(str(n) for n in new) 
		gstream=gstream+new	
		for stream in new:
			bitrate_thread(stream)
		return '\n\n  stream added %s.....\n\n' %strnew  



global gen_stream
gen_stream=[]


#This is used to delete streams 
@stark.route('/delete/<dele>', methods=['GET'])
@requires_login
def delete(dele):
	global gstream	
	if dele not in gstream:
		return'\n\n This %s stream is not present...\n\n' %dele
	else:	
		dele=dele.split(',')
		deleting=[]
		deleting=list(set(dele).intersection(gstream))
		strdeleting=",".join(str(l) for l in deleting) 
		gstream=list(set(gstream)-set(deleting))
		strgstream=",".join(str(x) for x in gstream)
		os.system("sudo pkill bitrate")
		for stream in gstream:
			bitrate_thread(stream)
		return "\n\n Bitrate stream deleted  \n\n"


#This is used to change streams 
@stark.route('/change/<stream>', methods=['GET'])
@requires_login
def change(stream):
	global change_stream
	global gstream
	global gen_stream
	change_stream = stream
	if change_stream in gstream: 
		return '\n...This %s stream currently running, change to another stream...\n\n' %change_stream	
	else:
		stop()
		del gen_stream[:]
		gstream=list(set(gstream)-set(gen_stream))
		run(change_stream)
		return '\n...bitrate stream changed to %s...\n\n' %change_stream	


#This starts the process 
def bitrate_thread(stream):
	bitrate_thread=threading.Thread(target=start_process,args=(stream,))
	bitrate_thread.deamon=True	
	bitrate_thread.start()

def start_process(str):
	start_process=subprocess.Popen(["unbuffer","bitrate","-i",eth_val,str],stdout=subprocess.PIPE)  
	influx_thread=threading.Thread(target=influx,args=(start_process.stdout,str,)) 
	influx_thread.start()

if __name__ == "__main__":
	stark.run(host='localhost', port=5000, debug=True) 
