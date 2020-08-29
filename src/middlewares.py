from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
import aiosqlite

from config import DB_URL


class AuthMiddleware(BaseMiddleware):
    """Middleware for storing all users in the database."""

    def __init__(self):
        BaseMiddleware.__init__(self)
        self._db: aiosqlite.Connection = None

    async def on_process_message(self, message: types.Message, data: dict):
        """Authentication when received message from user."""
        await self._auth(message.from_user)

    async def on_callback_query(self, cq: types.CallbackQuery, data: dict):
        """
        Authentication when a callback query is received from user.
        """
        await self._auth(cq.from_user)

    async def _auth(self, tg_user: types.User):
        """Main auth method."""
        try:
            user = await self._get_user(tg_user.id)
            if user == None:
                await self._create_user(tg_user.id)
        except aiosqlite.OperationalError:
            await self._create_db()
            await self._create_user(tg_user.id)
    

    async def _get_user(self, id: int):
        """Method for getting user from the database."""
        db = await self._get_db()
        try:
            cursor = await db.execute('SELECT * FROM users WHERE id= {} '\
                    .format(str(id)))
            user = await cursor.fetchone()
            await cursor.close()
        except aiosqlite.OperationalError:
            raise aiosqlite.OperationalError
        return user
    
    async def _create_user(self, id: int):
        """Method for inserting user for the database."""
        db = await self._get_db()
        await db.execute('INSERT INTO users (id, blocked) VALUES ({}, 0)'\
                .format(str(id)))
        await db.commit()
    
    async def _create_db(self):
        """Method for creating the database if it doesn't exist."""
        db = await self._get_db()
        await db.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, blocked '
                         'INTEGER NOT NULL)')
        await db.commit()
    
    async def _get_db(self) -> aiosqlite.Connection:
        """
        This method returns the connection to the database and
        creates it if it did not exist.
        """
        if self._db == None:
            self._db = await aiosqlite.connect(DB_URL)
        return self._db
    
    async def close(self):
        """Close the database connection when the bot shuts down."""
        if self._db:
            await self._db.close()
