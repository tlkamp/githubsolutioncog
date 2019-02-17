from redbot.core.commands import Cog, command
from discord import Embed


class Generic(Cog):
    """Generic commands that give information about a Discord server."""

    @command()
    async def showroles(self, ctx, inline: bool = True):
        """Lists the roles and number of users in the roles."""
        if not ctx.guild:
            await ctx.send('You must be in a server channel to use this command.')
            return
        roles = sorted(ctx.guild.roles, key=lambda r: r.name.lower())
        embed = Embed(title=f'{ctx.guild.name} Roles',
                      description=f'This server has {ctx.guild.member_count} users and {len(roles)} roles.')
        for role in roles:
            embed.add_field(name=role.name, value=f'{len(role.members)} have this role.', inline=inline)
        await ctx.send(embed=embed)
