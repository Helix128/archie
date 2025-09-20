import json
import click
import subprocess
from platformdirs import user_data_dir
from .cli import APP_NAME
import os

task_file = os.path.join(user_data_dir(APP_NAME), "tasks.json")
def _ensure_task_file_exists():
    if not os.path.exists(task_file):
        os.makedirs(os.path.dirname(task_file), exist_ok=True)
    subprocess.run(['sudo', 'touch', task_file], check=True)

def create_task(name, commands):
    _ensure_task_file_exists()
    tasks = load_tasks()
    if name not in tasks:
        tasks[name] = commands
        save_tasks()
        return True
    else:
        return False
    
def append_task(name, commands):
    _ensure_task_file_exists()
    tasks = load_tasks()
    if name in tasks:
        tasks[name].extend(commands)
        save_tasks()
        return True
    else:
        return False
    
def rename_task(old_name, new_name):
    _ensure_task_file_exists()
    tasks = load_tasks()
    if old_name in tasks and new_name not in tasks:
        tasks[new_name] = tasks.pop(old_name)
        save_tasks()
        return True
    else:
        return False

def delete_task(name):
    _ensure_task_file_exists()
    tasks = load_tasks()
    if name in tasks:
        del tasks[name]
        save_tasks()
        return True
    else:
        return False

def load_tasks():
    _ensure_task_file_exists()
    global tasks
    try:
        with open(task_file, 'r') as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = dict()
    return tasks

def run_task(name):
    tasks = load_tasks()
    if name in tasks:
        for command in tasks[name]:
            click.echo(click.style(f"$ {command}", fg="cyan", bold=True))
            subprocess.run(command, shell=True)
        return True
    else:
        return False

def save_tasks():
    _ensure_task_file_exists()
    content = json.dumps(tasks, indent=4)
    subprocess.run(['sudo', 'tee', task_file], input=content, text=True, check=True, stdout=subprocess.DEVNULL)

def locate_task_file():
    _ensure_task_file_exists()
    return task_file