Intro to Networks
Assignment 1
02/21/2018

  The structure of my server program is as follows, in the main loop, for each client connection a thread is made.
That thread receives a hostname from the client, it then proceeds to check the DNS_mapping.txt file for an entry
that matches the received hostname, if it finds one, it handles it by sending it over directly if there is only
one matching IP address, and finding the best IP address through pinging if there are more than one. Either way the
thread returns from it's operation.
  If the local DNS search comes up empty, the thread continues. It will not query the root DNS for an IP address to match
the hostname, it will add that IP address to the DNS table (if it doesn't resolve, then it'll add 'Can't be resolved'
entry to the DNS table). It will send whatever it found ('can't be resolved' or IP address) to the client, then the
thread will close.
  The server has a single port which can be connected to by multiple clients, because of the multithreading that is included
in the server, one port can juggle multiple socket connections. Thereby servicing multiple clients simultaneously, that is the
purpose of multithreading, a thread can be sent off to handle any given client connection with its own socket connection.
We handle multiple threads by having them execute the service independently per their own client.
