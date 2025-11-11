# Discord Bot - Ready to Run!

## ✅ ALREADY CONFIGURED
Your bot token is already hardcoded in the script. You're ready to go!

## Quick Start (3 Steps)

### 1. Install Dependencies
Open Command Prompt or Terminal in this folder and run:
```bash
pip install -r requirements.txt
```

### 2. Enable Bot Intents (IMPORTANT!)
1. Go to https://discord.com/developers/applications
2. Click on your bot application
3. Go to "Bot" section (left sidebar)
4. Scroll down to "Privileged Gateway Intents"
5. Enable: ✅ **Message Content Intent**
6. Click "Save Changes"

### 3. Run the Bot
```bash
python discord_bot.py
```

You should see:
```
Token loaded: MTQzNzg5MzUyNzAzOTEx...
✅ Logged in as YourBotName#1234
Bot is in 1 guild(s)
✅ Synced XX command(s)
```

## Invite Bot to Your Server
1. Go to Discord Developer Portal → Your App → OAuth2 → URL Generator
2. Select scopes: `bot` and `applications.commands`
3. Select permissions: `Administrator` (or customize)
4. Copy the generated URL and open it in your browser
5. Select your server and authorize

Or use this template (replace YOUR_CLIENT_ID):
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot%20applications.commands
```

## Files Included
- `discord_bot.py` - Main bot script (token already included)
- `requirements.txt` - Python dependencies
- `vcc_list.txt` - VCC storage (empty, ready to use)
- `email_list.txt` - 25off25 email storage
- `email_list_20off25.txt` - 20off25 email storage
- `settings.json` - Bot settings (ZIP, expiry)

## Available Commands
- `/payment` - Show all payment methods
- `/setpayment` - Update payment method (requires Payment Manager role)
- `/addvcc` - Add VCC(s)
- `/addemail25off25` - Add emails to main list
- `/addemail20off25` - Add emails to 20off25 list
- `/loadvcc` - Load VCCs from .txt file
- `/loademail25off25` - Load emails to main list
- `/load20off25` - Load emails to 20off25 list
- `/grab25off25` - Get next combo from main lists
- `/grab20off25` - Get next combo for 20 off 25
- `/grabvcc` - Get next VCC
- `/grabemail25off25` - Get next email from main list
- `/grabonly20off25` - Get next email from 20off25
- `/status` - Show counts of all lists
- `/setzip` - Set ZIP code
- `/setexpiry` - Set expiry date (MM/YY)
- `/deleteallvcc` - Clear all VCCs
- `/deleteallemail25off25` - Clear all main emails
- `/delete20off25email` - Clear all 20off25 emails

## Troubleshooting

**"401 Unauthorized" Error:**
Your token may be expired. To fix:
1. Go to Discord Developer Portal → Bot section
2. Click "Reset Token"
3. Copy the new token
4. Open `discord_bot.py` in a text editor
5. Find the line: `TOKEN = 'MTQzNzg5...'`
6. Replace the token with your new one
7. Save the file

**Commands not showing in Discord:**
- Wait 5-10 minutes for Discord to sync commands globally
- Make sure "Message Content Intent" is enabled
- Try using commands in DMs with the bot first

**Bot joins server but no commands:**
- Reinvite the bot with `applications.commands` scope
- Make sure bot has proper permissions in the server

**"Module not found" Error:**
Run: `pip install -r requirements.txt`

## Optional: Payment Manager Role
To use `/setpayment` command:
1. Create a role named "Payment Manager" in your Discord server (exact name)
2. Assign it to users who should manage payment methods
