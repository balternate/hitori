import discord
import lib.locareader
from lib.sussyconfig import get_config
import features.ticket as ticket
import lib.sussyhelper as sh

config = get_config()

CMD_NAME = "create_ticket"
loca_sheet = f"loca/loca - ticket.csv"

sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name=CMD_NAME,
        command_type=sh.CommandType.SLASH,
        description=lib.locareader.get_string_by_id(loca_sheet, "command_desc"),
        usage=lib.locareader.get_string_by_id(loca_sheet, "command_usage"),
        parameters=[
            sh.CommandParameterDescription(
                name="reason",
                description=lib.locareader.get_string_by_id(loca_sheet, "command_param_reason_desc"),
                required=True
            )
        ]
    ),
    sh.HelpSection.MODERATION
)


async def slash_command_listener(ctx: discord.Interaction, reason: str):
    print(f"{ctx.user} used {CMD_NAME} commands!")
    await ctx.response.defer(ephemeral=True)
    try:
        channel = await ticket.create_ticket(ctx.guild, ctx.user, reason)
    except discord.Forbidden:
        await ctx.followup.send(lib.locareader.get_string_by_id(loca_sheet, "bot_no_permission"))
        return
    await ctx.followup.send(
        lib.locareader.get_string_by_id(loca_sheet, "ticket_created").format(channel.mention)
    )


async def slash_command_listener_close(ctx: discord.Interaction):
    print(f"{ctx.user} used close_ticket commands!")
    await ctx.response.defer(ephemeral=True)
    if not ctx.user.guild_permissions.manage_channels:
        await ctx.followup.send(lib.locareader.get_string_by_id(loca_sheet, "no_permission"))
        return
    result = await ticket.close_ticket(ctx.channel)
    if not result:
        await ctx.followup.send(lib.locareader.get_string_by_id(loca_sheet, "not_a_ticket"))
        return
