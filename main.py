import discord
from discord.ext import commands
from discord.ui import Select, View
import os 
from dotenv import load_dotenv
from discord import app_commands
import random

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix ="!", intents=intents)

async def carregar_cogs(): 
    for arquivo in os.listdir('cogs'):
        if arquivo.endswith(".py"):
            await bot.load_extension(f"cogs.{arquivo[:-3]}")

@bot.event
async def on_ready():
    print(f'Bot conectado com sucesso como: {bot.user} ')
   
@bot.tree.command()
async def hello(interaction:discord.Interaction):
    await interaction.response.send_message(f'Olá! {interaction.user.name} ! Mero Mortal estou aqui para guiar seu caminho. Como posso te ajudar?')
   


@bot.tree.command(name='erigod', description='Responde a saudação do usuário')
async def erigod(interaction:discord.Interaction):
    await interaction.response.send_message(f'Olá, {interaction.user.name}! Como você está?')
@bot.event 
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel: 
        bemvindo = discord.Embed(
            title = 'Bem vindo ao servidor!',
            description = f'Olá {member.mention}, bem vindo ao **{guild.name}**',
            color = discord.Color.purple()
        )
        bemvindo.set_thumbnail(url=member.avatar.url if member.avatar else bot.user.avatar.url)
        await guild.system_channel.send(embed=bemvindo)
@bot.tree.command(name='about', description='Informações sobre o bot EriGod')
async def about(interaction: discord.Interaction):
    sobre = discord.Embed(
        title='Sobre o EriGod!',
        description='Eu sou um bot criado para auxiliar as partidas de RPG de mesa do sistema Mitos e Lendas',
        color=discord.Color.purple()
    )
    sobre.add_field(name='Comandos Disponíveis', value="`/about`, `/ping`, `/classe`", inline=False)
    sobre.set_footer(text='Criado por mystally')
    await interaction.response.send_message(embed=sobre)

class RoleSelect(Select):
    def __init__(self, roles):
        options = [discord.SelectOption(label=role.name, value=str(role.id)) for role in roles]
        super().__init__(placeholder="Escolha um cargo...", options=options)

    async def callback(self, interaction: discord.Interaction):
        role_id = int(self.values[0])
        role = interaction.guild.get_role(role_id)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f'Você removeu o cargo: {role.name}', ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f'Você atribuiu o cargo: {role.name}', ephemeral=True)

@bot.tree.command(name='classe', description='Escolha um cargo do servidor')
async def classe(interaction:discord.Interaction):
    
    roles = [role for role in interaction.guild.roles if role.name != "@everyone"]
    
    
    select = RoleSelect(roles)
    
    
    view = View()
    view.add_item(select)
    
    
    await interaction.response.send_message("Escolha um cargo:", view=view)
@bot.tree.command()
async def sincronize(interaction: discord.Interaction):
    if interaction.user.id == 884502356262264933:  
        await bot.tree.sync()  
        await interaction.response.send_message("Comandos sincronizados com sucesso!")
    else: 
        await interaction.response.send_message("Somente o meu Dono pode usar este comando.")
@bot.tree.command(name='shutdown', description='Desliga o bot')
async def shutdown(interaction: discord.Interaction):
    # Check if the user has the required permissions
    if interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('Desligando o bot...')
        await bot.close()  # This will shut down the bot
    else:
        await interaction.response.send_message('Você não tem permissão para desligar o bot.', ephemeral=True)

bot.run(TOKEN)