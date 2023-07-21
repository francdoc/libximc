from datetime import date
import logging
import os
from typing import Dict, List, Tuple
from pypi_creator import utils as ut


class PyPICreator:

    def __init__(self, config_path: str) -> None:
        """
        :param config_path: path to configuration file.
        """

        self._archive: str = None
        self._config_path: str = config_path
        self._dir: str = os.path.curdir
        self._dir_pypi: str = os.path.join(self._dir, "package")
        self._dir_pypi_src: str = os.path.join(self._dir_pypi, "src", "libximc")
        self._dir_pypi_tests: str = os.path.join(self._dir_pypi, "tests")
        self._dir_release: str = os.path.join(self._dir, "libximc_release")
        self._dir_templates: str = os.path.join(self._dir, "templates")
        self._dir_release_ximc: str = None
        self._dst_and_src: Dict[str, List[str]] = {}
        self._version: str = None

    def _add_destinations_and_sources(self) -> None:
        """
        Method creates dictionary where keys are destination directories and values ​​are lists of folders and files
        to be copied to destination directories.
        """

        self._dst_and_src = {self._dir_pypi: [os.path.join(self._dir_templates, "LICENSE"),
                                              os.path.join(self._dir_templates, "pyproject.toml")],
                             self._dir_pypi_src: [os.path.join(self._dir_templates, "__init__.py")]}

        dirs_from_release = ["debian-amd64", "debian-armhf", "debian-i386", "win32", "win64"]
        for dir_name in dirs_from_release:
            src_path = os.path.join(self._dir_release_ximc, dir_name)
            self._dst_and_src[self._dir_pypi_src].append(src_path)

        file_from_release = os.path.join(self._dir_release_ximc, "crossplatform", "wrappers", "python", "pyximc.py")
        self._dst_and_src[self._dir_pypi_src].append(file_from_release)

        readme_path = os.path.join(os.path.dirname(os.path.abspath(self._dir)), "README.md")
        self._dst_and_src[self._dir_pypi].append(readme_path)

    def _check_archive(self) -> bool:
        """
        :return: True if unpacked libximc release archive contains all required folders and files. There should also be
        all necessary files in 'templates' folder.
        """

        list_dir = os.listdir(self._dir_release)
        if len(list_dir) != 1 or not os.path.isdir(os.path.join(self._dir_release, list_dir[0])):
            logging.error("Check libximc release archive '%s'. There should be one folder in archive", self._archive)
            return False

        self._dir_release_ximc = os.path.join(self._dir_release, list_dir[0], "ximc")
        if not os.path.exists(self._dir_release_ximc):
            logging.error("Check libximc release archive '%s'. There is no 'ximc' folder in archive", self._archive)
            return False

        return True

    def _check_necessary_files_and_folders(self) -> bool:
        """
        :return: True if unpacked libximc release archive contains all required folders and files. There should also be
        all necessary files in 'templates' folder.
        """

        for files_or_dirs in self._dst_and_src.values():
            for file_or_dir in files_or_dirs:
                name = "file" if os.path.isfile(file_or_dir) else "folder"
                if not os.path.exists(file_or_dir):
                    logging.error("%s '%s' could not be found. This %s must be needed for release for PyPI",
                                  name.title(), file_or_dir, name)
                    return False
        return True

    def _copy_files_and_folders(self) -> bool:
        """
        :return: True if required folders and files copied successfully.
        """

        for dst_dir_path, files_or_dirs in self._dst_and_src.items():
            for file_or_dir in files_or_dirs:
                if os.path.isdir(file_or_dir):
                    dst_path = os.path.join(dst_dir_path, os.path.basename(file_or_dir))
                    if not ut.copy_dir(file_or_dir, dst_path):
                        logging.error("Failed to copy folder '%s' to folder '%s'", file_or_dir, dst_path)
                        return False
                    logging.info("Folder '%s' copied to folder '%s'", file_or_dir, dst_path)
                else:
                    if not ut.copy_file(file_or_dir, dst_dir_path):
                        logging.error("Failed to copy file '%s' to folder '%s'", file_or_dir, dst_dir_path)
                        return False
                    logging.info("File '%s' copied to folder '%s'", file_or_dir, dst_dir_path)
        return True

    def _create_dirs(self) -> bool:
        """
        :return: True if all folders created successfully.
        """

        for dir_path in (self._dir_pypi_src, self._dir_pypi_tests, self._dir_release):
            if not ut.create_dir(dir_path):
                logging.error("Failed to create folder '%s'", dir_path)
                return False
            logging.info("Folder '%s' created", dir_path)
        return True

    def _fix_license(self) -> None:
        file_path = os.path.join(self._dir_pypi, "LICENSE")
        try:
            content = ut.read_file(file_path)
            year = date.today().year
            new_content = content.replace("Copyright (c) 2023 EPC MSU", f"Copyright (c) {year} EPC MSU")
            ut.write_file(file_path, new_content)
        except Exception as exc:
            logging.error("Failed to change year in '%s' file (%s)", file_path, exc)
        else:
            logging.info("Year changed to '%d' in '%s' file", year, file_path)

    def _fix_version(self) -> None:
        file_path = os.path.join(self._dir_pypi, "pyproject.toml")
        try:
            content = ut.read_file(file_path)
            content = content.replace('version = ""', f'version = "{self._version}"')
            ut.write_file(file_path, content)
        except Exception as exc:
            logging.error("Failed to change version in '%s' file (%s)", file_path, exc)
        else:
            logging.info("Version changed to '%s' in '%s' file", self._version, file_path)

    def _get_archive_and_version(self) -> Tuple[str, str]:
        """
        :return: path to libximc release archive and version for PyPI release.
        """

        version = ut.parse_input_arguments(self._config_path) if self._config_path else None
        archive, version_from_name = ut.find_release_archive(self._dir)
        if not version and version_from_name:
            version = version_from_name
            logging.info("Release version '%s' is determined from archive name", version)
        elif not version and not version_from_name:
            logging.error("Unable to determine release version. Specify version in file 'config.ini'")
        return archive, version

    @staticmethod
    def _remove_dirs(dirs_to_remove: List[str], stop_if_error: bool = True) -> bool:
        """
        :param dirs_to_remove: list of directories to be removed;
        :param stop_if_error: if True, then execution of method should be terminated when error occurs.
        :return: True if all folders removed successfully.
        """

        for dir_path in dirs_to_remove:
            if os.path.exists(dir_path):
                result = ut.remove_dir(dir_path)
                if not result and stop_if_error:
                    logging.error("Failed to delete folder '%s'. Delete this folder and run script again", dir_path)
                    return False
                if result:
                    logging.info("Folder '%s' deleted", dir_path)
        return True

    def run(self) -> None:
        self._archive, self._version = self._get_archive_and_version()
        if not self._archive or not self._version:
            return
        if not self._remove_dirs([self._dir_pypi, self._dir_release]):
            return
        if not self._create_dirs():
            return
        if not ut.unzip_archive(self._archive, self._dir_release):
            return
        if not self._check_archive():
            return
        self._add_destinations_and_sources()
        if not self._check_necessary_files_and_folders():
            return
        if not self._copy_files_and_folders():
            return
        self._fix_license()
        self._fix_version()
        self._remove_dirs([self._dir_release])
