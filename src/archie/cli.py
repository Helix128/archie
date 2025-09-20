import click
import importlib.metadata
from .env import *

@click.group()
def cli():
  pass

@cli.command()
def version():
  """Get current installed Archie version"""
  click.echo(f"{importlib.metadata.version('archie')}")

@cli.command()
def help():
  """Show this message and exit."""
  click.echo(cli.get_help(click.Context(cli)))

#region env
@cli.group()
def env():
  """Manage global environment variables."""
  pass

@env.command()
@click.argument("key")
def get(key):
  """Get a global environment variable value."""
  result = get_env_var(key)
  if result is not None:
    click.echo(f"{key}={result}")
  else:
    click.echo(f"{key} not found.")

@env.command()
@click.argument("key")
@click.argument("value")
def set(key, value):
  """Set a global environment variable."""
  set_env_var(key, value)
  click.echo(f"{key}={value}")

@env.command()
@click.argument("key")
def delete(key):
  """Delete a global environment variable."""
  del_env_var(key)
  click.echo(f"Deleted {key}")

@env.command()
def list():
  """List all global environment variables."""
  vars = list_env_vars()
  click.echo(f"Found {len(vars)} global environment variables:")
  if vars:
    for var in vars:
      click.echo(var)
#endregion

if __name__ == "__main__":
  cli()