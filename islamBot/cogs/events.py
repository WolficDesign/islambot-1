import nextcord
from nextcord.ext import commands
import json
from main import DBConnect


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.client.get_channel(1014823240302084164) # Replace this ID by bot status channel ID to receive message on bot start
        embed = nextcord.Embed(title="Bot is ready...",
                               color=nextcord.Colour.brand_green())
        embed.description = "Bot is back online, and ready to be used 🤍"
        await channel.send(embed=embed)
        print(f'Logged in as {self.client.user}')

        db, cursor = DBConnect()
        cursor.execute("SELECT * FROM voice")
        results = cursor.fetchall()
        for row in results:
            guildID = int(row[0])
            channelID = int(row[1])
            urlDB = row[2]
            try:
                guild = self.client.get_guild(guildID)
                channel = self.client.get_channel(channelID)
                members = channel.members
                if not len(members) >= 1:
                    return
                await channel.connect()
                voice_client: nextcord.VoiceClient = nextcord.utils.get(
                    self.client.voice_clients, guild=guild)
                url = urlDB
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            except:
                continue

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        db, cursor = DBConnect()
        guildID = member.guild.id
        guild = self.client.get_guild(guildID)
        query = "SELECT * FROM voice WHERE guild_id=%s"
        cursor.execute(query, (str(guildID),))
        results = cursor.fetchall()
        if len(results) == 0:
            return
        for row in results:
            channelID = row[1]
            urlDB = row[2]

        if (f"{member.name}#{member.discriminator}" == f"{self.client.user}") and (not before.channel == None) and (not after.channel == None):
            try:
                voice_client: nextcord.VoiceClient = nextcord.utils.get(
                    self.client.voice_clients, guild=guild)
                await voice_client.disconnect()

                channel = self.client.get_channel(int(channelID))
                members = channel.members
                if len(members) >= 1:
                    await channel.connect()
                    voice_client: nextcord.VoiceClient = nextcord.utils.get(
                        self.client.voice_clients, guild=guild)
                    url = urlDB
                    ffmpeg_options = {
                        'options': '-vn',
                        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                    }
                    audio_source = nextcord.FFmpegPCMAudio(
                        url, options=ffmpeg_options)
                    voice_client.play(audio_source, after=None)
            except:
                pass

        if not before.channel == None:
            if (before.channel.id == int(channelID)):
                try:
                    channel = self.client.get_channel(int(channelID))
                    members = channel.members
                    if len(members) == 1:
                        voice_client: nextcord.VoiceClient = nextcord.utils.get(
                            self.client.voice_clients, guild=guild)
                        await voice_client.disconnect()
                except:
                    return
        if not after.channel == None:
            if (after.channel.id == int(channelID)):
                try:
                    channel = self.client.get_channel(int(channelID))
                    members = channel.members
                    if len(members) >= 1:
                        await channel.connect()
                        voice_client: nextcord.VoiceClient = nextcord.utils.get(
                            self.client.voice_clients, guild=guild)
                        url = urlDB
                        ffmpeg_options = {
                            'options': '-vn',
                            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                        }
                        audio_source = nextcord.FFmpegPCMAudio(
                            url, options=ffmpeg_options)
                        voice_client.play(audio_source, after=None)
                except:
                    return

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = nextcord.Embed(title=str(error))
            embed.color = nextcord.Colour.dark_red()
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(
                title="Please pass in all required arguments ( Check help )", description=str(error))
            embed.color = nextcord.Colour.dark_red()
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(title=str(error))
            embed.color = nextcord.Colour.dark_red()
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = nextcord.Embed(
                title="Bad Argument Error, Please check help", description=str(error))
            embed.color = nextcord.Colour.dark_red()
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.NoPrivateMessage):
            embed = nextcord.Embed(
                title=str(error))
            embed.color = nextcord.Colour.dark_red()
            await ctx.reply(embed=embed)
        else:
            embed = nextcord.Embed(
                title=str(error))
            embed.color = nextcord.Colour.dark_red()
            await ctx.reply(embed=embed)
            await ctx.reply(content="An error occured, That was logged and sent to bot developers\nIf the issue still appears in the next days, Then join our official server and report that bug", embed=embed)
            channel = self.client.get_channel(1014823241103188013)
            embedADM = nextcord.Embed(title=f'An Error Occured by {ctx.author.name}#{ctx.author.discriminator}  ( {ctx.author.id} ) at guild {ctx.guild.id}',
                                      color=nextcord.Colour.dark_gray())
            embedADM.description = str(error)
            await channel.send(embed=embedADM)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.client.get_channel(1014823241103188011) # Replace ID by your servers join logs channel
        embed = nextcord.Embed(title='Joined a new guild',
                               color=nextcord.Colour.dark_green())
        embed.description = f"Guild Name: {guild.name}\nGuild ID: {guild.id}\nOwnerID: {guild.owner_id}"
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.client.get_channel(1014823241103188012) # Replace ID by your servers left logs channel
        embed = nextcord.Embed(title='Guild was removed',
                               color=nextcord.Colour.dark_red())
        embed.description = f"Guild Name: {guild.name}\nGuild ID: {guild.id}\nOwnerID: {guild.owner_id}"
        await channel.send(embed=embed)


def setup(client):
    client.add_cog(Events(client))
