import discord
import random
import google.generativeai as genai
from newsapi import NewsApiClient
import datetime
import requests

@client.message
async def on_message(message):
# Providing a short description about the topic using wiki and then sending to gemini andn thentaking the response
    if message.content.startswith('!know about'):
        know_about = "Just tell me what you know about"
        Mood = "Reply with some humors" #Will be taking user mood , will be working on this later
        know_about_styles = [
            "Ugh, Even thoguh i'm a small brain but here is what i know about ",
            "Hehe, Here is what i know about ",
            "All i know is Moye Moye, But Here is what i know about ",
        ]
        know_about_styles = random.choice(know_about_styles) # updated the random choice style & will choose any random response style 

        today = datetime.datetime.now()
        date = today.strftime('%Y/%m/%d')
        search_topic = message.content[11:].strip()
        url = 'https://api.wikimedia.org/core/v1/wikipedia/en/page/{}/description'.format(search_topic) 

        headers = {
  'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyZGVkM2IzYjFiNmZjNWFlNjNlYmUxMzgwNjdhZjM0YiIsImp0aSI6IjcyN2RjNWNmMDRkNDFlOWU1MDg2MTRhOGFkZjM1ZWZjZmQ5NzdiYzBjMjA1OGVlNDVhYTAwN2QyOGJiZmE4ZTJhZDEyYzgxM2Y4YzVjNGYxIiwiaWF0IjoxNzEyNjgxNDMyLjY2Njc2OSwibmJmIjoxNzEyNjgxNDMyLjY2Njc3MywiZXhwIjozMzI2OTU5MDIzMi42NjU1NTgsInN1YiI6Ijc1MzkzODk1IiwiaXNzIjoiaHR0cHM6Ly9tZXRhLndpa2ltZWRpYS5vcmciLCJyYXRlbGltaXQiOnsicmVxdWVzdHNfcGVyX3VuaXQiOjUwMDAsInVuaXQiOiJIT1VSIn0sInNjb3BlcyI6WyJiYXNpYyJdfQ.mM7Hj0-WcUfpU8FIINd9bBwAu1Cy3DxTjrrkUoONi5Dx4TFCgTF7QtniE3rP9u8Uj1ZaX_d3LFjT0oSbI3Rx5cBRFmKGj-_cZey2djBh6aMDkdABN2DLqe0f-4hIjKB-cNvU3ITHiTi0o3WLjXIUuXQHgVwZev59s_t92TX89gZz82Ad9pnizuujOX7qWemJLd01S8jNw1wZjVQK60wdJgdDVKz-LK-wmCXY9rdthn_nYfSzGxWAT7DkeY3Dg7q2Y-P6FDqNlsIURjQ7EZGJd62_07e6Xb4jXj6HcjjWyGaJy6UUg5ORZSIVHHJlX0Bzp0B21qyvAFkHigRMMzDz3tqN3we8_RT1k4K5xzmcoD-Taw_j33ne3d9BmHf-RlmuNGtgpwrpvrXZ5Bk155GcZg5hq4Qik9sGmVKQOsmJUoeM99wp4v1WY_sypkhSRvxNBqyWnc5U64gs5P_DA82OFiIYMlNTXHmz6l2V99HVSB4YMfEwdttdX1KXVZJlYj1T25MRO98AbdxvCy9dEm-Ag6zPMKb5pO74QWYtxdVaK6zzJaI7DFH40R0OMpoHU4hcCWF0A3n67SpY8rr9kVJJrJIkgfjUTBCbueEyXEKeNU0UVVW4vYdVLIcVGBte-pu025cUXAll24FFfrlb4SuidP9GONGqopYb5A4dssYfAq4',
  'User-Agent': 'LavanyaGPT'
    }

        wikires = requests.get(url, headers=headers)
        data = wikires.json()
        if 'description' in data:
            description = data['description']  # Extract just the description
            prompt = know_about + search_topic + "Under 2000 characters" + Mood
            response = model.generate_content([prompt])
            response = response.text
            await message.channel.send(know_about_styles + response)
        else:
            await message.channel.send("Not Found!")
       