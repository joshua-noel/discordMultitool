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

        except pytube.exceptions.RegexMatchError:
            console.print("[red]Invalid URL[/red]")
            return 0

        except pytube.exceptions.VideoUnavailable:
            console.print("[red]Video unavailable[/red]")
            return 0

        except pytube.exceptions.ExtractError:
            console.print("[red]Error extracting video[/red]")
            return 0
        
        except pytube.exceptions.HTMLParseError:
            console.print("[red]Error parsing HTML[/red]")
            return 0

        except pytube.exceptions.LiveStreamError(url):
            console.print("[red]Live stream[/red]")
            return 0

        except pytube.exceptions.MaxRetriesExceeded:
            console.print("[red]Max retries exceeded[/red]")
            return 0
        
        else:     
            stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
            stream.download(os.getcwd() + "/videos/", filename= "video.mp4")
            console.print("[green]Downloaded a video[/green]")