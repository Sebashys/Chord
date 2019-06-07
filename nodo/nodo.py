import zmq
import hashlib
import os
import sys
import json
import time

K = 160 ## constante de numero de indicadores en la fingertable
MAX = 2**K ## maximo numero permitido
NODOPORT = '5999' ## puerto de comunicacion entre nodos


def hashing(string):
	objetohash = hashlib.sha1(string.encode('utf8'))
	cadena = objetohash.hexdigest()	
	return cadena

def main():# argv1 : nodoID  argv2 : ipnodo argv3 : ipconexion 
	
	if(len(sys.argv)==4):
		
		#______/ argumentos \__________#
		idHash = hashing(sys.argv[1])
		ipNodo = sys.argv[2]
		ipNodoConn = sys.argv[3]
		
		
		#___________________/ caracterizacion argumentos \____________#
		tcpNodo = 'tcp://'+ipNodo+':' + NODOPORT
		tcpNodoConn = 'tcp://'+ipNodoConn+':'+ NODOPORT
		
		
		#_________/ otros datos del nodo \________#
		miID = {'id':idHash,'name':tcpNodo}
		fingertable = {}
		start = {}
		for i in range(K):
			start[i] = hex(int(idHash,16) +(2**i) % (2**K)) ## formula para los identificadores de la fingertable del nodo (% para simular el anillo)
			print (start[i])             
			
			
		#__________/ Router del nodo  \_________#
		contextR = zmq.Context()
		sockrouter = contextR.socket(zmq.ROUTER)
		sockrouter.bind("tcp://*:"+ NODOPORT) 
		
				
		#__________/ primer dealer del nodo \_____________#
		context = zmq.Context()
		sock = context.socket(zmq.DEALER)
		sock.identity = idHash.encode('utf8')
		sock.connect(nodosConectados['Sucesor']['name'])
		
		#_____________/ poller \_______________#
		poller = zmq.Poller()
		poller.register(sys.stdin, zmq.POLLIN)
		poller.register(sock, zmq.POLLIN)
		poller.register(sockrouter,zmq.POLLIN)
		
		
		
		
		
if __name__ == '__main__':
    main()
