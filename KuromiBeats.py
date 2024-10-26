import discord, datetime, asyncio
from discord.ext import tasks
from queue import Queue
import os

q = Queue(maxsize = 15)
q_user = Queue(maxsize = 15)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


    



@client.event
async def send_BOF(): # Credit given to Dannycademy on Youtube for code on scheduled posts
    print("At the start! Time to wait?")
    while True:
        now = datetime.datetime.now()
        then = now.replace(hour=17, minute=12)
        if then < now:
            then += datetime.timedelta(days=1)
        wait_time = (then-now).total_seconds()
        await asyncio.sleep(wait_time)

        channel = client.get_channel(1283960235253301349)
        if q.empty != True:
            await channel.send("BOP OR FLOP! Todays Song: " + q.get() + " Requested by: " + q_user.get())
            await asyncio.sleep(70)
            print("Waiting done, restarting...")
            await send_BOF()
        else:
            await channel.send("Queue is empty! Request some songs guys!")
            await asyncio.sleep(70)
            print("Waiting done, restarting...")
            await send_BOF()
            
    

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await send_BOF()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$queue'): # Add a song to the queue, message format should be as follows: $queue youtube-link username
        if q.full() == True:
            await message.channel.send("BOP OR FLOP queue is full!")
        else:
            msg = message.content.split()
            q.put(msg[1])
            q_user.put(msg[2])
            await message.channel.send("Song has been inserted into queue!")
            print("Song inserted")

    elif message.content.startswith('$send'): # Test bot sending a song from the queue.
        if q.empty() == False:
            await message.channel.send("BOP OR FLOP! Todays Song: " + q.get() + " Requested by: " + q_user.get())
        else:
            await message.channel.send("Queue is empty! Add more songs!")
        return
    

client.run(os.environ["DISCORD_TOKEN"])