import discord

TYPE_INFO = 0
TYPE_SUCCESS = 1
TYPE_ERROR = 2
TYPE_WARNING = 3
TYPE_PROCESSING = 4
TYPE_SETUP = 5
TYPE_MATCHBOT = 6

name_dict = {
    TYPE_INFO: 'ℹ Info',
    TYPE_SUCCESS: '✅ Success',
    TYPE_ERROR: '❌ Error',
    TYPE_WARNING: '⚠ Warning',
    TYPE_PROCESSING: '⚙ Processing',
    TYPE_SETUP: '⚙ Setup',
    TYPE_MATCHBOT: '💖 MatchBot'
}

color_dict = {
    TYPE_INFO: discord.Color.dark_blue(),
    TYPE_SUCCESS: discord.Color.green(),
    TYPE_ERROR: discord.Color.red(),
    TYPE_WARNING: discord.Color.orange(),
    TYPE_PROCESSING: discord.Color.gold(),
    TYPE_SETUP: discord.Color.blurple(),
    TYPE_MATCHBOT: discord.Color.purple()
}


def get_standard_embed(embed_message: str, embed_type: int, title: str = None, show_emoji: bool = True):
    embed_default_title = name_dict.get(embed_type)
    embed_emoji = embed_default_title[:1]

    if title is None:
        embed_title = embed_default_title
    else:
        if show_emoji:
            embed_title = f'{embed_emoji} {title}'
        else:
            embed_title = title
    embed_color = color_dict.get(embed_type)

    return discord.Embed(title=embed_title, colour=embed_color, description=embed_message)


class Errors:
    @staticmethod
    def get_no_profile_embed(command_used: str):
        embed = get_standard_embed(f'The `{command_used}` command only works if you have a profile. '
                                   f'Use `!setup` to create a profile first.',
                                   TYPE_ERROR,
                                   'Profile not found')
        return embed

    @staticmethod
    def get_not_published_embed(command_used: str):
        embed = get_standard_embed(f'The `{command_used}` command only works after profile setup is complete. '
                                   f'Follow the instructions provided by `!setup` first, '
                                   f'then `!publish` your profile.',
                                   TYPE_ERROR,
                                   'Profile not published')
        return embed
