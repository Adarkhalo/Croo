import asyncio
import sys
import aiomysql
from package import Utility, ExceptionManager


class DatabaseManager:
    def __init__(self, mysql_host: str, mysql_user: str, mysql_password: str, mysql_db: str):
        self.__host = mysql_host
        self.__user = mysql_user
        self.__password = mysql_password
        self.__db = mysql_db

    async def put(self, parameters: list, table: str, values: list, exception: str, loop):
        try:
            parameters_str = Utility.list_to_mysql_parameters(parameters)
            values_str = Utility.bind_mysql_values(values)

            conn = await aiomysql.connect(host=self.__host, user=self.__user,
                                          password=self.__password, db=self.__db,
                                          loop=loop)
            async with conn.cursor() as cur:
                sql_insert_query = '''INSERT INTO ''' + table + '''(''' + parameters_str + ''') VALUES(''' + values_str + ''')'''
                query = values
                await cur.execute(sql_insert_query, query)
                insert_id = conn.insert_id()
                await conn.commit()
            conn.close()
            return insert_id
        except ValueError:
            e = sys.exc_info()
            print(e)
            ExceptionManager.return_exception(exception)

    async def get(self, parameters: list, table: str, parameters_values, values, orderby: str, exception: str, loop):
        try:
            parameters_str = Utility.list_to_mysql_parameters(parameters)
            parameters_values_str = Utility.list_to_mysql_parameters_values(parameters_values)
            conn = await aiomysql.connect(host=self.__host, user=self.__user,
                                          password=self.__password, db=self.__db,
                                          loop=loop)
            async with conn.cursor() as cur:
                sql_get_query = '''SELECT ''' + parameters_str + ''' FROM ''' + table
                if len(values) > 0:
                    sql_get_query += ''' WHERE ''' + parameters_values_str
                if orderby is not None:
                    sql_get_query += ' ' + orderby
                await cur.execute(sql_get_query, values)
                columns = cur.description
                result = [{columns[index][0]: column for index, column in enumerate(value)} for value in
                          await cur.fetchall()]
            conn.close()
            return result
        except ValueError:
            e = sys.exc_info()
            print(e)
            ExceptionManager.return_exception(exception)