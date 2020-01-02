# Monash University Woodside Building Timelapse (WIP)
A simple python script that pulls an image off [Monash University's Woodside](https://www.monash.edu/it/woodside-building) construction site every 10 minutes.

Motivations: 
* Being able to generate a time-lapse video of the building's construction.
* Was unable to find a repository of all of the images taken by the camera.
* My lonely Rapsberry Pi 2 can finally work on something.

Requires: 
* `pip3 install wget`
* `sudo apt install ffmpeg`

Features:
* Pulls an image off a website every 10 minutes
* Downloads images into individual day folders
* Uploads images into a cloud service
* Generates a timelapse video for the day at the end of the day

Usage:
* `python3 woodsideTimelapse.py`
