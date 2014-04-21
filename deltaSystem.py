### programs that aid in the investigation of sunflowers.
import random
import networkx as nx

class Spectrum(object):

    def __init__(self):
        self.vectors=[]
        self.repetitions=[]

    def add(self, vec):
        if vec in self.vectors:
            self.repetitions[self.vectors.index(vec)]+=1
        else:
            self.vectors.append(vec)
            self.repetitions.append(1)
    def __str__(self):
        s=""
        for i in range(len(self.repetitions)):
            s+=str(self.vectors[i])+"   "+str(self.repetitions[i])+"\n"
        return s
    def __repr__(self):
        return self.__str__()
    

class SunflowerException(Exception):
    def __init__(self, deltaSystemFree):
        self.deltaSystemFree=deltaSystemFree
    def __str__(self):
        s="The delta system "+ str(self.deltaSystemFree)+" has a sunflower with " + self.deltaSystemFree.sunflowerSize + " petals"
        return s

class PhiException(Exception):
    def __init__(self, deltaSystemFree):
        self.deltaSystemFree=deltaSystemFree
    def __str__(self):
        s="The delta system "+ str(self.deltaSystemFree)+" has a sunflower with " + self.deltaSystemFree.sunflowerSize + " petals"
        return s
    

class FamilyPSets(object):
    """A class to describe a set of sets of all the same size p."""
    def __init__(self,p,mylist=[]):
        
        self.setList=[]
        self.p=p
        self.__typeNameStr__="FamilyPSets"

        
        for i in mylist:
            newset=set(i)
            if len(newset)==p:
                self.setList.append(newset)
        
    def intersectionVector(self, myset):
        assert len(myset)==self.p
        ans=[0]*(len(myset)+1)
        for aset in self.setList:
            x=len(aset.intersection(myset))
            ans[x]+=1
        return ans[:-1]

    def size(self):
        return len(self.setList)

    def sets(self):
        return self.setList
                    

    @staticmethod
    def flattenlist(l):
        """Takes a set of sets and returns the single set that contains all the elements of each of the sets.  In other words
            creates the union of all the sets in the list, l."""

        return list(set([item for sublist in l for item in sublist]))

    @staticmethod
    def nsetmaker(mylist,n):
        """Makes sets of size n from the given list"""
        # this will store the sets as we make them
        ans=[]
        # this is a list containing the various positions that will be used for each set
        # start with the first n and eventually we will end with the last n.
        position=range(n)
        # What is the largest position (+1)
        rollover=len(mylist)
        
            
        while True:
            #create a new set
            newset=[]
            # put the right numbers in
            for i in position:
                newset.append(mylist[i])
            # add set to the final answer
            ans.append(set(newset))
            
            #print "1 ",position
            # if we have the last set then exit
            if position==range(len(mylist)-n,len(mylist)):
                break
            # prepare to change the positions
            flag=True
            # start at the back position
            i=-1
            while flag:
                #print position
                # increment the last position
                position[i]+=1
                # don't let it get too big. if we are reseting an earlier one make all
                # subsequent ones be consecutive.
                if position[i]<len(mylist)+i+1:
                    for j in range(i+1,0):
                        # Found the best place to shift now make everything that comes after
                        # that as small as possible
                        position[j]=position[j-1]+1
                    flag=False
                    #print position
                else:
                    # move to a previous place
                    i-=1
        return ans

    def residue(self,subset):
        newSets=[]
        for myset in self.setList:
            if subset.issubset(myset):
                
                newSets.append(myset-subset)
                #print newSets
        return FamilyPSets(self.p-len(subset),newSets)
    
    def support(self):
        """Finds the list of all the elements in any one of the sets"""
        return FamilyPSets.flattenlist(self.setList)

    def sizeOfSupport(self):
        """How many elements are in the union of the set of sets"""
        return len(self.support())
                           
    def addRandomPSet(self,maxn=100):
        
        flag=True
        
        while flag:
            ans=[]
            for i in range(self.p):
                ans.append(random.randint(1,maxn))
            ans=set(ans)
            if ans not in self.setList:
                self.setList.append(ans)
                flag=False
    def __str__(self):
        mytype=type(self)
        s=""+self.__typeNameStr__ + "\n"
        for myset in self.setList:
            s+=str(myset)+"\n"
        return s

    def __lshift__(self, i):
        if type(i)!=type(1):
            raise TypeError, "Must be an integer shift"
        ansset=[]
        for myset in self.setList:
            newset=[]
            for vertex in myset:
                newset.append(vertex+i)
            ansset.append(set(newset))
        self.setList=ansset

    def __repr__(self):
        return self.__str__()
            
            

