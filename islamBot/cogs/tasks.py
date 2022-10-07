import nextcord
from nextcord.ext import commands, tasks
import asyncio
import json
from itertools import cycle
from main import DBConnect


class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.change_status.start()
        self.check_vcs.start()

    @tasks.loop(seconds=10)
    async def check_vcs(self):
        await self.client.wait_until_ready()
        await asyncio.sleep(30)
        db, cursor = DBConnect()
        cursor.execute("SELECT * FROM voice")
        results = cursor.fetchall()
        for row in results:
            guildID = int(row[0])
            channelID = int(row[1])
            urlDB = row[2]
            try:
                guild = self.client.get_guild(int(guildID))
                channel = self.client.get_channel(int(channelID))
                voice_client: nextcord.VoiceClient = nextcord.utils.get(
                    self.client.voice_clients, guild=guild)
                if voice_client == None:
                    try:
                        members = channel.members
                        if len(members) == 0:
                            return
                        await channel.connect()
                        url = urlDB
                        ffmpeg_options = {
                            'options': '-vn',
                            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                        }
                        audio_source = nextcord.FFmpegPCMAudio(
                            url, options=ffmpeg_options)
                        voice_client.play(audio_source, after=None)
                        return
                    except:
                        pass
                else:
                    members = channel.members
                    if len(members) == 1:
                        await voice_client.disconnect()
                        return
                if not voice_client.is_playing():
                    url = urlDB
                    ffmpeg_options = {
                        'options': '-vn',
                        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                    }
                    audio_source = nextcord.FFmpegPCMAudio(
                        url, options=ffmpeg_options)
                    members = channel.members
                    if len(members) == 1:
                        return
                    voice_client.play(audio_source, after=None)
            except:
                pass

    @tasks.loop(seconds=5)
    async def change_status(self):
        await self.client.wait_until_ready()
        await self.client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=next(status)))


status = cycle(["أَلا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ", "Slash Commands"]) # You can add to bot cycling status here!


def setup(client):
    client.add_cog(Tasks(client))
