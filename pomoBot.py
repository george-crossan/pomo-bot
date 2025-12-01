# This example requires the 'message_content' intent.
import asyncio
import discord
import os
import urllib.parse 
import random
from dotenv import load_dotenv
from discord.ext import commands
from discord import Embed

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

client = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command(name='timer', help='Starts a timer for the specified number of minutes.')
async def start_timer(ctx, time = None):
    if time is None:
        await ctx.send('Please provide the time in minutes for the timer.')
        return

    try:
        time = int(time)   
        if time <= 0:
            await ctx.send('Please provide a positive integer for the timer.')
            return
    except ValueError:
        await ctx.send('Please provide a valid integer for the timer.')
        return

    await ctx.send(f'Timer started for {time} minutes!')
    while True:
        time -= 1
        if time == 0:
            break
        await asyncio.sleep(60)
        #cat delivering countdown message
        message_text = "Your countdown Has ended!"
        no_spaces = urllib.parse.quote(message_text) 

        #defo a better way to do this ignore for now
        randomyay = random.randint(1, 1000000)
        cat_url = f"https://cataas.com/cat/says/{no_spaces}?{randomyay}"
        embed = Embed()
        embed.set_image(url=cat_url)
        
    await ctx.send(f"{ctx.author.mention}", embed=embed)
    # play sound when timer ends

    sound_file_duck = 'duck.mp3'  
    sound_file_happycat = 'happycat.mp3'

    all_sounds = [sound_file_duck, sound_file_happycat]
    sound_file = random.choice(all_sounds)
    
    await play_sound(ctx, sound_file)


async def play_sound(ctx, sound_file):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("You are not connected to a voice channel.")
        return

    # connect to the author's voice channel (instance method)
    vc = await ctx.author.voice.channel.connect(timeout=10, reconnect=True)

    # play sound and wait until finished, then disconnect
    source = discord.FFmpegPCMAudio(sound_file)
    vc.play(source)

    while vc.is_playing():
        await asyncio.sleep(0.5)

    await vc.disconnect()


def main():
    bot.run(TOKEN)

if __name__ == '__main__':
    main()