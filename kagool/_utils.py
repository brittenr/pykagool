import subprocess


def process_cmd(command: str, **kwargs):
    subprocess_list = command.split(" ")

    output = subprocess.check_output(subprocess_list, kwargs)

    return output.decode("ascii").strip()
