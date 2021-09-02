import os
from pathlib import Path

import aiohttp
import discord
from discord.ext import commands

from utils import backend_commands, embed_generator, setup_helper


def setup(bot):
    bot.add_cog(MessageHandler(bot))


class MessageHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        author: discord.User = message.author
        discord_id: int = author.id
        if author == self.bot.user:
            return
        if isinstance(message.channel, discord.DMChannel):
            attachments: list = message.attachments
            if len(attachments) > 0:
                picture_extensions = ['.jpg', '.jpeg', '.png']
                attachment: discord.Attachment = message.attachments[0]
                url = attachment.url
                filename = attachment.filename
                for extension in picture_extensions:
                    if str(url).lower().endswith(extension):
                        user_exists = await backend_commands.check_if_user_exists_by_discord_id(discord_id)
                        if user_exists:
                            async with aiohttp.ClientSession() as session:
                                async with session.get(url) as response:
                                    if response.status == 200:
                                        image: bytes = await response.read()
                                        # Discord has an 8MB size limit for normal users
                                        if len(image) < 8000000:
                                            user_id = await backend_commands.get_user_id_by_discord_id(discord_id)
                                            Path(f".{os.sep}img").mkdir(parents=True, exist_ok=True)

                                            # Delete old image
                                            old_image_path = backend_commands.get_user_picture_path(user_id)
                                            if old_image_path is not None:
                                                os.remove(old_image_path)

                                            file_path = f'.{os.sep}img{os.sep}{user_id}{extension}'
                                            with open(file_path, 'wb+') as file:
                                                file.write(image)
                                                embed_message = f'The image `{filename}` ' \
                                                                f'has been uploaded to your profile.'
                                                embed = embed_generator.get_standard_embed(embed_message,
                                                                                           embed_generator.TYPE_SUCCESS,
                                                                                           'Image uploaded')
                                                await message.channel.send(embed=embed)

                                                await setup_helper.next_setup_step(message, discord_id)
                                        else:
                                            embed_message = 'Your image takes up too much space. ' \
                                                            'The maximum file size for a profile image is ' \
                                                            '`8 Megabytes`.'
                                            embed = embed_generator.get_standard_embed(embed_message,
                                                                                       embed_generator.TYPE_ERROR,
                                                                                       'Image too large')
                                            await message.channel.send(embed=embed)
                                    else:
                                        embed_message = 'We couldn\'t download your image from Discord\'s servers. ' \
                                                        'Please try again later.'
                                        embed = embed_generator.get_standard_embed(embed_message,
                                                                                   embed_generator.TYPE_ERROR,
                                                                                   'Network error')
                                        await message.channel.send(embed=embed)
                        else:
                            embed = embed_generator.get_standard_embed(
                                'You can only upload profile images if you have a profile. '
                                'Use `!setup` to create a profile first.',
                                embed_generator.TYPE_ERROR,
                                'Profile not found')
                            await message.channel.send(embed=embed)
