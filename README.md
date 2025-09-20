# archie
## A command line tool to make managing your Linux system easier

# Features
- User environment variable management
- Disk info visualization

# Installation
## Installation using pipx:
```bash
pipx install git+https://github.com/Helix128/archie.git
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
```

# Why?
I began using Arch (btw) recently and while it has a **ton** of tools available to configure the system, I did not find a tool for editing env variables *"quickly"* (by quickly, i mean not needing me to manually go to the file and edit it myself, I'm used to the Windows way of doing some things). So at first I made this tool to do just that. Call it laziness if you want (it is), I just wanted a quick way to do it and I hope someone else finds it useful as well. In the end, its a wrapper around some common Linux commands with a bit of extra functionality to make them more readable and noob-friendly.

# Note
While this tool only features an environment variable manager as of now, and it should work on Linux distros other than Arch, I can't guarantee I wont add Arch-specific features in the future.
I'd really love to hear your feedback and suggestions for new features, so feel absolutely free to open an issue or a PR!

In loving memory of my aunt's late dog, **Archie**.

