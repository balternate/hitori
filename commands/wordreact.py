import discord
import lib.locareader
from lib.sussyconfig import get_config
import lib.sussyhelper as sh
import config as bot_config

config = get_config()

loca_sheet = "loca/loca - wordreact.csv"


def get_loca(id_: str):
    return lib.locareader.get_string_by_id(loca_sheet, id_)


sh.HelpManager.add_command_help(
    sh.CommandHelpGroup(
        group_name="word_react",
        command_type=sh.CommandType.SLASH,
        description=get_loca("add_cmd_desc"),
        usage=get_loca("add_cmd_usage"),
        commands=[
            sh.CommandHelp(
                command_name="add_word_react",
                command_type=sh.CommandType.SLASH,
                description=get_loca("add_cmd_desc"),
                usage=get_loca("add_cmd_usage"),
                parameters=[
                    sh.CommandParameterDescription(
                        name="word",
                        description=get_loca("add_param_word_desc"),
                        required=True
                    ),
                    sh.CommandParameterDescription(
                        name="response",
                        description=get_loca("add_param_response_desc"),
                        required=True
                    ),
                ]
            ),
            sh.CommandHelp(
                command_name="remove_word_react",
                command_type=sh.CommandType.SLASH,
                description=get_loca("remove_cmd_desc"),
                usage=get_loca("remove_cmd_usage"),
                parameters=[
                    sh.CommandParameterDescription(
                        name="word",
                        description=get_loca("remove_param_word_desc"),
                        required=True
                    ),
                ]
            ),
            sh.CommandHelp(
                command_name="list_word_react",
                command_type=sh.CommandType.SLASH,
                description=get_loca("list_cmd_desc"),
                usage=get_loca("list_cmd_usage"),
            ),
        ]
    ),
    sh.HelpSection.GENERAL
)


async def slash_command_listener_add(ctx: discord.Interaction, word: str, response: str):
    print(f"{ctx.user} used add_word_react commands!")

    if ctx.user.id not in config.dev_ids:
        await ctx.followup.send(get_loca("no_permission"))
        return

    word_lower = word.lower()
    config.word_react_messages[word_lower] = response
    bot_config.json_config["word_react_messages"][word_lower] = response
    bot_config.save_config()

    await ctx.followup.send(get_loca("added").format(word_lower, response))


async def slash_command_listener_remove(ctx: discord.Interaction, word: str):
    print(f"{ctx.user} used remove_word_react commands!")

    if ctx.user.id not in config.dev_ids:
        await ctx.followup.send(get_loca("no_permission"))
        return

    word_lower = word.lower()
    if word_lower not in config.word_react_messages:
        await ctx.followup.send(get_loca("not_found").format(word_lower))
        return

    del config.word_react_messages[word_lower]
    del bot_config.json_config["word_react_messages"][word_lower]
    bot_config.save_config()

    await ctx.followup.send(get_loca("removed").format(word_lower))


async def slash_command_listener_list(ctx: discord.Interaction):
    print(f"{ctx.user} used list_word_react commands!")

    if not config.word_react_messages:
        await ctx.followup.send(get_loca("list_empty"))
        return

    entries = ""
    for word, response in config.word_react_messages.items():
        entries += get_loca("list_entry").format(word, response) + "\n"

    eb = discord.Embed(
        title=get_loca("list_title"),
        description=entries,
        color=discord.Color.blue()
    )
    await ctx.followup.send(embed=eb)
