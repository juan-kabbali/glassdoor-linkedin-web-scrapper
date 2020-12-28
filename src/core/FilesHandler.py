import glob
import loguru


def list_files(path, recursive=False):
    loguru.logger.debug("Listing files at {path}", path=path)
    return glob.glob(path, recursive=recursive)


