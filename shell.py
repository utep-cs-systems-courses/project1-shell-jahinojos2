import os, sys, re

def main():
    while True:
        command = input("$ ")
        if command == "exit":
            break
        elif command[:3] == "cd ":
            psh_cd(command[3:])
        elif (command.find(">") != -1):
            redirect_command(command)
        else:
            execute_commands(command)

def execute_commands(command):
    rc = os.fork()
    if rc < 0:
        sys.exit(1)

    elif rc == 0:
        if "|" in command:
            stdin, stdout = (0, 0)
            stdin = os.dup(0)
            stdout = os.dup(1)

            fileIn = os.dup(stdout)

            for cmd in command.split("|"):
                os.dup2(fileIn, 0)
                os.close(fileIn)
                if cmd == command.split("|")[-1]:
                    fileOut = os.dup(stdout)
                else:
                    fileIn, fileOut = os.pipe()

                os.dup2(fileOut, 1)
                os.close(fileOut)

                try:
                    print("It has been piped")

                except Exception:
                    pass
        else:
            args = [command.strip().split()[0]]
            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program, args, os.environ)
                except FileNotFoundError:
                    pass
            os.write(2, ("%s: command not found\n" % args[0]).encode())
            sys.exit(1)
    else:
        os.wait()

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
        os.chdir(os.path.abspath(command))
    except Exception:
        print("cd: no such file or direcory: {}".format(command))

if '__main__' == __name__:
    main()
