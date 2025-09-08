import discord
import os # Required to access the secret token
from discord.commands import Option # Required for slash command options

# --- BOT SETUP ---
# Create the bot instance with a command prefix and specify intents
intents = discord.Intents.default()
intents.message_content = True # Enable the message content intent
bot = discord.Bot(intents=intents)

# --- EVENT: ON READY ---
# This event runs when the bot has successfully connected to Discord
@bot.event
async def on_ready():
    print(f"✅ We have logged in as {bot.user}")
    print("✅ Bot is online and ready!")
    print("---------------------------------")

# --- SLASH COMMAND: /call ---
# This defines the slash command for creating a dispatch call
@bot.slash_command(
    name="call",
    description="Generate a new dispatch call embed."
    guild_ids=[1403411414361837588] 
)
async def create_call(
    ctx: discord.ApplicationContext,
    title: Option(str, "The title of the call (e.g., Robbery in Progress)", required=True),
    location: Option(str, "The location of the call (e.g., Conway Bank)", required=True),
    description: Option(str, "A detailed description of the situation.", required=True),
    priority: Option(str, "The priority level of the call.", choices=["Low", "Medium", "High", "Emergency"], required=True)
):
    # --- EMBED CREATION ---
    
    # Set the embed color based on the priority level
    if priority.lower() == "low":
        embed_color = discord.Color.green()
    elif priority.lower() == "medium":
        embed_color = discord.Color.gold()
    elif priority.lower() == "high":
        embed_color = discord.Color.orange()
    elif priority.lower() == "emergency":
        embed_color = discord.Color.red()
    else:
        embed_color = discord.Color.default() # Fallback color

    # Create the embed object
    embed = discord.Embed(
        title=f"📢 New Dispatch Call: {title}",
        description="All units, please respond accordingly.",
        color=embed_color,
        timestamp=discord.utils.utcnow() # Adds the current time
    )

    # Add fields to the embed for better organization
    embed.add_field(name="📍 Location", value=f"```{location}```", inline=False)
    embed.add_field(name="📝 Description", value=f"```{description}```", inline=False)
    embed.add_field(name="⚠️ Priority", value=f"**{priority.upper()}**", inline=True)
    embed.add_field(name="Dispatcher", value=f"{ctx.author.mention}", inline=True)
    
    # Set a footer and a thumbnail (optional)
    embed.set_footer(text="10-David")
    # You can upload a department logo to Replit and use its URL here
    # embed.set_thumbnail(url="https://media.discordapp.net/attachments/1403444626983096340/1403444627742392370/CCSD_logo.png?ex=68bf2029&is=68bdcea9&hm=9466d8f3f620567539e4a8c4a55b4c4bd76b608c0183f49537f63d4ec5e06a7d&=&format=webp&quality=lossless&width=780&height=780")

    # --- SEND THE EMBED ---
    # Send the embed to the channel where the command was used
    await ctx.respond(embed=embed)


# --- RUN THE BOT ---
# This line retrieves the token from secrets and starts the bot
bot.run(os.environ['TOKEN'])
