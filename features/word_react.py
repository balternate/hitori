import discord

supported_channel_types = [
    discord.ChannelType.text,
    discord.ChannelType.voice,
    discord.ChannelType.public_thread
]


async def react(word_react_messages: dict, message: discord.Message):
    if message.author.bot:
        return
    if message.channel.type not in supported_channel_types:
        return

    content = message.content.lower()
    for word, response in word_react_messages.items():
        if word in content:
            await message.channel.send(response)
            break
