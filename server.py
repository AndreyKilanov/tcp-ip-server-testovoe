import asyncio
import sys

from client import start_clients
from settings import SERVER_HOST, SERVER_PORT
from logger import logger


async def handle_client(reader, writer):
    """
    Обрабатывает каждое соединение с клиентом. Отправляет и получает сообщения.
    """
    addr = writer.get_extra_info('peername')
    logger.info(f'Установлено соединение с клиентом {addr}')

    try:
        while True:
            if not await reader.read(100):
                break

            data = await reader.read(100)
            message = data.decode()
            logger.info(f'Получено сообщение от клиента {addr}: {message}')
            logger.info(f'Отправлено ответ клиенту {addr}: {message}')

            writer.write(data)
            await writer.drain()

    except Exception as e:
        logger.error(e)

    finally:
        logger.info(f'Соединение с клиентом {addr} закрыто')
        writer.close()


async def start_server_and_clients():
    """
    Запускает сервер и клиентов. Ожидает завершения всех клиентов и
    останавливает сервер.
    """
    try:
        server = await asyncio.start_server(
            handle_client, SERVER_HOST, SERVER_PORT
        )

        if not server.is_serving():
            logger.error('Серевер не запущен')
            sys.exit(1)

        address = server.sockets[0].getsockname()
        logger.info(f'Сервер запущен на {address}')

        clients_task = asyncio.create_task(start_clients(server))
        await clients_task

        server.close()
        await server.wait_closed()

    except KeyboardInterrupt:
        pass

    except asyncio.CancelledError:
        logger.info('Сервер остановлен')

    except ConnectionResetError:
        logger.info('Соединение с клиентом разорвано')

    except Exception as e:
        logger.error(e)

    finally:
        logger.info('Сервер остановлен')
