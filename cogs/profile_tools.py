import os

import discord
from discord.ext import commands

from utils import backend_commands, checks, setup_helper, embed_generator, strings


def setup(bot):
    bot.add_cog(ProfileTools(bot))


class ProfileTools(commands.Cog, name='Profile Tools'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='publish', pass_context=True,
                      brief='Makes your profile viewable to others')
    @commands.dm_only()
    async def _publish(self, context: commands.Context):
        author: discord.User = context.author
        discord_id: int = author.id

        if not await checks.command_available(context.message, '!publish', published_profile_required=False):
            return

        profile_status = await backend_commands.get_value_by_discord_id(discord_id, 'status')
        if profile_status != backend_commands.ProfileStatus.PUBLISHED:
            setup_stage = await setup_helper.get_setup_stage(discord_id)
            if setup_stage == 8 or setup_stage == 0:
                old_status = profile_status
                await backend_commands.update_profile(discord_id,
                                                      'status',
                                                      backend_commands.ProfileStatus.PUBLISHED)

                embed = embed_generator.get_standard_embed('Your profile has been published and is now available!',
                                                           embed_generator.TYPE_SUCCESS,
                                                           'Profile published')
                await context.send(embed=embed)
                if old_status == backend_commands.ProfileStatus.NEW_SIGNUP_UNPUBLISHED:
                    embed = embed_generator.get_standard_embed(title='Start swiping!',
                                                               embed_message=strings.ProfileSetup.published_message,
                                                               embed_type=embed_generator.TYPE_MATCHBOT)
                    await context.send(embed=embed)
            else:
                embed = embed_generator.get_standard_embed(
                    'You can only `publish` your profile once you\'ve filled out all necessary information. '
                    'Follow the instructions provided by `!setup` first.',
                    embed_generator.TYPE_ERROR,
                    'Setup not complete')
                await context.send(embed=embed)
        else:
            embed = embed_generator.get_standard_embed('Your profile has already been `publish`ed. '
                                                       'You can use MatchBot\'s features freely. '
                                                       'If you wish to `unpublish` your profile, use `!unpublish`.',
                                                       embed_generator.TYPE_ERROR,
                                                       'Profile already published')
            await context.send(embed=embed)

    @commands.command(name='unpublish', pass_context=True,
                      brief='Hides your profile')
    @commands.dm_only()
    async def _unpublish(self, context: commands.Context):
        if not await checks.command_available(context.message, '!unpublish', published_profile_required=True):
            return
        await backend_commands.update_profile(context.author.id,
                                              'status',
                                              backend_commands.ProfileStatus.UNPUBLISHED)
        embed = embed_generator.get_standard_embed('Your profile has been unpublished '
                                                   'and is no longer visible in the queue.',
                                                   embed_generator.TYPE_SUCCESS,
                                                   'Profile unpublished')
        await context.send(embed=embed)

    @commands.command(name='delete-profile', pass_context=True,
                      brief='PERMANENTLY deletes your profile and all associated data')
    @commands.dm_only()
    async def _delete_profile(self, context: commands.Context, confirmation: str = ''):
        if not await checks.command_available(context.message, '!delete-profile', published_profile_required=False):
            return
        if confirmation.lower() == 'confirm':
            user_id = await backend_commands.get_user_id_by_discord_id(context.author.id)
            await backend_commands.delete_profile(user_id)
            await backend_commands.delete_matches(user_id)
            image_path = backend_commands.get_user_picture_path(user_id)
            if image_path is not None:
                os.remove(image_path)
            embed = embed_generator.get_standard_embed('Your profile and all associated data have been deleted. '
                                                       'We hope you enjoyed using MatchBot! 💖',
                                                       embed_generator.TYPE_SUCCESS,
                                                       'Profile deleted')
            await context.send(embed=embed)
        else:
            embed = embed_generator.get_standard_embed('This command will delete your profile, matches, '
                                                       'and all other data - forever! This action is non-reversible. '
                                                       'Any versions of your profile already sent to other users '
                                                       'will not be deleted. '
                                                       'If you want to hide your profile from others, '
                                                       'use `!unpublish` instead.\n'
                                                       'If you still wish to proceed, run `!delete-profile confirm`.',
                                                       embed_generator.TYPE_WARNING,
                                                       'Are you sure?')
            await context.send(embed=embed)
