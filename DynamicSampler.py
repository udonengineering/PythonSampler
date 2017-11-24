import Tkinter as tk
import tkFileDialog
import tkMessageBox
import winsound
import math
import os

class DynamicSampler:
	def __init__(self):
		self.buttonList = []
		self.keyList = "qwertyuiopasdfghjklzxcvbnm"
		self.root = tk.Tk()
		self.root.title("Dynamic Sampler")
		self.doQWERTY = tk.BooleanVar()
		self.root.configure(background="#242424")
		self.menuBar = tk.Menu(self.root)
		self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
		self.menuBar.add_cascade(label="File", menu=self.fileMenu)
		self.fileMenu.add_command(label='Import Folder', compound=tk.LEFT, command=self.wav_browser)
		self.fileMenu.add_checkbutton(label='QWERTY Layout', variable=self.doQWERTY)
		self.root.config(menu=self.menuBar)
		self.root.bind_all("<KeyPress-space>", self.stop_sound)
		self.root.mainloop()

	def wav_browser(self):
		wavPath = tkFileDialog.askdirectory(parent=self.root, title='Choose a folder with .wav samples.', initialdir="")
		if ( wavPath ):
			self.clear_buttons()
			self.run_crawler(wavPath)

	def clear_buttons(self):
		print "Clearing buttons..."
		for tempButton in self.buttonList:
			tempButton.grid_forget()
			tempButton.destroy()
		self.buttonList = []
		for letter in self.keyList:
			self.root.unbind_all("<KeyPress-" + letter + ">")

	def run_crawler(self, wavPath):
		print "Running crawler..."
		myCrawler = FileCrawler(wavPath, [".wav"])
		if ( self.doQWERTY.get() ):
			self.build_qwerty_gui(myCrawler.sampleList)
		else:
			self.build_standard_gui(myCrawler.sampleList)

	def build_standard_gui(self, sampleList):
		print "Building standard GUI..."
		numColumns = int(math.sqrt(len(sampleList)))
		currentColumn = 0
		currentRow = 0
		for sample in sampleList:
			self.add_button(currentRow, currentColumn, sample, "")
			if ( currentColumn < numColumns ):
				currentColumn += 1
			else:
				currentColumn = 0
				currentRow += 1
		for i in range(numColumns+1):
			self.root.columnconfigure(i, minsize=100)
		for i in range(currentRow+1):
			self.root.rowconfigure(i, minsize=50)

	def build_qwerty_gui(self, sampleList):
		if ( len(sampleList) > len(self.keyList) ):
			tkMessageBox.showerror("Error", "Too many samples for QWERTY layout!\nBuilding standard GUI.")
			self.build_standard_gui(sampleList)
		else:
			print "Building QWERTY GUI..."
			currentColumn = 0
			currentRow = 0
			sampleNum = 0
			for sample in sampleList:
				if ( currentRow == 0 ):
					if ( currentColumn < 10 ):
						self.add_button(currentRow, currentColumn, sample, self.keyList[sampleNum])
						currentColumn += 1
						sampleNum +=1
					else:
						currentColumn = 0
						currentRow = 1
				elif ( currentRow == 1 ):
					if ( currentColumn < 9 ):
						self.add_button(currentRow, currentColumn, sample, self.keyList[sampleNum])
						currentColumn += 1
						sampleNum +=1
					else:
						currentColumn = 0
						currentRow = 2
				elif ( currentRow == 2 ):
					self.add_button(currentRow, currentColumn, sample, self.keyList[sampleNum])
					currentColumn += 1
					sampleNum +=1
			for i in range(10):
				self.root.columnconfigure(i, minsize=100)
			for i in range(3):
				self.root.rowconfigure(i, minsize=50)

	def add_button(self, gridrow, gridcolumn, sampleName, shortcut):
		tempName = sampleName.split('\\')[-1].replace(".wav","")
		if ( shortcut != "" ):
			tempName = shortcut + "\n" + tempName
		tempButton = tk.Button(self.root, text=tempName, bg="#242424", fg="white", command=lambda:self.play_sound(sampleName))
		if ( shortcut != "" ):
			self.root.bind_all("<KeyPress-" + shortcut + ">", lambda e:self.play_sound(sampleName))
			print "Binding " + shortcut + " to sample " + sampleName
		self.buttonList.append(tempButton)
		tempButton.grid(row=gridrow, column=gridcolumn, sticky='wens')

	def play_sound(self, sampleName):
		if ( sampleName == "" ):
			self.stop_sound()
		else:
			winsound.PlaySound(sampleName, winsound.SND_ASYNC)
			print "Playing..." + sampleName

	def stop_sound(self, event):
		winsound.PlaySound(None, winsound.SND_ASYNC)

class FileCrawler:
	
	def __init__(self, startPath, extList):
		self.startPath = startPath
		self.extList = extList
		self.sampleList = []
		self.find_samples(startPath)

	def find_samples( self, currentPath ):
		for root, dirs, files in os.walk(currentPath):
			for filename in files:
				for extension in self.extList:
					if ( filename.lower().endswith(extension) ):
						fullpath = os.path.join(root, filename)
						self.sampleList.append(fullpath)

app = DynamicSampler()