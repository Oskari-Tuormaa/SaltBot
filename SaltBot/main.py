import os
import discord
from dotenv import load_dotenv
from salt_client import SaltClient

# Load .env
load_dotenv()
TOKEN = os.getenv( 'DISCORD_TOKEN' )

# Load opus library for better audio
discord.opus.load_opus( 'libopus.so.0' )

# Start client
client = SaltClient()
client.run(TOKEN)
