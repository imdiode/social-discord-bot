import discord
import os
import requests

client = discord.Client()
my_secret = os.getenv('token')
print(my_secret)

@client.event
async def on_ready():
  print("Bot ready to show-off!")


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith(".tweet"):
    await message.channel.send("Tweeted!")

  if message.content.startswith(".insta"):
    await message.channel.send("Posted!")

  if message.content.startswith(".fb"):
    await message.channel.send("Updated!")

  if message.content.startswith(".linkedin"):
    await message.channel.send("Done sire!")

#client.run(my_secret)
