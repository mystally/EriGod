import discord
from discord.ext import commands
from discord.ui import Select, View
from discord import app_commands
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix ="!", intents=intents)


class comand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.commands.command(name='ping', description='Verifica a latência do bot')
    async def ping(self, interact:discord.Interaction):
        latency = round(bot.latency * 1000)
        await interact.response.send_message(f'Pong! Latência {latency}ms') 
        
async def setup(bot): 
    await bot.add_cog(comand(bot))