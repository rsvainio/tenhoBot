import discord
from discord.ext import commands
from bot import embedDecorator
from pytubefix import YouTube
from pytubefix import Search
from pytubefix.cli import on_progress

class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.downloadFolder: str = 'media/videos'

    def addByUrl(self, url: str):
        filename: str = self.downloadVideo(YouTube(url, on_progress_callback=on_progress))
        if filename:
            self.addToQueue(filename)
        #player = discord.FFmpegPCMAudio(source, executable='utils/FFmpeg/bin/ffmpeg.exe')

    def addByQuery(self, query: str):
        results = Search(query)
        filename: str = self.downloadVideo(results.videos[0]) # download the first video in search results
        if filename:
            self.addToQueue(filename)

    def addToQueue(self, filename):
        return

    def downloadVideo(self, yt: YouTube):
        print(f'Attempting to download \'{yt.title}\'...')
        if yt.length > 300:
            print("Video longer than 5 minutes, not downloading...")
            return None

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


    #                               Bot commands
    # join the voice channel aswell
    @commands.command(name='start_queue', description="Start playing videos from the queue")
    async def start_queue(self, interaction: discord.Interaction):
        return
    
    # leave the voice channel aswell
    @commands.command(name='stop_queue', description="Stop playing videos from the queue")
    async def stop_queue(self, interaction: discord.Interaction):
        return

    @commands.command(name='add_video_by_url', description="Add a video to the queue by URL")
    async def add_video_by_url(self, interaction: discord.Interaction, response: str):
        return

    @commands.command(name='add_video_by_query', description="Add a video to the queue by search query")
    async def add_video_by_query(self, interaction: discord.Interaction, response: str):
        return

    @commands.command(name='skip_video', description="Skip the currently playing video")
    async def skip_video(self, interaction: discord.Interaction):
        return

    @commands.command(name='remove_from_queue', description="Remove a video from the queue by it's position in the queue")
    async def remove_from_queue(self, interaction: discord.Interaction, response: str):
        return

if __name__ == '__main__':
    #MusicPlayer(commands.Bot).addByUrl("www.youtube.com/watch?v=kofR7f7oNnE")
    MusicPlayer(commands.Bot).addByQuery("The Nightman cometh")

async def setup(bot: commands.Bot):
    await bot.add_cog(MusicPlayer(bot = bot))
