import os
import chainlit as cl
from dotenv import load_dotenv
from datetime import datetime  # 📅 For date/time feature
from agents import Agent, Runner, AsyncOpenAI, RunConfig, OpenAIChatCompletionsModel


# 🔒 Load environment variables (like API key)
load_dotenv()

MODEL_NAME = "gemini-2.0-flash"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🌐 Set up the external Gemini API client
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 🤖 Define the Gemini model
model = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=external_client
)

# ⚙️ Run configuration for the model
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# 🧠 Define your AI Assistant agent
my_assistant = Agent(
    name="AI Assistant",
    instructions=(
        "You are a helpful, friendly, and knowledgeable assistant. "
        "If the user asks for today's date or time, provide real-time information. "
        "Otherwise, respond helpfully to all queries."
    )
)

# 👋 Welcome message when chat starts
@cl.on_chat_start
async def start():
    await cl.Message(
    content="🎉 **Welcome to Moeed's Assistant**\n\n_Type something to get started..._"
).send()


# 💬 Handling user messages
@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content.lower().strip()

    try:
        # 🎯 Custom date/time response without using AI
        if "date" in user_input or "today" in user_input:
            today = datetime.now().strftime("%A, %d %B %Y")
            await cl.Message(content=f"📅 Today's date is: {today}").send()
            return

        if "time" in user_input:
            current_time = datetime.now().strftime("%I:%M %p")
            await cl.Message(content=f"⏰ Current time is: {current_time}").send()
            return

        # ✨ Typing indicator (optional)
        await cl.Message(content="🤖 Thinking...").send()

        # 🤖 Run the AI model
        result = await Runner.run(my_assistant, input=user_input, run_config=config)

        # ✅ Show AI result
        await cl.Message(content=result.final_output).send()

    except Exception as e:
        # ❌ Better error handling
        await cl.Message(content=f"⚠️ An error occurred:\n`{str(e)}`").send()
