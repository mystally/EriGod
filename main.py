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

@bot.event
async def on_ready():
    print(f'Bot conectado com sucesso como: {bot.user} ')

@bot.tree.command()
async def atualizar_comandos(interaction: discord.Interaction):
    if interaction.user.id == 884502356262264933:  
        await bot.tree.sync()  
        await interaction.response.send_message("Comandos sincronizados com sucesso!")
    else: 
        await interaction.response.send_message("Somente o meu Dono pode usar este comando.")
    
@bot.tree.command()
async def hello(interact:discord.Interaction):
    await interact.response.send_message(f'Olá! {interact.user.name} Mero Mortal estou aqui para guiar seu caminho. Como posso te ajudar?')
   
@bot.tree.command(name='ping', description='Verifica a latência do bot')
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f'Pong! Latência {latency}ms')
@bot.command(name="calc")
async def calc(ctx, num1: int, operador: str, num2: int):
    if operador == '+':
        resultado = num1 + num2
    elif operador == '-':
        resultado = num1 - num2
    elif operador == '*':
        resultado = num1 * num2
    elif operador == '/':
        if num2 != 0:
            resultado = num1 / num2
        else:
            await ctx.send("Erro: Divisão por zero!")
            return
    else:
        await ctx.send("Operador inválido! Use +, -, * ou /.")
        return

    await ctx.send(f"O resultado de {num1} {operador} {num2} é: {resultado}")
@bot.command(name='erigod')
async def erigod(ctx):
    
    member_name = ctx.author.display_name  
    response = f'Olá, {member_name}! Como você está?'
    await ctx.send(response)

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
@bot.command(name='about')
async def about(ctx):
    sobre = discord.Embed(
            title = 'Sobre o EriGod!',
            description = f'Eu sou um bot criado para auxiliar as partidas de RPG de mesa do sistema Mitos e Lendas',
            color = discord.Color.purple()
        )
    sobre.add_field(name='Comandos Disponíveis', value = "`!hello`, `!calc`, `!erigod`, `!about`, `!ping`, `!classe`", inline= False)
    sobre.set_footer(text='Criado por mystally')
    await ctx.send(embed=sobre)
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

@bot.command(name='classe')
async def setrole(ctx):
    roles = [role for role in ctx.guild.roles if role.name != "@everyone"]  # Exclui o cargo @everyone
    select = RoleSelect(roles)
    view = View()
    view.add_item(select)
    await ctx.send("Escolha um cargo:", view=view)



bot.run(TOKEN)