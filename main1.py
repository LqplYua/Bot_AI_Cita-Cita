import discord
from discord.ext import commands
from logic import gemini_api 

TOKEN = 'ISI SENDIRI' 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Fitur Baru: Menu Pilihan & Tombol ---
class CareerMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="Pilih bidang yang kamu minati...",
        options=[
            discord.SelectOption(label="Teknologi & Coding", emoji="💻", description="Software, Game, AI"),
            discord.SelectOption(label="Seni & Kreatif", emoji="🎨", description="Desain, Musik, Video"),
            discord.SelectOption(label="Sains & Medis", emoji="🧪", description="Dokter, Peneliti, Astronom"),
            discord.SelectOption(label="Bisnis & Sosmed", emoji="📈", description="Marketing, Entrepreneur, Influencer"),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.defer()
        bidang = select.values[0]
        
        # AI menganalisis berdasarkan pilihan menu
        hasil = gemini_api.analisa_cita_cita(f"Saya tertarik di bidang {bidang}")
        
        embed = discord.Embed(
            title=f"🚀 Rekomendasi Bidang: {bidang}",
            description=hasil,
            color=discord.Color.blue()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    @discord.ui.button(label="Cek Motivasi Harian", style=discord.ButtonStyle.success, emoji="🔥")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        motivasi = gemini_api.analisa_cita_cita("Berikan satu kalimat motivasi singkat untuk pelajar SMA kelas 10")
        await interaction.response.send_message(f"📢 **Pesan Untukmu:**\n{motivasi}", ephemeral=True)

# --- Event & Commands ---
@bot.event
async def on_ready():
    print(f'✅ Bot Startup {bot.user} aktif!')

@bot.command()
async def mulai(ctx):
    """Menampilkan menu interaktif"""
    embed = discord.Embed(
        title="👋 Halo, Selamat datang di Career Advisor",
        description="Pilih kategori di bawah atau ketik `!cita [hobi]` untuk konsultasi manual.",
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed, view=CareerMenuView())

@bot.command()
async def cita(ctx, *, hobi):
    async with ctx.typing():
        hasil = gemini_api.analisa_cita_cita(hobi)
        embed = discord.Embed(
            title="🎯 Analisis Minat Manual",
            description=f"Hobi: **{hobi}**\n\n{hasil}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

bot.run(TOKEN)