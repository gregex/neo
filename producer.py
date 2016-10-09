from flask import Flask, render_template,request,redirect,json
from time import sleep
from datetime import datetime
from os import system
import pika
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
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

@app.route('/gasimasinu')
def turnoff():
	system('sudo poweroff')

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
 
