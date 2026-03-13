import discord
from lib.sussyconfig import get_config

config = get_config()


async def on_member_join(member: discord.Member):
    channel = member.guild.get_channel(config.welcome_channel_id)
    if channel is None:
        return

    account_age = discord.utils.format_dt(member.created_at, "R")
    
    embed = discord.Embed(
        description=f"Chào mừng {member.mention} đến với **{member.guild.name}**!",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=member.display_avatar.url if member.display_avatar else None)
    embed.add_field(
        name="📅 Tài khoản được tạo",
        value=account_age,
        inline=True
    )
    embed.add_field(
        name="👥 Thành viên thứ",
        value=f"**{member.guild.member_count}**",
        inline=True
    )
    embed.set_footer(text=f"ID: {member.id}")
    await channel.send(embed=embed)