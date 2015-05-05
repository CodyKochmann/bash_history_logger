#!/usr/bin/env python
help_string="""
history logger to never lose a command entered in the terminal
author: Cody Kochmann
last updated: Tue May 5 08:52:55 PDT 2015
supported opperating systems: OSX
download the latest version at: https://github.com/CodyKochmann/bash_history_logger
options:
    -v --verbose     verbose output
    -p --print       print the collected command history
    -h --help        print this help string
"""

history_path="/Users/$USER/.bash_history"
log_path = "/Users/$USER/"
log_name = "command_history.log"
log_full_path = log_path + log_name

from os import popen
user=(popen("echo $USER").read()).split("\n")[0]
history_path=history_path.replace("$USER", user)
log_path=log_path.replace("$USER", user)
print log_path

def check_arg(*argv): 
    # checks for multiple arguments in sys.argv
    # By: Cody Kochmann
    from sys import argv as sys_args
    for a in argv:
        if a in sys_args:
            return(True)
    return(False)

VERBOSE=check_arg("-v","--verbose")

def get_file_text(file_path):
    # returns all text from a file. 
    # Warning this may block up scripts for long files.
    with open(file_path,"r") as f:
        return(str(f.read()))


if check_arg("-p","--print"):
    print(get_file_text(log_full_path))
    exit()
if check_arg("-h","--help"):
    print(help_string)
    exit()

def remove_empty_strings(input_array, verbose=False):
    c=0
    for i in list(input_array):
        if(len(i) == ""):
            input_array.remove(i)
            c+=1
    if verbose:
        print("removed %s empty strings" % (str(c)))
    return(input_array)

def check_for_line(line_checked,file_path,verbose=False):
    def ensure_file_in_path(file_path):
        import os
        path = "/".join(file_path.split("/")[:-1])+"/"
        file_name = file_path.split("/")[-1]
        if file_name not in os.listdir(path):
            os.system("touch "+file_path)
    def get_file_text(file_path):
        # returns all text from a file. 
        # Warning this may block up scripts for long files.
        with open(file_path,"r") as f:
            return(str(f.read()))
    def v_print(s):
        if (verbose):
            print(s)

    ensure_file_in_path(file_path)
    file_text = get_file_text(file_path).split('\n')
    if line_checked in file_text:
        v_print("found: "+line_checked)
        return(True)
    v_print("could not find: "+line_checked)
    return(False)

def append_line(line_to_append,file_path,verbose=False):
    if len(line_to_append) < 1:
        return()
    if(verbose):
        print("logging: "+line_to_append)
    last_line = ""
    with open(file_path,"r") as f:
        for line in f:
            last_line=line
    if len(last_line)>0:
        line_to_append="\n"+line_to_append
    with open(file_path,"a") as f:
        f.write(line_to_append)

def sys_command(cmd,return_out=True):
    # one stop shop for running commands in python
    if return_out:
        from os import popen
        return((popen(cmd)).read())
    else:
        from os import system
        system(cmd)



history = get_file_text(history_path).split("\n")
print len(history)
history = remove_empty_strings(history,True)
for i in history:
    if check_for_line(i, log_full_path, VERBOSE) is False:
        append_line(i, log_full_path, VERBOSE)
