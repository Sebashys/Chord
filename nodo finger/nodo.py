import random

k = 6
MAX = 2**k


def decr(value,size):
    if size <= value:
        return value - size
    else:
        return MAX-(size-value)
        

def between(value,init,end):
    if init == end:
        return True
    elif init > end : ##si el id inicial es mayor que el final
        shift = MAX - init
        init = 0
        end = (end +shift)%MAX
        value = (value + shift)%MAX # cambio de valor para comparar
    return init < value < end

def Ebetween(value,init,end):
    if value == init:
        return True
    else:
        return between(value,init,end)

def betweenE(value,init,end):
    if value == end:
        return True
    else:
        return between(value,init,end)

	

class Node:
    def __init__(self,id):
        self.id = id
        self.finger = {}
        self.start = {}
        for i in range(k):
            self.start[i] = (self.id+(2**i)) % (2**k) ## formula para los identificadores de la fingertable del nodo (% para simular el anillo)
                     
        print(self.start)

    def successor(self):
        return self.finger[0] # susesor en la finger[0]
    
    def find_successor(self,id):  
        if betweenE(id,self.predecessor.id,self.id): ## si la id dada esta entre el predecesor y yo
            return self
        n = self.find_predecessor(id) ## busca alguien anterior a mi en la finger con esa id
        return n.successor()
    
    def find_predecessor(self,id): ## busca alguien anterior a mi en la finger con esa id
        if id == self.id: ## si la id dada es mi misma id toma el predecesor
            return self.predecessor
        n1 = self
        while not betweenE(id,n1.id,n1.successor().id):## mientras la id dada no este entre el sucesor y yo
            n1 = n1.closest_preceding_finger(id)
        return n1
    
    def closest_preceding_finger(self,id):##buscamos en la finger quien podria ser ese sucesor
        for i in range(k-1,-1,-1):
            if between(self.finger[i].id,self.id,id):## comprobamos si las finger lo apuntan
                return self.finger[i] ## retornamos alguna finger que podria contenerlo
        return self # si no retornamos el mismo nodo ya que se debe encontrar alli
        
    
    def join(self,n1): # agrupamos nodos
        if self == n1: ## si se conecta a el mismo
            for i in range(k):
                self.finger[i] = self
            self.predecessor = self
        else: ## si se conecta a otro
            self.init_finger_table(n1)
            self.update_others()  
           
            
    def init_finger_table(self,n1): ## inicializacion de la fingertable
		
        self.finger[0] = n1.find_successor(self.start[0]) ## encuentra un sucesor para los indicaores de la finger
        self.predecessor = self.successor().predecessor
        self.successor().predecessor = self 
        self.predecessor.finger[0] = self
        for i in range(k-1):
            if Ebetween(self.start[i+1],self.id,self.finger[i].id):
                self.finger[i+1] = self.finger[i] ## el siguiente indicador era el anterior indicador
            else :
                self.finger[i+1] = n1.find_successor(self.start[i+1]) ## el indicador encontrara un sucesor para la finger
 
    def update_others(self):
        for i in range(k):
            prev  = decr(self.id,2**i)
            p = self.find_predecessor(prev)
            if prev == p.successor().id:
                p = p.successor()
            p.update_finger_table(self,i)
            
    def update_finger_table(self,s,i):
        if Ebetween(s.id,self.id,self.finger[i].id) and self.id!=s.id:
                self.finger[i] = s
                p = self.predecessor
                p.update_finger_table(s,i)

    def setSuccessor(self,succ):
        self.finger[0] = succ


def hash(line): ## se hashea una linea
    import sha
    key=long(sha.new(line).hexdigest(),16)
    return key ## hexadecimal
    

def id(): ## id random uniforme entre 0 y 2**k
    return long(random.uniform(0,2**k))


def printNodes(node): ## imprime nodos
    print (' Ring nodes:')
    end = node
    print (node.id)
    while end != node.successor():
        node = node.successor()
        print (node.id)
    print ('-----------')

def showFinger(node): #muestra la finger de un nodo
    print ('Finger table of node' + str(node.id))
    print ('start:node')
    for i in range(k):
        print ( str(node.start[i])+  ":" +str(node.finger[i].id) ) 
    print ('-----------')

def main():
	# author: Pedro Garcia Lopez, PhD
    




    n1 = Node(1)
    n2 = Node(8)
    n3 = Node(14)
    n4 = Node(21)
    n5 = Node(32)
    n6 = Node(38)
    n7 = Node(42)
    n8 = Node(48)
    n9 = Node(51)
    n10 = Node(56)
    
        
    n1.join(n1)
    n2.join(n1)
    n3.join(n1)
    n4.join(n1)
    n5.join(n1)
    n6.join(n1)
    n7.join(n1)
    n8.join(n1)
    n9.join(n1)
    n10.join(n1)
       
    
    showFinger(n1)
    showFinger(n2)
    showFinger(n3)
    printNodes(n1)
    
 
   

    



if __name__ == "__main__":

    main()
