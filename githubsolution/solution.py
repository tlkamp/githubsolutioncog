from redbot.core.commands import Cog, command, guild_only
from redbot.core import Config
from redbot.core import checks
from discord import Embed


class GithubSolution(Cog):
    """Posts a solution summary to a GitHub issue."""
    def __init__(self):
        self.config = Config.get_conf(self, identifier=9900990099, force_registration=True)
        default_guild = {
            "github_project": None,
            "github_token_var": None,
            "close_on_solution": False
        }
        self.config.register_guild(**default_guild)

    @command()
    @guild_only()
    @checks.admin_or_permissions(manage_roles=True)
    async def setautoclose(self, ctx, autoclose: bool = False):
        """
        Automatically close an issue when a solution is posted.
        """
        old_value = await self.config.guild(ctx.guild).close_on_solution()
        old_value = bool(old_value)
        await self.config.guild(ctx.guild).close_on_solution.set(autoclose)
        await ctx.send(f'`autoclose` set to {str(autoclose)} from {str(old_value)}')

    @command()
    @guild_only()
    @checks.is_owner()
    async def settokenvar(self, ctx, varname: str):
        """
        The environment variable name used to retrieve the GitHub token.
        Only the bot owner can set this value.
        """
        old_name = await self.config.guild(ctx.guild).github_token_var()
        await self.config.guild(ctx.guild).github_token_var.set(varname)
        await ctx.send(f'Value of `github_token_var` has changed from `{old_name}` to `{varname}`')

    @command()
    @guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    async def setproject(self, ctx, project: str):
        """
        Sets the GitHub project to use for this server.
        Should be in the format namespace/project
        Default is None.
        """
        old_project = await self.config.guild(ctx.guild).github_project()
        await self.config.guild(ctx.guild).github_project.set(project)
        await ctx.send(f'Value of `github_url` has changed from `{old_project}` to `{project}`')

    @command()
    async def solution(self, ctx, issue: int = None, *, summary: str = None):
        """
        Posts a solution summary to a GitHub issue.
        Example: [p]solution 123 The user did not try turning it off/on again.
        """
        success = await self.do_post(issue, summary, ctx)
        if success is None:
            await ctx.send('The token could not be read. Please double check your configuration.')
        else:
            embed = Embed(title=f'Solution to #{issue} posted!', colour=ctx.author.colour, url=success)
            embed.add_field(name='Summary', value=summary)
            embed.set_footer(text=f'Thanks, {ctx.author.name}!', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    async def do_post(self, issue, solution, ctx):
        text = [
            '**Solution**',
            f'{solution}',
            '<hr>',
            f'\n_This solution was posted by Discord user {ctx.author.name}._',
            f'_[View this message on Discord.]({ctx.message.jump_url})_'
        ]

        varname = await self.config.guild(ctx.guild).github_token_var()
        from os import environ
        from github3 import login
        token = environ.get(str(varname), None)
        if token:
            gh = login(token=token)
            repo = await self.config.guild(ctx.guild).github_project()
            iss = gh.issue(repo.split('/')[0], repo.split('/')[1], issue)
            response = iss.create_comment('\n'.join(text))
            return response.html_url
