import discord
from discord.ext import commands
from discord import app_commands
import os
import json
import atexit

# Bot Token - Replace this with your actual token
TOKEN = 'MTQzNzg5MzUyNzAzOTExNTQxNg.GQI3SQ.8rAiio8NPk5UhIMxY8eYaonLr-yAO1HFa3ciqo'

# Debug: Check if TOKEN was loaded
if TOKEN is None or TOKEN == '':
    print("ERROR: Please add your bot token in the script!")
    exit(1)

print(f"Token loaded: {TOKEN[:20]}..." if TOKEN else "Token is None")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
tree = bot.tree

# Payment Bot Functionality
PAYMENTS_FILE = 'payments.json'
DEFAULT_PAYMENTS = {
    'zelle': 'Not set',
    'applepay': 'Not set',
    'cashapp': 'Not set',
    'square': 'Not set'
}
PAYMENT_LOGOS = {
    'zelle': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Zelle_logo.svg/320px-Zelle_logo.svg.png',
    'applepay': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Apple_Pay_logo.svg/320px-Apple_Pay_logo.svg.png',
    'cashapp': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Cash_App_logo.svg/320px-Cash_App_logo.svg.png',
    'square': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Square_Inc._logo.svg/320px-Square_Inc._logo.svg.png'
}

def load_payments():
    if not os.path.exists(PAYMENTS_FILE):
        with open(PAYMENTS_FILE, 'w') as f:
            json.dump(DEFAULT_PAYMENTS, f)
    with open(PAYMENTS_FILE, 'r') as f:
        return json.load(f)

def save_payments(data):
    with open(PAYMENTS_FILE, 'w') as f:
        json.dump(data, f)

@tree.command(name='payment', description='Show all payment methods')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def payment(interaction: discord.Interaction):
    payments = load_payments()
    embed = discord.Embed(title='Payment Methods', color=discord.Color.blue())
    for method, info in payments.items():
        embed.add_field(name=method.capitalize(), value=info, inline=False)
    embed.set_thumbnail(url=PAYMENT_LOGOS['zelle'])
    await interaction.response.send_message(embed=embed)

@tree.command(name='setpayment', description='Update a payment method')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
@app_commands.describe(method='zelle, applepay, cashapp, or square', info='The new info (email, tag, or link)')
async def setpayment(interaction: discord.Interaction, method: str, info: str):
    required_role = 'Payment Manager'
    if not isinstance(interaction.user, discord.Member) or not any(role.name == required_role for role in interaction.user.roles):
        await interaction.response.send_message(f"You need the '{required_role}' role to use this command.", ephemeral=True)
        return

    method = method.lower()
    payments = load_payments()
    if method not in payments:
        await interaction.response.send_message('Invalid method. Choose from: zelle, applepay, cashapp, square.', ephemeral=True)
        return

    payments[method] = info
    save_payments(payments)
    await interaction.response.send_message(f"{method.capitalize()} payment info updated!")

# VCC and Email Bot Functionality
vcc_list = []
email_list = []
email_list_20off25 = []

zip_code = '00000'
expiry = '01/30'

VCC_FILE = 'vcc_list.txt'
EMAIL_FILE = 'email_list.txt'
EMAIL_20OFF25_FILE = 'email_list_20off25.txt'

SETTINGS_FILE = 'settings.json'


def load_data():
    global vcc_list, email_list, email_list_20off25, zip_code, expiry
    if os.path.exists(VCC_FILE):
        with open(VCC_FILE, 'r') as f:
            vcc_list[:] = [line.strip() for line in f if line.strip()]
    if os.path.exists(EMAIL_FILE):
        with open(EMAIL_FILE, 'r') as f:
            email_list[:] = [line.strip() for line in f if line.strip()]
    if os.path.exists(EMAIL_20OFF25_FILE):
        with open(EMAIL_20OFF25_FILE, 'r') as f:
            email_list_20off25[:] = [line.strip() for line in f if line.strip()]
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            data = json.load(f)
            zip_code = data.get('zip', '00000')
            expiry = data.get('expiry', '01/30')

def save_data():
    with open(VCC_FILE, 'w') as f:
        f.write('\n'.join(vcc_list))
    with open(EMAIL_FILE, 'w') as f:
        f.write('\n'.join(email_list))
    with open(EMAIL_20OFF25_FILE, 'w') as f:
        f.write('\n'.join(email_list_20off25))
    with open(SETTINGS_FILE, 'w') as f:
        json.dump({'zip': zip_code, 'expiry': expiry}, f)

atexit.register(save_data)

# Commands
@tree.command(name='addvcc', description='Add one or multiple VCCs (format: card,cvv...)')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def addvcc(interaction: discord.Interaction, data: str):
    added = 0
    for entry in data.split():
        if ',' in entry:
            card, cvv = entry.split(',', 1)
            vcc_list.append(f"{card.strip()},{cvv.strip()}")
            added += 1
    save_data()
    await interaction.response.send_message(f"Added {added} VCC(s).")

@tree.command(name='addemail25off25', description='Add email(s) to main list')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def addemail(interaction: discord.Interaction, emails: str):
    new = [e.strip() for e in emails.split('\n') if e.strip()]
    email_list.extend(new)
    save_data()
    await interaction.response.send_message(f"Added {len(new)} email(s).")

