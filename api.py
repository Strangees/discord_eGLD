import discord
import random
from pornhub_api import PornhubApi




#TOKEN = 'OTM5OTE5NTU2MzEzNDgxMzE2.Yf_2TQ.jX-75sX4mv_i33KZoyoJCPTo-DM'
TOKEN = 'OTQxODk1NDM5OTgzMTk4MjU4.YgcmfA.4rsDGYC4Gp0uSNArigj-f-5s2cc'

client = discord.Client()
api = PornhubApi()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})' )

    if message.author == client.user: 
        return
    if user_message.lower() == 'porr':
        tags = random.sample(api.video.tags("f").tags, 5)
        category = random.choice(api.video.categories().categories)
        result = api.search.search(ordering="mostviewed", tags=tags, category=category)
        videourl = result.videos[0].video_id
        videothumnail = result.videos[0].thumb
        videostars = result.videos[0].pornstars
        await message.channel.send(f'{videothumnail}')
        await message.channel.send(f'https://www.pornhub.com/embed/{videourl}')
        for vid in result.videos[0].pornstars:
            if len(videostars) == 0:
                print(await message.channel.send(f'No starring pornstars'))
                return
            else:
                print(await message.channel.send(f'This video is starring: {vid.pornstar_name}'))

        return


client.run(TOKEN)