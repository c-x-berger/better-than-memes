import asyncpg
from asyncpg.pool import Pool

import config

pool: Pool


async def init_pool():
    global pool
    pool = await asyncpg.create_pool(
        dsn="postgres://{user}:{pass}@{host}:{port}/{database}".format(
            **config.POSTGRES_CONFIG
        )
    )


async def get_post(id_: str):
    async with pool.acquire() as con:
        return await con.fetchrow("SELECT * FROM posts WHERE id = $1", id_)


async def get_comment(id_: str):
    async with pool.acquire() as con:
        return await con.fetchrow("SELECT * FROM comments WHERE id = $1", id_)
