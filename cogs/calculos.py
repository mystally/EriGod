import discord
from discord.ext import commands
from discord.ui import Select, View
from discord import app_commands
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix ="!", intents=intents)



class Calculos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name='somar', description='Realiza a operação de adição entre dois números')
    async def somar(self, interact:discord.Interaction, n1:float, n2:float):
        await interact.response.send_message(n1 + n2)
    @app_commands.command(name='subtrair', description='Realiza a operação de subtração entre dois números')
    async def subtrair(self, interact:discord.Interaction, n1:float, n2:float):
        await interact.response.send_message(n1 - n2)
    @app_commands.command(name='dividir', description='Realiza a operação de divisão entre dois números')
    async def dividir(self, interact:discord.Interaction, n1:float, n2:float):
        await interact.response.send_message(n1 / n2)
    @app_commands.command(name='multiplicar', description='Realiza a operação de multiplicação entre dois números')
    async def multiplicar(self, interact:discord.Interaction, n1:float, n2:float):
        await interact.response.send_message(n1 * n2)

async def setup(bot):
    await bot.add_cog(Calculos(bot))
