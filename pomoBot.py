# This example requires the 'message_content' intent.
import asyncio
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

client = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command(name='timer', help='Starts a timer for the specified number of seconds.')
async def start_timer(ctx, time = None):
    if time is None:
        await ctx.send('Please provide the time in seconds for the timer.')
        return

    try:
        time = int(time)   
        if time <= 0:
            await ctx.send('Please provide a positive integer for the timer.')
            return
    except ValueError:
        await ctx.send('Please provide a valid integer for the timer.')
        return

    await ctx.send(f'Timer started for {time} seconds!')
    while True:
        time -= 1
        if time == 0:
            break
        await asyncio.sleep(1)
    await ctx.send(f"{ctx.author.mention} Your countdown Has ended!")
    # play sound when timer ends
    sound_file = 'duck.mp3'  # specify your sound file here
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