from redbot.core.commands import Cog, command
from redbot.core import checks
from discord import Embed


class GitHubSolution(Cog):
    """Posts a solution summary to a GitHub issue."""
    @command()
    #@checks.role
    async def solution(self, ctx, issue: int = None, summary: str = None):
        """
        Posts a solution summary to a GitHub issue.
        Example: [p]solution 123 "The user did not try turning it off/on again."
        """
        embed = Embed(title=f'Solution to #{issue} posted!', colour=ctx.author.colour, url='https://github.com/tlkamp')
        embed.add_field(name='Summary', value=summary)
        embed.set_footer(text=f'Thanks, {ctx.author.name}!', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
