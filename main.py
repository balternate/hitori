import discord
import discord.app_commands as app_commands
from lib.sussyconfig import get_config
from lib.locareader import get_string_by_id
from lib.sussyutils import get_prefix, parse_command

# MARK: import commands
from commands import (
    help as bot_help,
    nijika, pick,
    ping, getprefix,
    avatar, doino,
    reactionroles, nijipray, momjoke, incase, ticket, wordreact
)

# MARK: import features
import features.onready_things
import features.auto_react_emoji
import features.on_bot_mentioned
import features.reaction_roles
import features.autoqr
import features.welcome
import features.word_react

config = get_config()

# MARK: Config
bot_version = config.bot_version

TOKEN = config.TOKEN

print(f'{config.bot_name} v{bot_version}')

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)


# loca thing
def get_string(id_: str, loca: str = "main"):
    return get_string_by_id(f"loca/loca - {loca}.csv", id_)


# MARK: Slash commands

@tree.command(name="help", description=get_string("command_help_desc"))
@app_commands.describe(
    option=get_string("help_param_option_desc", "help"),
    subcommand=get_string("help_param_subcommand_desc", "help"),
)
async def get_help(ctx: discord.Interaction, option: str | None = None, subcommand: str | None = None):
    await bot_help.slash_command_listener(ctx, option, subcommand)


@tree.command(name="ping", description=get_string("command_desc", "ping"))
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def pingpong(ctx: discord.Interaction):
    await ping.slash_command_listener(ctx, client)


@tree.command(name="avatar", description=get_string("command_desc", "avatar"))
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_avatar(ctx: discord.Interaction, user: discord.User, server_avatar: bool = True):
    await avatar.slash_command_listener(ctx, user, server_avatar)


@tree.command(name="nijika", description=get_string("command_desc", "nijika"))
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_nijika_image(ctx: discord.Interaction):
    await nijika.slash_command_listener(ctx)


@tree.command(name="get_prefix", description=get_string("command_desc", "getprefix"))
async def get_bot_prefix(ctx: discord.Interaction):
    await getprefix.slash_command_listener(ctx)


@tree.command(name="doino", description=get_string("command_desc", "doino"))
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_vietqr(
        ctx: discord.Interaction,
        bankname: doino.bank_names,
        accountnumber: str,
        accountname: str | None = None,
        amount: int | None = None,
        note: str | None = None):
    await doino.slash_command_listener(ctx, bankname, accountnumber, accountname, amount, note)


@tree.command(name="send_reaction_roles_message", description=get_string("command_desc", "reactionrole"))
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
@app_commands.default_permissions(manage_roles=True)
async def send_reaction_roles_message(
        ctx: discord.Interaction,
        prompt_message: str,
        role1: discord.Role,
        emoji1: str,
        role2: discord.Role | None,
        emoji2: str | None,
        role3: discord.Role | None,
        emoji3: str | None,
        role4: discord.Role | None,
        emoji4: str | None,
        role5: discord.Role | None,
        emoji5: str | None,
        one_role: bool = False
):
    await reactionroles.slash_command_listener(
        ctx, prompt_message, role1, emoji1, role2, emoji2, role3, emoji3, role4, emoji4, role5, emoji5, one_role
    )


@tree.command(name="nijipray", description=get_string("command_desc", "nijipray"))
async def nijipray_command(ctx: discord.Interaction):
    await nijipray.slash_command_listener_pray(ctx, client)


@tree.command(name="nijipray_leaderboard", description=get_string("lb_cmd_desc", "nijipray"))
async def nijipray_leaderboard(ctx: discord.Interaction):
    await nijipray.slash_command_listener_leaderboard(ctx, client)


@tree.command(name="nijipray_info", description=get_string("info_cmd_desc", "nijipray"))
async def nijipray_info(ctx: discord.Interaction, user: discord.User | None = None):
    await nijipray.slash_command_listener_info(ctx, client, user)


@tree.command(name="momjoke")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_momjoke(ctx: discord.Interaction):
    await momjoke.slash_command_listener(ctx)


