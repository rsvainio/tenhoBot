from discord import app_commands
from discord.ext import commands
from pytubefix import YouTube
from pytubefix import Search
from pytubefix.cli import on_progress
import json

class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.downloadFolder: str = 'media/videos'
        self.videoMetadata: dict = self.loadVideoMetadata()

    def addUrl(self, url: str):
        self.downloadVideo(url)
        self.playVideo()
        print("asd")
        #player = discord.FFmpegPCMAudio(source, executable='utils/FFmpeg/bin/ffmpeg.exe')

    def addQuery(self, query: str):
        results = Search(query)
        self.downloadVideo(results.videos[0].watch_url) # download the first video in search results
        self.playVideo()

    def playVideo(self):
        return

    def downloadVideo(self, url: str):
        filename = self.isInVideoCache(url)

        if not filename:
            yt = YouTube(url, on_progress_callback=on_progress)
            print(yt.title)

            ys = yt.streams.get_audio_only()
            filename = ys.download(output_path=self.downloadFolder)
            filename = self.shortenFilepath(filename)
            # add the newly downloaded file to the metadata file here

        return filename

    def isInVideoCache(self, url) -> str:
        # search through a metadata file and return the parameter url's corresponding video file's 
        # name if it exists and return it in f'media/videos/{filename}' format
        return ''

    @staticmethod
    def shortenFilepath(path: str) -> str:
        marker = 'media/videos/'
        index = path.find(marker)
        if index != -1:
            return path[index:]
        else:
            return path  # return the original string if marker is not found

    @staticmethod
    def loadVideoMetadata() -> dict:
        with open('media/videoMetadata.json', encoding='utf-8') as f:
            return

if __name__ == '__main__':
    MusicPlayer(commands.Bot).addUrl("https://www.youtube.com/watch?v=kofR7f7oNnE")

async def setup(bot: commands.Bot):
    await bot.add_cog(MusicPlayer(bot = bot))
