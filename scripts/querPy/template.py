


# title
# defines the title of the whole set of queries
# OPTIONAL, if not set, timestamp will be used
title = "TEST QUERIES"


# description
# defines the textual and human-intended description of the purpose of these queries
# OPTIONAL, if not set, nothing will be used or displayed
description = "This set of queries is used as a template for showcasing a valid configuration."


# output_destination
# defines where to save the results, input can be: 
# * a local path to a folder 
# * a URL for a google sheets document  
# * a URL for a google folder
# NOTE: On windows, folders in a path use backslashes, in such a case it is mandatory to attach a 'r' in front of the quotes, e.g. r"C:\Users\sresch\.."
# In the other cases the 'r' is simply ignored; thus best would be to always leave it there.
# OPTIONAL, if not set, folder of executed script will be used
output_destination = r"."


# output_format
# defines the format in which the result data shall be saved (currently available: csv, tsv, xml, json, xlsx)
# OPTIONAL, if not set, csv will be used
output_format = "csv"


# summary_sample_limit
# defines how many rows shall be displayed in the summary
# OPTIONAL, if not set, 5 will be used
summary_sample_limit = 3


# endpoint
# defines the SPARQL endpoint against which all the queries are run
# MANDATORY
endpoint = "https://virtuoso.parthenos.d4science.org/sparql"


# queries
# defines the set of queries to be run. 
# MANDATAORY
queries = [


    {
        # title
        # OPTIONAL, if not set, timestamp will be used
        "title" : "Optional title of first query" ,
        
        # description
        # OPTIONAL, if not set, nothing will be used or displayed
        "description" : "Optional description of first query, used to describe the purpose of the query." ,

        # query
        # the sparql query itself
        # MANDATORY
        "query" : """
            SELECT ?g ?s ?p ?o WHERE {
                GRAPH ?g {
                    ?s ?p ?o
                }
            }
        """
    }, 
    {    
        "query" : """
            SELECT COUNT(*) WHERE {
                ?s a ?o
            }
        """
    },  
    {    
        "title" : "Last query" , 
        "description" : "This query counts the occurences of distinct predicates" , 
        "query" : """
            SELECT DISTINCT ?p COUNT(?p) AS ?pCount WHERE {
                ?s ?p ?o
            }
            ORDER BY DESC ( ?pCount )
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


