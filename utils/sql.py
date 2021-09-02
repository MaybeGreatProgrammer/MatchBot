import aiosqlite

from utils import config

db_path = config.db_path


async def update_by_value(table_name: str, lookup_column: str, lookup_value, column_name: str, new_value):
    sql_update_by_value = f'UPDATE {table_name} SET {column_name} = ? WHERE {lookup_column} = "{lookup_value}";'
    async with aiosqlite.connect(db_path) as connection:
        await connection.execute(sql_update_by_value, (new_value,))
        await connection.commit()


async def update_by_two_values(table_name: str, lookup_column_1: str, lookup_value_1,
                               lookup_column_2: str, lookup_value_2, column_name: str, new_value):
    sql_update_by_value = f'UPDATE {table_name} SET {column_name} = ? WHERE {lookup_column_1} = "{lookup_value_1}" ' \
                          f'AND {lookup_column_2} = "{lookup_value_2}";'
    async with aiosqlite.connect(db_path) as connection:
        await connection.execute(sql_update_by_value, (new_value,))
        await connection.commit()


async def select_by_value(table_name: str, lookup_column: str, lookup_value, column_name: str):
    sql_select_by_value = f'SELECT {column_name} FROM {table_name} WHERE {lookup_column} = ?;'
    async with aiosqlite.connect(db_path) as connection:
        connection.row_factory = lambda sqlite_cursor, row: row[0]
        cursor: aiosqlite.Cursor = await connection.execute(sql_select_by_value, (lookup_value,))
        rows = await cursor.fetchall()
        return rows


async def select_by_two_values(table_name: str, lookup_column_1: str, lookup_value_1,
                               lookup_column_2:str, lookup_value_2, column_name: str):
    sql_select_by_value = f'SELECT {column_name} FROM {table_name} WHERE {lookup_column_1} = "{lookup_value_1}" ' \
                          f'AND {lookup_column_2} = "{lookup_value_2}";'
    return await get_cells(sql_select_by_value)


async def select_multiple_by_value(table_name: str, lookup_column: str, lookup_value, columns: tuple):
    columns_string = ', '.join(columns)
    sql_select_by_value = f'SELECT {columns_string} FROM {table_name} WHERE {lookup_column} = ?;'
    async with aiosqlite.connect(db_path) as connection:
        cursor: aiosqlite.Cursor = await connection.execute(sql_select_by_value, (lookup_value,))
        rows = await cursor.fetchall()
        return rows


async def select_multiple_by_two_values(table_name: str, lookup_column_1: str, lookup_value_1,
                                        lookup_column_2: str, lookup_value_2, columns: tuple):
    columns_string = ', '.join(columns)
    sql_select_by_value = f'SELECT {columns_string} FROM {table_name} WHERE {lookup_column_1} = "{lookup_value_1}" ' \
                          f'AND {lookup_column_2} = "{lookup_value_2}";'
    return await get_rows(sql_select_by_value)


async def delete_by_value(table_name: str, lookup_column: str, lookup_value):
    sql_delete_by_value = f'DELETE FROM {table_name} WHERE {lookup_column} = "{lookup_value}";'
    await execute(sql_delete_by_value)


async def insert_multiple(table_name: str, columns: tuple, values: tuple):
    columns_string = ', '.join(columns)
    values_string = '"' + '", "'.join(values) + '"'
    sql_insert_multiple = f'INSERT INTO {table_name} ({columns_string}) VALUES ({values_string});'
    await execute(sql_insert_multiple)


async def select_all_from_column(table_name: str, column_name: str):
    sql_select_all_from_column = f'SELECT {column_name} FROM {table_name};'
    return await get_cells(sql_select_all_from_column)


async def check_if_value_exists_in_column(table_name: str, column_name: str, value):
    sql_check_if_value_exists_in_column = f'SELECT EXISTS' \
                                          f'(SELECT 1 FROM {table_name} ' \
                                          f'WHERE {column_name} = ?);'
    async with aiosqlite.connect(db_path) as connection:
        cursor: aiosqlite.Cursor = await connection.execute(sql_check_if_value_exists_in_column, (value,))
        result = await cursor.fetchone()
        if len(result) == 0:
            return None
        return result[0]


async def check_if_column_not_empty_in_row(table_name: str, column_name: str, row_value_column_name: str, row_value):
    sql_check_if_value_exists_in_column = f'SELECT EXISTS(' \
                                          f'SELECT 1 FROM {table_name} ' \
                                          f'WHERE {row_value_column_name} = "{row_value}" ' \
                                          f'AND {column_name} IS NOT NULL);'
    return await get_result(sql_check_if_value_exists_in_column)


async def count_rows_in_table(table_name: str):
    sql_count_rows_in_table = f'SELECT COUNT(*) FROM {table_name};'
    return await get_result(sql_count_rows_in_table)


async def execute(sql):
    async with aiosqlite.connect(db_path) as connection:
        await connection.execute(sql)
        await connection.commit()


async def get_cells(sql):
    async with aiosqlite.connect(db_path) as connection:
        connection.row_factory = lambda sqlite_cursor, row: row[0]
        cursor: aiosqlite.Cursor = await connection.execute(sql)
        rows = await cursor.fetchall()
        return rows


async def get_rows(sql):
    async with aiosqlite.connect(db_path) as connection:
        cursor: aiosqlite.Cursor = await connection.execute(sql)
        rows = await cursor.fetchall()
        return rows


async def get_result(sql):
    async with aiosqlite.connect(db_path) as connection:
        cursor: aiosqlite.Cursor = await connection.execute(sql)
        result = await cursor.fetchone()
        if len(result) == 0:
            return None
        return result[0]
