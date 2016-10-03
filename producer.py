from flask import Flask, render_template,request,redirect,json
from time import sleep
from datetime import datetime
from os import system
import pika
from werkzeug.contrib.fixers import ProxyFix

#setTime='sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"'
app = Flask(__name__)
#system(setTime)
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/suggestion',methods=['POST'])
def suggestion():
	suggestion = request.form['suggestion']
	file=open("suggestions.txt","a")
	file.write(suggestion+"\n")
	file.close()
	return redirect('/')

@app.route('/text',methods=['POST'])
def text():
	text=request.form['text']
	con=pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
	chan=con.channel()
	chan.queue_declare(queue='theclock')
	chan.basic_publish(exchange="",routing_key='theclock',body=text)
	con.close()
	return redirect('/')

@app.route('/animation',methods=['POST'])
def button():
	button=request.form['button']
	print(button)
	con=pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
	chan=con.channel()
	chan.queue_declare(queue='theclock')
	chan.basic_publish(exchange="",routing_key='theclock',body=button)
	con.close()
	return redirect('/')

if __name__ == '__main__':
	app.run(host="0.0.0.0")
 
