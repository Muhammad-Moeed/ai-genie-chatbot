import os
import chainlit as cl
from dotenv import load_dotenv
from datetime import datetime
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Model
model = genai.GenerativeModel('gemini-pro')

@cl.on_chat_start
async def start():
    await cl.Message(
        content="🎉 **Welcome to AI Genie – Powered by Gemini (M.Moeed)**\n\n_Type something to get started..._"
    ).send()

@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content.lower().strip()

    try:
        # Date/Time Handling
        if "date" in user_input or "today" in user_input:
            today = datetime.now().strftime("%A, %d %B %Y")
            await cl.Message(content=f"📅 Today's date is: {today}").send()
            return

        if "time" in user_input:
            current_time = datetime.now().strftime("%I:%M %p")
            await cl.Message(content=f"⏰ Current time is: {current_time}").send()
            return

        await cl.Message(content="🤖 Thinking...").send()

        # Generate Gemini response
        response = model.generate_content(user_input)
        await cl.Message(content=response.text).send()

    except Exception as e:
        await cl.Message(content=f"⚠️ An error occurred:\n`{str(e)}`").send()