class DeltaSystemFree(FamilyPSets):
    """This class is meant to represent a set of sets of a particular size that is free of delta systems of a particulater
number of sets. """

 

    def __init__(self, p, sunflowerSize, mylist=[]):
        FamilyPSets.__init__(self,p,mylist)
        self.sunflowerSize=sunflowerSize
        self.__typeNameStr__="DeltaSystemFree"
        self.__spectrum__=Spectrum()

    @classmethod
    def proj_icosahedron(cls):
        x1 = PhiSets.proj_icosahedron()
        x2 = PhiSets.proj_icosahedron()
        x2<<6
        return x1+x2
    
    @staticmethod
    def dylanExample():
        setList=[[1, 2, 3],[1, 2, 4],[1, 3, 5],[2, 3, 6],[1, 6, 4],[1, 6, 5],[2, 5, 6],[2, 5, 4],[3, 4, 5],[3, 4, 6],[7, 8, 9],[7, 8, 4],[7, 9, 5                      ],[8, 9, 6],[7, 6, 4],[7, 6, 5],[8, 5, 6],[8, 5, 4],[9, 4, 5],[9, 4, 6],[1, 7, 3],[1, 7, 8],[2, 8, 1],[2, 8, 9],[3, 9, 2],[3, 9, 7],[10, 11, 12],[10, 11, 14],[10, 13, 14],[10, 13, 15],[11, 14, 15],[11, 13, 15],[11, 12, 13],[12, 13, 14],[12, 14, 15],[10, 12, 15]]
        return DeltaSystemFree(3,4,setList)

    @staticmethod
    def exoo_phiThreeFour():
        setList=[[1,2,9],[1,3,10],[1,4,7],[1,4,12],[1,7,12],[2,4,8],[2,5,11],[2,7,8],[2,9,12],[3,4,12],[3,6,9],[3,9,11],[4,5,8],[4,8,11],[5,6,9],[5,7,8],[5,9,12],[6,8,10],[7,10,12],[1,3,7],[1,3,12],[1,4,10],[1,6,9],[1,9,11],[2,5,6],[2,6,11],[2,8,10],[3,4,7],[3,5,9],[3,7,10],[3,10,12],[4,7,10],[4,10,12],[5,6,11],[5,8,11],[6,7,8],[6,8,11],[9,11,12]]
        return DeltaSystemFree(3,4,setList)
    
    @staticmethod
    def bestDeltaSystemFree2(n):
        """returns a DeltaSystemFree set of sets with maximum number"""
        if n%2==1:
            x1=PhiSets.bestPhiSetFree2(n)
            x2=PhiSets.bestPhiSetFree2(n)
            x2<<n
            return x1+x2
        

        else:
            ## Create two graphs one K_{n/2 -1} and one with n/2 +1 polygons and f
                    

    
        

    @staticmethod
    def __myhash__(set):
        ans=0L
        for i in set:
            ans+=long(pow(2,i))
        return ans

    @staticmethod
    def IsCliqueOfSize(cliquesize, nxGraph):
        """Determines if there is a clique in a graph of specific size
            inputs are a networkx type graph"""
        #if the graph is  too small for a clique then return false
        if cliquesize>nxGraph.number_of_nodes():
            return False
        #if the graph is so small that a clique is obviously true return true
        if cliquesize==1 and nxGraph.number_of_nodes()>=1:
            print(self.setList[nxGraph.nodes()[0]])
            return True
        else:
            #go through all the nodes that remain and see if one of them is the
            #start of a clique
            for node in nxGraph.nodes():
                if DeltaSystemFree.IsCliqueOfSize(cliquesize-1,nxGraph.subgraph(nxGraph.neighbors(node))):
                    print self.setList[node]
                    return True
        return False
    
    def spectrum(self):
        """Create a dictionary of all the spectrums that exist in the DeltaSystem"""
        
        for i in self.setList:
            self.__spectrum__.add(self.intersectionVector(i))
        return self.__spectrum__
    
    def residue(self,subset):
        """create a DeltaSystemFree that is the residue of a given subset"""
        subset=set(subset)
        fpSets=super(DeltaSystemFree, self).residue(subset)
        return DeltaSystemFree(self.p-len(subset), self.sunflowerSize, fpSets.setList)
                    
    def IsSunflowerFree(self):
        return not self.findSunflower(self.sunflowerSize)
        

    def findSunflower(self, r): # r is the number of petals in the sunflower
        """This method finds if there is a sunflower of size r in the family of sets""" 
        ### create all the intersections and keep track of the intersecting pairs
        self.__createDictIntersection__()
        # create graph to analyze for cliques
        nxGraph=nx.Graph()
        for key in self.DictIntersection:
            #for each possible intersection construct the graph and search for cliques
            nxGraph.add_nodes_from(range(len(self.setList)))
            nxGraph.add_edges_from(self.DictIntersection[key][1])
            if  DeltaSystemFree.IsCliqueOfSize(r, nxGraph):
                return True
            # empty the graph to start over
            nxGraph=nx.empty_graph()
        return False
    
        
