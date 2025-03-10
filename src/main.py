import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from config import check_env_vars

def main():
    check_env_vars()

    logger.info("Environment validated successfully")

if __name__ == "__main__":
    main()