'''
A utilities class for compiling images into a timelapse and uploading it into transfer.sh

Author: Jarret Jheng Ch'ng
Date created: 28/12/2019
'''

import os
import time

class BackgroundUtilities:

	FRAMES_ARCHIVE_NAME = "frames.tar.gz"
	URL_FILE_NAME = "archive-downloads.txt"

	def __init__(self, urlsPath, framesFolder):
		self.urlFile = urlsPath + self.URL_FILE_NAME
		self.framesFolder = framesFolder

	# creates the time lapse for the day, compresses and uploads
	def createVideoCompressAndUpload(self):
		self.createVideo()
		time.sleep(1)
		self.compress()
		time.sleep(1)
		self.upload()

	def compress(self):
		print('Compressing')
		os.system("tar -czvf " + self.framesFolder + self.FRAMES_ARCHIVE_NAME + " " + self.framesFolder)

	def upload(self):
		print('Uploading')
		downloadLink = os.popen("curl --upload-file " + self.framesFolder + self.FRAMES_ARCHIVE_NAME + \
			" https://transfer.sh/woodside_archive_" + time.strftime("%d-%m-%Y", time.localtime())).read() + ".tar.gz\n"
		
		file = open(self.urlFile,"a+")
		file.write(downloadLink)
		file.close()

	def createVideo(self):
		print('Compiling')
		os.system("ffmpeg -framerate " + str(TIME_LAPSE_OUTPUT_FPS) + " -i image-%000d%*.jpg -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p " + self.framesFolder + "timelapse.mp4")


if __name__ == '__main__':
	BackgroundUtilities("./","./testDir").compressAndUpload()