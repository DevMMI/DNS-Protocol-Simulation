#!/usr/bin/python
# Spring 2018 CSci4211: Introduction to Computer Networks
# This program serves as the client of DNS query.
# Written in Python v2.

import sys
from socket import *

def main():
	while 1:
		print "Type in a domain name to query, or 'q' to quit:"
		while 1:
			st = raw_input() # Get input from users.
			if st == "":
				continue
			else:
				break
		if st == "q" or  st == "Q":

			sys.exit(1) # If input is "q" or "Q", quit the program.
		else:
			host = "localhost" # Remote hostname. It can be changed to anything you desire.
			port = 5001 # Port number.

			try:
				cSock = socket(AF_INET, SOCK_STREAM)
			except error as msg:
				cSock = None # Handle exception

			try:
				cSock.connect((host, port))
			except error as msg:
				cSock = None # Handle exception

			if cSock is None:
				print "Error: cannot open socket"
				sys.exit(1) # If the socket cannot be opened, quit the program.
			print st
			cSock.send(st) # Otherwise, send the input to server.
			data = cSock.recv(1024) # Receive from server.
			print "Received:", data # Print out the result.
			cSock.close()

main()
