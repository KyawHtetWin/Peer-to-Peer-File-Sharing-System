"""
TESTED MODULE: Class models a node in a chord protocol based structure
This Chord protocol serves as an implementation of a DHT in a peer to peer system

Code base modifed and pulled from Distributed Systems 3rd edition book
by Steen and Tanenbaum

"""


import channel 
import random, math 
from constChord import * 


class ChordNode:

  # Class constructor
  def __init__(self, chan):                    
    self.chan    = chan                        				 	# Create ref to actual channel 
    self.numberOfBits   = chan.numberOfBits                	    # Num of bits for the ID space 
    self.MAXPROC = chan.MAXPROC                					# Maximum num of processes     
    self.nodeID  = int(self.chan.join('node')) # Find out node identity       
    self.fingerTable      = [None for i in range(self.numberOfBits+1)]   # fingerTable[0] is predecessor 
    self.nodeSet = []                        				    # Nodes discovered so far     


  # method to determine if a key is between a lower bound and upper bound in the network
  def inbetween(self, key, lowerbound, upperbound):                                         
    if lowerbound <= upperbound:                                                            
      return lowerbound <= key and key < upperbound                                         
    else:                                                                     
      return (lowerbound <= key and key < upperbound + self.MAXPROC) or (lowerbound <= key + self.MAXPROC and key < upperbound)                        #-

  # method adds a node with the specifed ID to the internal list of nodes in the set
  def addNode(self, nodeID):                                                  
    self.nodeSet.append(int(nodeID))                                          
    self.nodeSet = list(set(self.nodeSet))                                    
    self.nodeSet.sort()                                                       


  # method deletes a specified node from the internal list
  def delNode(self, nodeID):                                                  
    assert nodeID in self.nodeSet, ''       # check id node is in set                                  
    del self.nodeSet[self.nodeSet.index(nodeID)]   	# delete node at index of specified id                           
    self.nodeSet.sort()                          #sort the list                             


  # method used to create and maintain a finger table for each node to facilitate with 
  # resolving the key k. Lookup speed with this algo is O(log(N))
  # fingers of a node are effectively calculated succesors from that node position in the chord
  def finger(self, i):
    succesor = (self.nodeID + pow(2, i-1)) % self.MAXPROC    # succesor(p+2^(i-1)) is algorithm from book
    lowerboundIndex = self.nodeSet.index(self.nodeID)               # own index in nodeset
    upperboundIndex = (lowerboundIndex + 1) % len(self.nodeSet)                # index next neighbor
    for k in range(len(self.nodeSet)):                   # go through all segments
      if self.inbetween(succesor, self.nodeSet[lowerboundIndex]+1, self.nodeSet[upperboundIndex]+1):
        return self.nodeSet[upperboundIndex]                        # found successor
      (lowerboundIndex,upperboundIndex) = (upperboundIndex, (upperboundIndex+1) % len(self.nodeSet)) # go to next segment
    return None                                                                


  # method recomputes finger table if the node network has changed 
  def recomputeFingerTable(self):
    self.fingerTable[0]  = self.nodeSet[self.nodeSet.index(self.nodeID)-1] # Predecessor
    self.fingerTable[1:] = [self.finger(i) for i in range(1,self.numberOfBits+1)] # Successors


  # method computer local succesor node of given key
  def localSuccNode(self, key): 
    if self.inbetween(key, self.fingerTable[0]+1, self.nodeID+1): # key in (fingerTable[0],self]
      return self.nodeID                                 # node is responsible
    elif self.inbetween(key, self.nodeID+1, self.fingerTable[1]): # key in (self,fingerTable[1]]
      return self.fingerTable[1]                                  # successor responsible
    for i in range(1, self.numberOfBits+1):                     # go through rest of fingerTable
      if self.inbetween(key, self.fingerTable[i], self.fingerTable[(i+1) % self.numberOfBits]):
        return self.fingerTable[i]                                # key in [fingerTable[i],fingerTable[i+1]) 


  # run the chord network
  def run(self): 
    self.chan.bind(self.nodeID) 	# bind channel to node id
    self.addNode(self.nodeID) 		# add node with given node id
    others = list(self.chan.channel.smembers('node') - set([str(self.nodeID)])) 
    for i in others: 	# iterate through list of others and add node
      self.addNode(i) 
      self.chan.sendTo([i], (JOIN)) 
    self.recomputeFingerTable() # recompute finger table as needed
 

    while True: 
      message = self.chan.recvFromAny() # Wait for any request 
      sender  = message[0]              # Identify the sender 
      request = message[1]              # And the actual request 
      if request[0] != LEAVE and self.chan.channel.sismember('node',str(sender)): 
        self.addNode(sender) # add node if req's met
      if request[0] == STOP: 
        break 
      if request[0] == LOOKUP_REQ:                       # A lookup request 
        nextID = self.localSuccNode(request[1])          # look up next node 
        self.chan.sendTo([sender], (LOOKUP_REP, nextID)) # return to sender 
        if not self.chan.exists(nextID): 
          self.delNode(nextID) 
      elif request[0] == JOIN: 
        continue 
      elif request[0] == LEAVE: 
        self.delNode(sender) 
      self.recomputeFingerTable() 
    print 'fingerTable[','%04d'%self.nodeID,']: ',['%04d' % k for k in self.fingerTable] 
 