##    def fatten(self):
##        
##        support=DeltaSystemFree.flattenlist(self.setList)
##        mymax=max(support)
##        #support+=[mymax+1,mymax+2,mymax+3,mymax+4,mymax+5, mymax+6]
##        nsets=DeltaSystemFree.nsetmaker(support,self.p)
##        for nset in nsets:
##            if nset not in self.setList:
##                self.setList.append(nset)
##                x=self.findSunflower(3)
##                if x==False:
##                    print "Found one",nset
##                else:
##                    self.setList.remove(nset)
                
    def __searchForSetToAdd__(self,support,seed):
        #support=flattenlist(self.setList)
        #mymax=max(support)
        #support+=[mymax+1,mymax+2,mymax+3,mymax+4,mymax+5, mymax+6]
        nsets=DeltaSystemFree.nsetmaker(support,self.p)
        random.seed(seed)
        #for nset in nsets:
        while len(nsets)!=0:
            mynext=random.randint(0,len(allsets)-1)
            
            if nset not in self.setList:
                Flag=True
                for myset in self.setList:
                    if myset.intersection(nset)==set([]):
                        Flag=False
                        break
                if Flag:
                    self.setList.append(nset)
                
                    doesHaveSunflower=self.findSunflower(self.sunflowerSize)
                    if doesHaveSunflower:
                        self.setList.remove(nset)
                    else:
                        return nset
        raise SunflowerException
    

    def fatten(self,seed=10, support=-1):
        """attempt to add another set to the DeltaSystemFree. Will use the support given to it, and a seed for  the random search.
support=-1 indicates that you would like to use the current support."""
        
        try:
            newSet=self.__searchForSetToAdd__(self, support, seed)
            return DeltaSystemFree(self.p, self.sunflowerSize, self.mylist.append(newSet))
        except:
            print("Couldn't find a set that would lead to a sunflower free set")
            return self
        
        
        
    def __createDictIntersection__(self):
        """Creates a dictionary of intersections that can be used to search for sunflowers"""
        # create dictionary to store the number of occurences of various intersections
        self.DictIntersection={}
        # creat graph 
        self.graph=nx.Graph()
        strsetlist=[str(i) for i in self.setList]
        self.graph.add_nodes_from(strsetlist)
        # go through all pairs of sets
        for i in range(len(self.setList)):
            for j in range(i+1, len(self.setList)):
                # find the current intersection
                currentintersection=self.setList[i].intersection(self.setList[j])
                # create a hash of the intersection
                lcurrentint=DeltaSystemFree.__myhash__(currentintersection)
                # there is an intersection
                if lcurrentint!=0:
                    # create the graph edges
                    self.graph.add_edge(str(self.setList[i]), str(self.setList[j]), label=str(currentintersection))
                 # if we haven't seen this intersection before add it to the dictionary with a
                 # a tuple indicating which sets intersected, and that we have only found one
                 # intersection
                if lcurrentint not in self.DictIntersection.keys():
                    self.DictIntersection[lcurrentint]=(1, [set([i,j])])
                # otherwise update the previous entry.
                
                else:
                    old=self.DictIntersection[lcurrentint]
                    #print lcurrentint, old
                    self.DictIntersection[lcurrentint]=(old[0]+1,old[1]+[set([i,j])])
    def __rshift__(self, subset):
        subset=set(subset)
        newSetList=[]
        for newset in self.setList:
            if len(newset.intersection(subset))>0:
                raise ValueError, "cannot have an intersection with any of the sets already"
            newSetList.append(newset.union(subset))
        self.setList=newSetList
        
            

class PhiSets(DeltaSystemFree):

    @classmethod
    def proj_icosahedron(cls):
        nset=[[0,1,2],[0,1,4],[0,3,4],[0,3,5],[1,4,5],[1,3,5],[1,2,3],[2,3,4],[2,4,5],[0,2,5]]
        return cls(3,3,nset)

    @classmethod
    def bestPhiSetFree2(cls,n):
        setList=[]
        if n%2==1:
            support=range(n)
            setList=[]
            for i in range(len(support)):
                for j in range(i+1, len(support)):
                    setList.append(set([i,j]))
        return PhiSets(2, n,setList)
    
    def __init__(self, p, sunflowerSize, mylist=[]):
        DeltaSystemFree.__init__(self, p, sunflowerSize, mylist)
        self.__typeNameStr__="PhiSet"


    def IsPhiSet(self):
        self.__createDictIntersection__()
        return (not self.findSunflower(self.sunflowerSize)) and (0L not in self.DictIntersection.keys())
    
    def __add__(self, x):
        if x.IsPhiSet():
            if x.p==self.p:
                ans=DeltaSystemFree(self.p, self.sunflowerSize, self.setList+x.setList)
                #if ans.IsSunflowerFree():
                return ans
                #else:
                #    raise SunflowerException(ans)
            else:
                raise ValueError, "Not the same set size"
        else:
            raise ValueError, "Must add to PhiSets to each other"
        
 
