import discord
from discord.ext import commands
from pytubefix import YouTube
from pytubefix import Search
from pytubefix.cli import on_progress

#TODO: should make a list of downloaded videos so that they don't need to be redownloaded
downloadFolder: str = 'media/videos'

@commands.command()
async def addUrl(url: str):
    await downloadVideo(url)
    playVideo()
    #player = discord.FFmpegPCMAudio(source, executable='utils/FFmpeg/bin/ffmpeg.exe')

async def addQuery(query: str):
    results = Search(query)
    await downloadVideo(results.videos[0].watch_url) # download the first video in search results
    playVideo()

async def playVideo():
    return

async def downloadVideo(url: str):
    filename = isInVideoCache(url)

    if not filename:
        yt = YouTube(url, on_progress_callback=on_progress)
        print(yt.title)

        ys = yt.streams.get_audio_only()
        filename = ys.download(output_path=downloadFolder)
        filename = shortenFilepath(filename)
        # add the newly downloaded file to the metadata file here

    return filename


def isInVideoCache(url) -> str:
    # search through a metadata file and return the parameter url's corresponding video file's 
    # name if it exists and return it in f'media/videos/{filename}' format
    return ''

def shortenFilepath(path: str) -> str:
    marker = 'media/videos/'
    index = path.find(marker)
    if index != -1:
        return path[index:]
    else:
        return path  # return the original string if marker is not found
