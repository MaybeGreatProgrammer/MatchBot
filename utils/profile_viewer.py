from random import randrange

import discord
from discord.ext import commands

from utils import backend_commands, strings


async def view_profile(bot: commands.Bot, profile_values: dict,
                       primary_user: discord.User = None,
                       channel: discord.TextChannel = None):

    if primary_user is not None:
        channel = primary_user

    user: discord.User = await bot.fetch_user(profile_values.get('discord_id'))
    user_avatar_url = user.avatar_url

    gender_dict = {
        'M': 'Male',
        'F': 'Female',
        'O': 'Other'
    }

    user_id = profile_values.get('user_id')
    user_name = profile_values.get('full_name')
    user_age = profile_values.get('age')
    user_class = profile_values.get('class')
    user_gender = profile_values.get('gender')
    user_custom_gender = profile_values.get('custom_gender')
    user_bio = profile_values.get('bio')

    if user_custom_gender == 'None' or user_custom_gender == '':
        user_gender_final = gender_dict.get(user_gender)
    else:
        user_gender_final = f'{gender_dict.get(user_gender)} ({user_custom_gender})'

    embed: discord.Embed = discord.Embed(title=user_name,
                                         colour=discord.Color.from_rgb(255, 255, 255))

    file = None
    file_path, image_extension = backend_commands.get_user_picture_path(user_id, return_extension=True)
    if file_path is not None:
        file = discord.File(file_path, filename=f'image{image_extension}')
        embed.set_image(url=f'attachment://image{image_extension}')

    embed.add_field(name='Class', value=user_class)
    embed.add_field(name='Age', value=user_age)
    embed.add_field(name='Gender', value=user_gender_final)

    embed.add_field(name='Bio', value=user_bio, inline=False)

    embed.set_author(name=str(user),
                     icon_url=user_avatar_url)

    formatted_user_id = '{' + user_id + '}'
    embed.set_footer(text=f'Profile ID: {formatted_user_id}')

    return await channel.send(embed=embed, file=file)


async def view_random_profile(bot: commands.Bot, primary_user: discord.User):
    available_profiles = await backend_commands.get_unseen_profile_ids_by_discord_id(primary_user.id)
    if available_profiles is None:
        user_count = await backend_commands.get_profile_count()

        embed = discord.Embed(title='😢 No more compatible profiles',
                              description=strings.Swipe.no_compatible_profiles.format(user_count=user_count),
                              colour=discord.Color.blue())
        await primary_user.send(embed=embed)
        return

    random_index = randrange(len(available_profiles))
    random_profile = available_profiles[random_index]
    profile_values = await backend_commands.get_whole_profile_by_user_id(random_profile)

    return await view_profile(bot, profile_values, primary_user=primary_user)
