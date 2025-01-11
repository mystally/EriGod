import discord                      ## Importing the required libraries
from discord.ext import commands
from discord.ui import Select, View
import os
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default() ## Granting the necessary permissions
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def carregar_cogs(bot): ## importing the cogs
    caminho_cogs = os.path.join(os.getcwd(), "cogs")
    for arquivo in os.listdir(caminho_cogs):
        if arquivo.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{arquivo[:-3]}")
                print(f"Cog carregada: {arquivo}")
            except Exception as e:
                print(f"Erro ao carregar a cog {arquivo}: {e}")

@bot.event  
async def on_ready():
    print("Bot está inicializando...")
    await carregar_cogs(bot)
    try:
        synced = await bot.tree.sync()
        print(f"Comandos sincronizados: {len(synced)} comandos")
    except Exception as e:
        print(f"Erro ao sincronizar os comandos: {e}")
    print(f'Bot conectado com sucesso como: {bot.user}')

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel:
        bemvindo = discord.Embed(
            title='Bem vindo ao servidor!',
            description=f'Olá {member.mention}, bem vindo ao **{guild.name}**',
            color=discord.Color.purple()
        )
        bemvindo.set_thumbnail(url=member.avatar.url if member.avatar else bot.user.avatar.url)
        try:
            await guild.system_channel.send(embed=bemvindo)
        except Exception as e:
            print(f"Erro ao enviar mensagem de boas-vindas: {e}")

class RoleSelect(Select):
    def __init__(self, roles):
        options = [discord.SelectOption(label=role.name, value=str(role.id)) for role in roles]
        super().__init__(placeholder="Escolha um cargo...", options=options[:25])

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
async def classe(interaction: discord.Interaction):
    roles = [role for role in interaction.guild.roles if role.name != "@everyone"][:25]
    select = RoleSelect(roles)
    view = View()
    view.add_item(select)
    await interaction.response.send_message("Escolha um cargo:", view=view)

@bot.tree.command(name='shutdown', description='Desliga o bot')
async def shutdown(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('Desligando o bot...')
        await bot.close()
    else:
        await interaction.response.send_message(
            'Você não tem permissão para desligar o bot.', ephemeral=True
        )

bot.run(TOKEN)
