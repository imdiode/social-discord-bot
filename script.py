import discord
import os
import requests
import tweepy
from keep_alive import keep_alive
import json
from dotenv import load_dotenv
load_dotenv()

# Twitter API config
tauth = tweepy.OAuthHandler(
    os.environ['consumer_key'], os.environ['consumer_secret'])
tauth.set_access_token(
    os.environ['access_token'], os.environ['access_token_secret'])
tapi = tweepy.API(tauth)

# Facebook Grpah API config
FBPID = os.environ['fbPID']
FBToken = os.environ['fbAccessToken']
instapid = os.environ['igpid']

# Discord Config
client = discord.Client()
my_secret = os.environ['token']

# Ready Flag


@client.event
async def on_ready():
  print("Bot ready to show-off!")

# Actions


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith(".tweet"):
    text = message.content
    tweet = text.partition(" ")[2]
    if (len(message.attachments) > 0):
      if (message.attachments[0].content_type == "image/png"):
        # Saving attachment from discord
        await message.attachments[0].save(message.attachments[0].filename)
        # Uploading on twitter
        media = tapi.media_upload(message.attachments[0].filename)
        await tapi.update_status(status=tweet, media_ids=[media.media_id])
        # Removing file
        os.remove(message.attachments[0].filename)
      else:
        tapi.update_status(tweet)
    else:
        tapi.update_status(tweet)

    await message.channel.send("Tweeted!")

  if message.content.startswith(".insta"):
    allowedToPost = False
    Mrole = "Design"
    for x in message.author.roles:
      if Mrole in str(x):
        allowedToPost = True

    if (allowedToPost):
      text = message.content
      icaption = text.partition(" ")[2]
      if (len(message.attachments) > 0):
        if (message.attachments[0].content_type == "image/png"):
          await message.attachments[0].save(message.attachments[0].filename)
          post_url = 'https://graph.facebook.com/v12.0/{}/media'.format(
              instapid)
          payload = {
              'image_url': message.attachments[0].url,
              'caption': icaption,
              'access_token': FBToken
          }
          r = requests.post(post_url, data=payload)
          print(r.text)
          result = json.loads(r.text)
          if 'id' in result:
            creation_id = result['id']
            second_url = 'https://graph.facebook.com/v12.0/{}/media_publish'.format(
                instapid)
            second_payload = {
                'creation_id': creation_id,
                'access_token': FBToken
            }
            requests.post(second_url, data=second_payload)
          await message.channel.send("Posted!")
          os.remove(message.attachments[0].filename)
        else:
          await message.channel.send("The file type is invalid")
      else:
        await message.channel.send("Unable to post")
    else:
      await message.channel.send("Only Design team is allowed to post here")

  if message.content.startswith(".fb"):
    allowedToPost = False
    Mrole = "Design"
    for x in message.author.roles:
      if Mrole in str(x):
        allowedToPost = True

    if (allowedToPost):
      text = message.content
      fbpost = text.partition(" ")[2]
      if (len(message.attachments) > 0):
        if (message.attachments[0].content_type == "image/png"):
          # Saving attachment from discord
          await message.attachments[0].save(message.attachments[0].filename)
          # Uploading on Facebook
          post_url = 'https://graph.facebook.com/{}/photos'.format(FBPID)
          payload = {
              'message': fbpost,
              'url': message.attachments[0].url,
              'access_token': FBToken
          }
          r = requests.post(post_url, data=payload)
          # Removing file
          os.remove(message.attachments[0].filename)
          print(r.text)
        else:
          post_url = 'https://graph.facebook.com/{}/feed'.format(FBPID)
          payload = {
              'message': fbpost,
              'access_token': FBToken
          }
          r = requests.post(post_url, data=payload)
          print(r.text)
      else:
          post_url = 'https://graph.facebook.com/{}/feed'.format(FBPID)
          payload = {
              'message': fbpost,
              'access_token': FBToken
          }
          r = requests.post(post_url, data=payload)
          print(r.text)

      await message.channel.send("Updated!")
    else:
      await message.channel.send("Only Design team is allowed to post here")

  if message.content.startswith(".linkedin"):

    await message.channel.send("Done sire!")

# Run continuously
keep_alive()

# Discord connection
client.run(my_secret)
