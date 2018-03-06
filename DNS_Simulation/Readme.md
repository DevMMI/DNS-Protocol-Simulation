# Project
Implement a simulation of a DNS server and client to better understand how the DNS protocol works


# To Run
Run the server and then the client
Type a Domain name into the client
You will receive an IP address from the server
Server will use cached IP addresses if possible, if not it will function as a recursive DNS server and will return an authoritative answer. The answer will be cached for the next time. 
Special feature: if two or more IP address are cached for a domain name, it will ping and return the IP address will the lowest latency

python 2.7
