import logging
import re
import os
import shutil
import tarfile
from configparser import ConfigParser
from typing import Optional, Tuple


def check_success(func):
    """
    Decorator catches error while executing function.
    :param func: function to decorate.
    """

    def wrapper(*args, **kwargs):
        result = True
        try:
            func(*args, **kwargs)
        except Exception as exc:
            logging.error("Error occurred while executing function '%s(%s, %s)' (%s)", func.__name__, args, kwargs, exc)
            result = False
        return result

    return wrapper


@check_success
def copy_dir(src_path: str, dst_path: str) -> None:
    """
    :param src_path: path to folder to be copied;
    :param dst_path: path to folder where to copy folder.
    """

    shutil.copytree(src_path, dst_path)


@check_success
def copy_file(src_path: str, dst_dir_path: str) -> None:
    """
    :param src_path: path to file to be copied;
    :param dst_dir_path: path to folder where to copy file.
    """

    shutil.copy(src_path, dst_dir_path)


@check_success
def create_dir(dir_path: str) -> None:
    """
    :param dir_path: folder to be created.
    """

    os.makedirs(dir_path)


def find_release_archive(dir_path: str) -> Tuple[str, str]:
    """
    :param dir_path: folder where to find possible archive with release of libximc.
    :return: path to possible archive with libximc release and its version.
    """

    logging.info("Searching for libximc release archive in folder '%s'...", os.path.abspath(dir_path))
    archives = []
    good_name_archives = []
    name_pattern = re.compile(r"^libximc-(?P<version>\d+\.\d+\.\d+)(.*)?\.tar\.gz$")
    for file_name in os.listdir(dir_path):
        path = os.path.join(dir_path, file_name)
        if os.path.isfile(path):
            result = name_pattern.match(file_name)
            if result:
                good_name_archives.append({"archive": path,
                                           "version": result.group("version")})
            elif file_name.endswith(".tar.gz"):
                archives.append({"archive": path,
                                 "version": None})

    data = {}
    if good_name_archives:
        data = good_name_archives[0]
    elif archives:
        data = archives[0]

    archive = data.get("archive", None)
    version = data.get("version", None)

    if archive:
        logging.info("Possible libximc release archive found: '%s'", data["archive"])
    else:
        logging.warning("Unable to find libximc release archive")
    return archive, version


def get_config_path() -> Optional[str]:
    """
    :return: path to configuration file.
    """

    config_path = os.path.join(os.path.curdir, "config.ini")
    if not os.path.exists(config_path):
        logging.warning("Config file '%s' not found. Script will try to determine release version from archive name",
                        config_path)
        config_path = None
    return config_path


def parse_input_arguments(config_path: Optional[str] = None) -> str:
    """
    :param config_path: path to configuration file.
    :return: version for release.
    """

    logging.info("Parsing config file '%s'...", config_path)
    config_structure = {"MAIN": [{"name": "version",
                                  "type": str}]}
    config_parser = ConfigParser()
    config_parser.read(config_path)

    data = {}
    for section, options in config_structure.items():
        data[section] = {}
        if config_parser.has_section(section):
            for option in options:
                option_name = option["name"]
                if config_parser.has_option(section, option_name):
                    convert_func = option.get("type", str)
                    try:
                        data[section][option_name] = convert_func(config_parser.get(section, option_name))
                    except Exception as exc:
                        logging.warning("Invalid value of option '%s' in section '%s' (%s)", option_name, section, exc)
                else:
                    logging.warning("Config file '%s' has no option '%s' in section '%s'", config_path, option_name,
                                    section)
        else:
            logging.warning("Config file '%s' has no section '%s'", config_path, section)

    if data.get("MAIN"):
        version = data["MAIN"].get("version", None)
    else:
        version = None

    if not version:
        logging.warning("Release version not found in config file '%s'", config_path)
    else:
        logging.info("Release version '%s' found in config file '%s'", version, config_path)
    return version


def read_file(file_path: str) -> str:
    """
    :param file_path: path to file to be read.
    :return: text in file.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


@check_success
def remove_dir(dir_path: str) -> None:
    """
    :param dir_path: directory to be removed.
    """

    shutil.rmtree(dir_path)


def unzip_archive(archive_path: str, dir_path: str) -> bool:
    """
    :param archive_path: path to archive with libximc release;
    :param dir_path: folder where to unpack archive.
    :return: True if archive was successfully unpacked.
    """

    if not os.path.exists(archive_path):
        logging.error("There is no libximc release archive '%s'", archive_path)
        return False

    archive_file = None
    result = False
    try:
        archive_file = tarfile.open(archive_path)
        archive_file.extractall(dir_path)
        result = True
        logging.info("Archive '%s' unpacked into folder '%s'", archive_path, dir_path)
    except Exception as exc:
        logging.error("Failed to unpack archive '%s' with libximc release into folder '%s' (%s)", archive_path,
                      dir_path, exc)
    if archive_file:
        archive_file.close()
    return result


def write_file(file_path: str, text: str) -> None:
    """
    :param file_path: path to file to be written;
    :param text: text for file.
    """

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)
