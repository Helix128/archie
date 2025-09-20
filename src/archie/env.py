import subprocess

env_file = "/etc/environment"

def list_env_vars():
    try:
        with open(env_file, 'r') as file:
            return [line.strip() for line in file if '=' in line and not line.strip().startswith('#')]
    except FileNotFoundError:
        return []

def get_env_var(var_name):
    try:
        with open(env_file, 'r') as file:
            for line in file:
                if line.startswith(f"{var_name}="):
                    return line.strip().split('=', 1)[1].strip('"')
    except FileNotFoundError:
        pass
    return None

def set_env_var(var_name, var_value):
    lines = []
    found = False
    try:
        with open(env_file, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.startswith(f"{var_name}="):
                    lines[i] = f'{var_name}="{var_value}"\n'
                    found = True
                    break
    except FileNotFoundError:
        pass

    if not found:
        lines.append(f'{var_name}="{var_value}"\n')

    content = ''.join(lines)
    subprocess.run(['sudo', 'tee', env_file], input=content, text=True, check=True, stdout=subprocess.DEVNULL)

def del_env_var(var_name):
    lines = []
    try:
        with open(env_file, 'r') as file:
            lines = file.readlines()
            lines = [line for line in lines if not line.startswith(f"{var_name}=")]
    except FileNotFoundError:
        pass

    content = ''.join(lines)
    subprocess.run(['sudo', 'tee', env_file], input=content, text=True, check=True, stdout=subprocess.DEVNULL)