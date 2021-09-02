import os

from utils import sql, config

db_path = config.db_path
profiles_table = config.profiles_table
matches_table = config.matches_table


async def create_default_tables():
    sql_create_profiles_table = """ CREATE TABLE IF NOT EXISTS profiles (
                                        user_id text PRIMARY KEY,
                                        discord_id integer NOT NULL,
                                        full_name text,
                                        age integer,
                                        gender text,
                                        custom_gender text,
                                        gender_preference text,
                                        class text,
                                        bio text,
                                        status integer,
                                        channel_id integer
                                    ); """
    await sql.execute(sql_create_profiles_table)

    sql_create_matches_table = """  CREATE TABLE IF NOT EXISTS matches (
                                        primary_user_id text,
                                        secondary_user_id text,
                                        liked integer,
                                        matched integer,
                                        message_id integer,
                                        CONSTRAINT pk_match PRIMARY KEY (primary_user_id, secondary_user_id),
                                        CONSTRAINT fk_primary_user
                                            FOREIGN KEY (primary_user_id)
                                            REFERENCES profiles(user_id)
                                            ON DELETE CASCADE,
                                        CONSTRAINT fk_secondary_user
                                            FOREIGN KEY (secondary_user_id)
                                            REFERENCES profiles(user_id)
                                            ON DELETE CASCADE
                                        ); """
    await sql.execute(sql_create_matches_table)

    sql_create_user_id_index = 'CREATE INDEX IF NOT EXISTS index_user_id ON profiles (user_id);'
    await sql.execute(sql_create_user_id_index)

    sql_create_discord_id_index = 'CREATE INDEX IF NOT EXISTS index_discord_id ON profiles (discord_id);'
    await sql.execute(sql_create_discord_id_index)

    sql_create_primary_id_index = 'CREATE INDEX IF NOT EXISTS index_primary_id ON matches (primary_user_id);'
    await sql.execute(sql_create_primary_id_index)

    sql_create_secondary_id_index = 'CREATE INDEX IF NOT EXISTS index_secondary_id ON matches (secondary_user_id);'
    await sql.execute(sql_create_secondary_id_index)


async def get_unseen_profile_ids_by_discord_id(discord_id: int):
    user_id = await get_user_id_by_discord_id(discord_id)
    if user_id is None:
        return None

    user_gender_preference: str = await get_value_by_discord_id(discord_id, 'gender_preference')

    user_gender_preference_list = list(user_gender_preference)
    preference_string = '"' + '", "'.join(user_gender_preference_list) + '"'

    user_gender = await get_value_by_discord_id(discord_id, 'gender')
    sql_get_unseen_profile_ids = f"""SELECT DISTINCT user_id
                                     FROM profiles
                                     WHERE NOT user_id = "{user_id}"
                                     AND gender IN ({preference_string})
                                     AND gender_preference LIKE "%{user_gender}%"
                                     AND status = "1"
                                     AND user_id NOT IN (
                                         SELECT secondary_user_id
                                         FROM matches
                                         WHERE primary_user_id = "{user_id}"
                                 );"""

    result = await sql.get_cells(sql_get_unseen_profile_ids)
    if len(result) == 0:
        return None
    return result


async def create_profile(user_id: str, discord_id: int, channel_id: int):
    await sql.insert_multiple(profiles_table, ('user_id', 'discord_id', 'status', 'channel_id'),
                              (user_id, str(discord_id), str(ProfileStatus.NEW_SIGNUP_UNPUBLISHED), str(channel_id)))


async def update_profile(discord_id: int, column_name: str, new_value):
    await sql.update_by_value(profiles_table, 'discord_id', discord_id, column_name, str(new_value))


async def get_whole_profile_by_user_id(user_id: str):
    result = await sql.select_multiple_by_value(profiles_table, 'user_id', user_id,
                                                ('discord_id', 'full_name', 'age',
                                                 'gender', 'custom_gender',
                                                 'class', 'bio'))
    if len(result) == 0:
        return None
    result = result[0]
    profile_values = {
        'user_id': user_id,
        'discord_id': result[0],
        'full_name': result[1],
        'age': result[2],
        'gender': result[3],
        'custom_gender': result[4],
        'class': result[5],
        'bio': result[6]
    }
    return profile_values


