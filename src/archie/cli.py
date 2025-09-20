import click
import importlib.metadata
from difflib import get_close_matches

APP_NAME = "archie-cli"

# archie modules
from .env import *
from .disk import *
from .task import *

@click.group()
def cli():
  pass

#region core
@cli.command()
def version():
  """Get installed Archie version."""
  click.echo(f"{importlib.metadata.version(APP_NAME)}")

@cli.command()
def help():
  """Show this message and exit."""
  click.echo(cli.get_help(click.Context(cli)))

@cli.command()
def about():
  """About Archie."""
  click.echo(click.style("Archie version: ", fg="cyan"), nl=False)
  click.echo(f"{importlib.metadata.version(APP_NAME)}")
  click.echo(click.style("GitHub repo: ", fg="cyan"), nl=False)
  click.echo("https://github.com/helix128/archie")
  click.echo("Made with <3 by ",nl=False)
  click.echo(click.style("Helix128", fg="blue"))

#endregion
#region env
@cli.group()
def env():
  """Manage environment variables."""
  pass

@env.command()
@click.argument("key")
def get(key):
  """Get an environment variable value."""
  result = get_env_var(key)
  if result is not None:
    click.echo(click.style(f"{result}", fg="white"))
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
      varName = var.split('=', 1)[0].strip()
      varValue = var.split('=', 1)[1].strip().strip('"')
      click.echo(click.style(f"{varName}={varValue}", fg="white"))
      
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
  """Show detailed information about a disk."""
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
          if len(closest) == 1:
            original_match = next(n for n in all_names if n.lower() == closest[0])
            matching_disk = next((d for d in disks if d.get('name', '').lower() == closest[0] or d.get('model', '').lower() == closest[0]), None)
            if matching_disk:
              click.echo(f"Did you mean '{original_match}'? Showing info:")
              print_disk_info(matching_disk)
            return
          original_matches = [next(n for n in all_names if n.lower() == match) for match in closest]
          click.echo(f"Disk '{name}' not found. Closest matches: {', '.join(original_matches)}")
        else:
          click.echo(f"Disk '{name}' not found.")
      else:
        click.echo(f"Disk '{name}' not found.")
#endregion
#region task
@cli.group()
def task():
  """Manage custom tasks."""
  pass

@task.command()
def locate():
  """Open the task configuration file."""
  task_file = locate_task_file()
  click.echo(click.style(f"Task configuration file located at: {task_file}", fg="white"))

@task.command()
@click.argument("name")
@click.argument("commands",nargs=-1)
def set(name, commands):
  """Create a new task or overwrite an existing one."""
  if create_task(name, commands):
    click.echo(click.style(f"Task '{name}' defined with command(s): {', '.join(commands)}", fg="white"))
  else:
    click.echo(click.style(f"Task '{name}' already exists.", fg="red"))

@task.command()
@click.argument("name")
@click.argument("commands", nargs=-1)
def append(name, commands):
  """Append a command to an existing task."""
  if append_task(name, commands):
    click.echo(click.style(f"Appended command(s) to task '{name}': {commands}", fg="white"))
  else:
    click.echo(click.style(f"Task '{name}' not found.", fg="red"))

@task.command()
@click.argument("old_name")
@click.argument("new_name")
def rename(old_name, new_name):
  """Rename an existing task."""
  if rename_task(old_name, new_name):
    click.echo(click.style(f"Task '{old_name}' renamed to '{new_name}'.", fg="white"))
  else:
    click.echo(click.style(f"Task '{old_name}' not found or '{new_name}' already exists.", fg="red"))

@task.command()
@click.argument("name")
def delete(name):
  """Delete an existing task."""
  if delete_task(name):
    click.echo(click.style(f"Task '{name}' deleted.", fg="white"))
  else:
    click.echo(click.style(f"Task '{name}' not found.", fg="red"))

@task.command()
def list():
  """List all tasks."""
  tasks = load_tasks()
  if tasks:
    click.echo(f"Found ",nl=False)
    click.echo(click.style(f"{len(tasks)}", fg="cyan"), nl=False)
    click.echo(" task(s):")
    for name, commands in tasks.items():
      click.echo(click.style(f"- {name}:", fg="cyan"))
      for cmd in commands:
        click.echo(click.style(f"  - {cmd}", fg="white"))
  else:
    click.echo("No tasks found.")

@task.command()
@click.argument("name")
def run(name):
  """Run a task."""
  if run_task(name):
    click.echo(click.style(f"Task '{name}' done.", fg="white"))
  else:
    click.echo(click.style(f"Task '{name}' not found.", fg="red"))

@cli.command()
@click.argument("name")
def pls(name):
  """Run a task."""
  if run_task(name):
    click.echo(click.style(f"Task '{name}' done.", fg="white"))
  else:
    click.echo(click.style(f"Task '{name}' not found.", fg="red"))

#endregion

if __name__ == "__main__":
  cli()