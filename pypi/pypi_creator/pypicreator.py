from datetime import date
import logging
import os
from typing import List, Tuple
from pypi_creator import utils as ut


class PyPICreator:

    FILE_FROM_RELEASE: str = os.path.join("crossplatform", "wrappers", "python", "pyximc.py")
    FOLDERS_FROM_RELEASE: List[str] = ["debian-amd64", "debian-armhf", "debian-i386", "win32", "win64"]

    def __init__(self, config_path: str) -> None:
        """
        :param config_path: path to configuration file.
        """

        self._archive: str = None
        self._config_path: str = config_path
        self._dir: str = os.path.curdir
        self._dir_for_pypi: str = os.path.join(self._dir, "package")
        self._dir_for_pypi_src: str = os.path.join(self._dir_for_pypi, "src", "libximc")
        self._dir_for_release: str = os.path.join(self._dir, "libximc_release")
        self._dir_templates: str = os.path.join(self._dir, "templates")

        self._dst_and_src = {self._dir_for_pypi: [os.path.join(self._dir_templates, "LICENSE"),
                                                  os.path.join(self._dir_templates, "pyproject.toml")],
                             self._dir_for_pypi_src: [os.path.join(self._dir_templates, "__init__.py")]}
        self._version: str = None

    def _add_dst_and_src(self) -> None:
        for dir_name in PyPICreator.FOLDERS_FROM_RELEASE:
            src_path = os.path.join(self._dir_ximc, dir_name)
            self._dst_and_src[self._dir_for_pypi_src].append(src_path)

        self._dst_and_src[self._dir_for_pypi_src].append(os.path.join(self._dir_ximc, PyPICreator.FILE_FROM_RELEASE))

    def _check_archive(self) -> bool:
        """
        :return: True if unpacked libximc release archive contains all required folders and files.
        """

        list_dir = os.listdir(self._dir_for_release)
        if len(list_dir) != 1 or not os.path.isdir(os.path.join(self._dir_for_release, list_dir[0])):
            logging.error("Check libximc release archive '%s', there should be one folder in archive", self._archive)
            return False

        self._dir_ximc: str = os.path.join(self._dir_for_release, list_dir[0], "ximc")
        if not os.path.exists(self._dir_ximc):
            logging.error("Check libximc release archive '%s', there is no 'ximc' folder in archive", self._archive)
            return False

        for dir_name in PyPICreator.FOLDERS_FROM_RELEASE:
            dir_path = os.path.join(self._dir_ximc, dir_name)
            if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
                logging.error("Check libximc release archive '%s', folder '%s' not found in archive", self._archive,
                              os.path.join("ximc", dir_name))
                return False

        file_path = os.path.join(self._dir_ximc, PyPICreator.FILE_FROM_RELEASE)
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            logging.error("Check libximc release archive '%s', file '%s' not found in archive", self._archive,
                          os.path.join("ximc", PyPICreator.FILE_FROM_RELEASE))
            return False

        return True

    def _copy_files_and_folders(self) -> bool:
        """
        :return: True if required folders and files copied successfully.
        """

        for dst_dir_path, files_and_folders in self._dst_and_src.items():
            for file_or_folder in files_and_folders:
                if os.path.isdir(file_or_folder):
                    dst_path = os.path.join(dst_dir_path, os.path.basename(file_or_folder))
                    if not ut.copy_dir(file_or_folder, dst_path):
                        logging.error("Failed to copy folder '%s' to folder '%s'", file_or_folder, dst_path)
                        return False
                    logging.info("Folder '%s' copied to folder '%s'", file_or_folder, dst_path)
                else:
                    if not ut.copy_file(file_or_folder, dst_dir_path):
                        logging.error("Failed to copy file '%s' to folder '%s'", file_or_folder, dst_dir_path)
                        return False
                    logging.info("File '%s' copied to folder '%s'", file_or_folder, dst_dir_path)
        return True

    def _create_dirs(self) -> bool:
        """
        :return: True if all folders created successfully.
        """

        for dir_path in (self._dir_for_pypi_src, self._dir_for_release):
            if not ut.create_dir(dir_path):
                logging.error("Failed to create folder '%s'", dir_path)
                return False
            logging.info("Folder '%s' created", dir_path)
        return True

    def _fix_license(self) -> None:
        file_name = "LICENSE"
        file_path = os.path.join(self._dir_for_pypi, file_name)
        try:
            content = ut.read_file(file_path)
            year = date.today().year
            new_content = content.replace("Copyright (c) 2023 EPC MSU", f"Copyright (c) {year} EPC MSU")
            ut.write_file(file_path, new_content)
        except Exception as exc:
            logging.error("Failed to change year in '%s' file (%s)", file_name, exc)
        else:
            logging.info("Year changed to %d in '%s' file", year, file_name)

    def _fix_version(self) -> None:
        file_name = "pyproject.toml"
        file_path = os.path.join(self._dir_for_pypi, file_name)
        try:
            content = ut.read_file(file_path)
            content = content.replace('version = ""', f'version = "{self._version}"')
            ut.write_file(file_path, content)
        except Exception as exc:
            logging.error("Failed to change version in '%s' file (%s)", file_name, exc)
        else:
            logging.info("Version changed to %s in '%s' file", self._version, file_name)

    def _get_archive_and_version(self) -> Tuple[str, str]:
        """
        :return: path to archive with libximc release and version for PyPI release.
        """

        input_data = {}
        if self._config_path:
            input_data = ut.parse_input_arguments(self._config_path)
        if not input_data.get("archive"):
            data = ut.find_release_archive(self._dir)
            input_data["archive"] = data.get("archive")
            input_data["version"] = input_data.get("version") or data.get("version")
        return input_data.get("archive"), input_data.get("version")

    def _remove_dirs(self) -> bool:
        """
        :return: True if all folders removed successfully.
        """

        for dir_path in (self._dir_for_pypi, self._dir_for_release):
            if os.path.exists(dir_path):
                logging.warning("Folder '%s' will be deleted", dir_path)
                if not ut.remove_dir(dir_path):
                    logging.error("Failed to delete folder '%s'. Delete this folder and run script again", dir_path)
                    return False
        return True

    def run(self) -> None:
        self._archive, self._version = self._get_archive_and_version()
        if not self._archive or not self._version:
            return
        if not self._remove_dirs():
            return
        if not self._create_dirs():
            return
        if not ut.unzip_archive(self._archive, self._dir_for_release):
            return
        if not self._check_archive():
            return
        self._add_dst_and_src()
        if not self._copy_files_and_folders():
            return
        self._fix_license()
        self._fix_version()
