# http://setup.reliveit.com.au/api/installations/8827/TrgviRsRHT/latestPhotoWithMarks.jpg

import time
import wget

image_url = "http://setup.reliveit.com.au/api/installations/8827/TrgviRsRHT/latestPhotoWithMarks.jpg"

while True:
	fileName = time.strftime("%d-%m-%Y_%I-%M-%S-%p", time.localtime()) + ".jpg"

	localImageFilename = wget.download(image_url,fileName)

	time.sleep(600)