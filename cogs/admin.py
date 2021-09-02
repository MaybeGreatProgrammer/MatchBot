import os

import discord
from utils import embed_generator, allowlist, backend_commands, lookup, config
from discord.ext import commands


def setup(bot):
    bot.add_cog(Admin(bot))


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='allow', pass_context=True,
                      brief='Adds a user to the allowlist')
    @commands.is_owner()
    async def _allow(self, context: commands.Context, user: discord.User):
        user_id = user.id
        if user_id in allowlist.allowlist_cache:
            embed = embed_generator.get_standard_embed(f'User {user.mention} is already on the allowlist.',
                                                       embed_generator.TYPE_WARNING,
                                                       'User already on allowlist')
            await context.send(embed=embed)
            return

        allowlist.add(user_id)
        allowlist.commit()

        embed = embed_generator.get_standard_embed(f'User {user.mention} has been added to the allowlist.',
                                                   embed_generator.TYPE_SUCCESS,
                                                   'User added')
        await context.send(embed=embed)

    @commands.command(name='unallow', pass_context=True,
                      brief='Removes a user from the allowlist')
    @commands.is_owner()
    async def _unallow(self, context: commands.Context, user: discord.User):
        user_id = user.id
        if user_id not in allowlist.allowlist_cache:
            embed = embed_generator.get_standard_embed(f'User {user.mention} is not on the allowlist.',
                                                       embed_generator.TYPE_WARNING,
                                                       'User not on allowlist')
            await context.send(embed=embed)
            return

        allowlist.remove(user_id)
        allowlist.commit()

        embed = embed_generator.get_standard_embed(f'User {user.mention} has been removed to the allowlist.',
                                                   embed_generator.TYPE_SUCCESS,
                                                   'User removed')
        await context.send(embed=embed)

    @commands.command(name='allow-all', pass_context=True,
                      brief='Adds all users in the channel to the allowlist')
    @commands.is_owner()
    async def _allow_all(self, context: commands.Context):
        current_allowlist = allowlist.allowlist_cache
        channel: discord.TextChannel = context.channel
        channel_members = channel.members
        added_members = []
        processing_embed_message = f'Adding all users in channel `{channel.name}` to allowlist...'
        processing_embed = embed_generator.get_standard_embed(processing_embed_message,
                                                              embed_generator.TYPE_PROCESSING,
                                                              'Adding users')
        message = await context.send(embed=processing_embed)

        for member in channel_members:
            if member.id not in current_allowlist:
                member: discord.Member
                allowlist.add(member.id)
                added_members.append(member.display_name)

        if len(added_members) > 0:
            allowlist.commit()
            added_members_string = '\n'.join(added_members)
            if len(added_members_string) < 1000:
                embed_message = f'Added `{len(added_members)}` users to the allowlist:\n```{added_members_string}```'
            else:
                embed_message = f'Added `{len(added_members)}` users to the allowlist.'
            embed = embed_generator.get_standard_embed(embed_message,
                                                       embed_generator.TYPE_SUCCESS,
                                                       'Users added')
            await message.edit(embed=embed)
        else:
            embed_message = f'All users in `{channel.name}` are already on the allowlist.'
            embed = embed_generator.get_standard_embed(embed_message,
                                                       embed_generator.TYPE_WARNING,
                                                       'No new users added')
            await message.edit(embed=embed)

    @commands.command(name='unallow-all', pass_context=True,
                      brief='Clears the allowlist')
    @commands.is_owner()
    async def _unallow_all(self, context: commands.Context):
        allowlist_length = len(allowlist.allowlist_cache)
        allowlist.clear()
        allowlist.commit()

        embed = embed_generator.get_standard_embed(f'Removed `{allowlist_length}` users from the allowlist.',
                                                   embed_generator.TYPE_SUCCESS,
                                                   'Allowlist cleared')
        await context.send(embed=embed)

    @commands.command(name='create-default-tables', pass_context=True,
                      brief='Adds the default tables to the database')
    @commands.is_owner()
    async def _create_default_tables(self, context: commands.Context):
        await backend_commands.create_default_tables()
        await context.send(embed=embed_generator.get_standard_embed('Created default tables in database.',
                                                                    embed_generator.TYPE_SUCCESS,
                                                                    'Tables created'))

    @commands.command(name='del-acc', pass_context=True,
                      brief='Deletes a user\'s account')
    @commands.is_owner()
    async def _del_acc(self, context: commands.Context, search: str):
        user_id = await lookup.look_up(context, search)
        if user_id is None:
            return
        await backend_commands.delete_profile(user_id)
        await backend_commands.delete_matches(user_id)
        image_path = backend_commands.get_user_picture_path(user_id)
        if image_path is not None:
            os.remove(image_path)
        await context.send(embed=embed_generator.get_standard_embed(f'User with ID {user_id} deleted.',
                                                                    embed_generator.TYPE_SUCCESS,
                                                                    'User deleted'))

    @commands.command(name='backup',
                      brief='Backs up the entire database and allowlist')
    @commands.is_owner()
    async def _backup(self, context: commands.Context):
        db_path = config.db_path
        if os.path.isfile(db_path):
            file = discord.File(db_path)
            await context.send(file=file)
        else:
            embed = embed_generator.get_standard_embed('The bot couldn\'t find the database file. '
                                                       'That can\'t be good.',
                                                       embed_generator.TYPE_ERROR,
                                                       'Database not found')
            await context.send(embed=embed)

        allowlist_path = config.allowlist_path
        if os.path.isfile(allowlist_path):
            file = discord.File(allowlist_path)
            await context.send(file=file)
        else:
            embed = embed_generator.get_standard_embed('The bot couldn\'t find the allowlist file. '
                                                       'That can\'t be good either.',
                                                       embed_generator.TYPE_ERROR,
                                                       'Allowlist not found')
            await context.send(embed=embed)

    @commands.command(name='id',
                      brief='Returns a user\'s Discord ID')
    @commands.is_owner()
    async def _id(self, context: commands.Context, user: discord.User):
        user_name = user.name
        user_id = user.id
        embed = embed_generator.get_standard_embed(f'{user.mention}\'s Discord ID is: ```{user_id}```',
                                                   embed_generator.TYPE_SUCCESS,
                                                   f'{user_name}\'s ID')
        await context.send(embed=embed)
