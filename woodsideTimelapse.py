'''
Pulls an image every 10 minutes from Monash's Woodside construction site
Live-feed discovered on: https://www.monash.edu/it/woodside-building

Author: Jarret Jheng Ch'ng
Date created: 27/12/2019
'''

import time
import wget
import os
# import woodsideUtilities

class WoodsideTimeLapse:

	IMAGE_URL = "http://setup.reliveit.com.au/api/installations/8827/TrgviRsRHT/latestPhotoWithMarks.jpg" # URL to download the image from
	TIME_LAPSE_OUTPUT_FPS = 5 # FPS for the output video
	CAPTURE_FREQUENCY = 5 # * 60 for 10 minutes 
	#CUT_OFF_TIME = "7:03 PM"
	#START_TIME = "UNKNOWN"
	RECORDING_FOLDER = "recordings/" # folder to dump downloaded pictures

	currentRecordingPath = None
	fileDate = None
	fileTime = None
	imageId = 0

	def __init__(self):
		self.updateTimeDate()
		self.initRecordingFolder()
		time.sleep(1)
		self.createNewDay()

		self.startRecording()

	# Start capturing pictures
	def startRecording(self):
		while True:
			self.checkAndCreateNewFolder()

			self.updateTimeDate()

			pathName = self.currentRecordingPath + self.getImageName() + ".jpg"

			localImageFilename = wget.download(self.IMAGE_URL,pathName)

			time.sleep(self.CAPTURE_FREQUENCY)

	# Creates a new folder if the date changes
	def checkAndCreateNewFolder(self):
		if self.fileDate != self.getCurrentDate():
			print("It's a new day!")
			os.system("python3 woodsideUtilities.py ./ " + self.currentRecordingPath + " &") # Runs work compiler in the background "&"
			self.createNewDay()
			self.imageId = 0

	# Update program's time
	def updateTimeDate(self):
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