import discord
from discord.ext import commands
from discord import app_commands
import json
from config import TOKEN, ADMIN_ROLE, POINTS_TABLE
from google_sheets import add_team

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

scrims = {
    "open": False,
    "teams": []
}

def save():
    with open("data/scrims.json", "w") as f:
        json.dump(scrims, f)

def load():
    global scrims
    try:
        with open("data/scrims.json") as f:
            scrims = json.load(f)
    except:
        save()

@bot.event
async def on_ready():
    load()
    await bot.tree.sync()
    print("Scrims bot ready")

# 🔓 Open Registrations
@bot.tree.command(name="open")
@app_commands.checks.has_role(ADMIN_ROLE)
async def open_scrims(interaction: discord.Interaction):
    scrims["open"] = True
    scrims["teams"] = []
    save()
    await interaction.response.send_message("✅ Scrims registration OPEN")

# 🔒 Close Registrations
@bot.tree.command(name="close")
@app_commands.checks.has_role(ADMIN_ROLE)
async def close_scrims(interaction: discord.Interaction):
    scrims["open"] = False
    save()
    await interaction.response.send_message("❌ Registration CLOSED")

# 📝 Register Team
@bot.tree.command(name="register")
async def register(interaction: discord.Interaction, team_name: str):
    if not scrims["open"]:
        await interaction.response.send_message("❌ Registration closed")
        return

    if team_name in scrims["teams"]:
        await interaction.response.send_message("⚠️ Team already registered")
        return

    scrims["teams"].append(team_name)
    slot = len(scrims["teams"])
    save()
    add_team(team_name, slot)

    await interaction.response.send_message(
        f"✅ **{team_name}** registered | Slot {slot}"
    )

# 📋 Slot List
@bot.tree.command(name="slots")
async def slots(interaction: discord.Interaction):
    if not scrims["teams"]:
        await interaction.response.send_message("No teams registered")
        return

    msg = "**📋 SLOT LIST**\n"
    for i, t in enumerate(scrims["teams"], 1):
        msg += f"{i}. {t}\n"

    await interaction.response.send_message(msg)

# 🏠 Room Details
@bot.tree.command(name="room")
@app_commands.checks.has_role(ADMIN_ROLE)
async def room(interaction: discord.Interaction, room_id: str, password: str):
    await interaction.response.send_message(
        f"🏠 **ROOM DETAILS**\n"
        f"ID: `{room_id}`\n"
        f"PW: `{password}`"
    )

# 🏆 Points
@bot.tree.command(name="points")
@app_commands.checks.has_role(ADMIN_ROLE)
async def points(interaction: discord.Interaction,
                 team: str, position: int, kills: int):
    placement = POINTS_TABLE.get(position, 0)
    total = placement + kills

    await interaction.response.send_message(
        f"🏆 **{team} Results**\n"
        f"Placement: {placement}\n"
        f"Kills: {kills}\n"
        f"Total: **{total}**"
    )

bot.run(TOKEN)
