
from coin_algorithm.server import back_test_server
import logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Set the logging format
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

def main():
   # log start back test server
   logger = logging.getLogger("main")
   logger.info("Starting back test server")
   back_test_server.serve(port='8888', bot_module='bot.my_macd_bot', bot_class='MyMacdBot')


if __name__ == '__main__':
    main()