async def get_match_status(primary_user_id: str, secondary_user_id: str):
    match_status = {
        'exists': False,
        'liked': -1,
        'matched': -1
    }

    result = await sql.select_multiple_by_two_values(matches_table,
                                                     'primary_user_id', primary_user_id,
                                                     'secondary_user_id', secondary_user_id,
                                                     ('liked', 'matched'))
    if len(result) == 0:
        return match_status
    result = result[0]
    match_status = {
        'exists': True,
        'liked': result[0],
        'matched': result[1]
    }
    return match_status


async def get_match_message_id(primary_user_id: str, secondary_user_id: str):
    result = await sql.select_by_two_values(matches_table,
                                            'primary_user_id', primary_user_id,
                                            'secondary_user_id', secondary_user_id,
                                            'message_id')
    if len(result) == 0:
        return None
    return result[0]


async def add_new_match(primary_user_id: str, secondary_user_id: str, liked: int, matched: int):
    await sql.insert_multiple(matches_table,
                              ('primary_user_id', 'secondary_user_id', 'liked', 'matched'),
                              (primary_user_id, secondary_user_id, str(liked), str(matched)))


async def update_match(primary_user_id: str, secondary_user_id: str, column: str, value):
    await sql.update_by_two_values(matches_table,
                                   'primary_user_id', primary_user_id,
                                   'secondary_user_id', secondary_user_id,
                                   column, str(value))


async def delete_profile(user_id: str):
    await sql.delete_by_value(profiles_table, 'user_id', user_id)


async def delete_matches(user_id: str):
    await sql.delete_by_value(matches_table, 'primary_user_id', user_id)
    await sql.delete_by_value(matches_table, 'secondary_user_id', user_id)


async def check_if_user_exists_by_discord_id(discord_id: int):
    return await sql.check_if_value_exists_in_column(profiles_table, 'discord_id', discord_id)


async def check_if_user_exists_by_user_id(user_id: str):
    return await sql.check_if_value_exists_in_column(profiles_table, 'user_id', user_id)


async def check_if_profile_has_column_by_discord_id(discord_id: int, column_name: str):
    return await sql.check_if_column_not_empty_in_row(profiles_table, column_name, 'discord_id', discord_id)


async def get_all_discord_ids():
    return await sql.select_all_from_column(profiles_table, 'discord_id')


async def get_user_id_by_name(name: str):
    result = await sql.select_by_value(profiles_table, 'full_name', name, 'user_id')
    if len(result) == 0:
        return None
    return result[0]


async def get_user_id_by_discord_id(discord_id: int):
    result = await sql.select_by_value(profiles_table, 'discord_id', discord_id, 'user_id')
    if len(result) == 0:
        return None
    return result[0]


async def get_discord_id_by_user_id(user_id: str):
    result = await sql.select_by_value(profiles_table, 'user_id', user_id, 'discord_id')
    if len(result) == 0:
        return None
    return result[0]


async def get_value_by_discord_id(discord_id: int, column_name: str):
    result = await sql.select_by_value(profiles_table, 'discord_id', discord_id, column_name)
    return result[0]


async def get_profile_count():
    return await sql.count_rows_in_table(profiles_table)


def get_user_picture_path(user_id: str, return_extension: bool = False):
    picture_extensions = ['.jpg', '.jpeg', '.png']
    file_path = None
    extension = None

    for extension_search in picture_extensions:
        file_path_search = f'.{os.sep}img{os.sep}{user_id}{extension_search}'
        if os.path.isfile(file_path_search):
            file_path = file_path_search
            extension = extension_search

    if return_extension:
        return file_path, extension
    else:
        return file_path


class ProfileStatus:
    NEW_SIGNUP_UNPUBLISHED = 0
    PUBLISHED = 1
    UNPUBLISHED = 2
