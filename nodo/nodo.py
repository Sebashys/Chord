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
		predecesor = None ## predecesor sin definir
		sucesor = None ## sucesor sin definir
		
			
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
		
		
		#______________________/ funciones despues de iniciar un nodo\_________________________________#
		def successor():
			return fingertable[0] # susesor en la finger[0]
			
		def find_successor(Aid):  
			if betweenE(Aid, predecesor ,idHash): ## si la id dada esta entre el predecesor y yo
				return idHash # el susesor soy yo
			n = self.find_predecessor(id) ## busca alguien anterior a mi en la finger con esa id
			return n.successor()
    
		def find_predecessor(Aid): ## busca alguien anterior a mi en la finger con esa id
			if Aid == idHash: ## si la id dada es mi misma id toma el predecesor
				return predecesor
			proxyId = idHash
			proxySucesor = sucesor
			while not betweenE(Aid,proxyId,proxySucesor):## mientras la id dada no este entre mi sucesor y yo
				proxyId, proxySucesor  = closest_preceding_finger(Aid) ## retoma otras proxy ID y sucesor para ubicar esa id
			return n1
		
		def closest_preceding_finger(Aid): ## funcion para revisar quien sigue en la fingertable
			 ##### aqui se debe implementar saltos en la finger y conexiones con estos ###
		
		
if __name__ == '__main__':
    main()
