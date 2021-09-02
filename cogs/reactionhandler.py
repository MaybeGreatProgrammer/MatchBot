import discord
from discord import Embed
from discord.ext import commands

from utils import backend_commands, strings, embed_generator, config, profile_viewer


def setup(bot):
    bot.add_cog(ReactionHandler(bot))


async def notify_user_of_match(message: discord.Message, other_user: discord.User):
    other_user_id = other_user.id
    other_user_name = await backend_commands.get_value_by_discord_id(other_user_id, 'full_name')
    other_user_mention = other_user.mention
    notification_message = strings.Swipe.mutual_match.format(user_name=other_user_name,
                                                             user_mention=other_user_mention)
    embed = discord.Embed(title='💘 Match found! 💘',
                          description=notification_message,
                          colour=discord.Color.magenta())

    await message.reply(embed=embed)


class ReactionHandler(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        bot_id = self.bot.user.id
        discord_id = payload.user_id
        message_id = payload.message_id
        partial_emoji: discord.PartialEmoji = payload.emoji
        emoji: str = partial_emoji.name
        if discord_id == bot_id:
            return
        if payload.guild_id is not None:
            if emoji.lower() == 'matchbot':
                channel: discord.TextChannel = await self.bot.fetch_channel(payload.channel_id)
                if channel.name.lower() == 'matchbot' or channel.name.lower() == 'welcome':
                    user_exists = await backend_commands.check_if_user_exists_by_discord_id(discord_id)
                    embed = embed_generator.get_standard_embed(title='Welcome to MatchBot!',
                                                               embed_message=strings.ProfileSetup.start_message,
                                                               embed_type=embed_generator.TYPE_MATCHBOT)

                    if not user_exists:
                        user = await self.bot.fetch_user(discord_id)
                        await user.send(embed=embed)
            return
        if emoji == config.yes_emoji or emoji == config.no_emoji:
            dm_channel: discord.DMChannel = await self.bot.fetch_channel(payload.channel_id)
            message: discord.Message = await dm_channel.fetch_message(message_id)

            if message.author.id != bot_id:
                return

            footer_text: str = message.embeds[0].footer.text
            if footer_text == Embed.Empty:
                return
            if 'Profile ID: {' not in footer_text:
                return

            secondary_user_id = footer_text[footer_text.find('{') + 1:footer_text.find('}')]
            secondary_user_discord_id = await backend_commands.get_discord_id_by_user_id(secondary_user_id)

            if secondary_user_discord_id is None:
                embed = embed_generator.get_standard_embed('The user you\'re interacting with has deleted '
                                                           'their profile, or their User ID is invalid.',
                                                           embed_generator.TYPE_ERROR,
                                                           'Profile not found')
                await dm_channel.send(embed=embed)
                return

            secondary_user = await self.bot.fetch_user(secondary_user_discord_id)
            primary_user = await self.bot.fetch_user(discord_id)
            primary_user_id = await backend_commands.get_user_id_by_discord_id(discord_id)

            if primary_user_id is None:
                embed = embed_generator.get_standard_embed('You need a profile to be able to '
                                                           '`swipe` on others. Create one with `!setup`.',
                                                           embed_generator.TYPE_ERROR,
                                                           'No profile')
                await dm_channel.send(embed=embed)
                return
            if primary_user_id == secondary_user_id:
                embed = embed_generator.get_standard_embed('Very clever, but sorry, you can\'t `swipe` on yourself. '
                                                           'You SHOULD still love yourself though! 💖',
                                                           embed_generator.TYPE_MATCHBOT,
                                                           'That\'s your own profile!')
                await dm_channel.send(embed=embed)
                return

            match_status: dict = await backend_commands.get_match_status(primary_user_id, secondary_user_id)

            if match_status.get('matched') == 1:
                embed = embed_generator.get_standard_embed(f'You\'ve already matched with {secondary_user.mention}, '
                                                           'so you can\'t change your mind.',
                                                           embed_generator.TYPE_ERROR,
                                                           'Already matched')
                await dm_channel.send(embed=embed)
                return

            emoji_meanings = {
                config.yes_emoji: 1,
                config.no_emoji: 0
            }
            reaction_meaning = emoji_meanings.get(emoji)

            reverse_match_status: dict = await backend_commands.get_match_status(secondary_user_id, primary_user_id)
            reverse_match_liked = reverse_match_status.get('liked')
            if reverse_match_liked == 1 and reaction_meaning == 1:
                mutual_match = 1
            else:
                mutual_match = 0

            if match_status.get('exists'):
                if match_status.get('liked') != reaction_meaning:
                    await backend_commands.update_match(primary_user_id, secondary_user_id,
                                                        'liked', reaction_meaning)
            else:
                await backend_commands.add_new_match(primary_user_id, secondary_user_id,
                                                     reaction_meaning, mutual_match)

            await backend_commands.update_match(primary_user_id, secondary_user_id, 'message_id', message_id)

            if mutual_match:
                if match_status.get('exists'):
                    await backend_commands.update_match(primary_user_id, secondary_user_id, 'matched', 1)
                await backend_commands.update_match(secondary_user_id, primary_user_id, 'matched', 1)

                primary_message = message

                secondary_message_id = await backend_commands.get_match_message_id(secondary_user_id,
                                                                                   primary_user_id)
                secondary_channel_id = await backend_commands.get_value_by_discord_id(secondary_user_discord_id,
                                                                                      'channel_id')
                secondary_channel: discord.DMChannel = await self.bot.fetch_channel(secondary_channel_id)
                secondary_message = await secondary_channel.fetch_message(secondary_message_id)

                await notify_user_of_match(primary_message, secondary_user)
                await notify_user_of_match(secondary_message, primary_user)

            if not match_status.get('exists'):
                profile_message: discord.Message = await profile_viewer.view_random_profile(self.bot, primary_user)
                if profile_message is not None:
                    await profile_message.add_reaction(config.yes_emoji)
                    await profile_message.add_reaction(config.no_emoji)
