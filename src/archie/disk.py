import json
import subprocess

import click
def parse_size_to_bytes(size_str):
    if not size_str:
        return 0

    size_str = size_str.strip().upper()
    if size_str[-1].isdigit():
        return int(size_str)

    multipliers = {'K': 1024, 'M': 1024**2, 'G': 1024**3, 'T': 1024**4}
    unit = size_str[-1]
    number_str = size_str[:-1].replace(',', '.')
    number = float(number_str)

    return int(number * multipliers.get(unit, 1))

def parse_bytes(size_bytes):
    if size_bytes < 0:
        return "0B"
    elif size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024**2:
        return f"{size_bytes / 1024:.2f}K"
    elif size_bytes < 1024**3:
        return f"{size_bytes / 1024**2:.2f}M"
    elif size_bytes < 1024**4:
        return f"{size_bytes / 1024**3:.2f}G"
    else:
        return f"{size_bytes / 1024**4:.2f}T"
    

def get_disks():
    output = subprocess.check_output(["lsblk", "-J", "-o", "NAME,SIZE,MODEL,MOUNTPOINT"]).decode()
    data = json.loads(output)
    disks = []

    for disk in data["blockdevices"]:
        disk_size = parse_size_to_bytes(disk["size"])
        
        disk_obj = {
            "name": disk["name"].upper(),
            "model": disk.get("model", "") or "Unknown",
            "used": 0,
            "size": disk_size,
            "partitions": []
        }
        
        total_used = 0
        
        if "children" in disk:
            for partition in disk["children"]:
                partition_size = parse_size_to_bytes(partition["size"])
                partition_used = 0
                
                partition_obj = { 
                    "name": partition["name"].upper(),
                    "size": partition_size,
                    "mountpoint": partition.get("mountpoint") or "Not mounted",
                    "used": 0
                }
                
                if partition.get("mountpoint"):
                    try:
                        df_output = subprocess.check_output(
                            ["df", "-B1", partition["mountpoint"]], 
                            stderr=subprocess.DEVNULL
                        ).decode().strip().split('\n')[1].split()
                        
                        partition_used = int(df_output[2])
                        
                    except (subprocess.CalledProcessError, IndexError, ValueError):
                        pass
                
                if not partition.get("mountpoint") and partition_size > 0:
                    partition_used = 0 
                
                partition_obj["used"] = partition_used
                total_used += partition_used
                disk_obj["partitions"].append(partition_obj)
        
        disk_obj["used"] = total_used
        disks.append(disk_obj)
    
    return disks


def print_disk_info(disk):
    disk_model = disk["model"]
    disk_name = disk["name"].lower()
    click.echo(click.style(f"{disk_model} ({disk_name})", fg="cyan"))
    disk_size = disk["size"]
    click.echo(f"Size: {parse_bytes(disk_size)}")

    disk_used = disk["used"]
    usage_pct = (disk_used / disk_size * 100) if disk_size > 0 else 0
    usage_color = "white" if usage_pct < 70 else "yellow" if usage_pct < 90 else "red"

    click.echo("Used: ", nl=False)
    click.echo(click.style(f"{parse_bytes(disk_used)} ({usage_pct:.2f}%)", fg=usage_color))
    click.echo(" [", nl=False)

    for i in range(0,20):
        if (i / 20 * 100) < usage_pct:
            click.echo(click.style("▰", fg=usage_color), nl=False)
        else:
            click.echo("▱", nl=False)

    click.echo("]")
    click.echo(f"Partitions:")
    
    disk_partitions = disk["partitions"]
    if disk_partitions:
        for partition in disk_partitions:
            partition_name = partition["name"].lower()
            partition_used = partition["used"]
            partition_size = partition["size"]
            partition_mountpoint = partition["mountpoint"]
            click.echo(f"- {partition_name} ({parse_bytes(partition_used)} / {parse_bytes(partition_size)}) [{partition_mountpoint}]")
    else:
        click.echo(click.style("None", fg="yellow"))