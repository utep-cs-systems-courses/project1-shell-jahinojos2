import os, sys, re
import subprocess
def main():
    while True:
        command = input("$ ")
        if command == "exit":
            break
        elif command == "help":
            print("psh: simple shell written in python")
        elif command[:3] == "cd ":
            psh_cd(command[3:])
        else:
            execute_commands(command)

def execute_commands(command):
    try:
        subprocess.run(command.split())

    except Exception:
        print("psh: command not found: {}".format(command))

def psh_cd(command):
    """convert to absolute path change directory"""
    try:
        os.chdir(os.path.abspath(command))
    except Exception:
        print("cd: no such file or direcory: {}".format(command))

if '__main__' == __name__:
    main()
