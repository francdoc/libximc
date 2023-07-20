import logging
import re
import os
import shutil
import tarfile
from configparser import ConfigParser
from typing import Dict, Optional


def copy_dir(src_path: str, dst_path: str) -> bool:
    """
    :param src_path: path to folder to be copied;
    :param dst_path: path to folder where to copy folder.
    :return: True if folder copied successfully.
    """

    result = False
    try:
        shutil.copytree(src_path, dst_path)
    except Exception as exc:
        logging.error("Error occurred while copying folder '%s' to folder '%s' (%s)", src_path, dst_path, exc)
    else:
        result = True
    return result


def copy_file(src_path: str, dst_dir_path: str) -> bool:
    """
    :param src_path: path to file to be copied;
    :param dst_dir_path: path to folder where to copy file.
    :return: True if file copied successfully.
    """

    result = False
    try:
        shutil.copy(src_path, dst_dir_path)
    except Exception as exc:
        logging.error("Error occurred while copying file '%s' to folder '%s' (%s)", src_path, dst_dir_path, exc)
    else:
        result = True
    return result


def create_dir(dir_path: str) -> bool:
    """
    :param dir_path: folder to be created.
    :return: True if folder created.
    """

    try:
        os.makedirs(dir_path)
    except Exception as exc:
        logging.error("Error occurred while creating folder '%s' (%s)", dir_path, exc)
    return os.path.exists(dir_path)


def find_release_archive(dir_path: str) -> Dict[str, str]:
    """
    :param dir_path: folder where to find possible archive with release of libximc.
    :return: dictionary with path to possible archive with libximc release and its version.
    """

    logging.info("Searching for libximc release archive in folder '%s'...", os.path.abspath(dir_path))
    archives = []
    good_name_archives = []
    name_pattern = re.compile(r"^libximc-(?P<version>\d+\.\d+\.\d+)-.*\.tar\.gz$")
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

    if data.get("archive"):
        logging.info("Possible libximc release archive found: '%s'", data["archive"])
    else:
        logging.warning("Unable to find libximc release archive")
    return data


def get_config_path() -> Optional[str]:
    """
    :return: path to configuration file.
    """

    config_path = os.path.join(os.path.curdir, "config.ini")
    if not os.path.exists(config_path):
        logging.warning("Configuration file '%s' not found. Script will try to find archive with libximc release on "
                        "its own and determine release version", os.path.basename(config_path))
        config_path = None
    return config_path


def parse_input_arguments(config_path: Optional[str] = None) -> Dict[str, str]:
    """
    :param config_path: path to configuration file.
    :return: dictionary with path to possible archive with libximc release and its version.
    """

    config_file = os.path.basename(config_path)
    logging.info("Parsing config file '%s'...", config_file)
    config_structure = {"MAIN": [{"name": "archive",
                                  "type": str},
                                 {"name": "version",
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
                    logging.warning("Config file '%s' has no option '%s' in section '%s'", config_file, option_name,
                                    section)
        else:
            logging.warning("Config file '%s' has no section '%s'", config_file, section)

    if data.get("MAIN"):
        data = {"archive": data["MAIN"].get("archive"),
                "version": data["MAIN"].get("version")}
    else:
        data = {"archive": None,
                "version": None}
    logging.info("Parsing competed: archive = '%s', version = '%s'", data["archive"], data["version"])
    return data


def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def remove_dir(dir_path: str) -> bool:
    """
    :param dir_path: directory to be removed.
    :return: True if directory was successfully removed.
    """

    try:
        shutil.rmtree(dir_path)
    except Exception as exc:
        logging.error("Error occurred while deleting folder '%s' (%s)", dir_path, exc)
    return not os.path.exists(dir_path)


def unzip_archive(archive_path: str, dir_path: str) -> bool:
    """
    :param archive_path: path to archive with libximc release;
    :param dir_path: folder where to unpack archive.
    :return: True if archive could not be unpacked.
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
        logging.info("Archive '%s' is unpacked into folder '%s'", archive_path, dir_path)
    except Exception as exc:
        logging.error("Failed to unpack archive '%s' with libximc release into folder '%s' (%s)", archive_path,
                      dir_path, exc)
    if archive_file:
        archive_file.close()
    return result


def write_file(file_path: str, text: str) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)
