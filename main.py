from scripts.main_wrapper import MainWrapper

import traceback


def main():
    try:
        MainWrapper()  # The last class in the inheritance chain
    except Exception as e:
        print(f"Main error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
