import discord
from lib.locareader import get_string_by_id
from lib.sussyconfig import get_config
from lib.mongomanager import MongoManager

config = get_config()

loca_sheet = "loca/loca - ticket.csv"

collection = MongoManager.get_collection("tickets", config.MONGO_DB_NAME)


async def create_ticket(guild: discord.Guild, user: discord.Member, reason: str):
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }

    channel = await guild.create_text_channel(
        name=f"ticket-{user.name}",
        overwrites=overwrites,
        reason=get_string_by_id(loca_sheet, "ticket_embed_desc").format(user.display_name)
    )

    collection.insert_one(
        {
            "_id": str(channel.id),
            "guild_id": str(guild.id),
            "user_id": str(user.id),
            "reason": reason
        }
    )

    eb = discord.Embed(
        title=get_string_by_id(loca_sheet, "ticket_embed_title"),
        description=get_string_by_id(loca_sheet, "ticket_embed_desc").format(user.mention),
        color=discord.Color.blue()
    )
    eb.add_field(
        name=get_string_by_id(loca_sheet, "ticket_embed_reason"),
        value=reason,
        inline=False
    )
    eb.set_footer(text=get_string_by_id(loca_sheet, "ticket_embed_footer"))
    await channel.send(embed=eb)

    return channel


async def close_ticket(channel: discord.TextChannel):
    ticket = collection.find_one({"_id": str(channel.id)})
    if not ticket:
        return False
    collection.delete_one({"_id": str(channel.id)})
    await channel.delete()
    return True
