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

    def addUrl(self, url: str):
        self.downloadVideo(url)
        self.playVideo()
        #player = discord.FFmpegPCMAudio(source, executable='utils/FFmpeg/bin/ffmpeg.exe')

    def addQuery(self, query: str):
        results = Search(query)
        self.downloadVideo(results.videos[0].watch_url) # download the first video in search results
        self.playVideo()

    def playVideo(self):
        return

    def downloadVideo(self, url: str):
        yt = YouTube(url, on_progress_callback=on_progress)
        print(yt.title)

        ys = yt.streams.get_audio_only()
        filename = ys.download(output_path=self.downloadFolder)
        filename = self.shortenFilepath(filename)
        # add the newly downloaded file to the metadata file here

        return filename

    @staticmethod
    def shortenFilepath(path: str) -> str:
        marker = 'media/videos/'
        index = path.find(marker)
        if index != -1:
            return path[index:]
        else:
            return path  # return the original string if marker is not found

if __name__ == '__main__':
    MusicPlayer(commands.Bot).addUrl("https://www.youtube.com/watch?v=kofR7f7oNnE")

async def setup(bot: commands.Bot):
    await bot.add_cog(MusicPlayer(bot = bot))
