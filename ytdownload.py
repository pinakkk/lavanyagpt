from pytube import Youtube 
import os 
from pathlib import Path
import discord

@client.event  
async def on_message(message):
    if message.content.startswith('!downloadvideo'):
        url = message.content.split(' ')[1] 
        
        try: 
            yt = y=Youtube(url)
            video = yt.streams.get_highest_resolution()

            output_path = './' 
            filepath = Path(video.download(output_path))

            new_filename = 'downloaded_video.mp4'  # Customize as needed
            new_filepath = filepath.with_name(new_filename)

            filepath.rename(new_filepath) 

            async with message.channel.typing(): 
                with open(new_filepath, 'rb') as f: 
                    await message.channel.send(file=discord.File(f, new_filename))

            os.remove(new_filepath) 
        except Exception as e: 
            await message.channel.send(f"An error occurred: {e}")