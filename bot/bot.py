from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import Command
import os, sys, asyncio, json, logging, aiormq
from sys import stdout

# from config import TOKEN, rabbitMQConfig
from config_reader import bot_config, rabbit_config
from ZipTimedRotatingFileHandler import ZipTimedRotatingFileHandler


bot = Bot(token=bot_config.token.get_secret_value())
dp = Dispatcher()

os.makedirs('logs', exist_ok=True)
fileHandler = ZipTimedRotatingFileHandler(filename='logs/bot_log.log', when="W1", interval=1, backupCount=3, encoding='utf-8')
fileHandler.suffix = "%Y-%m-%d"
consoleHandler = logging.StreamHandler(stdout) #set streamhandler to stdout
logging.basicConfig(handlers=[fileHandler,consoleHandler],
                    format="%(asctime)s %(levelname)s %(message)s",level=logging.INFO)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    logging.info(f'Пользователь {message.from_user.id} дал команду start')
    await message.reply("Теперь вы будете получать уведомления из системы ЕМЕ! Для подписки на определённые уведомления обратитесь к @leon_ob.")
    await bot.send_message(254922339, f'Пользователь {message.from_user.full_name} {message.from_user.id} нажал start')

@dp.message(Command("help"))
async def cmd_help(message: Message):
    logging.info(f'Пользователь {message.from_user.id} дал команду help')
    await message.reply("Это бот уведомлений.\nДля подписки на уведомления и при неполадках обращайтесь к @leon_ob.")

@dp.message()
async def echo_message(message: Message):
    logging.info(f'Пользователь {message.from_user.id} дал неизвестную команду')
    await bot.send_message(message.from_user.id, 'Данный бот только отправляет уведомления')

#------RabbitMQ-----------------------------------

# действие при пойманном сообщении от кролика
async def callbackRabbit(message):
    try:
        jsonData = message.body.decode('utf-8')
        print(" [x] Received RabbitMQ %r" % jsonData)
        dictData = json.loads(jsonData)
        await bot.send_message(dictData['user_tg_id'], dictData['message'])
        logging.info(f'Пользователь {dictData["user_tg_id"]} получил сообщение {dictData["message"]}')
    except Exception as e:
        logging.error('Error at %s', 'division', exc_info=e)


# прослушивание кролика на сообщения
async def runConsumeRabbit():
    logging.warning("runConsumeRabbit запускается")
    while True:
        try:
            connection = await aiormq.connect(
                f'amqp://{rabbit_config.user.get_secret_value()}:{rabbit_config.password.get_secret_value()}'
                f'@{rabbit_config.host}:{rabbit_config.port}/{rabbit_config.vhost}',)
            channel = await connection.channel()
            await channel.basic_consume(queue=rabbit_config.queue, consumer_callback=callbackRabbit, no_ack=True)
            logging.warning("runConsumeRabbit подключились!")
            break
        except Exception as e:
            logging.error('Error at %s', 'division', exc_info=e)
            logging.error("runConsumeRabbit ошибка подключения! Попробуем через 5 секунд.")
            await asyncio.sleep(5)

async def runBot():
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(dp.start_polling(bot), runConsumeRabbit())
    

if __name__ == '__main__':
    try:
        asyncio.run(runBot()) 
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)