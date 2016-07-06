'''
Created on 24.05.2013
Part of my project paper "implementations of design pattern"

@author: Christoph Gerneth
'''

import re
import requests
import time
import sys
import networkx as nx
import matplotlib.pyplot as plt



class Tools(object):

    """a Decorator Example"""
    @classmethod
    def time_this(self, func):
        def decorated(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            sys.stdout.write("[ran in" + str(time.time() - start) +"s] ")
            return result
        return decorated
    
    

class Component(object):
    """
    Superclass of the Composite Pattern.
    """
    def __init__(self, parent=None):
        self.setParent(parent)
        
    def component_function(self):
        pass
    
    def isOrphan(self):
        #if there is no parent component the component is an orphan. 
        #The 'root' is always an orphan
        return True if self.parent == None else False
    
    
    def setParent(self, parent):
        self.parent = parent
        try:
            self.parent.append_child(self) #register myself at Parent (if there is any)
        except AttributeError:
            # parent is none
            pass

class Leaf(Component):
    """
    Composite Pattern: a Leaf
    Inherits from Component. This means that each leaf may be part of a Composite.
    a Leaf cannot have children, so there is no 'append_child'-function.
    """
    def __init__(self, *args, **kw):
        Component.__init__(self, *args, **kw)

    def component_function(self):
        print "hello, i'm a Leaf"
        
class Composite(Component):
    """
    CompositePattern: a Composite
    Inherits from Component. This means that each Composite may be part of another Composite.
    
    """
    def __init__(self, *args, **kw):
        Component.__init__(self, *args, **kw)
        self.children = []

    def append_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def component_function(self):
        #do this function for all children
        map(lambda x: x.component_function(), self.children)
        




class AbstractPage(object):
    """The Abstract Page Class"""
    def __init__(self, url):
        self.url = url
    
    def getAbsolutePath(self, func):
        try:
            #return  "".join(self.parent.getAbsolutePath()).append(self.url)
            parentPath = self.parent.getAbsolutePath()
        except AttributeError:
            parentPath = ""
        return func(parentPath)
    
    def __repr__(self, *args, **kwargs):
        return "<Page "+ self.url+ ">"
    
    

    
class ExternalPage(AbstractPage, Leaf):
    """is a Leaf"""
    def __init__(self, url, parent):
        #super(ExternalPage, self).__init__(url, parent)
        AbstractPage.__init__(self, url)
        Leaf.__init__(self, parent)
        
    def __repr__(self, *args, **kwargs):
        return "<ExternalPage "+ self.url + ">"
    
    def getAbsolutePath(self):
        return AbstractPage.getAbsolutePath(self, self.__pathJoin)
    
    def __pathJoin(self, parentPath):
        return parentPath + "  -->  " + self.url
        
class InternalPage(AbstractPage, Composite):
    """is a Composite"""
    def __init__(self, url, parent):
        #super(InternalPage, self).__init__(url, parent)
        AbstractPage.__init__(self, url)
        Composite.__init__(self, parent)
    
    def __repr__(self, *args, **kwargs):
        return "<InternalPage "+ self.url+ ">"
    
    #override function from composite
    def component_function(self):
        print "Hello, I'm Internal Page", self.url
            
        
    def getAbsolutePath(self):
        return AbstractPage.getAbsolutePath(self, self.__pathJoin)    
    
    def __pathJoin(self, parentPath):
        if len(parentPath) > 0:
            if parentPath[-1] == "/" or self.url[0] == "/":
                return parentPath + self.url
            else:
                return parentPath + "/" + self.url
                
        else:
            return self.url
      
class AnchorPage(AbstractPage, Leaf):
    """Is a Leaf"""
    def __init__(self, url, parent):
        #super(AnchorPage, self).__init__(url, parent)
        AbstractPage.__init__(self, url)
        Leaf.__init__(self, parent)
        
    def __repr__(self):
        return "<Anchor "+ self.url+ ">"
    
    def getAbsolutePath(self):
        return AbstractPage.getAbsolutePath(self, self.__pathJoin)
    
    def __pathJoin(self, parentPath):
        return parentPath + self.url

 
  
class PageFactory(object):
    """
    Factory
    """
    
    def __call__(self, *args, **kwargs):
        return self.factoryMethod(*args)
    
    def factoryMethod(self, url, parent=None):
        #external page
        if url.startswith("http"):
            return ExternalPage(url, parent)
        #None-Page
        if url.startswith("javascript:"):
            #drop every href content, which starts with javascript
            return None
        #internal page
        elif url.startswith("/"):
            return InternalPage(url, parent)
        elif url.startswith("./"):
            #return InternalPage(url[1:], parent)
            return None
        elif str.isalpha((url[0])):
            return InternalPage(url, parent)
        #Anchor Page:
        elif url.startswith("#"):
            return AnchorPage(url, parent)
        

class Crawler(object):
    def __init__(self, start_url, max_deep=3):
        self.root = InternalPage(start_url, parent=None) #first Container
        self.max_deep = max_deep
        self.factory = PageFactory()     #factory erzeugen
   
    def start(self):
        #initialize
        children = [self.root]
        href_pattern = r'href=[\'"]?([^\'" >]+)'
        deep_counter = 0
        #do-loop
        for parent in children:
            #seite lesen
            html_content = self.__get_page(parent.getAbsolutePath()).replace("\n", '')
            result_urls = re.findall(href_pattern, html_content)
            print "%s: %i urls found" % (parent.getAbsolutePath(), len(result_urls))
            #objekte aus url-liste erzeugen und zum parent hinzufuegen
            for r in result_urls:
                factorized = self.factory(r, parent)
                if isinstance(factorized, InternalPage):
                    #typvergleich: gehe sicher, dass keine None-Objekte dem parent hinzugefuegt werden
                    if not factorized.getAbsolutePath() in map(InternalPage.getAbsolutePath, children): children.append(factorized) # for recursive list
            if deep_counter >= self.max_deep:
                break
            deep_counter =+ 1
     
    @Tools.time_this
    def __get_page(self, url):
        """retun content from a given url"""
        r = requests.get(url)
        content = r.text.encode('utf-8', 'ignore')
        return content
    
    @classmethod
    def drawGraph(cls, root_node):
        val_map = {ExternalPage: 1.0,
                   InternalPage: 0.7,
                   AnchorPage  : 0.4}
        
        graph = nx.Graph()
        children = root_node.children
        for node in children:
            graph.add_node(node)
            graph.add_edge(node, node.parent)
            #if not node in children: children.add(node)
            try:
                children.extend(node.children)
            except AttributeError:
                pass #is an external Page or a AnchorPage
            print "add", node
        #nx.draw(graph, pos=nx.spring_layout(graph))
        values = [val_map.get(type(node), 0.1) for node in graph.nodes()]
        nx.draw_spring(graph, with_labels=True, font_size=6, cmap=plt.get_cmap('jet'), node_color = values)
        plt.draw()
        #plt.show()
        plt.savefig("exout.png", dpi=500)


       
if __name__ == "__main__":
    url = 'http://localhost:8000'
    #url = "http://gerneth.info/script-vz.html"
    concrete_crawler = Crawler(url, max_deep=5)
    concrete_crawler.start()
    print """
    +-------------------+
    +     Results       +
    +-------------------+
    """
    print "all %i Pages:" % len(concrete_crawler.root.children)
    for node in concrete_crawler.root.children:
        print type(node).__name__ + " : " + node.getAbsolutePath()
    
    
    Crawler.drawGraph(concrete_crawler.root)
