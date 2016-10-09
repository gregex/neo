#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
from random import randint
import time
import pika
from os import system

class consumer(SampleBase):
	def __init__(self, *args, **kwargs):
		super(consumer, self).__init__(*args, **kwargs)  	
	
	def Run(self):
		offscreenCanvas = self.matrix.CreateFrameCanvas()
		font = graphics.Font()
		font.LoadFont("kset.bdf")
		textColor = graphics.Color(255, 165, 0)
		pos = offscreenCanvas.width
		text=[]
		myText=''
		con = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		chan = con.channel()
		chan.queue_declare(queue='theclock')
		text.append("NEO THE CLOCK")
		def penis():
			text.append("8==o")
			print('do penis')
		def kset():
			text.append("KSET")
			print("do kset")
		def matrix():
			print('do matrix')
		
		animations={"Penis":penis,"Matrix":matrix,"KSET":kset}

		def callback(ch, method, properties, body):
			body=body.decode("utf-8")
			if body in animations:
				return animations[body]()
			else:
				text.append(body)
					
		chan.basic_consume(callback,queue='theclock',no_ack=True)
        	     
		while True:
			offscreenCanvas.Clear()
			leng = graphics.DrawText(offscreenCanvas, font, pos, 20, textColor, myText)
			pos -= 1
			if (pos + leng < 0):
				pos = offscreenCanvas.width
				if len(text):
					myText=text[0]
					del text[0]
				else:
					myText=time.strftime("%H:%M")    
			offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
			chan.connection.process_data_events(time_limit=0.05)

# Main function
if __name__ == "__main__":
#	setTime='sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"'
#	system(setTime)
	display = consumer()
	display.process().Run()
