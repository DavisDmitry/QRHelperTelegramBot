from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
import aiosqlite

from config import DB_URL


class AuthMiddleware(BaseMiddleware):
    def __init__(self):
        BaseMiddleware.__init__(self)
        self._db: aiosqlite.Connection = None

    async def on_process_message(self, message: types.Message, data: dict):
        await self._auth(message.from_user)

    async def _auth(self, tg_user: types.User):
        try:
            user = await self._get_user(tg_user.id)
            if user == None:
                await self._create_user(tg_user.id)
                await self._get_user(tg_user.id)
        except aiosqlite.OperationalError:
            await self._create_db()
            await self._create_user(tg_user.id)
            await self._get_user(tg_user.id)
    

    async def _get_user(self, id: int):
        db = await self._get_db()
        try:
            cursor = await db.execute('SELECT * FROM users WHERE id= {} '.format(str(id)))
            user = await cursor.fetchone()
            await cursor.close()
        except aiosqlite.OperationalError:
            raise aiosqlite.OperationalError
        return user
    
    async def _create_user(self, id: int):
        db = await self._get_db()
        await db.execute('INSERT INTO users (id, blocked) VALUES ({}, 0)'.format(str(id)))
        await db.commit()
    
    async def _create_db(self):
        db = await self._get_db()
        await db.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, blocked INTEGER NOT NULL)')
        await db.commit()
    
    async def _get_db(self) -> aiosqlite.Connection:
        if self._db == None:
            self._db = await aiosqlite.connect(DB_URL)
        return self._db
    
    async def close(self):
        if self._db:
            await self._db.close()
