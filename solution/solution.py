from redbot.core.commands import Cog, command
from redbot.core import Config
from redbot.core import checks
from discord import Embed


class GitHubSolution(Cog):
    """Posts a solution summary to a GitHub issue."""
    def __init__(self):
        self.config = Config.get_conf(self, identifier=9900990099)
        default_guild = {
            "github_url": None
        }
        self.config.register_guild(**default_guild)

    @command()
    @checks.admin_or_permissions(manage_guild=True)
    @checks.bot_in_a_guild()
    async def setproject(self, ctx, project_url: str):
        """
        Sets the GitHub URL to project_url.
        Default is None.
        """
        new_url = project_url.replace('<', '').replace('>', '')
        old_url = await self.config.guild(ctx.guild).github_url()
        await self.config.guild(ctx.guild).github_url.set(new_url)
        await ctx.send(f'Value of `github_url` has changed from <{old_url}> to <{new_url}>')

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
