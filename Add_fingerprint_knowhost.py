import asyncssh
import asyncio

async def connect_and_trust():
    try:
        conn = await asyncssh.connect(
            'petersburg',  # адрес сервера
            username='webpub1c',
            password='Gkt78j4eUSi'
        )
        print("Подключение успешно!")
        conn.close()
    except Exception as e:
        print(f"Ошибка: {e}")

asyncio.run(connect_and_trust())
input(':-)> ')
