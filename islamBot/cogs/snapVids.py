import nextcord
from nextcord.ext import commands, tasks, application_checks
from nextcord import slash_command, SlashOption, Interaction, ChannelType
from nextcord.abc import GuildChannel
import datetime
import json
import random
from main import DBConnect


class QuranShorts(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.send_vid.start()

    @tasks.loop(seconds=75)
    async def send_vid(self):
        await self.client.wait_until_ready()
        await sendVideos(self.client)

    @commands.command(help="`<TextChannel>`\nSet text channel for vids")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def shorts(self, ctx,  channel: nextcord.TextChannel):
        db, cursor = DBConnect()
        var2 = channel.id
        time = str(datetime.datetime.utcnow())
        query1 = "SELECT * FROM shorts WHERE guild_id=%s"
        var1 = str(ctx.guild.id)
        cursor.execute(query1, (var1,))
        results1 = cursor.fetchall()
        if not len(results1) == 0:
            query2 = "UPDATE shorts SET channel_id=%s, timestamp=%s WHERE guild_id=%s"
            cursor.execute(query2, (var2, time, var1))
        else:
            query2 = "INSERT INTO shorts (guild_id, channel_id, timestamp) VALUES (%s, %s, %s)"
            cursor.execute(query2, (var1, var2, time))
        db.commit()
        await ctx.reply(f"✅ **Successfully changed your Videos channel, I'll start sending short quran videos to {channel.mention} within the next hour**")

    @slash_command(name="shorts", description="Set a text channel for vids")
    @application_checks.has_permissions(administrator=True)
    @application_checks.guild_only()
    async def _shorts(self, interaction: Interaction,  channel: GuildChannel = SlashOption(name="channel", description="Pick a text channel", channel_types=[ChannelType.text], required=True)):
        db, cursor = DBConnect()
        var2 = channel.id
        time = str(datetime.datetime.utcnow())
        query1 = "SELECT * FROM shorts WHERE guild_id=%s"
        var1 = str(interaction.guild.id)
        cursor.execute(query1, (var1,))
        results1 = cursor.fetchall()
        if not len(results1) == 0:
            query2 = "UPDATE shorts SET channel_id=%s, timestamp=%s WHERE guild_id=%s"
            cursor.execute(query2, (var2, time, var1))
        else:
            query2 = "INSERT INTO shorts (guild_id, channel_id, timestamp) VALUES (%s, %s, %s)"
            cursor.execute(query2, (var1, var2, time))
        db.commit()
        await interaction.response.send_message(f"✅ **Successfully changed your Videos channel, I'll start sending short quran videos to {channel.mention} within the next hour**")


def setup(client):
    client.add_cog(QuranShorts(client))


async def getVideos(ctx, client):
    # How this works? I manually post some islamic related videos to a channel and the bot picks a random one to send!
    CHANNEL_ID = 976944211318431824 # So you will need to replace ID here by your posting channel ID
    CHANNEL = client.get_channel(CHANNEL_ID)
    msgs = await CHANNEL.history().flatten()
    post = random.choice(msgs)
    sent = False
    for attachment in post.attachments:
        if sent:
            return
        if attachment.url.lower().endswith('.mp4'):
            try:
                await ctx.send(f"** ♥ URL: {attachment} **")
                sent = True
            except:
                pass
            return
        else:
            await getVideos(ctx, client)


async def sendVideos(client):
    db, cursor = DBConnect()
    query = "SELECT * FROM shorts"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        guildID = row[0]
        channelID = row[1]
        timestampDB = row[2]
        now = datetime.datetime.utcnow()
        diff = now - timestampDB
        diff_in_hours = diff.total_seconds() / 3600
        if not diff_in_hours >= 1:
            continue
        try:
            channel = client.get_channel(int(channelID))
        except:
            continue
        await getVideos(channel, client)

        query2 = "UPDATE shorts SET timestamp=%s WHERE guild_id=%s"
        cursor.execute(query2, (now, guildID))
        db.commit()
