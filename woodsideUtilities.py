'''
A utilities class for compiling images into a timelapse and uploading it to 0x0.st (was transfer.sh)

Author: Jarret Jheng Ch'ng
Date created: 28/12/2019

Usage: 
python3 woodsideUtilities [path to url text file] [path to downloaded frames folder] [fps for video]

'''

import os
import sys
import time

class BackgroundUtilities:

	FRAMES_ARCHIVE_NAME = "frames.tar.gz" # default archive name
	URL_FILE_NAME = "archive-downloads.txt" # saves all archive urls into this text file


	def __init__(self):

		self.urlFile = sys.argv[1] + self.URL_FILE_NAME 
		self.framesFolder = sys.argv[2]
		self.TIME_LAPSE_OUTPUT_FPS = int(sys.argv[3])

		# pulling the date straight from the path string (it's ugly)
		self.archiveDate = self.framesFolder.split('/')[-2]


	# creates the time lapse for the day, compresses and uploads
	def createVideoCompressAndUpload(self):

		self.addToLog("Archiving " + self.archiveDate)

		self.addToLog("Encoding video")
		self.createVideo()

		time.sleep(1)
		
		self.addToLog("Compressing files")
		self.compress()
		
		time.sleep(1)

		self.addToLog("Uploading files")
		self.upload()

		self.addToLog("Archived and uploaded")


	# Compiles the frames into a video with a specified fps
	def createVideo(self):
		# regex to find all files with image-[number][number][number]_[[anything]...].jpg
		os.system("ffmpeg -framerate " + str(self.TIME_LAPSE_OUTPUT_FPS) + " -pattern_type glob -i " + self.framesFolder + "\"image-[0-9][0-9][0-9]_*.jpg\" -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p " + self.framesFolder + "timelapse.mp4")


	# Compresses the contents of the folder
	def compress(self):
		os.system("tar -czf " + self.framesFolder + self.FRAMES_ARCHIVE_NAME + " " + self.framesFolder)


	# Uploads the archive to 0x0.st and saves url into a urls text file
	def upload(self):
		downloadLink = os.popen("curl -F '@=" + self.framesFolder + self.FRAMES_ARCHIVE_NAME + \
			"' https://0x0.st/").read()
		
		file = open(self.urlFile,"a+") # append to a file, creates one if it doesn't already exist
		file.write(self.archiveDate + ":	" + downloadLink + "\n")
		file.close()


	# Prints to stdout with a timestamp
	def addToLog(self, message):
		print("\n[" + time.strftime("%d-%m-%Y", time.localtime()) + " " + time.strftime("%H-%M-%S", time.localtime()).replace("-",":") + "]:	" + message + "\n")


if __name__ == '__main__':
	BackgroundUtilities().createVideoCompressAndUpload()
	# BackgroundUtilities("./","./testDir")