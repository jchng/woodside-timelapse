'''
Pulls an image every 10 minutes from Monash's Woodside construction site
Live-feed discovered on: https://www.monash.edu/it/woodside-building

Author: Jarret Jheng Ch'ng
Date created: 27/12/2019
'''

import datetime
import time
import wget
import os
# import woodsideUtilities

class WoodsideTimeLapse:

	IMAGE_URL = "http://setup.reliveit.com.au/api/installations/8827/TrgviRsRHT/latestPhotoWithMarks.jpg" # URL to download the image from
	TIME_LAPSE_OUTPUT_FPS = 5 # FPS for the output video
	CAPTURE_FREQUENCY = 10 * 60 # * 60 seconds for 10 minutes 
	CUT_OFF_TIME = "19-20-00" # for the day
	START_TIME = "06-50-00"
	RECORDING_FOLDER = "recordings/" # folder to dump downloaded pictures

	currentRecordingPath = None
	fileDate = None
	fileTime = None
	imageId = 0
	newDay = False

	def __init__(self):
		self.updateFileTimeDate()
		self.initRecordingFolder()

		time.sleep(1)
		
		self.createNewDay()
		self.startRecording()

	# Start capturing pictures
	def startRecording(self):
		while True:
			self.checkAndCreateNewFolder()

			if not self.newDay:

				self.updateFileTimeDate()

				pathName = self.currentRecordingPath + self.getImageName() + ".jpg"

				localImageFilename = wget.download(self.IMAGE_URL,pathName)

				time.sleep(self.CAPTURE_FREQUENCY-1)

	# Creates a new folder if the date changes
	def checkAndCreateNewFolder(self):

		currentTime = datetime.datetime.strptime(self.getCurrentTime(), "%H-%M-%S") 
		cutOff = datetime.datetime.strptime(self.CUT_OFF_TIME, "%H-%M-%S") 
		startTime = datetime.datetime.strptime(self.START_TIME, "%H-%M-%S") 

		if (currentTime >= cutOff):
			self.newDay = True
		elif (currentTime >= startTime):
			self.newDay = False

		if self.fileDate != self.getCurrentDate():

			print("\n\n\n ===============================\n-====== [It's a new day!] ======-\n ===============================")

			os.system("python3 woodsideUtilities.py ./ " + self.currentRecordingPath + " " + str(self.TIME_LAPSE_OUTPUT_FPS) + " &") # Runs work compiler in the background "&"

			self.createNewDay()
			self.imageId = 0

	# Update program's time
	def updateFileTimeDate(self):
		self.fileDate = self.getCurrentDate()
		self.fileTime = self.getCurrentTime()

	# Get the file name of the image
	def getImageName(self):
		# Examples:
		# image-0_DD-MM-YYYY_HH-MM-SS
		# image-1_DD-MM-YYYY_HH-MM-SS

		imageName = "image-" + str(self.imageId).zfill(3) + "_" + self.fileDate + "_" + self.fileTime
		self.imageId += 1

		return imageName

	def getCurrentDate(self):
		return time.strftime("%d-%m-%Y", time.localtime())

	def getCurrentTime(self):
		return time.strftime("%H-%M-%S", time.localtime())

	def createNewDay(self):
		'''Creates a new folder for a new day'''
		try:
			os.mkdir(self.RECORDING_FOLDER + self.getCurrentDate())
		except FileExistsError:
			pass

		self.currentRecordingPath = self.RECORDING_FOLDER + self.getCurrentDate() + "/"

	# Check if the recording folder exists, creates one if it does not
	def initRecordingFolder(self):
		'''Creates a new folder for the photos/videos'''
		try:
			os.mkdir(self.RECORDING_FOLDER)
		except FileExistsError:
			pass

if __name__ == '__main__':
	WoodsideTimeLapse()