#!/usr/bin/python
# Spring 2018 CSci4211: Introduction to Computer Networks
# This program serves as the server of DNS query.
# Written in Python v2.

import sys, threading, os, random
import socket
import subprocess
import re

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
	path = "DNS_mapping.txt"

	# Check if dns directory exists, else make it
	if not os.path.isfile(path):
		os.makedirs(path)
	else:
		localCacheExists = True

	# Receive data from socket
	data = connectionSock.recv(1024) # Receive host from server.
	if not data: # improper host
		print "improper host sent over: "
		errorMessage = "Invalid format"
		cSock.send(errorMessage)
		return

	# Find DNS
	if localCacheExists:
		ipFound = False
		try:
			file = open(path, 'r')
		except IOError:
			print "File Open Error\n"
			file = open(path, 'w')
	else:

		# look for host in local cache
		try:
			myFile = open(path, 'r')
			localCacheExists = True
		except IOError:
			print "error opening file"
			localCacheExists = False
			sys.exit(-1)

		# file is opened
		# check the DNS_mapping.txt to see if the host name exists
		line = parseLocalCache(myFile, data)
		if line is not None: # Cache line was found
			ipFound = True
			arr = line.split(":")
			if len(arr) > 2: # Cache line has multiple ip's
				ip = dnsSelection(arr[1:])
			response = "Local DNS:",data,": ",ip
			cSock.send(response)
		else:
			# Host not cached, escalate to DNS system
			try:
				queryIP = gethostbyname(data)
			except socket.gaierror, err:
				print "cannot resolve hostname: ", data, error
				errorMessage = "Host not found"
				cSock.send(errorMessage)
				return

			# found hostname IP address
			response = "Public DNS:",data,": ",queryIP
			cSock.send(response)
	#set local file cache to predetermined file.

        #if it does exist, read the file line by line to look for a
        #match with the query sent from the client
        #If match, use the entry in cache.
            #However, we may get multiple IP addresses in cache, so call dnsSelection to select one.
    #If no lines match, query the local machine DNS lookup to get the IP resolution
	#write the response in DNS_mapping.txt
	#print response to the terminal
	#send the response back to the client
	#Close the server socket.

def parseLocalCache(f, data): # returns String or None
	for line in f:
        arr = line.split(":")
		if data == arr[0]:
			f.close()
			return line
	f.close()
	return None

def getPing(address): # returns float, large number if failure, ping value in ms if success
    try:
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
	    return float(word.split("=")[1])
	except:
    	return float(10000)

def dnsSelection(ipList):
	print "Hi"
	maxName = ""
	maxPing = float(10000)
	for i in range(len(ipList)):
		ip = ipList[i].strip()
		host = host.split(':')[0]
		val = getPing(host)
		if val < maxPing:
			maxName = host
			maxPing = val

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
