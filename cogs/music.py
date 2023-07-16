from discord.ext import commands
import discord
import asyncio
from pytube import YouTube
import requests
import random
import os
import re

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
    # def search_yt
    # def play_next
    # command skip
    # command queue
    # command clear
    # command add (add to queue)

    def is_youtube_link(self, url):
        youtube_pattern = r"(?:https?://)?(?:www\.)?youtu(?:be\.com|\.be)/(?:watch\?v=|embed/|v/|user/)?([\w-]{11})"
        match = re.match(youtube_pattern, url)
        return match is not None

    async def playNext(self, ctx, nextUrl=None):
        # todo add useful here XDD
        print("playnext")
        await self.playMusic(ctx, await self.manageUrl(nextUrl))
        print("await")
        await asyncio.sleep(1)

    async def join(self, ctx):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if voice_channel is None and ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            return

        if ctx.voice_client is not None:
            if ctx.voice_client.channel == voice_channel:
                # todo fix
                if ctx.voice_client.is_paused():
                    ctx.voice_client.resume()
                return
            else:
                await ctx.voice_client.move_to(voice_channel)
        else:
            await voice_channel.connect()

    async def manageUrl(self, link):
        default_audio = requests.get("https://rcph-smz.github.io/rcph_player_src/fetch/kawaiineko.json").json()
        audio_url = f'{default_audio.get("path")}/{random.choice(default_audio.get("list"))}'
        thumbnail_url = self.bot.user.display_avatar.url
        title = os.path.basename(audio_url).replace(".mp3","")

        if self.is_youtube_link(link):
            video_url = link or random.choice(["https://youtu.be/urH09Bu4NLo","https://youtu.be/d8rzpLfZXLU"])
            youtube = YouTube(video_url)
            audio_url = youtube.streams.get_highest_resolution().url
            thumbnail_url = youtube.thumbnail_url
            title = youtube.title

        return {
            "audio_url": audio_url,
            "thumbnail_url": thumbnail_url,
            "title": title
        }

    
    async def playMusic(self, ctx, data):
        try:
            # todo temporary
            ctx.voice_client.stop()

            embed = discord.Embed(
                title='_Now Playing_',
                description=data['title'],
                color=discord.Color.from_rgb(84,74,165)
            )
            embed.set_thumbnail(url=data['thumbnail_url'])
            await ctx.send(embed=embed)

            audio_source = await discord.FFmpegOpusAudio.from_probe(data['audio_url'])
            ctx.voice_client.play(audio_source, after=lambda e: print("Playback Finished"))

        except asyncio.TimeoutError:
            print("Timeout occurred while fetching audio URL")

    @commands.command()
    async def play(self, ctx, link=None):

        await self.join(ctx)
        await self.playMusic(ctx, await self.manageUrl(link))
        
    
    @commands.command(aliases=["dc"])
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(aliases=["freeze"])
    async def pause(self, ctx):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if voice_channel is not None and voice_channel == ctx.voice_client.channel:
            await ctx.voice_client.pause()

    @commands.command(aliases=["continue"])
    async def resume(self, ctx):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if voice_channel is not None and voice_channel == ctx.voice_client.channel:
            await ctx.voice_client.resume()

    @commands.command()
    async def stop(self, ctx):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if voice_channel is not None and voice_channel == ctx.voice_client.channel:
            await ctx.voice_client.stop()

async def setup(bot):
    await bot.add_cog(Music(bot))
