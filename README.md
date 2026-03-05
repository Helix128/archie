# archie
  A command line tool to make managing your Linux system easier

# Features
- Environment variable management
- Disk info visualization
- Custom command system

# Installation
## Installation using pipx:
```bash
pipx install archie-cli
```

# Example usage
```bash
# See help
archie --help
# or
archie help

# About 
archie info

## Environment module (env)
# List env variables
archie env list

# Add or update an env variable
archie env set TEST_ENV 25 # TEST_ENV=25
archie env set SECRET_KEY my_api_key # SECRET_KEY="my_api_key"
# For string values with spaces, use quotes
archie env set BEST_GAME "Risk of Rain 2" # BEST_GAME="Risk of Rain 2"

## Disk module (disk)
# List available disks
archie disk list

# Show detailed info about all disks
archie disk info --all

## Task module (task)
# List all tasks
archie task list

# Create new tasks
# Single command
archie task set diskinfo "archie disk info --all"

# Multiple commands
archie task set archieinfo "echo Showing Archie info..." "archie info"

# This also works
archie task set "disk all" "archie disk list" "archie disk info --all"

# Run a specific task
archie task run diskinfo 
# same as
archie pls diskinfo

# This also works
archie pls "disk all"

# Find Archie task file (for sharing or manual edits)
archie task locate

```
