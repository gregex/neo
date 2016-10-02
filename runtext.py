#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
from random import randint
import time

class RunText(SampleBase):
	def __init__(self, *args, **kwargs):
		super(RunText, self).__init__(*args, **kwargs)
      
	def Run(self):
		offscreenCanvas = self.matrix.CreateFrameCanvas()
		font = graphics.Font()
		font.LoadFont("./kset.bdf")
		textColor = graphics.Color(255, 165, 0)
		pos = offscreenCanvas.width
		myText="S.A.T  v0.1"
        	     
		while True:
			offscreenCanvas.Clear()
			len = graphics.DrawText(offscreenCanvas, font, pos, 20, textColor, myText)
			pos -= 1
			if (pos + len < 0):
				pos = offscreenCanvas.width
				checkMe=int(time.strftime("%M"))
				if(checkMe%2==0):
					myText=time.strftime("%H:%M")
				else:
					myText="KSET!"
				time.sleep(0.05)    
				offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
            

# Main function
if __name__ == "__main__":
	parser = RunText()
	parser.process().Run()
