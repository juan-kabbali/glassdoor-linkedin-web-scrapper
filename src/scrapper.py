import click
import loguru

from src.commands.LoadConfigCommand import LoadConfigFileCommand
import setup


@click.command()
@click.option('-c', '--config-file', 'config_file', required=True, help="Path to config file")
@click.option('-v', '--verbose', 'verbosity', count=True, help="Activate verbosity output")
@click.option('-V', '--version', 'is_version', is_flag=True, help="Print current version and stops execution")
def main(config_file, verbosity, is_version):

    if is_version:
        loguru.logger.success("You are running scrapper V.{version}", version=setup.version)
        exit(0)

    LoadConfigFileCommand(file_path=config_file).execute()
    pass
