import sqlite3
import os

connection = None  # sqlite3.Connection
cursor = None  # sqlite3.Cursor
databaseName = "chatLogs.db"


def connect():
    global connection, cursor
    existed = os.path.exists(databaseName)  # file created on .connect This is much prettier way to do this.
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()
    if not existed:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS chat_logs(guild INTEGER, channel TEXT, model TEXT, author TEXT, ctx TEXT, reply TEXT, date INTEGER)")
        connection.commit()


async def sql_insert_into(guild: int, channel: str, model: str, author: str, message: str, reply: str, date: int):
    if None not in (connection, cursor):
        sql = f"""INSERT INTO chat_logs (guild, channel, model, author, ctx, reply, date) VALUES ({guild}, '{channel}', '{model}', '{author}', '{message}', '{reply}', {date})"""
        try:
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            return f"Insertion Error: {e}"
        else:
            return True
    else:
        return f"Insertion Error: You have not connected the database!"


def sql_retrieve_last_10_messages(guild: int):
    if None not in (connection, cursor):
        sql = f"""SELECT * FROM chat_logs WHERE guild == {guild} ORDER BY date LIMIT 10;"""
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
        except Exception as e:
            return f"Retrieval Error: {e}."
        else:
            return results