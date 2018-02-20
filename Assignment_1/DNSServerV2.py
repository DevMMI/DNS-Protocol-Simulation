#!/usr/bin/python
# Spring 2018 CSci4211: Introduction to Computer Networks
# This program serves as the server of DNS query.
# Written in Python v2.

import sys, threading, os, random
import socket

def main():
	host = "localhost" # Hostname. It can be changed to anything you desire.
	#port = 5001 # Port number.
	port = 5005


	#create a socket object, SOCK_STREAM for TCP
	sSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sSock.bind((host, port))


	#Listen on the given socket maximum number of connections queued is 20
	sSock.listen(20)

	monitor = threading.Thread(target=monitorQuit, args=[])
	monitor.start()

	print "Server is listening..."
	while 1:
		#blocked until a remote machine connects to the local port 5001
		try:
			connectionSock, addr = sSock.accept()
			server = threading.Thread(target=dnsQuery, args=[connectionSock, addr[0]])
			server.start()
		except KeyboardInterrupt:
			sSock.close()
			print "\nClosed Port\n"
			break

	print "(Ctrl Z) to end the program"

def dnsQuery(connectionSock, srcAddress):
	# definitions
	localCacheExists = False
	path = "./dns/",srcAddress

	# Check if directory exists, else make it
	if not os.path.isdir(path):
		os.makedirs(path)
	else:
		localCacheExists = True

	# Receive data from socket
	data = connectionSock.recv(1024) # Receive from server.
	# Find DNS
	if localCacheExists:
		ipFound = False
		# look for host in local cache
		try:
			file = open(path, 'r')
		except IOError:
			print "File Open Error\n"
	else:
		# query DNS system


	try:
		#file = open(fn, 'r')
		localCacheExists = True
	except: #IOError:
		print "error"
		#file = open(fn, 'w')

	if localCacheExists:
		#ip_address = parseLocalCache()
		print "hi"
	else:
		print "hello"

	#check the DNS_mapping.txt to see if the host name exists
	#set local file cache to predetermined file.
        #create file if it doesn't exist
        #if it does exist, read the file line by line to look for a
        #match with the query sent from the client
        #If match, use the entry in cache.
            #However, we may get multiple IP addresses in cache, so call dnsSelection to select one.
    #If no lines match, query the local machine DNS lookup to get the IP resolution
	#write the response in DNS_mapping.txt
	#print response to the terminal
	#send the response back to the client
	#Close the server socket.

def dnsSelection(ipList):
	print "Hi"
	#checking the number of IP addresses in the cache
	#if there is only one IP address, return the IP address
	#if there are multiple IP addresses, select one and return.
	##bonus project: return the IP address according to the Ping value for better performance (lower latency)

def monitorQuit():
	while 1:
		sentence = raw_input()
		if sentence == "exit":
			os.kill(os.getpid(),9)

main()
