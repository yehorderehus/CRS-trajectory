from scripts.main_wrapper import MainWrapper
from scripts.logging_config import logger


def main():
    try:
        MainWrapper()  # The last class in the inheritance chain
    except Exception as e:
        logger.error(f'Main Error: {e}')


if __name__ == "__main__":
    main()
