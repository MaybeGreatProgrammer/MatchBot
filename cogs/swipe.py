import discord
from discord.ext import commands

from utils import backend_commands, embed_generator, config, checks, lookup, profile_viewer


def setup(bot):
    bot.add_cog(Swipe(bot))


class Swipe(commands.Cog, name='Profile Browsing'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='swipe', pass_context=True,
                      brief='Shows a random compatible profile')
    @commands.dm_only()
    async def _swipe(self, context: commands.Context):
        if not await checks.command_available(context.message, '!swipe', published_profile_required=True):
            return
        profile_message: discord.Message = await profile_viewer.view_random_profile(self.bot, context.author)
        if profile_message is not None:
            await profile_message.add_reaction(config.yes_emoji)
            await profile_message.add_reaction(config.no_emoji)

    @commands.command(name='view-profile', pass_context=True,
                      brief='Shows either your own profile or a specified user\'s')
    async def _view_profile(self, context: commands.Context, *, search: str = None):
        author_id = context.author.id
        if search is None:
            user_id = await backend_commands.get_user_id_by_discord_id(author_id)
            if user_id is None:
                embed = embed_generator.get_standard_embed('To view your own profile, you first need to set it up. '
                                                           'Use `!setup`.',
                                                           embed_generator.TYPE_ERROR,
                                                           'Profile doesn\'t exist')
                await context.send(embed=embed)
                return
        else:
            if author_id != config.owner_id:
                embed = embed_generator.get_standard_embed('You aren\'t allowed to view other people\'s profiles '
                                                           'through `!view-profile <name>`. '
                                                           'You can view your own profile with `!view-profile`.',
                                                           embed_generator.TYPE_ERROR,
                                                           'Access denied')
                await context.send(embed=embed)
                return
            user_id = await lookup.look_up(context, search)
            if user_id is None:
                return

        profile_values = await backend_commands.get_whole_profile_by_user_id(user_id)

        await profile_viewer.view_profile(self.bot, profile_values, channel=context.channel)
