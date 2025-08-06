import discord
from discord import app_commands
from discord.ext.commands import Bot, Cog
from bot import embedDecorator, joinVoiceChannel
import asyncio
from pytubefix import YouTube
from pytubefix import Search
from pytubefix.cli import on_progress

class MusicPlayer(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.downloadFolder: str = 'media/videos'
        self.videoQueue: list = []
        self.videoTask: asyncio.Task
        self.playingQueue = False

    def addByUrl(self, url: str):
        result = self.downloadVideo(YouTube(url, on_progress_callback=on_progress))
        filename: str = result[0]
        videoLength: int = result[1]
        if filename:
            self.addToQueue(filename=filename, length=videoLength)

    def addByQuery(self, query: str):
        results = Search(query)
        result = self.downloadVideo(results.videos[0]) # download the first video in search results
        filename: str = result[0]
        videoLength: int = result[1]
        if filename:
            self.addToQueue(filename=filename, length=videoLength)

    def addToQueue(self, filename: str, length: int):
        print(f'Adding to queue: {filename}')
        self.videoQueue.append((filename, length))
    
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
        marker = 'media\\videos\\'
        index = path.find(marker)
        if index != -1:
            return path[index + len(marker):]
        else:
            return path  # Return the original string if marker is not found

    #                               Bot commands
    # join the voice channel aswell
    @app_commands.command(name='start_queue', description="Start playing videos from the queue")
    async def start_queue(self, interaction: discord.Interaction):
        print('Starting to play video queue')
        voiceClient: discord.VoiceClient = await joinVoiceChannel(interaction)
        self.playingQueue = True

        async def playVideo():
            video: tuple = self.videoQueue[0]
            filename: str = video[0]
            length: int = video[1]
            self.videoQueue.pop(0)
            print(f'Videos left in queue: {len(self.videoQueue)}')

            source = f'media/videos/{filename}'
            print(f'Now playing video {filename}, length: {length}s')
            player = discord.FFmpegPCMAudio(source, executable='utils/FFmpeg/bin/ffmpeg.exe')

            try:
                voiceClient.play(player, after=lambda e: voiceClient.stop())
                await asyncio.sleep(length) # sleep for the duration of the video
                player.cleanup()
            except discord.errors.ClientException:
                voiceClient.stop()
                player.cleanup()

        while bool(self.videoQueue) and self.playingQueue: # not empty and playing queue
            if voiceClient.is_playing():
                await asyncio.sleep(5)
                continue

            self.videoTask = asyncio.create_task(playVideo())
            await self.videoTask

        self.playingQueue = False
        await voiceClient.disconnect()
        voiceClient.cleanup()

    # leave the voice channel aswell
    @app_commands.command(name='stop_queue', description="Stop playing videos from the queue")
    async def stop_queue(self, interaction: discord.Interaction):
        self.playingQueue = False
        self.videoTask.cancel()
        voiceClient: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        await voiceClient.disconnect()
        voiceClient.cleanup()

    @app_commands.command(name='add_video_by_url', description="Add a video to the queue by URL")
    async def add_video_by_url(self, interaction: discord.Interaction, response: str):
        response = str(response)
        if len(response) > 255:
            embed = embedDecorator(interaction)
            embed.add_field(name='Give a url fewer than 255 characters', value='')
            await interaction.response.send_message(embed=embed)
            return
        self.addByUrl(response)

    @app_commands.command(name='add_video_by_query', description="Add a video to the queue by search query")
    async def add_video_by_query(self, interaction: discord.Interaction, response: str):
        response = str(response)
        if len(response) > 127:
            embed = embedDecorator(interaction)
            embed.add_field(name='Give a search query fewer than 127 characters', value='')
            await interaction.response.send_message(embed=embed)
            return
        self.addByQuery(response)

    @app_commands.command(name='skip_video', description="Skip the currently playing video")
    async def skip_video(self, interaction: discord.Interaction):
        voiceClients: list[discord.VoiceClient] = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if bool(voiceClients) and self.playingQueue: # if voice clients exist and playing queue
            self.videoTask.cancel()

    @app_commands.command(name='remove_from_queue', description="Remove a video from the queue by it's position in the queue")
    async def remove_from_queue(self, interaction: discord.Interaction, response: str):
        if not bool(self.videoQueue): # if empty
            print('Video queue is empty, not removing')
            return

        self.videoQueue.pop(response)
        print(f'Videos left in queue: {len(self.videoQueue)}')

if __name__ == '__main__':
    #MusicPlayer(commands.Bot).addByUrl("www.youtube.com/watch?v=kofR7f7oNnE")
    MusicPlayer(Bot).addByQuery("The Nightman cometh")

async def setup(client: Bot):
    await client.add_cog(MusicPlayer(bot = client))
    print('Added cog musicPlayer succesfully')
