from flask import Flask, render_template,request,redirect,json
from time import sleep
from datetime import datetime
from os import system

#setTime='sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"'
app = Flask(__name__)
#system(setTime)

textToDisplay=[]
beingUsed=0

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/suggestion',methods=['POST'])
def suggestion():
	suggestion = request.form['suggestion']
	file=open("suggestions.txt","a")
	file.write(suggestion)
	file.write("/n")
	file.close()
	return redirect('/')

@app.route('/text',methods=['POST'])
def text():
	global textToDisplay
	text = request.form['text']
	textToDisplay.append(text)
	return redirect('/')


if __name__ == '__main__':
	app.run(host="0.0.0.0")
 
