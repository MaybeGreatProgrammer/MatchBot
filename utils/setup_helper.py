import discord

from utils import backend_commands, embed_generator, strings


async def get_setup_stage(discord_id: int):
    profile_status = await backend_commands.get_value_by_discord_id(discord_id, 'status')
    if profile_status == backend_commands.ProfileStatus.NEW_SIGNUP_UNPUBLISHED:
        if not await backend_commands.check_if_profile_has_column_by_discord_id(discord_id, 'full_name'):
            return 1
        elif not await backend_commands.check_if_profile_has_column_by_discord_id(discord_id, 'class'):
            return 2
        elif not await backend_commands.check_if_profile_has_column_by_discord_id(discord_id, 'age'):
            return 3
        elif not await backend_commands.check_if_profile_has_column_by_discord_id(discord_id, 'gender'):
            return 4
        elif not await backend_commands.check_if_profile_has_column_by_discord_id(discord_id, 'gender_preference'):
            return 5
        elif not await backend_commands.check_if_profile_has_column_by_discord_id(discord_id, 'bio'):
            return 6
        user_id = await backend_commands.get_user_id_by_discord_id(discord_id)
        if backend_commands.get_user_picture_path(user_id) is not None:
            return 8
        return 7
    else:
        return 0


async def next_setup_step(message: discord.Message, discord_id: int):
    setup_stage = await get_setup_stage(discord_id)
    if setup_stage == 1:
        embed = embed_generator.get_standard_embed(strings.Help.set_name,
                                                   embed_generator.TYPE_SETUP,
                                                   'Step 1/7: Name')
    elif setup_stage == 2:
        embed = embed_generator.get_standard_embed(strings.Help.set_class,
                                                   embed_generator.TYPE_SETUP,
                                                   'Step 2/7: Class')
    elif setup_stage == 3:
        embed = embed_generator.get_standard_embed(strings.Help.set_age,
                                                   embed_generator.TYPE_SETUP,
                                                   'Step 3/7: Age')
    elif setup_stage == 4:
        embed = embed_generator.get_standard_embed(strings.Help.set_gender,
                                                   embed_generator.TYPE_SETUP,
                                                   'Step 4/7: Gender')
    elif setup_stage == 5:
        embed = embed_generator.get_standard_embed(strings.Help.set_preference,
                                                   embed_generator.TYPE_SETUP,
                                                   'Step 5/7: Gender preference')
    elif setup_stage == 6:
        embed = embed_generator.get_standard_embed(strings.Help.set_bio,
                                                   embed_generator.TYPE_SETUP,
                                                   'Step 6/7: Bio')
    elif setup_stage == 7:
        embed = embed_generator.get_standard_embed(strings.Help.set_pic,
                                                   embed_generator.TYPE_SETUP,
                                                   'Step 7/7: Profile picture')
    elif setup_stage == 8:
        embed = embed_generator.get_standard_embed(title='Ready to start!',
                                                   embed_message=strings.ProfileSetup.ready_to_publish,
                                                   embed_type=embed_generator.TYPE_MATCHBOT)
    else:
        return
    await message.channel.send(embed=embed)
