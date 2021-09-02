from discord.ext import commands

from utils import strings, embed_generator, error_handler

set_dict = {
    'name': strings.Help.set_name,
    'class': strings.Help.set_class,
    'age': strings.Help.set_age,
    'gender': strings.Help.set_gender,
    'preference': strings.Help.set_preference,
    'bio': strings.Help.set_bio,
    'picture': strings.Help.set_pic
}


def setup(bot):
    bot.add_cog(Info(bot))


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(name='info', pass_context=True,
                      brief='Provides information on all the elements of your profile')
    async def _info(self, context: commands.Context, item: str):
        item = item.lower()
        if item in set_dict.keys():
            embed = embed_generator.get_standard_embed(set_dict.get(item),
                                                       embed_generator.TYPE_INFO,
                                                       f'Setting your {item}')
            await context.send(embed=embed)

    @_info.error
    async def info_error(self, context: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            valid_set_info = '`' + '`, `'.join(set_dict.keys()) + '`'
            embed_message = f'The `!info` command requires you to specify ' \
                            f'the `item` you\'re trying to find info about. ' \
                            f'This can be one of the following: \n' \
                            f'{valid_set_info}\n' \
                            f'Full syntax: `!info <item>`'
            embed = embed_generator.get_standard_embed(embed_message,
                                                       embed_generator.TYPE_ERROR,
                                                       'Missing argument')
            await context.send(embed=embed)
        else:
            await error_handler.handle_error(context, error)
