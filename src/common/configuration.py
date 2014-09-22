from ConfigParser import SafeConfigParser
import logging
from rdflib.namespace import Namespace

class Configuration(object):
    def __init__(self, configFileName):
        try :
            # Read the config file
            self.config = SafeConfigParser()
            self.config.read(configFileName)
            
            # Load the namespaces
            self.namespaces = {}
            for (name, value) in self.config.items("namespaces"):
                self.namespaces[name] = Namespace(value)
                
            # Set the logger level
            verbose = self.config.get('debug', 'verbose')
            logLevel = logging.DEBUG if verbose == "1" else logging.INFO
            logging.basicConfig(level=logLevel)
        except :
            logging.error("Could not find configuration file")
    
    def isCompress(self):
        return self.config.get('debug', 'compress') == '1';
    
    def isOverwrite(self):
        return self.config.get('debug', 'overwrite') == '1';
    
    def bindNamespaces(self, graph):
        for (name, value) in self.namespaces.iteritems():
            graph.namespace_manager.bind(name, value)
    
    def getURI(self, ns, resourceName):
        return self.namespaces[ns][resourceName]
    
    def get_Graph(self, name):
        return self.config.get('graphs', name)
    
    def get_SPARQL(self):
        return self.config.get('general', 'sparql_endpoint')
    
    def get_prefixes(self):
        '''
        prefix tablink: <http://example.org/ns/tablink#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        '''
        prefixes = ""
        for (name, value) in self.namespaces.iteritems():
            prefixes = "%s prefix %s: <%s>\n" % (prefixes, name, value)
        return prefixes
        
