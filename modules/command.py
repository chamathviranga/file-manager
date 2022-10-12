import subprocess

class Command:

    def __init__(self) -> None:
        self.name = 'test'


    def run (command_str):
        command_str = command_str
        command = subprocess.Popen([command_str], stdout=subprocess.PIPE, shell=True)
        (output, error) = command.communicate()

        # print(f"\n----------------------\n {output} \n----------------------\n")
        # print(f"\n----------------------\n {error} \n----------------------\n")
        return (output,error)