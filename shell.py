#! /usr/bin/env python3

import os, sys, re

def main():
    while True:
        if 'PS1' in os.environ:
            os.write(1, os.environ['PS1'].encode())
        else:
            os.write(1, ("$ ").encode())
        try:
            command = input()
        except EOFError:
            sys.exit(1)
        command = command.strip()
        if command == "exit":
            break

        elif "cd" in command:
            executable = command.split()
            psh_cd(executable[1])
            if len(executable) > 2:
                for i in range(len(executable), 2):
                    print(executable[i])
                    execute_commands(executable[i])

        elif ">" in command:
            redirect_command(command)
        else:
            command = command.split(" ", 1)
            execute_commands(command)

def execute_commands(command):

    rc = os.fork()
    if rc == 0:
        if command != "":
            try:  # in case the whole path is given
                os.execve(command[0], command, os.environ)
            except FileNotFoundError:
                pass
            for dir in re.split(":", os.environ["PATH"]):  # searches for the program in PATH
                program = "%s/%s" % (dir, command[0])
                try:
                    os.execve(program, command, os.environ)
                except FileNotFoundError:
                    pass
            print(command[0] + ": command not found.")

def redirect_command(command):
    rc = os.fork()
    if rc < 0:
        sys.exit(1)

    elif rc == 0:
        args = [command.strip().split()[0]]

        os.close(1)
        sys.stdout = open(command.strip().split()[2], "w")
        os.set_inheritable(1, True)

        for dir in re.split(":", os.environ['PATH']):
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ)
            except FileNotFoundError:
                pass

        os.write(2, ("%s: command not found\n" % args[0]).encode())
        os.wait()
        sys.exit(1)
    else:
        childPidCode = os.wait()


def psh_cd(command):
    """convert to absolute path change directory"""
    try:
        os.chdir(command)
    except Exception:
        os.write(2, "cd: no such file or directory".encode())

if '__main__' == __name__:
    main()
