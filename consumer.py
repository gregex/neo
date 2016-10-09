#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics,RGBMatrix
from random import randint
import time
import pika
from subprocess import call

class consumer(SampleBase):
	def __init__(self, *args, **kwargs):
		super(consumer, self).__init__(*args, **kwargs)  	

	def Run(self):
		text=[]
		text.append("NeoV1")
		uCu=[]
		offscreenCanvas = self.matrix.CreateFrameCanvas()
		font = graphics.Font()
		font.LoadFont("kset.bdf")
		textColor = graphics.Color(255, 165, 0)
		pos = offscreenCanvas.width
		myText=''

		con = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		chan = con.channel()
		chan.queue_declare(queue='theclock')
		
		def penis():
			uCu.append('./demo -D1 -t 5 --led-chain=2 maca.ppm')
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
				elif len(uCu):
					self.matrix=''
					yay=call(uCu[0],shell=True)
					del uCu[0]
					self.matrix = RGBMatrix(self.args["rows"], self.args["chain"], self.args["parallel"])
					self.matrix.pwmBits = self.args["pwmbits"]
					self.matrix.brightness = self.args["brightness"]
					offscreenCanvas = self.matrix.CreateFrameCanvas()
					myText=time.strftime("%H:%M")
				else:
					myText=time.strftime("%H:%M")
    
			offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
			chan.connection.process_data_events(time_limit=0.05)

if __name__ == "__main__":
	display=consumer()
	display.process()
		