@tree.command(name="trongtruonghop")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def trongtruonghop(ctx: discord.Interaction):
    await incase.slash_command_listener(ctx)


@tree.command(name="create_ticket", description=get_string("command_desc", "ticket"))
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
async def create_ticket_command(ctx: discord.Interaction, reason: str):
    await ticket.slash_command_listener(ctx, reason)


@tree.command(name="close_ticket", description=get_string("close_command_desc", "ticket"))
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
@app_commands.default_permissions(manage_channels=True)
async def close_ticket_command(ctx: discord.Interaction):
    await ticket.slash_command_listener_close(ctx)



@tree.command(name="add_word_react", description=get_string("add_cmd_desc", "wordreact"))
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
async def add_word_react_command(ctx: discord.Interaction, word: str, response: str):
    await ctx.response.defer()
    await wordreact.slash_command_listener_add(ctx, word, response)


@tree.command(name="remove_word_react", description=get_string("remove_cmd_desc", "wordreact"))
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
async def remove_word_react_command(ctx: discord.Interaction, word: str):
    await ctx.response.defer()
    await wordreact.slash_command_listener_remove(ctx, word)


@tree.command(name="list_word_react", description=get_string("list_cmd_desc", "wordreact"))
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
async def list_word_react_command(ctx: discord.Interaction):
    await ctx.response.defer()
    await wordreact.slash_command_listener_list(ctx)


# MARK: On ready
@client.event
async def on_ready():
    # tree.clear_commands(guild = None) # Uncomment this to clear all commands
    await tree.sync()
    await features.onready_things.on_ready(client)


# MARK: On raw reaction add
@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    await features.reaction_roles.reaction_roles_on_raw_reaction_add_and_remove(payload, client)


# MARK: On raw reaction remove
@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    await features.reaction_roles.reaction_roles_on_raw_reaction_add_and_remove(payload, client)


@client.event
async def on_member_join(member):
    await features.welcome.on_member_join(member)


# MARK: On message
@client.event
async def on_message(message: discord.Message):
    # log console
    if message.author == client.user:
        print(">Bot:", message.content, "\n")
        return

    userid = str(message.author.id)
    username = message.author.global_name
    prefix = get_prefix(message.channel.guild)

    # If someone use command
    if message.content.startswith(prefix):

        # log console
        print(f"{message.author.global_name} at #{message.channel} on {message.guild} : {message.content}")

        # bot user can not use this bot's commands
        if message.author.bot:
            if message.author != client.user:
                await message.channel.send(get_string("bot_use_command_prompt"))
                return

        if int(userid) in config.banned_users:
            await message.channel.send(get_string("banned_user_prompt"))
            return

        # Get requested command
        command = message.content.split()[0].replace(prefix, '')

        plain_args = message.content[len(prefix + command) + 1:]
        args = parse_command(plain_args)

        # MARK: Prefix commands
        if command == 'debug':
            await message.channel.send(
                f"user_id: {message.author.id}, channel_id: {message.channel.id}, guild: {message.guild}")

        elif command == 'getloca':
            await message.channel.send(get_string_by_id(f"loca/loca - {args[0]}.csv", args[1], args[2]))

        elif command in bot_help.cmd_names:
            await bot_help.command_listener(message, args)

        elif command in ping.cmd_names:
            await ping.command_listener(message, client)

        elif command in nijika.cmd_names:
            await nijika.command_listener(message)
            
        elif command in nijipray.cmd_names:
            await nijipray.command_listener(message, client, args)
        
        elif command in incase.cmd_names:
            await incase.command_listener(message)

        # Invalid command
        else:
            await message.channel.send(get_string("command_not_found_prompt"))

    # MARK: Features
    else:
        await features.on_bot_mentioned.reply(client, message)
        await features.auto_react_emoji.react(config.autoreact_emojis, message)
        await features.word_react.react(config.word_react_messages, message)
        await features.autoqr.check_auto_qr(message)


client.run(TOKEN)
