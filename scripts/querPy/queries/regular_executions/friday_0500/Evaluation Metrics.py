


# title
# defines the title of the whole set of queries
# OPTIONAL, if not set, timestamp will be used
title = "Evaluation Metrics"


# description
# defines the textual and human-intended description of the purpose of these queries
# OPTIONAL, if not set, nothing will be used or displayed
description = "Set of queries which shall produce quantifiable metrics so that the development of these metrics can be statistically and continuously recorded and distilled."


# output_destination
# defines where to save the results, input can be: 
# * a local path to a folder 
# * a URL for a google sheets document  
# * a URL for a google folder
# NOTE: On windows, folders in a path use backslashes, in such a case it is mandatory to attach a 'r' in front of the quotes, e.g. r"C:\Users\sresch\.."
# In the other cases the 'r' is simply ignored; thus best would be to always leave it there.
# OPTIONAL, if not set, folder of executed script will be used
output_destination = r"https://drive.google.com/drive/folders/1ZFDByQ_5itFU4YEvMJNKPm8O5etflHx-"


# output_format
# defines the format in which the result data shall be saved (currently available: csv, tsv, xml, json, xlsx)
# OPTIONAL, if not set, csv will be used
output_format = ""


# summary_sample_limit
# defines how many rows shall be displayed in the summary
# OPTIONAL, if not set, 5 will be used
summary_sample_limit = 3


# cooldown_between_queries
# defines how many seconds should be waited between execution of individual queries in order to prevent exhaustion of Google API due to too many writes per time-interval
# OPTIONAL, if not set, 0 will be used
cooldown_between_queries = 10


# endpoint
# defines the SPARQL endpoint against which all the queries are run
# MANDATORY
endpoint = "https://virtuoso.parthenos.d4science.org/sparql"


# queries
# defines the set of queries to be run. 
# MANDATAORY
queries = [

    {    
        "title" : "Count of all triples in Virtuoso" , 
        "query" : """
			SELECT COUNT(*) WHERE { 
				[][][] 
			}
        """
    },
    {    
        "title" : "All used predicates + their frequencies" , 
        "query" : """
			SELECT ?p (COUNT(?p) as ?pCount) WHERE {
				[] ?p []
			}
			GROUP BY ?p
			ORDER BY DESC(?pCount)
        """
    },
    {    
        "title" : "All used Subject types + their frequencies" , 
        "query" : """
			SELECT ?type (COUNT(?type) as ?typeCount) WHERE {
				[] a ?type
			}
			GROUP BY ?type
			ORDER BY DESC(?typeCount)			
        """
    },
    {    
        "title" : "Number of graphs" , 
        "query" : """
			SELECT (COUNT (DISTINCT ?g) AS ?numberOfGraphs) WHERE { 
				GRAPH ?g { ?s ?p ?o }
			}
        """
    },
    {    
        "title" : "All graphs, sorted by their number of triples contained within" , 
        "query" : """
			SELECT DISTINCT ?g (count(?p) as ?triples) WHERE { 
				GRAPH ?g { ?s ?p ?o } 
			} 
			GROUP BY ?g
			ORDER BY DESC (?triples)
        """
    },
    {    
        "title" : "Return most connected entities" , 
        "query" : """
			SELECT ?resource COUNT(*) AS ?countOfConnections WHERE {
				{ ?resource ?pTo ?rTo } UNION
				{ ?rFrom ?pFrom ?resource } 
			} 
			GROUP BY ?resource
			ORDER BY DESC ( ?countOfConnections )
        """
    },
    {    
        "title" : "Duplicate tripes (spread over different graphs)" , 
        "description" : "Heuristically one can assume that the lower this number, the better the data quality" , 
        "query" : """
			SELECT ?s ?p ?o COUNT( DISTINCT ( ?g ) ) AS ?countOfOccurrence WHERE {
				GRAPH ?g { ?s ?p ?o }
			}
			GROUP BY ?s ?p ?o
			ORDER BY DESC( ?countOfOccurrence )
        """
    },
]

# Notes on syntax of queries-set:
# * the set of queries is enclosed by '[' and ']'
# * individual queries are enclosed by '{' and '},'
# * All elements of a query (title, description, query) need to be defined using quotes as well as their contents, and both need to be separated by ':'
# * All elements of a query (title, description, query) need to be separated from each other using quotes ','
# * The content of a query needs to be defined using triple quotes, e.g. """ SELECT * WHERE .... """
# * Any indentation (tabs or spaces) do not influence the queries-syntax, they are merely syntactic sugar.


