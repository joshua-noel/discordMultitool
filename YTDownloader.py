#!/usr/bin/env python
import pytube
from pytube import YouTube
import os

class Downloader:
    def __init__(self):
        pass

    def download(self, url):
        #exception handling
        try:
            yt = YouTube(str(url))

        except pytube.exceptions.RegexMatchError:
            print("Invalid URL")
            return 0

        except pytube.exceptions.VideoUnavailable:
            print("Video unavailable")
            return 0

        except pytube.exceptions.ExtractError:
            print("Error extracting video")
            return 0
        
        except pytube.exceptions.HTMLParseError:
            print("Error parsing HTML")
            return 0

        except pytube.exceptions.LiveStreamError(url):
            print("Live stream")
            return 0

        except pytube.exceptions.MaxRetriesExceeded:
            print("Max retries exceeded")
            return 0
        
        else:    
            print("Dowmlading {}".format(yt.title))    
            stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
            stream.download(os.getcwd() + "/videos/", filename= "video.mp4")
