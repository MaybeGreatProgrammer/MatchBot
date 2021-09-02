import discord

from utils import backend_commands, embed_generator


async def command_available(message: discord.Message, command: str, published_profile_required: bool):
    discord_id = message.author.id
    user_exists = await backend_commands.check_if_user_exists_by_discord_id(discord_id)
    if user_exists:
        if published_profile_required:
            profile_status = await backend_commands.get_value_by_discord_id(discord_id, 'status')
            if profile_status != backend_commands.ProfileStatus.PUBLISHED:
                await message.channel.send(embed=embed_generator.Errors.get_not_published_embed(command))
                return False
            else:
                return True
        else:
            return True
    else:
        await message.channel.send(embed=embed_generator.Errors.get_no_profile_embed(command))
        return False
