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
    async def ping(self,interaction:discord.Interaction):
        latency = round(bot.latency * 1000)
        await interaction.response.send_message(f'Pong! Latência {latency}ms')    
    @app_commands.command()
    async def hello(self, interaction:discord.Interaction):
        await interaction.response.send_message(f'Olá! {interaction.user.name} ! Mero Mortal estou aqui para guiar seu caminho. Como posso te ajudar?')
    @app_commands.command(name='erigod', description='Responde a saudação do usuário')
    async def erigod(self, interaction:discord.Interaction):
        await interaction.response.send_message(f'Olá, {interaction.user.name}! Como você está?')  
    @app_commands.command(name='about', description='Informações sobre o bot EriGod')
    async def about(interaction: discord.Interaction):
        sobre = discord.Embed(
        title='Sobre o EriGod!',
        description='Eu sou um bot criado para auxiliar as partidas de RPG de mesa do sistema Mitos e Lendas',
        color=discord.Color.purple()
    )
        sobre.add_field(name='Comandos Disponíveis', value="`/about`, `/ping`, `/classe`", inline=False)
        sobre.set_footer(text='Criado por mystally')
        await interaction.response.send_message(embed=sobre)
    @app_commands.command()
    async def sincronize(interaction: discord.Interaction):
        if interaction.user.id == 884502356262264933:  
            await bot.tree.sync()  
            await interaction.response.send_message("Comandos sincronizados com sucesso!")
        else: 
            await interaction.response.send_message("Somente o meu Dono pode usar este comando.")
async def setup(bot): 
    await bot.add_cog(comand(bot))