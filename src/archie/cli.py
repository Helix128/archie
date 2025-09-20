import click
import importlib.metadata
from difflib import get_close_matches

# archie modules
from .env import *
from .disk import *

@click.group()
def cli():
  pass

#region core
@cli.command()
def version():
  """Get installed Archie version."""
  click.echo(f"{importlib.metadata.version('archie-cli')}")

@cli.command()
def help():
  """Show this message and exit."""
  click.echo(cli.get_help(click.Context(cli)))
#endregion
#region env
@cli.group()
def env():
  """Manage profile environment variables."""
  pass

@env.command()
@click.argument("key")
def get(key):
  """Get an environment variable value."""
  result = get_env_var(key)
  if result is not None:
    click.echo(click.style(f"{key} = {result}", fg="white"))
  else:
    click.echo(click.style(f"{key} not found.", fg="red"))

@env.command()
@click.argument("key")
@click.argument("value")
def set(key, value):
  """Set an environment variable."""
  set_env_var(key, value)
  click.echo(click.style(f"{key}={value}", fg="white"))

@env.command()
@click.argument("key")
def delete(key):
  """Delete an environment variable."""
  del_env_var(key)
  click.echo(click.style(f"Deleted {key}", fg="white"))

@env.command()
def list():
  """List all environment variables."""
  vars = list_env_vars()
  click.echo("Found",nl=False)
  click.echo(click.style(f" {len(vars)} ", fg="cyan"), nl=False)
  click.echo("environment variable(s):")
  if vars:
    for var in vars:
      exportIndex = var.index("export")
      varName = var[exportIndex + len("export "):].split('=', 1)[0].strip()
      varValue = var[exportIndex + len("export "):].split('=', 1)[1].strip().strip('"')
      click.echo(click.style(f"{varName} = {varValue}", fg="white"))
      
#endregion
#region disk
@cli.group()
def disk():
  """Manage disks."""
  pass
@disk.command()
def list():
  """List all disks."""
  disks = get_disks()
  click.echo(f"Found {len(disks)} disks:")
  if disks:
    for disk in disks:
      disk_name = disk.get('name', 'Unknown')
      disk_model = disk.get('model', 'Unknown')
      click.echo("- ", nl=False)
      click.echo(click.style(f"{disk_model} ", fg="cyan"), nl=False)
      click.echo(click.style(f"({disk_name})", fg="white"))
      
      
@disk.command()
@click.argument("name", required=False)
@click.option("--all", is_flag=True, help="Show all disks")
def info(name, all):
  disks = get_disks()
  if all:
    for disk in disks:
      click.echo("-"*30)
      print_disk_info(disk)
    click.echo("-"*30)
  else:
    if not name:
      click.echo("Disk name is required if --all is not specified.")
      return
    name_lower = name.lower()
    disk_by_model = next((d for d in disks if d.get('model', '').lower() == name_lower), None)
    if disk_by_model:
      print_disk_info(disk_by_model)
    else:
      disk_by_name = next((d for d in disks if d.get('name', '').lower() == name_lower), None)
      if disk_by_name:
        print_disk_info(disk_by_name)
        return
      all_names = [d.get('name', '') for d in disks] + [d.get('model', '') for d in disks]
      all_names = [n for n in all_names if n] 
      
      if all_names:
        closest = get_close_matches(name_lower, [n.lower() for n in all_names], n=3, cutoff=0.6)
        if closest:
          original_matches = [next(n for n in all_names if n.lower() == match) for match in closest]
          click.echo(f"Disk '{name}' not found. Closest matches: {', '.join(original_matches)}")
        else:
          click.echo(f"Disk '{name}' not found.")
      else:
        click.echo(f"Disk '{name}' not found.")
#endregion

if __name__ == "__main__":
  cli()