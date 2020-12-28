import os
import sys
import loguru

from src.core.Config import Config


def init_logger(verbosity=3):
    Config.verbosity = verbosity

    log_file_name = "scrapper_{time}.log"
    output = os.path.join(Config.dirs['logger_output'], log_file_name)

    if verbosity >= 5:
        level = "TRACE"

    if verbosity == 4:
        level = "DEBUG"

    if verbosity == 3:
        level = "INFO"

    if verbosity == 2:
        level = "SUCCESS"

    if verbosity <= 1:
        level = "WARNING"

    loguru.logger.remove()
    loguru.logger.add(sys.stderr, level=level)
    loguru.logger.add(output, level=level)

    loguru.logger.success("Logger level set to {level}", level=level)
    loguru.logger.success("Logger file saved at {output}", output=output)
