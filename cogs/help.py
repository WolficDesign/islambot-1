import nextcord as discord
from nextcord.ext import commands
from nextcord.errors import Forbidden
from main import PREFIX


async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue?", embed=embed)


class Help(commands.Cog, description="Help Commands"):

    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    async def help(self, ctx, *input):
        prefix = PREFIX

        if not input:
            emb = discord.Embed(title='Commands and modules', color=discord.Color.blue(),
                                description=f'Use `{prefix}help <module>` to gain more information about that module')

            cogs_desc = ''
            for cog in self.client.cogs:
                if (not cog == "Tasks") and (not cog == "Help") and (not cog == "Events"):
                    cogs_desc += f'`{cog}` {self.client.cogs[cog].description}\n'
            emb.add_field(name='Modules', value=cogs_desc, inline=True)

            commands_desc = ''
            for command in self.client.walk_commands():
                if not command.cog_name and not command.hidden:
                    commands_desc += f'`{prefix}{command.name}`\n{command.help}\n\n'
            if commands_desc:
                emb.add_field(name='Not belonging to a module',
                              value=commands_desc, inline=True)

        elif len(input) == 1:
            for cog in self.client.cogs:
                if cog.lower() == input[0].lower():
                    if (input[0].lower() == "private"):
                        return
                    emb = discord.Embed(title=f'{cog} - Commands', description=self.client.cogs[cog].description,
                                        color=discord.Color.green())
                    for command in self.client.get_cog(cog).get_commands():
                        if not command.hidden:
                            emb.add_field(
                                name=f"`{prefix}{command.name}`", value=command.help, inline=True)
                    break
            else:
                emb = discord.Embed(title="What's that?!",
                                    description=f"I've never heard from a module called `{input[0]}` before :scream:",
                                    color=discord.Color.orange())

        elif len(input) > 1:
            emb = discord.Embed(title="That's too much.",
                                description="Please request only one module at once :sweat_smile:",
                                color=discord.Color.orange())

        else:
            emb = discord.Embed(title="It's a magical place.",
                                description="I don't know how you got here. But I didn't see this coming at all.\n"
                                            "Would you please be so kind to report that issue to me?\n",
                                color=discord.Color.red())
        await send_embed(ctx, emb)


def setup(client):
    client.add_cog(Help(client))
