from telebot.types import Message

from bot.bot import get_bot

bot = get_bot()


@bot.message_handler(commands=["start"])  # type: ignore
async def start(message: Message) -> None:
    welcome_text = (
        f"Hello, {message.from_user.first_name} {message.from_user.last_name}!"
    )
    await bot.send_message(chat_id=message.chat.id, text=welcome_text)


@bot.message_handler(func=lambda message: True)  # type: ignore
async def echo(message: Message) -> None:
    await bot.reply_to(message=message, text=message.text)
