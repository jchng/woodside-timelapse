'''
Pulls an image every 10 minutes from Monash's Woodside construction site
Live-feed discovered on: https://www.monash.edu/it/woodside-building

Author: Jarret Jheng Ch'ng
Date created: 27/12/2019
'''

import time
import wget
import os

class WoodsideTimeLapse:

	IMAGE_URL = "http://setup.reliveit.com.au/api/installations/8827/TrgviRsRHT/latestPhotoWithMarks.jpg"
	TIME_LAPSE_OUTPUT_FPS = 5
	CUT_OFF_TIME = "7:10 PM"
	START_TIME = "UNKNOWN"
	RECORDING_FILE = "recordings/"

	currentDate = None
	currentTime = None
	imageId = 0

	def __init__(self):
		currentDate = self.getCurrentDate()
		currentTime = self.getCurrentTime()
		self.initRecordingFolder()
		time.sleep(1)
		self.createNewDay()

	# def startRecording(self):


	def getImageName(self):
		# Examples:
		# image-0_DD-MM-YYYY_HH-MM-SS
		# image-1_DD-MM-YYYY_HH-MM-SS

		imageName = "image-" + str(imageId) + currentDate + "_" + currentTime
		imageId += 1

		return imageName

	def getCurrentDate(self):
		return time.strftime("%d-%m-%Y", time.localtime())

	def getCurrentTime(self):
		return time.strftime("%H-%M-%S", time.localtime())

	def createNewDay(self):
		'''Creates a new folder for a new day'''
		try:
			os.mkdir(self.RECORDING_FILE + self.getCurrentDate())
		except FileExistsError:
			pass

	def initRecordingFolder(self):
		'''Creates a new folder for the photos/videos'''
		try:
			os.mkdir(self.RECORDING_FILE)
		except FileExistsError:
			pass

	# while True:
	# 	fileName = time.strftime("%d-%m-%Y_%I-%M-%S-%p", time.localtime()) + ".jpg"

	# 	localImageFilename = wget.download(IMAGE_URL,fileName)

	# 	time.sleep(600)

if __name__ == '__main__':
	WoodsideTimeLapse()