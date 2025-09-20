# archie
## A command line tool to make managing your Linux system easier

# Features
- Environment variable management
- Disk info visualization
- Custom tasks

# Installation
## Installation using pipx:
```bash
pipx install archie-cli
```

# Usage
```python
# Help
archie --help

## Environment module (env)
# List env variables
archie env list

# Add or update an env variable
archie env set <key> <value>

## Disk module (disk)
# List available disks
archie disk list

# Show detailed info about all disks
archie disk info --all

## Task module (task)
# List all tasks
archie task list

# Create a new task
archie task create <task_name> <command1> [<command2> ...]

# Run a specific task
archie task run <task_name> 
# OR
archie pls <task_name>

```

# Why?
I began using Arch (btw) recently and while it has a **ton** of tools available to configure the system, I did not find a tool for editing env variables *"quickly"* (by quickly, i mean not needing me to manually go to the file and edit it myself, I'm used to the Windows way of doing some things). So at first I made this tool to do just that. Call it laziness if you want (it is), I just wanted a quick way to do it and I hope someone else finds it useful as well. In the end, its a wrapper around some common Linux commands with a bit of extra functionality to make them more readable and noob-friendly.

# Note
This tool doesn't have many features as of now and it should work on most Linux distros other than Arch, but I can't guarantee I wont add Arch-specific features in the future.
I'd really love to hear your feedback and suggestions for new features, so feel absolutely free to open an issue or a PR!

