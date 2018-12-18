


# -------------------- OPTIONAL SETTINGS --------------------

# title
# defines the title of the whole set of queries
# OPTIONAL, if not set, timestamp will be used
title = "Parthenos Statistics Per Datasource 2 WithLabels"


# description
# defines the textual and human-intended description of the purpose of these queries
# OPTIONAL, if not set, nothing will be used or displayed
description = "A set of queries as created by Elias, which give the population of instances of type for a CRM class and all of its subclasses."


# output_destination
# defines where to save the results, input can be:
# * a local path to a folder
# * a URL for a google sheets document
# * a URL for a google folder
# NOTE: On windows, folders in a path use backslashes, in such a case it is mandatory to attach a 'r' in front of the quotes, e.g. r"C:\Users\sresch\.."
# In the other cases the 'r' is simply ignored; thus best would be to always leave it there.
# OPTIONAL, if not set, folder of executed script will be used
output_destination = r"https://drive.google.com/drive/folders/1Hw2OJUMGX6WPg5Hs5cpMClIE9uaQU-3x"


# output_format
# defines the format in which the result data shall be saved (currently available: csv, tsv, xml, json, xlsx)
# OPTIONAL, if not set, csv will be used
output_format = "csv"


# summary_sample_limit
# defines how many rows shall be displayed in the summary
# OPTIONAL, if not set, 5 will be used
summary_sample_limit = 10


# cooldown_between_queries
# defines how many seconds should be waited between execution of individual queries in order to prevent exhaustion of Google API due to too many writes per time-interval
# OPTIONAL, if not set, 0 will be used
cooldown_between_queries = 10


# write_empty_results
# Should empty results be written to summary files? Possible values are python boolean values: True, False
# OPTIONAL, if not set, False will be used
write_empty_results = False


# -------------------- MANDATORY SETTINGS --------------------

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
        "title" : "E2" ,


        # query
        # the sparql query itself
        # NOTE: best practise is to attach a 'r' before the string so that python would not interpret some characters as metacharacters, e.g. "\n"
        # MANDATORY
        "query" : r"""
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix crm: <http://www.cidoc-crm.org/cidoc-crm/>

            SELECT  (str(?ds) as ?voc), ?e2class  , (COUNT(DISTINCT  ?instanceURI ) as ?cnt)
            WHERE {


               ?e2class rdfs:subClassOf* crm:E2_Temporal_Entity .

               graph ?gRecord  {
                  ?instanceURI a ?e2class.
               }

               GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> {
                     ?gRecord <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?api .
                     ?api <http://www.d-net.research-infrastructures.eu/provenance/isApiOf> ?ds
               }

            }

            GROUP BY ?ds ?e2class
            order by ?voc DESC(COUNT(DISTINCT ?instanceURI ))
        """
    },
    {
        "title" : "E5",
        "query" : r"""
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix crm: <http://www.cidoc-crm.org/cidoc-crm/>

            SELECT  (str(?ds) as ?voc), ?class  , (COUNT(DISTINCT  ?instanceURI ) as ?cnt)
            WHERE {

               ?class rdfs:subClassOf* crm:E5_Event .

               graph ?gRecord  {
             ?instanceURI a ?class.
               }

               GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> {
                     ?gRecord <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?api .
                     ?api <http://www.d-net.research-infrastructures.eu/provenance/isApiOf> ?ds
               }

            }

            GROUP BY ?ds ?class
            order by ?voc DESC(COUNT(DISTINCT ?instanceURI ))
        """
    },
    {
        "title" : "E55",
        "query" : r"""
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix crm: <http://www.cidoc-crm.org/cidoc-crm/>

            SELECT  (str(?ds) as ?voc), ?e55class  , (COUNT(DISTINCT  ?instanceURI ) as ?cnt)
            WHERE {


               ?e55class rdfs:subClassOf* crm:E55_Type .

               graph ?gRecord  {
                  ?instanceURI a ?e55class.
               }

               GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> {
                     ?gRecord <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?api .
                     ?api <http://www.d-net.research-infrastructures.eu/provenance/isApiOf> ?ds
               }

            }

            GROUP BY ?ds ?e55class
            order by ?voc DESC(COUNT(DISTINCT ?instanceURI ))
        """
    },
    {
        "title" : "E2->P2->E55 Instances",
        "query" : r"""
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix crm: <http://www.cidoc-crm.org/cidoc-crm/>

            SELECT  (str(?ds) as ?voc), ?x,  (str(?litVal) as ?lbl), (COUNT(DISTINCT  ?instanceURI ) as ?cnt)
            WHERE {
               ?e2class rdfs:subClassOf* crm:E2_Temporal_Entity .  # same results with rdfs:subClassOf+

               FILTER(?p2 = crm:P2_has_type).
            #   tried   ?p2 rdfs:subPropertyOf* crm:P2_has_type .
            #   but returned irrelevant values (propbably all properties including literals)

               graph ?gRecord  {
                  ?instanceURI a ?e2class .
                  ?instanceURI ?p2 ?x.
                  ?x rdfs:label ?litVal.

               }
               GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> {
                     ?gRecord <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?api .
                     ?api <http://www.d-net.research-infrastructures.eu/provenance/isApiOf> ?ds
               }
            }

            GROUP BY ?ds ?x ?litVal
            order by ?voc DESC(COUNT(DISTINCT ?instanceURI  ))
        """
    },
    {
        "title" : "E2->P2->E55 Instances",
        "query" : r"""
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix crm: <http://www.cidoc-crm.org/cidoc-crm/>

            SELECT (str(?ds) as ?voc), ?e2class, ?x, (str(?litVal) as ?lbl), (COUNT(DISTINCT ?instanceURI ) as ?cnt)
            WHERE {
               ?e2class rdfs:subClassOf* crm:E2_Temporal_Entity .  # same results with rdfs:subClassOf+

               FILTER(?p2 = crm:P2_has_type).
            #   tried   ?p2 rdfs:subPropertyOf* crm:P2_has_type .
            #   but returned irrelevant values (propbably all properties including literals)

               graph ?gRecord  {
                  ?instanceURI a ?e2class .
                  ?instanceURI ?p2 ?x.
                  ?x rdfs:label ?litVal.

               }
               GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> {
                     ?gRecord <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?api .
                     ?api <http://www.d-net.research-infrastructures.eu/provenance/isApiOf> ?ds
               }
            }

            GROUP BY ?ds ?e2class ?x ?litVal
            order by ?voc DESC(COUNT(DISTINCT ?instanceURI  )) ?e2class
        """
    }
]

# Each query is itself encoded as a python dictionary, and together these dictionaries are collected in a python list. Beginner's note on such syntax as follows:
# * the set of queries is enclosed by '[' and ']'
# * individual queries are enclosed by '{' and '},'
# * All elements of a query (title, description, query) need to be defined using quotes as well as their contents, and both need to be separated by ':'
# * All elements of a query (title, description, query) need to be separated from each other using quotes ','
# * The content of a query needs to be defined using triple quotes, e.g. """ SELECT * WHERE .... """
# * Any indentation (tabs or spaces) do not influence the queries-syntax, they are merely syntactic sugar.
