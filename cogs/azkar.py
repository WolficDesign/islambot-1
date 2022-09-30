import nextcord
from nextcord.ext import commands, tasks, application_checks
from nextcord import slash_command, SlashOption, Interaction, ChannelType
from nextcord.abc import GuildChannel
import datetime
import json
import random
from main import DBConnect


class Azkar(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.send_now.start()

    @tasks.loop(seconds=30)
    async def send_now(self):
        await self.client.wait_until_ready()
        await send_zekr(self.client)

    @commands.command(help="`<TextChannel>`\nSet text channel for azkar")
    @commands.has_permissions(administrator=True)
    async def azkar(self, ctx,  channel: nextcord.TextChannel):
        db, cursor = DBConnect()
        var2 = channel.id
        time = str(datetime.datetime.utcnow())
        query1 = "SELECT * FROM azkar WHERE guild_id=%s"
        var1 = str(ctx.guild.id)
        cursor.execute(query1, (var1,))
        results1 = cursor.fetchall()
        if not len(results1) == 0:
            query2 = "UPDATE azkar SET channel_id=%s, timestamp=%s WHERE guild_id=%s"
            cursor.execute(query2, (var2, time, var1))
        else:
            query2 = "INSERT INTO azkar (guild_id, channel_id, timestamp) VALUES (%s, %s, %s)"
            cursor.execute(query2, (var1, var2, time))

        db.commit()
        await ctx.reply(f"✅ **Successfully changed your Azkar channel, I'll start sending azkar to {channel.mention} within the next hour**")

    @slash_command(name="azkar", description="Set a text channel for azkar")
    @application_checks.has_permissions(administrator=True)
    async def _azkar(self, interaction: Interaction,  channel: GuildChannel = SlashOption(name="channel", description="Pick a text channel", channel_types=[ChannelType.text], required=True)):
        db, cursor = DBConnect()
        var2 = channel.id
        time = str(datetime.datetime.utcnow())
        query1 = "SELECT * FROM azkar WHERE guild_id=%s"
        var1 = str(interaction.guild.id)
        cursor.execute(query1, (var1,))
        results1 = cursor.fetchall()
        if not len(results1) == 0:
            query2 = "UPDATE azkar SET channel_id=%s, timestamp=%s WHERE guild_id=%s"
            cursor.execute(query2, (var2, time, var1))
        else:
            query2 = "INSERT INTO azkar (guild_id, channel_id, timestamp) VALUES (%s, %s, %s)"
            cursor.execute(query2, (var1, var2, time))

        db.commit()
        await interaction.response.send_message(f"✅ **Successfully changed your Azkar channel, I'll start sending azkar to {channel.mention} within the next hour**")


async def send_zekr(client):
    azkar = await get_azkar()
    db, cursor = DBConnect()
    query = "SELECT * FROM azkar"
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

        zekrList = azkar
        zekr = random.randint(0, len(zekrList) - 1)
        title = azkar[zekr]["category"]
        embed = nextcord.Embed(
            title=title, color=nextcord.Colour.brand_green())
        if not zekrList[zekr]["reference"] == "":
            zekrCon = zekrList[zekr]["zekr"]
            ZekrCon2 = zekrList[zekr]["reference"]
            embed.description = f"{zekrCon}\n{ZekrCon2}"
        else:
            zekrCon = zekrList[zekr]["zekr"]
            embed.description = f"{zekrCon}"
        rep = zekrList[zekr]["count"]
        if not rep == "":
            embed.set_author(name=f"Repeat: {rep}")
        if (zekrList[zekr]["description"] == ""):
            try:
                await channel.send(embed=embed)
            except:
                continue
        else:
            bless = zekrList[zekr]["description"]
            embed.set_footer(text=f"{bless}")
            try:
                await channel.send(embed=embed)
            except:
                continue

        query2 = "UPDATE azkar SET timestamp=%s WHERE guild_id=%s"
        cursor.execute(query2, (now, guildID))
        db.commit()


async def get_azkar():
    with open('./islamBot/data/azkar.json', 'r', encoding='utf-8') as f:
        azkar = json.load(f)
    return azkar


def setup(client):
    client.add_cog(Azkar(client))
