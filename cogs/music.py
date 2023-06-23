from discord.ext import commands
import discord
import asyncio
from pytube import YouTube
import requests
import random


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # def search_yt
    # def play_next
    # command skip
    # command queue
    # command clear
    # command add (add to queue)

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

    async def linkURL(self, link):
        video_url = link or random.choice(["https://youtu.be/urH09Bu4NLo","https://youtu.be/d8rzpLfZXLU"])
        youtube = YouTube(video_url)

        return {
            "audio_url": youtube.streams.get_highest_resolution().url,
            "thumbnail_url": youtube.thumbnail_url,
            "title": youtube.title
        }
    
    async def playMusic(self, ctx, data):
        try:
            # todo temporary
            ctx.voice_client.stop()

            embed = discord.Embed(
                title='_Now Playing_',
                description=data['title'],
                color=discord.Color.from_rgb(198, 175, 165)
            )
            embed.set_thumbnail(url=data['thumbnail_url'])
            await ctx.send(embed=embed)

            audio_source = await discord.FFmpegOpusAudio.from_probe(data['audio_url'])
            ctx.voice_client.play(audio_source, after=lambda e: print("Playback finished."))

        except asyncio.TimeoutError:
            print("Timeout occurred while fetching audio URL")

    @commands.command()
    async def play(self, ctx, link=None):

        await self.join(ctx)
        await self.playMusic(ctx, await self.linkURL(link))
        
    
    @commands.command(aliases=["dc"])
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def pause(self, ctx):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if voice_channel is not None and voice_channel == ctx.voice_client.channel:
            await ctx.voice_client.pause()

    @commands.command()
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
