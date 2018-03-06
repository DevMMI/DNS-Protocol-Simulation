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
	port = 5002


	#create a socket object, SOCK_STREAM for TCP
	sSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sSock.bind((host, port))


	#Listen on the given socket maximum number of connections queued is 20
	sSock.listen(20)

	monitor = threading.Thread(target=monitorQuit, args=[])
	monitor.start()
	global response
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

def userInput():
	print "type (exit) to quit"
	response = raw_input("type (exit) to quit")
	sys.stdout.flush()

def dnsQuery(connectionSock, srcAddress):
	# definitions
	path = "DNS_mapping.txt"
	sys.stdout.flush()
	# Check if dns directory exists, else make it
	if not os.path.isfile(path):
		fa = open("DNS_mapping.txt", 'w')
		fa.close()

	# Receive data from socket
	data = connectionSock.recv(1024) # Receive host from server.
	if not data: # improper host
		errorMessage = "Invalid format"
		connectionSock.send(errorMessage)
		return

	try:
		myFile = open(path, 'r') # file is opened
		# check the DNS_mapping.txt to see if the host name exists
		line = parseLocalCache(myFile, data)
		if line is not None: # Cache line was found
			arr = line.split(":")
			if len(arr) > 2: # Cache line has multiple ip's
				ip = dnsSelection(arr[1:])
			else:
				ip = arr[1]
			if ip == "Can't Be Resolved\n":
				errorMessage = "Host not found\n"
				connectionSock.send(errorMessage)
				return
			else:
				response = "Local DNS:"+data+":"+ip+"\n"
				connectionSock.send(response)
				return
	except IOError:
		print "File Open Error\n"
		file = open(path, 'w')
	sys.stdout.flush()
	# looked for host in local cache,
	# Host not cached, escalate to DNS system
	try:
		queryIP = socket.gethostbyname(data)
	except socket.gaierror, err:
		errorMessage = "Host not found"
		#print "Sending error message"

		try:
			fa = open("DNS_mapping.txt", "a")
			fa.write(data+":"+"Can't Be Resolved\n")
			fa.close()
			connectionSock.send(errorMessage)
			return
		except IOError:
			fa = open("DNS_mapping.txt", 'w')
			fa.write(data+":"+"Can't Be Resolved\n")
			fa.close()
			connectionSock.send(response)
			return

	# found hostname IP address
	response = "Root DNS:"+data+":"+queryIP+"\n"
	try:
		fa = open("DNS_mapping.txt", "a")
		fa.write(data+":"+queryIP+"\n")
		fa.close()
		connectionSock.send(response)
	except IOError:
		fa = open("DNS_mapping.txt", 'w')
		fa.write(data+":"+queryIP+"\n")
		fa.close()
		connectionSock.send(response)

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
				return float(word.split("=")[1])
				break
	except:
		return float(10000)

def dnsSelection(ipList):
	#print "Hi"
	maxName = ""
	maxPing = float(10000)
	for i in range(len(ipList)):
		ip = ipList[i].strip()
		val = getPing(ip)
		#print "Comparison"
		#print ip, " : ", val
		if val < maxPing:
			maxName = ip
			maxPing = val
	#print maxName
	return maxName
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
