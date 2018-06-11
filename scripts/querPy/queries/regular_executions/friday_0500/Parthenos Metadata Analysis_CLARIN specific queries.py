


# title
# defines the title of the whole set of queries
# OPTIONAL, if not set, timestamp will be used
title = "CLARIN specific queries"


# description
# defines the textual and human-intended description of the purpose of these queries
# OPTIONAL, if not set, nothing will be used or displayed
description = "Some sample queries trying to analyze only CLARIN data."


# output_destination
# defines where to save the results, input can be: 
# * a local path to a folder 
# * a URL for a google sheets document  
# * a URL for a google folder
# NOTE: On windows, folders in a path use backslashes, in such a case it is mandatory to attach a 'r' in front of the quotes, e.g. r"C:\Users\sresch\.."
# In the other cases the 'r' is simply ignored; thus best would be to always leave it there.
# OPTIONAL, if not set, folder of executed script will be used
output_destination = r"https://drive.google.com/drive/folders/1zKlPMak3sM-vt6miA6OmXrHdpOlI8Y2t"


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
        "title" : "Q1 List of classes with COUNT" , 
        "description" : "" , 
        "query" : """
			SELECT DISTINCT ?c (count(?c) as ?count)
			   WHERE {
				 GRAPH ?g
				   {[] a ?c .}
			   FILTER regex(?g, "clarin") }
			GROUP BY ?c
			ORDER BY DESC (?count)			
        """
    }, 
    {    
        "title" : "Q2 Number of triples per CLARIN graph" , 
        "description" : "" , 
        "query" : """
			SELECT DISTINCT ?g (count(?p) as ?triples)
			 WHERE { GRAPH ?g { ?s ?p ?o }
			 FILTER regex(?g, "clarin")
			 }
			GROUP BY ?g
			ORDER BY DESC (?triples)			
        """
    }, 
    {    
        "title" : "Q3 Find out which classes are in use per graph " , 
        "description" : "" , 
        "query" : """
			SELECT ?g ?class (count(?s) as ?count)
			 WHERE {GRAPH ?g { ?s a ?class}
			 FILTER regex(?g, "clarin") }
			GROUP BY ?class ?g
			ORDER BY DESC (?count)			
        """
    }, 
    {    
        "title" : "Q3.1 Which properties are in use in CLARIN graphs " , 
        "description" : "" , 
        "query" : """
			Select ?p (count(?p) as ?count)
			WHERE { GRAPH ?g {?s ?p ?o }
			FILTER regex(?g, "clarin")
			FILTER(?p != rdf:type)
			FILTER(?p != rdfs:label) }
			GROUP BY ?p
			ORDER BY DESC(?count)			
        """
    }, 
    {    
        "title" : "Q4 Find out which PE classes are in use in each CLARIN graph " , 
        "description" : "" , 
        "query" : """
			SELECT ?g ?class (count(?s) as ?count)
			 WHERE {GRAPH ?g { ?s a ?class}
			 FILTER regex(?g, "clarin")
			 FILTER(STRSTARTS(STR(?class), "pe:")) }
			GROUP BY ?class ?g
			ORDER BY DESC (?count)			
        """
    }, 
    {    
        "title" : "Q4.1 Find out which PE entities are used in CLARIN graphs" , 
        "description" : "" , 
        "query" : """
			SELECT ?class (count(?s) as ?count)
			 WHERE {GRAPH ?g { ?s a ?class}
			 FILTER regex(?g, "clarin")
			 FILTER(STRSTARTS(STR(?class), "pe:")) }
			GROUP BY ?class 
			ORDER BY DESC (?count)			
        """
    }, 
    {    
        "title" : "Q5 The most connected entities " , 
        "description" : "" , 
        "query" : """
			SELECT  ?g ?resource  COUNT(*) AS ?countOfConnections
			 WHERE {
				GRAPH ?g {
				{ ?resource ?pTo ?resourceTo } UNION
				{ ?resourceFrom ?pFrom ?resource } FILTER regex(?g, "clarin")
				} } 
			GROUP BY ?g ?resource
			ORDER BY DESC (?countOfConnections) ?g			
        """
    }, 
    {    
        "title" : "Q6 All used predicates + frequencies " , 
        "description" : "" , 
        "query" : """
			SELECT ?g ?p (count(?p) as ?count)
			 WHERE {GRAPH ?g {[] ?p []}
			 FILTER regex(?g, "clarin") }
			GROUP BY ?p ?g
			ORDER BY DESC(?count)			
        """
    }, 
    {    
        "title" : "Q7 The number of nodes equals to the sum of distinct subjects and objects" , 
        "description" : "" , 
        "query" : """
			SELECT ?g (COUNT (DISTINCT ?node) AS ?vNum)
			WHERE { {GRAPH ?g
			 { ?node ?p ?obj }}
			 UNION
			{ { ?obj ?p ?node }
			}
			FILTER regex(?g, "clarin") }
			ORDER BY DESC(?vNum)			
        """
    }, 
    {    
        "title" : "Q8 Number of single triples between two graphs " , 
        "description" : "" , 
        "query" : """
			SELECT ?g ?s ?o (COUNT (*) AS ?tNum)
			FROM Named <http://parthenos.d4science.org/handle/api_________::parthenos___::clarin::p_1357720977461/clarin______::2e87aeb259e8566e2fbc8eca20b93eb5>
			FROM Named <http://parthenos.d4science.org/handle/api_________::parthenos___::clarin::p_1349361150727/clarin______::819b94220a62615bd37bd594d3efe6a2>
			WHERE { 
			    GRAPH ?g {
			        { ?s ?p ?o }
			        UNION { ?o ?q ?s } 
                }
            }
			GROUP BY ?g ?s ?o ORDER BY DESC (?tNum)
        """
    }, 
    {    
        "title" : "PE15_Data_E-Service" , 
        "description" : "" , 
        "query" : """
			SELECT ?g ?p ?c (COUNT(?p) AS ?pc)
			WHERE {GRAPH ?g
			{
			 ?f a <pe:PE15_Data_E-Service> .
			 ?t a ?c .
			 ?f ?p ?t .
			 FILTER(?c != owl:Class)
			 FILTER regex(?g, "clarin")
			}}
			GROUP BY ?g ?p ?c
			ORDER BY DESC(?pc)			
        """
    }, 
    {    
        "title" : "PE29_Access_Point" , 
        "description" : "" , 
        "query" : """
			SELECT ?g ?p ?c (COUNT(?p) AS ?pc)
			WHERE {GRAPH ?g
			{ ?f a <pe:PE29_Access_Point> .
			  ?t a ?c .
			  ?f ?p ?t .
			   FILTER(?c != owl:Class)
			   FILTER regex(?g, "clarin")
			}}
			GROUP BY ?g ?p ?c
			ORDER BY DESC(?pc)			
        """
    }, 
    {    
        "title" : "PE24_Volatile_Dataset" , 
        "description" : "" , 
        "query" : """
			SELECT ?g ?p ?c (COUNT(?p) AS ?pc)
			WHERE {GRAPH ?g
			{ ?f a <pe:PE24_Volatile_Dataset> .
			  ?t a ?c .
			  ?f ?p ?t .
			 FILTER(?c != owl:Class)
			 FILTER regex(?g, "clarin")
			}}
			GROUP BY ?g ?p ?c
			ORDER BY DESC(?pc)
        """
    }, 
    {    
        "title" : "E39_Actor" , 
        "description" : "" , 
        "query" : """
			SELECT ?g ?p ?c (COUNT(?p) AS ?pc)
			WHERE {GRAPH ?g
			{
			 ?f a <crm:E39_Actor> .
			 ?t a ?c .
			 ?f ?p ?t .
			 FILTER(?c != owl:Class)
			 FILTER regex(?g, "clarin")
			}}
			GROUP BY ?g ?p ?c
			ORDER BY DESC(?pc)			
        """
    }, 
    {    
        "title" : "Q10 Count instances belonging to a given class (E39)" , 
        "description" : "" , 
        "query" : """
			SELECT (COUNT(?s) AS ?rc)
			   WHERE {
				 GRAPH ?g
				   {?s a <crm:E39_Actor> .}
				   FILTER regex(?g, "clarin")
			   }			
        """
    }, 
    {    
        "title" : "Q11 Count triples whose subject belongs to PE29 and whose object is literal." , 
        "description" : "" , 
        "query" : """
			SELECT (COUNT(?s) AS ?rc)
			   WHERE {
				 GRAPH ?g {
				   ?s ?p ?o .
				   ?s a <pe:PE29_Access_Point>  .
				   FILTER(isLiteral(?o))
				   FILTER regex(?g, "clarin")
				 }}			
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


