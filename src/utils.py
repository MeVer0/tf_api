
# Для вставки в таблицу
from sqlalchemy import select


async def insert(engine, table, columns_values: dict):

    async with engine.begin() as conn:
        await conn.execute(
            insert(table).values(columns_values)
    )
