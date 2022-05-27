#!/usr/bin/env python
import pytube
from pytube import YouTube
from rich.console import Console
from rich.progress import Progress
import os

console = Console()

class Downloader:
    def __init__(self):
        pass

    def progress(self, stream, chunk, bytes_remaining):
        with Progress(refresh_per_second= 0.2, transient= True) as progress:
            downloadTask = progress.add_task("[green]Downloading...", total= (stream.filesize * 100))

            while not progress.finished:
                progress.update(downloadTask, advance= (100 - round(bytes_remaining / stream.filesize * 100)))

    def download(self, url):
        #exception handling
        try:
            yt = YouTube(str(url), on_progress_callback= self.progress)

        except Exception:
            pass
        
        else:     
            stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
            stream.download(os.getcwd() + "/videos/", filename= "video.mp4")
            console.log("Downloaded a video")