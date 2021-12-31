#!/usr/bin/python3

import os
import subprocess

def cd(path):
    """convert to absolute path and change directory"""
    try:
      if(path!=" "):
        os.chdir(os.path.abspath(path))
      else:
        os.getenv("HOME")
    except Exception:
        err = "An error has occurred\n"
        print(err, file=os.sys.stderr)

def pwd():
    try:
        print(os.getcwd())
    except Exception:
        err = "An error has occurred\n"
        print(err, file=os.sys.stderr)

def batchmode(fichier):
    try :
        with open(fichier,'r') as fichier:
            for line in fichier:
                line=line.strip("\n")
                stderr_fileno = os.sys.stderr.fileno()
                os.write(stderr_fileno, line)
                if line == "exit":
                    os._exit(0)
                elif line[:3] == "cd ":
                    cd(line[3:])
                elif line[:3] == "pwd":
                    pwd()
                elif line == "help":
                    print("sorry, no help")
                else:
                    execute_command(line)
    except:
        err = "An error has occurred\n"
        print(err, file=os.sys.stderr)


def execute_command(command):
    """execute commands and handle piping"""
    try:
        if "|" in command:
            # save for restoring later on
            s_in, s_out = (0, 0)
            s_in = os.dup(0)
            s_out = os.dup(1)

            # first command takes commandut from stdin
            fdin = os.dup(s_in)

            # iterate over all the commands that are piped
            for cmd in command.split("|"):
                # fdin will be stdin if it's the first iteration
                # and the readable end of the pipe if not.
                os.dup2(fdin, 0)
                os.close(fdin)

                # restore stdout if this is the last command
                if cmd == command.split("|")[-1]:
                    fdout = os.dup(s_out)
                else:
                    fdin, fdout = os.pipe()

                # redirect stdout to pipe
                os.dup2(fdout, 1)
                os.close(fdout)

                try:
                    subprocess.run(cmd.strip().split(),shell=True)
                except Exception:
                    print("error: command not found: {}".format(cmd.strip()))

            # restore stdout and stdin
            os.dup2(s_in, 0)
            os.dup2(s_out, 1)
            os.close(s_in)
            os.close(s_out)
        else:
            if "echo" not in command:
                subprocess.run(command.split(" "),shell=True)
            else:
                subprocess.run(command.split(" "))
    except Exception:
        err = "An error has occurred\n"
        print(err, file=os.sys.stderr)



def main():
    print("$ ./mysh")
    while True:
        inp = input("mysh$ ")
        if inp == "exit":
            os._exit(0)
        elif inp[:3] == "cd ":
            cd(inp[3:])
        elif inp[:3] == "pwd":
            pwd()
        elif inp == "help":
            print("sorry, no help")
        elif inp[:1]=="[":
            inp1=inp.strip("[")
            inp2=inp1.strip("]")
            batchmode(inp2)
        else:
            execute_command(inp)


main()