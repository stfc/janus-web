from janus_core.cli.janus import janus_help
import typer

def show_options():
    command = typer.main.get_command(janus_help())
    with typer.Context(command) as ctx:
        return command.get_help(ctx)
    
if __name__ == "__main__":
    show_options()

