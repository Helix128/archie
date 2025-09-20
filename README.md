# archie
## A command line tool to make managing your Arch Linux system easier

# Features
- Global environment variable management
- Disk info visualization

# Installation
## Installation using pipx:
```bash
pipx install git+https://github.com/Helix128/archie.git
```

# Usage
```bash
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

# Show detailed info about a specific disk
archie disk info <name>
```

# Why?
I began using Arch (btw) recently and while it has a **ton** of tools available to configure the system, there is no such thing as a tool for editing env variables *"quickly"* (by quickly, i mean not needing me to manually go to the file and edit it myself). So I made this tool to do just that. 
I game on Linux and one of the first things i had to do was set up an env variable to give my GPU a bigger shader cache, and found it a bit tedious to do it manually. Call it laziness if you want, I just wanted a quick way to do it and I hope this tool can help you as well.

# Note
While this tool only features an environment variable manager as of now, and it should work on Linux distros other than Arch, I can't guarantee I wont add Arch-specific features in the future.

In loving memory of my aunt's late dog, **Archie**.