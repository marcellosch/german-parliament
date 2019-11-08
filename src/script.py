import download
import parse
import logging


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    download.main()
    parse.main()