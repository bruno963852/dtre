import src.bot as bot
import logging
import sys

# noinspection PyArgumentList
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] -%(pathname)s- %(message)s",
    handlers=[
        logging.FileHandler('../debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.info("Initializing application...")

bot.run()
