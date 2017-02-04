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
#inicijalizcija varijabli i fonta i pocetnog teksta
		self.matrix.brightness = 70
		text=[]
		sat = 0
		text.append("Neo")
		uCu=[]
		offscreenCanvas = self.matrix.CreateFrameCanvas()
		font = graphics.Font()
		font.LoadFont("kset.bdf")
		textColor = graphics.Color(255, 165, 0)
		pos = offscreenCanvas.width
		myText=''
#inicijalizacija konekcije na rabbitMQ
		con = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		chan = con.channel()
		chan.queue_declare(queue='theclock')

#fukcije za gumbice		
		def penis():
			uCu.append('./demo -D1 -t 5 --led-chain=2 penis.ppm')
		def kset():
			text.append("KSET")
		def helloKitty():
			uCu.append('./demo -D1 -t 5 --led-chain=2 maca.ppm')
		def tux():
			uCu.append('./demo -D1 -t 5 --led-chain=2 tux.ppm')

		animations={"Penis":penis,"Hello Kitty":helloKitty,"KSET":kset,"Tux":tux}


#funkcija koja se zove kada dodje nesto na queue
		def callback(ch, method, properties, body):
			body=body.decode("utf-8")
			if body in animations:
				return animations[body]()
			else:
				text.append(body)
#konzumacija podatka s queuea					
		chan.basic_consume(callback,queue='theclock',no_ack=True)        	     

#petlja koja provjerava jel neka od lista sadrzi element i sukladno tome ispisuje element neke liste
		ajde,textNova=0,[]
#		ispis = ["10","9","8","7","6","5","4","3","2","1","0", "2016...pusi...kurac"]
#		potencijalnoVrijeme = ["23:59:47","23:59:48","23:59:50","23:59:49","23:59:51"]
		while True:
			offscreenCanvas.Clear()
			leng = graphics.DrawText(offscreenCanvas, font, pos, 28, textColor, myText)
			pos -= 1
#izabire se novi prikaz
			if (pos + leng < 0):
				pos = offscreenCanvas.width
#				if len(textNova)>0:
#					myText=textNova.pop(0)
				if len(text):
					textColor=graphics.Color(0,255,0)
					myText = text[0]
					del text[0]
					sat = 0
				elif len(uCu):
#brisanje matrice, jer u suprotnom sve flickera u picku materinu
					self.matrix=''
#izvrsavanje c koda u shellu
					yay=call(uCu[0],shell=True)
					del uCu[0]
					self.matrix = RGBMatrix(self.args["rows"], self.args["chain"], self.args["parallel"])
					self.matrix.pwmBits = self.args["pwmbits"]
					self.matrix.brightness = self.args["brightness"]
					offscreenCanvas = self.matrix.CreateFrameCanvas()
					myText=time.strftime("%H:%M")
					sat = 1
				else:
					textColor=graphics.Color(255,165,0)
					myText=time.strftime("%H:%M")
					sat = 1

#			if (time.strftime("%H:%M:%S") in potencijalnoVrijeme) and len(textNova)==0:
#				textNova = ["10","9","8","7","6","5","4","3","2","1","0","2016...pusi...kurac"]
#				continue
#hehe
			if myText=="16:20" or myText=="Kpop" or myText=="420":
				textColor=graphics.Color(randint(0,255),randint(0,255),randint(0,255))
			elif myText=="12:00":
				textColor=graphics.Color(255,0,0)
				myText="bum!"
			elif myText=="16:00":
				textColor=graphics.Color(255,255,0)
				myText="gdje...je...onaj....cvijetak...zuti"
#			elif myText in ispis:
#				textColor=graphics.Color(randint(0,255),randint(0,255),randint(0,255))
			offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
#za novu godinu
#			if myText in ispis:
#				time.sleep(0.0085)

#za kontinuirano prikazivanje slika
#			if sat==1 and len(uCu)==0:
#				if ajde%5 == 0:
#					ajde+=1
#					uCu.append('./demo -D1 -t 5 --led-chain=2 chicats.ppm')
#				elif ajde%5==1:
#					ajde+=1
#					uCu.append('./demo -D1 -t 5 --led-chain=2 druga.ppm')
#				elif ajde%5==3:
#					ajde+=1
#					uCu.append('./demo -D1 -t 5 --led-chain=2 prva.ppm')
#				else:
#					ajde+=1
#					uCu.append('./demo -D1 -t 5 --led-chain=2 treca.ppm')

			if pos==-2 and sat==1:
				chan.connection.process_data_events(time_limit=3)
			else:
				chan.connection.process_data_events(time_limit=0.03)

if __name__ == "__main__":
	display=consumer()
	display.process()
		
