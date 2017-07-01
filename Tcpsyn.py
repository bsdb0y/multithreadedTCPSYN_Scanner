import threading
from queue import Queue
import time
import socket
import sys
import os
import subprocess

'''def checkid():

	print("This scan requires root privilege!")
	sys.exit(1)
'''
from scapy.all import *
# a print_lock is what is used to prevent "double" modification of shared variables.
# this is used so while one thread is using a variable, others cannot access
# it. Once done, the thread releases the print_lock.
# to use it, you want to specify a print_lock per thing you wish to print_lock.
print_lock = threading.Lock()



target = sys.argv[1]
#ip = socket.gethostbyname(target)


def stealth_scan(port):

	ip = IP(dst=target)
	TCP_SYN = TCP(sport=RandShort(),dport=int(port),flags='S',seq=40) 
	TCP_SYNACK = sr1(ip/TCP_SYN,timeout=0.3,verbose=0) # send packet and wait for the first reply
	if not TCP_SYNACK or TCP_SYNACK.getlayer(TCP).flags != 0x12: # SEQ Number for SYN-ACK
		pass#print "\n"+str(port)+":closed\n" # response from our target aka hostip - expect RST
	else:
		print("\n"+str(port)+":open\n") # response from our target aka hostip - expect SYN-ACK


	





# The threader thread pulls an worker from the queue and processes it
def threader():
	while True:
        # gets an worker from the queue
		worker = q.get()

        # Run the example job with the avail worker in queue (thread)
		stealth_scan(worker)

        # completed with the job
		q.task_done()



        

# Create the queue and threader 
q = Queue()

# how many threads are we going to allow for
for x in range(40):
	t = threading.Thread(target=threader)

     # classifying as a daemon, so they will die when the main dies
	t.daemon = True

     # begins, must come after daemon definition
	t.start()


start = time.time()

# 100 jobs assigned.
for worker in range(int(sys.argv[2]),int(sys.argv[3])):
	q.put(worker)

# wait until the thread terminates.
q.join()


print(('Entire job took:',time.time() - start))
