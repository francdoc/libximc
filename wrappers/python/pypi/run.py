from pypi_creator import PyPICreator, set_logger, utils as ut


def main() -> None:
    set_logger()
    config_path = ut.get_config_path()
    pypi_creator = PyPICreator(config_path)
    pypi_creator.run()


if __name__ == "__main__":
    main()
