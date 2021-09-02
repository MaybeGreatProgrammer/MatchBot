import re
import uuid

import discord
from discord.ext import commands

from utils import allowlist, backend_commands, embed_generator, strings, checks, error_handler, setup_helper


def setup(bot):
    bot.add_cog(ProfileSetup(bot))


class ProfileSetup(commands.Cog, name='Profile Setup'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='start', pass_context=True,
                      brief='Shows the intro message')
    async def _start(self, context: commands.Context):
        author: discord.User = context.author
        discord_id: int = author.id
        user_exists = await backend_commands.check_if_user_exists_by_discord_id(discord_id)

        embed = embed_generator.get_standard_embed(title='Welcome to MatchBot!',
                                                   embed_message=strings.ProfileSetup.start_message,
                                                   embed_type=embed_generator.TYPE_MATCHBOT)

        if not user_exists:
            await author.send(embed=embed)
            await context.message.add_reaction('✅')

    @commands.command(name='setup', pass_context=True,
                      brief='Begins account setup')
    @commands.dm_only()
    async def _setup(self, context: commands.Context):
        author: discord.User = context.author
        discord_id: int = author.id
        user_exists = await backend_commands.check_if_user_exists_by_discord_id(discord_id)
        if not user_exists:
            if discord_id in allowlist.allowlist_cache:
                user_id = str(uuid.uuid4())
                await backend_commands.create_profile(user_id, discord_id, context.channel.id)
                embed = embed_generator.get_standard_embed('Your profile and Discord ID '
                                                           'have been registered.',
                                                           embed_generator.TYPE_SUCCESS,
                                                           'Profile created')
                await context.send(embed=embed)
                await setup_helper.next_setup_step(context.message, discord_id)
            else:
                embed = embed_generator.get_standard_embed(strings.ProfileSetup.not_on_allowlist,
                                                           embed_generator.TYPE_ERROR,
                                                           'Access denied')
                await context.send(embed=embed)
        else:
            profile_status = await backend_commands.get_value_by_discord_id(discord_id, 'status')
            if profile_status == backend_commands.ProfileStatus.NEW_SIGNUP_UNPUBLISHED:
                await setup_helper.next_setup_step(context.message, discord_id)
            else:
                embed = embed_generator.get_standard_embed(strings.ProfileSetup.edit_profile,
                                                           embed_generator.TYPE_INFO,
                                                           'Profile editing')
                embed.add_field(name='Name', value=strings.Help.set_name)
                embed.add_field(name='Class', value=strings.Help.set_class)
                embed.add_field(name='Age', value=strings.Help.set_age)
                embed.add_field(name='Gender', value=strings.Help.set_gender)
                embed.add_field(name='Gender Preference', value=strings.Help.set_preference)
                embed.add_field(name='Bio', value=strings.Help.set_bio)
                embed.add_field(name='Profile Picture', value=strings.Help.set_pic, inline=False)
                await context.send(embed=embed)

    @commands.command(name='set', pass_context=True,
                      brief='Changes parts of your profile')
    @commands.dm_only()
    async def _set(self, context: commands.Context, element: str, *, content: str):
        author: discord.User = context.author
        discord_id: int = author.id
        element = element.lower()

        if not await checks.command_available(context.message, '!set', published_profile_required=False):
            return

        if element == 'name':
            value = content[:50]
            await backend_commands.update_profile(discord_id, 'full_name', value)
            embed = embed_generator.get_standard_embed(f'Your name has been set to `{value}`.',
                                                       embed_generator.TYPE_SUCCESS,
                                                       'Name set')
            await context.send(embed=embed)
        elif element == 'class':
            value = content[:6]
            await backend_commands.update_profile(discord_id, 'class', value)
            embed = embed_generator.get_standard_embed(f'Your class has been set to `{value}`.',
                                                       embed_generator.TYPE_SUCCESS,
                                                       'Class set')
            await context.send(embed=embed)
        elif element == 'age':
            digits = re.findall("\\d+", content)
            if len(digits) > 0:
                age = int(digits[0])
                if 20 > age > 14:
                    await backend_commands.update_profile(discord_id, 'age', age)
                    embed = embed_generator.get_standard_embed(f'Your age has been set to `{age}`.',
                                                               embed_generator.TYPE_SUCCESS,
                                                               'Age set')
                    await context.send(embed=embed)
                else:
                    embed = embed_generator.get_standard_embed(f'`{age}` is not between 15 and 19. '
                                                               f'Please set an appropriate age to proceed.',
                                                               embed_generator.TYPE_ERROR,
                                                               'Inappropriate age')
                    await context.send(embed=embed)
                    return
            else:
                embed = embed_generator.get_standard_embed(f'`{content}` is not a number.',
                                                           embed_generator.TYPE_ERROR,
                                                           'Invalid age')
                await context.send(embed=embed)
                return
        elif element == 'gender':
            if content.upper().startswith(('M', 'F', 'O')):

                gender_dict = {
                    'M': 'Male',
                    'F': 'Female',
                    'O': 'Other'
                }

                value = content.upper()[:1]
                await backend_commands.update_profile(discord_id, 'gender', value)
                full_gender_name = gender_dict.get(value)

                if ' ' in content:
                    custom_gender = content[content.find(' ') + 1:]
                    custom_gender = custom_gender[:25]
                    await backend_commands.update_profile(discord_id, 'custom_gender', custom_gender)
                    embed_message = f'Your gender has been set to `{full_gender_name} ({custom_gender})`.'
                else:
                    await backend_commands.update_profile(discord_id, 'custom_gender', None)
                    embed_message = f'Your gender has been set to `{full_gender_name}`.'

                embed = embed_generator.get_standard_embed(embed_message,
                                                           embed_generator.TYPE_SUCCESS,
                                                           'Gender set')
                await context.send(embed=embed)
            else:
                embed = embed_generator.get_standard_embed(f'The gender `{content}` '
                                                           f'is not available in our system, please select either '
                                                           f'`Male`, `Female`, or `Other` to proceed.',
                                                           embed_generator.TYPE_ERROR,
                                                           'Gender not supported')
                await context.send(embed=embed)
                return
        elif element == 'preference':
            content_upper = content.upper()
            final_preference = ''
            final_preference_full = []
            if 'M' in content_upper:
                final_preference += 'M'
                final_preference_full.append('Male')
            if 'F' in content_upper:
                final_preference += 'F'
                final_preference_full.append('Female')
            if 'O' in content_upper:
                final_preference += 'O'
                final_preference_full.append('Other')

            if not final_preference == '':
                embed_preference_string = '`' + '`, `'.join(final_preference_full) + '`'
                await backend_commands.update_profile(discord_id, 'gender_preference', final_preference)
                embed = embed_generator.get_standard_embed(f'Your gender preference has been set to '
                                                           f'{embed_preference_string}.',
                                                           embed_generator.TYPE_SUCCESS,
                                                           'Gender Preference set')
                await context.send(embed=embed)
            else:
                embed = embed_generator.get_standard_embed('Your gender preference must contain at least one of '
                                                           'the following letters: `M`, `F`, or `O`',
                                                           embed_generator.TYPE_ERROR,
                                                           'Gender Preference not supported')
                await context.send(embed=embed)
                return
        elif element == 'bio':
            value = content[:500]
            await backend_commands.update_profile(discord_id, 'bio', value)
            embed = embed_generator.get_standard_embed(f'Your bio has been set to```\n{value}```',
                                                       embed_generator.TYPE_SUCCESS,
                                                       'Bio set')
            await context.send(embed=embed)
        else:
            embed = embed_generator.get_standard_embed(
                f'Sorry, `{element}` is not a valid element of your profile. '
                'The `!set` command can edit your profile\'s '
                '`name`, `class`, `gender`, `preference`, or `bio`.',
                embed_generator.TYPE_ERROR,
                'Invalid profile element')
            await context.send(embed=embed)
            return
        profile_status = await backend_commands.get_value_by_discord_id(discord_id, 'status')
        if profile_status == backend_commands.ProfileStatus.NEW_SIGNUP_UNPUBLISHED:
            await setup_helper.next_setup_step(context.message, discord_id)

    @_set.error
    async def set_error(self, context: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            embed_message = f'The `!set` command requires you to specify ' \
                            f'the `element` of your profile you\'re editing ' \
                            f'and the `value` you\'d like to set that element to.\n' \
                            f'Full syntax: `!set <element> <value>`'
            embed = embed_generator.get_standard_embed(embed_message,
                                                       embed_generator.TYPE_ERROR,
                                                       'Missing argument')
            await context.send(embed=embed)
        else:
            await error_handler.handle_error(context, error)
