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
        self.is_playing = False 

    def is_youtube_link(self, url=None):
        if url is None:
            return None

        youtube_pattern = r"(?:https?://)?(?:www\.)?youtu(?:be\.com|\.be)/(?:watch\?v=|embed/|v/|user/)?([\w-]{11})"
        match = re.match(youtube_pattern, url)
        return match is not None

    async def join(self, ctx):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if voice_channel is None and ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            return

        if ctx.voice_client is not None:
            if ctx.voice_client.channel == voice_channel:
                if ctx.voice_client.is_paused():
                    ctx.voice_client.resume()
                return
            else:
                await ctx.voice_client.move_to(voice_channel)
        else:
            await voice_channel.connect()

    async def manageUrl(self, link=None):
        default_audio = requests.get("https://rcph-smz.github.io/rcph_player_src/fetch/kawaiineko.json").json()
        audio_url = f'{default_audio.get("path")}/{random.choice(default_audio.get("list"))}'
        thumbnail_url = self.bot.user.display_avatar.url
        title = os.path.basename(audio_url).replace(".mp3", "")

        if self.is_youtube_link(link):
            video_url = link or random.choice(["https://youtu.be/urH09Bu4NLo", "https://youtu.be/d8rzpLfZXLU"])
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
            ctx.voice_client.stop()

            embed = discord.Embed(
                title='_Now Playing_',
                description=data['title'],
                color=discord.Color.from_rgb(84, 74, 165)
            )
            embed.set_thumbnail(url=data['thumbnail_url'])
            await ctx.send(embed=embed)

            audio_source = await discord.FFmpegOpusAudio.from_probe(data['audio_url'])
            ctx.voice_client.play(audio_source, after=lambda e: print("Playback Finished"))

        except asyncio.TimeoutError:
            print("Timeout occurred while fetching audio URL")

    async def check_queue(self, ctx):
        if len(self.queue) > 0:
            data = await self.manageUrl(self.queue[0])
            self.queue.pop(0)
            await self.playMusic(ctx, data)

    @commands.command()
    async def play(self, ctx, link=None):
        await self.join(ctx)
        await self.playMusic(ctx, await self.manageUrl(link))

    @commands.command(aliases=["dc", "leave","quit"])
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

    @commands.command(aliases=["end","skip"])
    async def stop(self, ctx):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if voice_channel is not None and voice_channel == ctx.voice_client.channel:
            await ctx.voice_client.stop()

    @commands.command()
    async def add(self, ctx, *req):
        self.queue.extend(req)
        await ctx.send("Added to queue!")

    @commands.command(aliases=["pop"])
    async def remove(self, ctx, index: int):
        if 0 <= index < len(self.queue):
            removed_item = self.queue.pop(index)
            await ctx.send(f"Removed item at index {index}: {removed_item}")
        else:
            await ctx.send("Invalid index!")

    @commands.command()
    async def queue(self, ctx):
        if len(self.queue) > 0:
            queue_str = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(self.queue)])
            await ctx.send(f"Queue:\n{queue_str}")
        else:
            await ctx.send("The queue is empty!")

    @commands.command()
    async def clear(self, ctx):
        self.queue.clear()
        await ctx.send("Queue cleared!")

    #TODO this is not command fix elsewhere.
    @commands.command()
    async def search_yt(self, ctx, *query):
        query = " ".join(query)
        youtube_search_url = f"https://www.youtube.com/results?search_query={query}"
        await ctx.send(f"YouTube search results: {youtube_search_url}")


async def setup(bot):
    await bot.add_cog(Music(bot))
