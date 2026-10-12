import discord
import os
from dotenv import load_dotenv # type: ignore
from discord import app_commands
from discord.ext import commands

load_dotenv()

# load token via .env
discord_token = str(os.getenv("BOT_TOKEN"))

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!",intents=intents)


# sync command tree when logging in
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    try:
        # sync commands with Discord
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# the track command
@client.tree.command(name="track", description="Tracks a parcel.")
@app_commands.describe(
    courier="The postage service, eg NZ Post", 
    tracking_code="The parcel's tracking number", 
    nice_name="Item being shipped"
)
@app_commands.choices(courier=[
    app_commands.Choice(name="NZ Post", value="nzpost")
])
async def track(
    interaction: discord.Interaction,
    courier: str,
    tracking_code: str,
    nice_name: str
    ):
    emoji = ""
    courier_nice_name = "Unknown Courier"
    if courier == "nzpost":
        emoji = "<:nzpost:1536879960151687209>"
        courier_nice_name = "NZ Post"

    channel = interaction.channel # get current channel
    if isinstance(channel, discord.TextChannel): # check if its a text channel cos threads cant be made in DMs, etc
        thread = await channel.create_thread(
            name=f"{nice_name}",
            auto_archive_duration=60,
            type=discord.ChannelType.public_thread,
            reason=f"Creating thread to track {tracking_code} VIA {courier_nice_name} {emoji}!"
        )
        
        await thread.send(
            content=(
                f"Tracking **{nice_name}** ({tracking_code}) with {courier_nice_name} {emoji}.\n"
                "Tracking updates with appear here."
            )
        )

        # reply using intercation.response, dear future nur: ephemeral means "Only visible to you" btw
        await interaction.response.send_message(
            f"Created a tracking thread for **{nice_name}** ({tracking_code}) via {emoji} {courier_nice_name}.",
            ephemeral=True
        ) 
    else:
        await interaction.response.send_message("Unable to create thread, is this a DM?") # reply using intercation.response, dear future nur: ephemeral means "Only visible to you" btw
    

client.run(discord_token)
