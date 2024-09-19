import logging

logging.basicConfig(level=logging.INFO, filemode='w', filename='py.log',
                    format='%(asctime)s | %(levelname)s | %(message)s')


def main():
    logging.info('START BOT')


if __name__ == '__main__':
    main()
