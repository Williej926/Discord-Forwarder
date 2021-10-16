from typing import DefaultDict
import discord
import json
from discord import channel
from discord import Webhook,AsyncWebhookAdapter
import aiohttp
j = 0
with open('config.json','r') as f:
    j = json.loads(f.read())
token = ''
webhooks = dict()
channels = DefaultDict(int)
for user in j['user_tokens']:
    token = j['user_tokens'][user]
for channel in j['channels']:
    channels[int(j['channels'][channel])] = j['webhooks'][channel]



print(token)



client = discord.Client()
@client.event
async def on_message(message):

    if(message.channel.id in channels):
        
        embed = "";
        try:
            embed = message.embeds[0]
            e = embed.to_dict()
            e['footer']['text'] = "Discord Forwarder"
            e['color'] = 12212731
            embed = discord.Embed.from_dict(e)
            print(embed.image)
            try:
                s = embed.title
                s = s[s.rindex(' ')+1:]
            except Exception as f:
                s = embed.title
        except Exception as e:
            pass
        async with aiohttp.ClientSession() as session:
            w = channels[message.channel.id]
            webhook = Webhook.from_url(w, adapter=AsyncWebhookAdapter(session))
            try:
                for a in message.attachments:
                    print(a)
                    await webhook.send(a.url)
                await webhook.send(message.content)
                await webhook.send(embed=embed)
            except Exception as e:
                await webhook.send(embed=embed)
                print('sent!')
      


client.run(token)
