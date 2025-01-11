import discord
from discord.ext import commands
from discord.ui import Select, View
from discord import app_commands
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix ="!", intents=intents)

class Command(commands.Cog):  ## Class name
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name='ping', description='Verifica a latência do bot')
    async def ping(self, interact: discord.Interaction):
        latency = round(self.bot.latency * 1000) 
        await interact.response.send_message(f'Pong! Latência {latency}ms')

    @app_commands.command(name='hello', description='Diz olá ao usuário')
    async def hello(self, interact: discord.Interaction):
        await interact.response.send_message(f'Olá, {interact.user.name}! Mero mortal, estou aqui para guiar seu caminho. Como posso te ajudar?')

    @app_commands.command(name='erigod', description='Responde a saudação do usuário')
    async def erigod(self, interact: discord.Interaction):
        await interact.response.send_message(f'Olá, {interact.user.name}! Como você está?')

    @app_commands.command(name='about', description='Informações sobre o bot EriGod')
    async def about(self, interact: discord.Interaction):
        sobre = discord.Embed(
            title='Sobre o EriGod!',
            description='Eu sou um bot criado para auxiliar as partidas de RPG de mesa do sistema Mitos e Lendas',
            color=discord.Color.purple()
        )
        sobre.add_field(name='Comandos Disponíveis', value="`/about`, `/ping`, `/classe`", inline=False)
        sobre.set_footer(text='Criado por mystally')
        await interact.response.send_message(embed=sobre)

    @app_commands.command(name='sincronize', description='Sincroniza os comandos do bot')
    async def sincronize(self, interact: discord.Interaction):  
        if interact.user.id == 884502356262264933:  # Specific ID for verification
            await self.bot.tree.sync()  
            await interact.response.send_message("Comandos sincronizados com sucesso!")
        else:
            await interact.response.send_message("Somente o meu Dono pode usar este comando.")

async def setup(bot):
    await bot.add_cog(Command(bot))  
