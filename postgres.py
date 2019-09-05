import collections
from abc import ABC
from typing import Optional

import asyncpg
import psycopg2
from psycopg2.extras import RealDictCursor

import config
from storage import ThingStorage
from things import Thing


class PostgresStorage(ThingStorage, ABC):
    Authentication = collections.namedtuple("Authentication", ["username", "password"])

    def __init__(
        self,
        database: str,
        table: str,
        auth: Authentication,
        host: str = "localhost",
        port: int = 5432,
    ):
        self.connection = psycopg2.connect(
            dbname=database,
            user=auth.username,
            password=auth.password,
            host=host,
            port=port,
            cursor_factory=RealDictCursor,
        )
        self.table = table
        self.db_cursor = self.connection.cursor()

    def __getitem__(self, item: str) -> Optional[dict]:
        self.db_cursor.execute("SELECT * FROM %s WHERE id = %s", (self.table, item))
        return self.db_cursor.fetchone()

    def __setitem__(self, key: str, value: Thing):
        with self.db_cursor as curs:
            serialized = value.serialize()
            exec_str = "INSERT INTO %s (id, {}) VALUES ({})".format(
                ", ".join(serialized.keys()), ", ".join(["%s"] * len(serialized))
            )
            curs.execute(exec_str, (self.table, *serialized.values()))


pool = asyncpg.create_pool(
    dsn="postgres://{user}:{pass}@{host}:{port}/{database}".format(
        **config.POSTGRES_CONFIG
    )
)


async def get_post(id_: str):
    async with pool.acquire() as con:
        return await con.fetchrow("SELECT * FROM posts WHERE id = $1", id_)
