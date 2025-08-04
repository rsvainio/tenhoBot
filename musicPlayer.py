import discord
from discord.ext import commands
from bot import embedDecorator
from bot import joinVoiceChannel
import asyncio
from pytubefix import YouTube
from pytubefix import Search
from pytubefix.cli import on_progress

class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.downloadFolder: str = 'media/videos'
        self.videoQueue: list = []
        self.playingQueue = False

    def addByUrl(self, url: str):
        result = self.downloadVideo(YouTube(url, on_progress_callback=on_progress))
        filename: str = result[0]
        videoLength: int = result[1]
        if filename:
            self.addToQueue(filename=filename, length=videoLength)
        #player = discord.FFmpegPCMAudio(source, executable='utils/FFmpeg/bin/ffmpeg.exe')

    def addByQuery(self, query: str):
        results = Search(query)
        result = self.downloadVideo(results.videos[0]) # download the first video in search results
        filename: str = result[0]
        videoLength: int = result[1]
        if filename:
            self.addToQueue(filename=filename, length=videoLength)

    def addToQueue(self, filename: str, length: int):
        self.videoQueue.append((filename, length))
        if not self.playingQueue:
            return
    
    def downloadVideo(self, yt: YouTube):
        print(f'Attempting to download \'{yt.title}\'...')
        videoLength = yt.length
        if videoLength > 300:
            print("Video longer than 5 minutes, not downloading...")
            return None

        ys = yt.streams.get_audio_only()
        filename = ys.download(output_path=self.downloadFolder)
        filename = self.shortenFilepath(filename)
        # add the newly downloaded file to the metadata file here

        return (filename, videoLength)

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
        voiceClient: discord.VoiceClient = await joinVoiceChannel(interaction)

        async def playVideo():
            while bool(self.videoQueue): # not empty
                if voiceClient.is_playing:
                    await asyncio.sleep(5)
                    continue

                video = nextVideo()
                filename: str = video[0]
                length: int = video[1]
                source = f'media/videos/{filename}'
                print(f'Now playing video {filename}, length: {length}s')
                player = discord.FFmpegPCMAudio(source, executable='utils/FFmpeg/bin/ffmpeg.exe')

                try:
                    voiceClient.play(player, after=lambda e: voiceClient.stop())
                    await asyncio.sleep(length) # sleep for the duration of the video
                except discord.errors.ClientException:
                    voiceClient.stop()
                    break
                    #voiceClient.play(player, after=lambda e: voiceClient.stop())

            await voiceClient.disconnect()
            voiceClient.cleanup()            

        def nextVideo() -> tuple:
            video: tuple = self.videoQueue[0]
            self.videoQueue.pop(0)
            print(f'Videos left in queue: {len(self.videoQueue)}')
            return video

    # leave the voice channel aswell
    @commands.command(name='stop_queue', description="Stop playing videos from the queue")
    async def stop_queue(self, interaction: discord.Interaction):
        return

    @commands.command(name='add_video_by_url', description="Add a video to the queue by URL")
    async def add_video_by_url(self, interaction: discord.Interaction, response: str):
        response = str(response)
        if len(response > 255):
            embed = embedDecorator(interaction)
            embed.add_field(name='Give a url fewer than 255 characters', value='')
            await interaction.response.send_message(embed=embed)
            return
        self.addByUrl(response)
        return

    @commands.command(name='add_video_by_query', description="Add a video to the queue by search query")
    async def add_video_by_query(self, interaction: discord.Interaction, response: str):
        response = str(response)
        if len(response > 127):
            embed = embedDecorator(interaction)
            embed.add_field(name='Give a search query fewer than 127 characters', value='')
            await interaction.response.send_message(embed=embed)
            return
        self.addByQuery(response)
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
