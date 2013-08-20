from socket import *

targetIP = gethostbyname('localhost')
for i in range(20, 1025):
    s = socket(AF_INET, SOCK_STREAM)
    if s.connect_ex((targetIP, i)) == 0:
        print 'Port %d open' % i
    s.close()
