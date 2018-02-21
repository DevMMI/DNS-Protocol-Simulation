#!/usr/bin/python
import sys, threading, os, random
import socket
import subprocess
import re

def main():
    try:
        address = "206.190.39.42"
        command = "ping -c 1 "+address
        test = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = test.communicate()
        result = out.split(" ")
        for i in range(len(result)):
            word = result[i]
            pattern = 'time=[\d.]*'
            match = re.match(pattern, word, flags=0)
            if match:
                break
        print float(word.split("=")[1])
    except:
        print '0'
        return float(0)
    
        
main()
