import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.exceptions.databases import DatabaseNotConnected
from app.models.databases import DatabaseBase, Database


def get_engine(database: DatabaseBase):
    return create_async_engine(database.url())

class ConnectedDatabase:
    def __init__(self, database: Database | DatabaseBase):
        logging.debug("Connecting to database")
        self.db_name = database.db_name
        self.engine = get_engine(database)
        self.db_session = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def verify_connection(self):
        try:
            await self._execute_query("SELECT 1")
        except Exception as e:
            logging.error(f"Error connecting to database: {e}")
            raise DatabaseNotConnected from e

    async def get_data(self, query):
        query_result = await self._execute_query(query)
        data = query_result.all()
        return data

    async def _execute_query(self, query):
        async with self.engine.begin() as conn:
            query_executed = await conn.execute(text(query))
            logging.debug(f"Query executed: {query}")
            return query_executed

    async def get_schema(self):
        query = (f"SELECT TABLE_NAME, COLUMN_NAME "
                 f"FROM INFORMATION_SCHEMA.COLUMNS "
                 f"WHERE TABLE_SCHEMA = '{self.db_name}';")
        return await self.get_data(query)

    async def get_tables(self):
        query = (f"SELECT TABLE_NAME "
                 f"FROM INFORMATION_SCHEMA.TABLES "
                 f"WHERE TABLE_SCHEMA = '{self.db_name}';")
        result = await self.get_data(query)
        flattened_list = [item for sublist in result for item in sublist]
        return flattened_list

    async def get_columns(self, table: str):
        query = (f"SELECT COLUMN_NAME "
                 f"FROM INFORMATION_SCHEMA.columns "
                 f"WHERE TABLE_SCHEMA = '{self.db_name}' AND TABLE_NAME = '{table}';")
        result = await self.get_data(query)
        flattened_list = [item for sublist in result for item in sublist]
        return flattened_list

    async def get_sample(self, table: str, column: str):
        query = (f"SELECT {column} "
                 f"FROM {self.db_name}.{table} "
                 f"WHERE {column} IS NOT NULL LIMIT 1;")
        result = await self.get_data(query)
        return result[0][0]
