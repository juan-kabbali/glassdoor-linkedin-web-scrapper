import codecs
import glob
import loguru


def list_files(path, recursive=False):
    loguru.logger.debug("Listing files at {path}", path=path)
    return glob.glob(path, recursive=recursive)


def load_file(file_path):
    with open(file_path, "r", encoding="utf8") as file:
        loguru.logger.trace("Opening file at {file_path}", file_path=file_path)
        return file.read()
