from janus_core.cli.janus import app
import typer

def show_options():
    command = typer.main.get_command(app)
    with typer.Context(command) as ctx:
        return command.get_help(ctx)
    
if __name__ == "__main__":
    show_options()

