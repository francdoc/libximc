import logging


def set_logger() -> None:
    logging.basicConfig(format="[%(asctime)s.%(msecs)03d %(levelname)7s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S",
                        level=logging.INFO)