@tree.command(name='addemail20off25', description='Add email(s) to 20off25 list')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def addemail20off25(interaction: discord.Interaction, emails: str):
    new = [e.strip() for e in emails.split('\n') if e.strip()]
    email_list_20off25.extend(new)
    save_data()
    await interaction.response.send_message(f"Added {len(new)} email(s) to 20off25 list.")

@tree.command(name='loadvcc', description='Load VCCs from .txt')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def loadvcc(interaction: discord.Interaction, file: discord.Attachment):
    if not file.filename.endswith('.txt'):
        return await interaction.response.send_message('Upload a .txt file.', ephemeral=True)
    content = await file.read()
    lines = content.decode().splitlines()
    cnt = 0
    for ln in lines:
        if ',' in ln:
            vcc_list.append(ln)
            cnt += 1
    save_data()
    await interaction.response.send_message(f"Loaded {cnt} VCC(s).")

@tree.command(name='loademail25off25', description='Load emails to main list')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def loademail(interaction: discord.Interaction, file: discord.Attachment):
    if not file.filename.endswith('.txt'):
        return await interaction.response.send_message('Upload a .txt file.', ephemeral=True)
    lines = (await file.read()).decode().splitlines()
    new = [e for e in lines if e.strip()]
    email_list.extend(new)
    save_data()
    await interaction.response.send_message(f"Loaded {len(new)} email(s).")

@tree.command(name='load20off25', description='Load emails to 20off25 list')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def load20off25(interaction: discord.Interaction, file: discord.Attachment):
    if not file.filename.endswith('.txt'):
        return await interaction.response.send_message('Upload a .txt file.', ephemeral=True)
    new = [e for e in (await file.read()).decode().splitlines() if e.strip()]
    email_list_20off25.extend(new)
    save_data()
    await interaction.response.send_message(f"Loaded {len(new)} email(s) to 20off25 list.")

@tree.command(name='grab25off25', description='Get next combo from main lists')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def grab(interaction: discord.Interaction, link: str):
    if not vcc_list or not email_list:
        return await interaction.response.send_message('VCC or Email list is empty.')
    card, cvv = vcc_list.pop(0).split(',')
    email = email_list.pop(0)
    save_data()
    await interaction.response.send_message(f"{link},{card},{expiry},{cvv},{zip_code},{email}")

@tree.command(name='grab20off25', description='Get next combo with Uber Eats group link for 20 off 25')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def grab20off25(interaction: discord.Interaction, link: str):
    if not vcc_list or not email_list_20off25:
        return await interaction.response.send_message('VCC or 20off25 list empty.')
    card, cvv = vcc_list.pop(0).split(',')
    email = email_list_20off25.pop(0)
    save_data()
    await interaction.response.send_message(f"{link},{card},{expiry},{cvv},{zip_code},{email}")

@tree.command(name='grabvcc', description='Get next VCC formatted')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def grabvcc(interaction: discord.Interaction):
    if not vcc_list:
        return await interaction.response.send_message('VCC list empty.')
    card, cvv = vcc_list.pop(0).split(',')
    save_data()
    await interaction.response.send_message(f"`{card},{expiry},{cvv},{zip_code}`")

@tree.command(name='grabemail25off25', description='Get next email from main list')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def grabemail(interaction: discord.Interaction):
    if not email_list:
        return await interaction.response.send_message('Email list empty.')
    e = email_list.pop(0)
    save_data()
    await interaction.response.send_message(f"Email: {e}")

@tree.command(name='grabonly20off25', description='Get next email from 20off25')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def grabonly20off25(interaction: discord.Interaction):
    if not email_list_20off25:
        return await interaction.response.send_message('20off25 list empty.')
    e = email_list_20off25.pop(0)
    save_data()
    await interaction.response.send_message(f"20off25 Email: {e}")

@tree.command(name='status', description='Show counts of all lists')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def status(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"✅ Available:\n- VCCs: {len(vcc_list)}\n- Emails: {len(email_list)}\n- 20off25: {len(email_list_20off25)}"
    )

@tree.command(name='setzip', description='Set ZIP code')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def setzip(interaction: discord.Interaction, code: str):
    global zip_code
    zip_code = code
    save_data()
    await interaction.response.send_message(f"ZIP set to {zip_code}")

@tree.command(name='setexpiry', description='Set expiry (MM/YY)')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def setexpiry(interaction: discord.Interaction, exp: str):
    global expiry
    expiry = exp
    save_data()
    await interaction.response.send_message(f"Expiry set to {expiry}")

@tree.command(name='deleteallvcc', description='Clear all VCCs')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def deleteallvcc(interaction: discord.Interaction):
    vcc_list.clear()
    save_data()
    await interaction.response.send_message('All VCCs deleted.')

@tree.command(name='deleteallemail25off25', description='Clear all main emails')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def deleteallemail(interaction: discord.Interaction):
    email_list.clear()
    save_data()
    await interaction.response.send_message('All emails deleted.')

@tree.command(name='delete20off25email', description='Clear all 20off25 emails')
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def delete20off25email(interaction: discord.Interaction):
    email_list_20off25.clear()
    save_data()
    await interaction.response.send_message('All 20off25 emails deleted.')

@bot.event
async def on_ready():
    load_data()
    print(f"✅ Logged in as {bot.user}")
    print(f"Bot is in {len(bot.guilds)} guild(s)")
    try:
        synced = await tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

if __name__ == "__main__":
    bot.run(TOKEN)
