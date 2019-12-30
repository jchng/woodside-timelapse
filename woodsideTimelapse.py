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
	CUT_OFF_TIME = "19-20-00" 	# Stops recording after 
	START_TIME = "06-50-00" 	# Start recording after
	RECORDING_FOLDER = "recordings/" # folder to dump downloaded pictures

	currentRecordingPath = None # The current download folder
	fileDate = None				# the latest date file written
	fileTime = None				# "	  "		 time file written
	imageId = 0					#
	waitForStart = True			# checks if it is waiting for the start time


	def __init__(self):
		self.addToLog("Initialising folders")
		self.updateFileTimeDate()
		self.initRecordingFolder()

		time.sleep(1) # wait for all folders to be created before moving on
		
		self.createNewDay() # creates a new day folder
		self.startRecording() # start recording


	# Start capturing pictures from website and dumping it into the respective folders
	def startRecording(self):

		self.addToLog("Start recording")

		while True: # Goes on forever until ctrl + c
			self.checkAndCreateNewFolder() # check if a new folder is needed, also checks for cutoff/start times

			if not self.waitForStart: # if not waiting for new day, record

				self.updateFileTimeDate() # update file names

				pathName = self.currentRecordingPath + self.getImageName() + ".jpg" # get the correct paths

				localImageFilename = wget.download(self.IMAGE_URL,pathName) # download the image from website

				self.addToLog("Captured image: " + str(self.imageId).zfill(3)) 

				self.imageId += 1 # for ffmpeg sorting purposes

			time.sleep(self.CAPTURE_FREQUENCY-1) # wait until next frame


	# Prints to stdout with a timestamp
	def addToLog(self, message):
		print("\n[" + self.getCurrentDate() + " " + self.getCurrentTime().replace("-",":") + "]:	" + message + "\n")


	# Check if a new folder is needed (creates one on a new day), also checks for cutoff/start times
	def checkAndCreateNewFolder(self):

		# Convert all times into datetime object for comparison purposes
		currentTime = datetime.datetime.strptime(self.getCurrentTime(), "%H-%M-%S") 
		cutOff = datetime.datetime.strptime(self.CUT_OFF_TIME, "%H-%M-%S") 
		startTime = datetime.datetime.strptime(self.START_TIME, "%H-%M-%S") 

		# If the current time is after the cut off time and it is not waiting for start time yet
		if (currentTime >= cutOff) and not self.waitForStart:
			self.addToLog("Recording paused automatically. (End of day)")
			self.addToLog("Archiving today's work.")

			# Run the python script for archiving
			os.system("python3 woodsideUtilities.py ./ " + self.currentRecordingPath + " " + str(self.TIME_LAPSE_OUTPUT_FPS) + " &") # Runs work compiler in the background "&"
			self.waitForStart = True

		# If the current time is before cutoff time and after start time and is currently waiting for start time
		elif (cutOff >= currentTime >= startTime) and self.waitForStart:
			self.addToLog("Recording resumed automatically.")

			# disable wait
			self.waitForStart = False

		# Creates a new folder when the date changes
		if self.fileDate != self.getCurrentDate():

			self.addToLog("It's a new day!")

			self.createNewDay()
			self.imageId = 0 # resets the image id

			self.updateFileTimeDate()


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

		return imageName


	# Get the current date as a string
	def getCurrentDate(self):
		return time.strftime("%d-%m-%Y", time.localtime())


	# Get the current time as a string
	def getCurrentTime(self):
		return time.strftime("%H-%M-%S", time.localtime())


	# Create a new folder for a new day
	def createNewDay(self):
		try:
			os.mkdir(self.RECORDING_FOLDER + self.getCurrentDate())
			self.addToLog("New recording day folder created.")
		except FileExistsError:
			pass

		self.currentRecordingPath = self.RECORDING_FOLDER + self.getCurrentDate() + "/"


	# Check if the recording folder exists, creates one if it does not
	def initRecordingFolder(self):
		try:
			os.mkdir(self.RECORDING_FOLDER)
		except FileExistsError:
			pass

if __name__ == '__main__':
	WoodsideTimeLapse()