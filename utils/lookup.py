from discord.ext import commands

from utils import embed_generator, backend_commands


async def look_up(context: commands.Context, search: str):
    if '{' in search:
        user_id = search[search.find('{') + 1:search.find('}')]
    elif '@' in search:
        search = search.strip('<@!>')
        try:
            user_id = await backend_commands.get_user_id_by_discord_id(int(search))
        except ValueError:
            embed = embed_generator.get_standard_embed('Couldn\'t convert that Discord mention to a user ID.',
                                                       embed_generator.TYPE_ERROR,
                                                       'Conversion failed')
            await context.send(embed=embed)
            return
        if user_id is None:
            embed = embed_generator.get_standard_embed('That Discord user doesn\'t appear to be in our database.',
                                                       embed_generator.TYPE_ERROR,
                                                       'Discord ID not found')
            await context.send(embed=embed)
            return
    else:
        user_id = await backend_commands.get_user_id_by_name(search)
    if user_id is None:
        embed = embed_generator.get_standard_embed('That name doesn\'t appear to be in our database.',
                                                   embed_generator.TYPE_ERROR,
                                                   'Name not found')
        await context.send(embed=embed)
        return

    user_exists = await backend_commands.check_if_user_exists_by_user_id(user_id)
    if user_exists:
        return user_id
    else:
        embed = embed_generator.get_standard_embed('That User ID doesn\'t appear to be in our database.',
                                                   embed_generator.TYPE_ERROR,
                                                   'User ID not found')
        await context.send(embed=embed)
        return
