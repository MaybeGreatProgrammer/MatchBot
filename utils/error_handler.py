import inspect

from discord.ext import commands

from utils import embed_generator


async def handle_error(context: commands.Context, error: commands.CommandError):
    error = getattr(error, 'original', error)

    if isinstance(error, commands.MissingRequiredArgument):
        parameter: inspect.Parameter = error.param
        embed_message = f'Command is missing required argument `{parameter.name}`.'
        await send_error_message(context, embed_message, 'Missing argument')
    elif isinstance(error, commands.UserNotFound):
        embed_message = 'The specified user could not be found.'
        await send_error_message(context, embed_message, 'User not found')
    elif isinstance(error, commands.NotOwner):
        embed_message = 'This command can only be used by the bot developer.'
        await send_error_message(context, embed_message, 'Not authorized')
    elif isinstance(error, commands.PrivateMessageOnly):
        embed_message = 'This command needs to be sent to the bot through a Direct Message.\n' \
                        'If you haven\'t yet created a profile, the `!start` command will guide you through the ' \
                        'setup process.'
        await send_error_message(context, embed_message, 'DM required')
    elif isinstance(error, commands.UnexpectedQuoteError):
        embed_message = 'Unexpected quotation mark (") found in command. ' \
                        'Please remove any quotation marks and try again.'
        await send_error_message(context, embed_message, 'Unexpected quotation mark')
    elif isinstance(error, commands.CommandNotFound):
        await context.message.add_reaction('🤨')
    else:
        embed_message = f'Unexpected exception occurred:\n```{type(error)}``````{str(error)}```'
        await send_error_message(context, embed_message)


async def send_error_message(context: commands.Context, error_message: str, title: str = None):
    embed = embed_generator.get_standard_embed(error_message, embed_generator.TYPE_ERROR, title)
    await context.send(embed=embed)
