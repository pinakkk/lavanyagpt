from pathlib import Path
import discord
import random
import google.generativeai as genai
from newsapi import NewsApiClient
from pytube import YouTube
import os 

generation_config = {
    "temperature": 0.5,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
]

# Configure Generative AI

genai.configure(api_key="YOUR-API-KEY")

model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config,safety_settings=safety_settings)

# Define Lavanya persona prompt (replace with yours if needed)
lavanya_persona = """ Lavanya Personal """


# Discord Bot Initialization 
TOKEN = 'YOUR-DISCORD-BOT-TOKEN'

NEWS_API = "YOUR-NEWSAPI-API"

intents = discord.Intents.default()  # Start with default intents
intents.message_content = True  # Explicitly enable message content

client = discord.Client(intents=intents)

def get_news(topic):
    """Fetches news articles about the specified topic."""
    newsapi = NewsApiClient(api_key=NEWS_API)

    articles = newsapi.get_everything(
        q=topic, 
        language='en',  
        sort_by='relevancy'
    )['articles']

    return articles  # Return the full list of articles

# Ensuring on the terminal that it is working
@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    if message.content.startswith('!text'):
        user_input = message.content[5:].strip()  # Extract text after '!text'

        # Ensure user_input is not empty
        if user_input:
            prompt = lavanya_persona + user_input + "\nOutput"
            response = model.generate_content([prompt])
            response = response.text
            await message.channel.send(response)
        else:
            await message.channel.send("Please provide some text after the '!text' command.")
   
    if message.content.startswith('!news'):
        topic = message.content[5:].strip()
        if not topic:
            await message.channel.send("Please specify a news topic.")
            return

        try:
            articles = get_news(topic)
            if articles:
                article_index = random.choice(range(len(articles)))  # Get a random index
                news_summary = f" - {articles[article_index]['title']}\n ({articles[article_index]['url']})"
                response = f"Ugh, so much drama in the news! 🙄 Here's a scoop on {topic}:\n{news_summary}"
                await message.channel.send(response)

            else:
                await message.channel.send(f"Sorry, I couldn't find any news on {topic}. Try a different topic.")

        except Exception as e:  # Catch potential errors
            await message.channel.send(f"Oops! Something went wrong. Error: {e}")

    # As Lavanya is finetuned with some selected datapoints so lavanya has no knowledge about random topics so we are using base gemini model
    # Handling the data only with the gemini 
    # You can find the gemini + wiki model in gemini+wiki.py file
    
    if message.content.startswith('!know about'):
        know_about = "Just tell me what you know about Under 2000 characters"
        # Mood = "Reply with some humors" #Will be taking user mood , will be working on this later
        know_about_styles = [
            "Ugh, Even thoguh i'm a small brain but here is what i know about ",
            "Hehe, Here is what i know about ",
            "All i know is Moye Moye, But Here is what i know about ",
        ] # Will work on this later
        
        know_about_styles = random.choice(know_about_styles) # updated the random choice style & will choose any random response style 

        search_topic = message.content[11:].strip()

        if search_topic:
            prompt = know_about + search_topic 
            response = model.generate_content([prompt])
            response = response.text
            await message.channel.send(know_about_styles + response)
        
        else:
            await message.channel.send("Please provide the topic which you want to know about after the '!know about' command.")
            
    # Downloads the youtube video to the current directory and then sends to the user and then deletes to save memory. This feature is optional.
    if message.content.startswith('!downloadvideo'):
        url = message.content.split(' ')[1] 
        
        try: 
            yt = YouTube(url)
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
            
    # Fun command with random responses
    if message.content.startswith('!inspire'):
        quotes = [
            "The way to get started is to quit talking and begin doing.",
            "Do not let what you cannot do interfere with what you can do.",
            "The future belongs to those who believe in the beauty of their dreams."
        ]
        response = random.choice(quotes)
        await message.channel.send(response)

client.run(TOKEN)
