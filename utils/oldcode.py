import discord

from utils import backend_commands, embed_generator, strings


async def next_setup_step(message: discord.Message, discord_id: int):
    if not await backend_commands.check_if_profile_has_column_by_discord_id(discord_id, 'full_name'):
        embed = embed_generator.get_standard_embed(strings.Help.set_name,
                                                   embed_generator.TYPE_SETUP,
                                                   'Step 1/6: Name')
        await message.channel.send(embed=embed)
        return
    elif not await backend_commands.check_if_profile_has_column_by_discord_id(discord_id, 'class'):
        embed = embed_generator.get_standard_embed(strings.Help.set_class,
                                                   embed_generator.TYPE_SETUP,
                                                   'Step 2/6: Class')
        await message.channel.send(embed=embed)
        return
    elif not await backend_commands.check_if_profile_has_column_by_discord_id(discord_id, 'gender'):
        embed = embed_generator.get_standard_embed(strings.Help.set_gender,
                                                   embed_generator.TYPE_SETUP,
                                                   'Step 3/6: Gender')
        await message.channel.send(embed=embed)
        return
    elif not await backend_commands.check_if_profile_has_column_by_discord_id(discord_id, 'gender_preference'):
        embed = embed_generator.get_standard_embed(strings.Help.set_preference,
                                                   embed_generator.TYPE_SETUP,
                                                   'Step 4/6: Gender preference')
        await message.channel.send(embed=embed)
        return
    elif not await backend_commands.check_if_profile_has_column_by_discord_id(discord_id, 'bio'):
        embed = embed_generator.get_standard_embed(strings.Help.set_bio,
                                                   embed_generator.TYPE_SETUP,
                                                   'Step 5/6: Bio')
        await message.channel.send(embed=embed)
        return
    user_id = await backend_commands.get_user_id_by_discord_id(discord_id)
    if backend_commands.get_user_picture_path(user_id) is not None:
        embed = discord.Embed(title='💖 Ready to start!',
                              description=strings.ProfileSetup.ready_to_publish,
                              colour=discord.Color.purple())
        await message.channel.send(embed=embed)
        return
    embed = embed_generator.get_standard_embed(strings.Help.set_pic,
                                               embed_generator.TYPE_SETUP,
                                               'Step 6/6: Profile picture')
    await message.channel.send(embed=embed)


preference_string = ''
user_ida = ''
user_gender = ''
# Don't question the words of SQLJesus
# It Just Works!
sql_get_unseen_profile_ids = f"""SELECT DISTINCT user_id FROM (
                                        SELECT user_id FROM profiles
                                        WHERE NOT user_id = "{user_ida}"
                                        AND gender IN ({preference_string})
                                        AND gender_preference LIKE "%{user_gender}%"
                                        AND status = "1"
                                    )
                                    WHERE NOT EXISTS (
                                        SELECT 1
                                        FROM (
                                            SELECT DISTINCT secondary_user_id FROM matches
                                            WHERE primary_user_id = "{user_ida}"
                                        )
                                        WHERE secondary_user_id = user_id
                                    ); """
