import nextcord
from nextcord.ext import commands, application_checks
from nextcord import slash_command, SlashOption, Interaction, ChannelType
from nextcord.abc import GuildChannel
import json
import asyncio
from main import DBConnect


class QuranPlayer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="`<VoiceChannel>`\nSet voice channel for quran")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def quran(self, ctx,  channel: nextcord.VoiceChannel):
        sheikh = ['https://Qurango.net/radio/maher_al_meaqli',
                  'https://Qurango.net/radio/mohammed_ayyub',
                  'https://Qurango.net/radio/mohammed_siddiq_alminshawi ',
                  'https://Qurango.net/radio/mahmoud_khalil_alhussary ',
                  'https://Qurango.net/radio/mishary_alafasi ',
                  'https://Qurango.net/radio/nasser_alqatami ',
                  'https://Qurango.net/radio/khalid_aljileel ',
                  'https://qurango.net/radio/yasser_aldosari']
        # 0 Maher Al-Meaqli
        # 1 Mohammed Ayyub
        # 2 Mohammed Siddiq Al-Minshawi
        # 3 Mahmoud Khalil Al-Hussary
        # 4 Mishary Al-Afasi
        # 5 Nasser Al-Qatami
        # 6 Khalid Al-Jileel
        # 7 Yasser Al-Dosari
        listS = ['Maher Al-Meaqli', 'Mohammed Ayyub', 'Mohammed Siddiq Al-Minshawi',
                 'Mahmoud Khalil Al-Hussary', 'Mishary Al-Afasi', 'Nasser Al-Qatami', 'Khalid Al-Jileel', 'Yasser Al-Dosari']
        listNums = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
        db, cursor = DBConnect()
        query1 = "SELECT * FROM voice WHERE guild_id=%s"
        var1 = str(ctx.guild.id)
        cursor.execute(query1, (var1,))
        results1 = cursor.fetchall()
        if not len(results1) == 0:
            query2 = "UPDATE voice SET channel_id=%s WHERE guild_id=%s"
            cursor.execute(query2, (str(channel.id), var1))
        else:
            query2 = "INSERT INTO voice (guild_id, channel_id, url) VALUES (%s, %s, %s)"
            cursor.execute(query2, (var1, str(channel.id), "None"))

        db.commit()

        channel = self.client.get_channel(channel.id)
        try:
            voice_client: nextcord.VoiceClient = nextcord.utils.get(
                self.client.voice_clients, guild=ctx.guild)
            if voice_client.is_connected():
                await voice_client.disconnect()
            await channel.connect()
            voice_client: nextcord.VoiceClient = nextcord.utils.get(
                self.client.voice_clients, guild=ctx.guild)
        except:
            await channel.connect()
            voice_client: nextcord.VoiceClient = nextcord.utils.get(
                self.client.voice_clients, guild=ctx.guild)

        sheikhEmbed = nextcord.Embed(
            title="Please choose sheikh name...", description="\n".join("{} {}".format(num, name) for num, name in zip(listNums, listS)))
        sheikhMsg = await ctx.reply(embed=sheikhEmbed)
        await sheikhMsg.add_reaction('1️⃣')
        await sheikhMsg.add_reaction('2️⃣')
        await sheikhMsg.add_reaction('3️⃣')
        await sheikhMsg.add_reaction('4️⃣')
        await sheikhMsg.add_reaction('5️⃣')
        await sheikhMsg.add_reaction('6️⃣')
        await sheikhMsg.add_reaction('7️⃣')
        await sheikhMsg.add_reaction('8️⃣')

        def check(reaction, user):
            return (reaction.message.id == sheikhMsg.id) and (str(reaction.emoji) in listNums) and (user.id == ctx.author.id)
        try:
            response, userRes = await self.client.wait_for('reaction_add', timeout=30, check=check)
            if response.emoji == "1️⃣":
                url = sheikh[0]
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            elif response.emoji == "2️⃣":
                url = sheikh[1]
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            elif response.emoji == "3️⃣":
                url = sheikh[2]
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            elif response.emoji == "4️⃣":
                url = sheikh[3]
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            elif response.emoji == "5️⃣":
                url = sheikh[4]
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            elif response.emoji == "6️⃣":
                url = sheikh[5]
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            elif response.emoji == "7️⃣":
                url = sheikh[6]
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            elif response.emoji == "8️⃣":
                url = sheikh[7]
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            elif response is None:
                await voice_client.disconnect()
                await sheikhMsg.edit(content=f"{ctx.author.mention}, You are timed-out")

            queryURL = "UPDATE voice SET url=%s WHERE guild_id=%s"
            cursor.execute(queryURL, (url, var1))
            db.commit()

        except asyncio.TimeoutError:
            await voice_client.disconnect()
            await sheikhMsg.edit(content=f"{ctx.author.mention}, You are timed-out")
            return

        await ctx.reply(f"✅ **Successfully changed your Quran channel to {channel.mention}**\nPlease notice that if you didn't join the voice channel the bot will leave it ( it auto re-join when any member joins again )")

    @slash_command(name="quran", description="Set a voice channel to play quran 24/7")
    @application_checks.has_permissions(administrator=True)
    @application_checks.guild_only()
    async def _quran(self, interaction: Interaction,  channel: GuildChannel = SlashOption(name="channel", description="Pick a voice channel", channel_types=[ChannelType.voice], required=True)):
        sheikh = ['https://Qurango.net/radio/maher_al_meaqli',
                  'https://Qurango.net/radio/mohammed_ayyub',
                  'https://Qurango.net/radio/mohammed_siddiq_alminshawi ',
                  'https://Qurango.net/radio/mahmoud_khalil_alhussary ',
                  'https://Qurango.net/radio/mishary_alafasi ',
                  'https://Qurango.net/radio/nasser_alqatami ',
                  'https://Qurango.net/radio/khalid_aljileel ',
                  'https://qurango.net/radio/yasser_aldosari']
        # 0 Maher Al-Meaqli
        # 1 Mohammed Ayyub
        # 2 Mohammed Siddiq Al-Minshawi
        # 3 Mahmoud Khalil Al-Hussary
        # 4 Mishary Al-Afasi
        # 5 Nasser Al-Qatami
        # 6 Khalid Al-Jileel
        # 7 Yasser Al-Dosari
        listS = ['Maher Al-Meaqli', 'Mohammed Ayyub', 'Mohammed Siddiq Al-Minshawi',
                 'Mahmoud Khalil Al-Hussary', 'Mishary Al-Afasi', 'Nasser Al-Qatami', 'Khalid Al-Jileel', 'Yasser Al-Dosari']
        listNums = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
        db, cursor = DBConnect()
        query1 = "SELECT * FROM voice WHERE guild_id=%s"
        var1 = str(interaction.guild.id)
        cursor.execute(query1, (var1,))
        results1 = cursor.fetchall()
        if not len(results1) == 0:
            query2 = "UPDATE voice SET channel_id=%s WHERE guild_id=%s"
            cursor.execute(query2, (str(channel.id), var1))
        else:
            query2 = "INSERT INTO voice (guild_id, channel_id, url) VALUES (%s, %s, %s)"
            cursor.execute(query2, (var1, str(channel.id), "None"))

        db.commit()

        channel = self.client.get_channel(channel.id)
        try:
            voice_client: nextcord.VoiceClient = nextcord.utils.get(
                self.client.voice_clients, guild=interaction.guild)
            if voice_client.is_connected():
                await voice_client.disconnect()
            await channel.connect()
            voice_client: nextcord.VoiceClient = nextcord.utils.get(
                self.client.voice_clients, guild=interaction.guild)
        except:
            await channel.connect()
            voice_client: nextcord.VoiceClient = nextcord.utils.get(
                self.client.voice_clients, guild=interaction.guild)

        sheikhEmbed = nextcord.Embed(
            title="Please choose sheikh name...", description="\n".join("{} {}".format(num, name) for num, name in zip(listNums, listS)))
        sheikhMsg = await interaction.channel.send(embed=sheikhEmbed)
        await sheikhMsg.add_reaction('1️⃣')
        await sheikhMsg.add_reaction('2️⃣')
        await sheikhMsg.add_reaction('3️⃣')
        await sheikhMsg.add_reaction('4️⃣')
        await sheikhMsg.add_reaction('5️⃣')
        await sheikhMsg.add_reaction('6️⃣')
        await sheikhMsg.add_reaction('7️⃣')
        await sheikhMsg.add_reaction('8️⃣')

        def check(reaction, user):
            return (reaction.message.id == sheikhMsg.id) and (str(reaction.emoji) in listNums) and (user.id == interaction.user.id)
        try:
            response, userRes = await self.client.wait_for('reaction_add', timeout=30, check=check)
            if response.emoji == "1️⃣":
                url = sheikh[0]
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            elif response.emoji == "2️⃣":
                url = sheikh[1]
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            elif response.emoji == "3️⃣":
                url = sheikh[2]
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            elif response.emoji == "4️⃣":
                url = sheikh[3]
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            elif response.emoji == "5️⃣":
                url = sheikh[4]
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            elif response.emoji == "6️⃣":
                url = sheikh[5]
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            elif response.emoji == "7️⃣":
                url = sheikh[6]
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            elif response.emoji == "8️⃣":
                url = sheikh[7]
                ffmpeg_options = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
                audio_source = nextcord.FFmpegPCMAudio(
                    url, options=ffmpeg_options)
                voice_client.play(audio_source, after=None)
            elif response is None:
                await voice_client.disconnect()
                await sheikhMsg.edit(content=f"{interaction.user.mention}, You are timed-out")

            queryURL = "UPDATE voice SET url=%s WHERE guild_id=%s"
            cursor.execute(queryURL, (url, var1))
            db.commit()

        except asyncio.TimeoutError:
            await voice_client.disconnect()
            await sheikhMsg.edit(content=f"{interaction.user.mention}, You are timed-out")
            return

        await interaction.channel.send(f"{interaction.user.mention} ,✅ **Successfully changed your Quran channel to {channel.mention}**\nPlease notice that if you didn't join the voice channel the bot will leave it ( it auto re-join when any member joins again )")


def setup(client):
    client.add_cog(QuranPlayer(client))
