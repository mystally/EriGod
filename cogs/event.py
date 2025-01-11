import discord
from discord.ext import commands
from discord.ui import Select, View
from discord import app_commands
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix ="!", intents=intents)



class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel:  # Verifica se o canal do sistema está configurado
            bemvindo = discord.Embed(
                title="Bem-vindo ao servidor!",
                description=f"Olá {member.mention}, bem-vindo ao **{guild.name}**!",
                color=discord.Color.purple(),
            )
            # Verifica se o membro tem avatar e utiliza o avatar padrão do bot como fallback
            bemvindo.set_thumbnail(
                url=member.display_avatar.url
                if member.display_avatar
                else self.bot.user.display_avatar.url
            )

            try:
                # Tenta enviar o embed ao canal do sistema
                await guild.system_channel.send(embed=bemvindo)
            except discord.Forbidden:
                print("Permissões insuficientes para enviar mensagens no canal do sistema.")
            except discord.HTTPException as e:
                print(f"Erro ao enviar mensagem de boas-vindas: {e}")

async def setup(bot):
    await bot.add_cog(Event(bot))
