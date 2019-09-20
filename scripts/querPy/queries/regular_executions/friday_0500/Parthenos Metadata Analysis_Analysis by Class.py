


# title
# defines the title of the whole set of queries
# OPTIONAL, if not set, timestamp will be used
title = "Analysis by Class"


# description
# defines the textual and human-intended description of the purpose of these queries
# OPTIONAL, if not set, nothing will be used or displayed
description = "Enumerate classes linked from a given class and predicates that link instances of the given class and the target classes. Queries extracted from google doc: https://docs.google.com/document/d/1aJnpoMIr2MUOLlGKk3ZvLTE5mEGk6fzaixunrMF4HhE/edit#heading=h.3at1eb9qj22g"


# output_destination
# defines where to save the results, input can be: 
# * a local path to a folder 
# * a URL for a google sheets document  
# * a URL for a google folder
# NOTE: On windows, folders in a path use backslashes, in such a case it is mandatory to attach a 'r' in front of the quotes, e.g. r"C:\Users\sresch\.."
# In the other cases the 'r' is simply ignored; thus best would be to always leave it there.
# OPTIONAL, if not set, folder of executed script will be used
output_destination = r"https://drive.google.com/drive/folders/1PALpNYRISD1BX_W6yq0iKN7O0Hf2I14x"


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
        "title" : "qPE1a - PE1_Service" , 
        "description" : "" , 
        "query" : """
			SELECT ?p ?c (COUNT(?p) AS ?pc) {
			  ?f a pe:PE1_Service .
			  ?t a ?c .
			  ?f ?p ?t .
			  FILTER(?c != owl:Class)
			} GROUP BY ?p ?c
        """
    },
    {    
        "title" : "qPE1b" , 
        "description" : "Same as qPE1a, with change in the FILTER option and the declaration of the predicate ?p" , 
        "query" : """
			SELECT ?p ?c (COUNT(?p) AS ?pc) {
				?f a pe:PE1_Service ;
				?p [ a ?c ].
				FILTER(!sameTerm(?c, owl:Class))
			} 
			GROUP BY ?p ?c
        """
    },
    {    
        "title" : "qPE1c - PE1 with inheritance" , 
        "description" : "" , 
        "query" : """
			DEFINE input:inference 'parthenos_rules'
			SELECT ?p (COUNT(?p) AS ?pc) WHERE {GRAPH ?g {
			  ?s a crmpe:PE1_Service .
			  ?s ?p ?o .
			} }
			GROUP BY ?p
			ORDER BY DESC (?pc)
        """
    },
    {    
        "title" : "qPE1d - Properties of sample PE1 entities" , 
        "description" : "" , 
        "query" : """
			SELECT ?f ?t {
			  ?f a pe:PE1_Service .
			  ?t a ?c .
			  ?f ?p ?t .
			  FILTER(?c != owl:Class)
			}
        """
    },
    {    
        "title" : "PE7_Data_Hosting_Service" , 
        "description" : "" , 
        "query" : """
			SELECT ?p ?c (COUNT(?p) AS ?pc) {
			  ?f a pe:PE7_Data_Hosting_Service .
			  ?t a ?c .
			  ?f ?p ?t .
			  FILTER(?c != owl:Class)
			} GROUP BY ?p ?c
        """
    },
    {    
        "title" : "PE12_Data_Curating_Service" , 
        "description" : "" , 
        "query" : """
			SELECT ?p ?c (COUNT(?p) AS ?pc) {
			  ?f a pe:PE12_Data_Curating_Service .
			  ?t a ?c .
			  ?f ?p ?t .
			  FILTER(?c != owl:Class)
			} GROUP BY ?p ?c			
        """
    },
    {    
        "title" : "PE13_Software_Computing_E-Service" , 
        "description" : "" , 
        "query" : """
			SELECT ?p ?c (COUNT(?p) AS ?pc) {
			  ?f a pe:PE13_Software_Computing_E-Service .
			  ?t a ?c .
			  ?f ?p ?t .
			  FILTER(?c != owl:Class)
			} GROUP BY ?p ?c			
        """
    },
    {    
        "title" : "PE15_Data_E-Service" , 
        "description" : "" , 
        "query" : """
			SELECT ?p ?c (COUNT(?p) AS ?pc) {
			?f a pe:PE15_Data_E-Service .
			?t a ?c .
			?f ?p ?t .
			FILTER(?c != owl:Class)
			} GROUP BY ?p ?c
        """
    },
    {    
        "title" : "PE17_Curated_Data_E-Service" , 
        "description" : "" , 
        "query" : """
			SELECT ?p ?c (COUNT(?p) AS ?pc) {
			  ?f a pe:PE17_Curated_Data_E-Service .
			  ?t a ?c .
			  ?f ?p ?t .
			  FILTER(?c != owl:Class)
			} GROUP BY ?p ?c
        """
    },
    {    
        "title" : "PE21_Persistent_Software" , 
        "description" : "" , 
        "query" : """
			SELECT ?p ?c (COUNT(?p) AS ?pc) {
			  ?f a pe:PE21_Persistent_Software .
			  ?t a ?c .
			  ?f ?p ?t .
			  FILTER(?c != owl:Class)
			} GROUP BY ?p ?c
        """
    },
    {    
        "title" : "PE22_Persistent_Dataset" , 
        "description" : "" , 
        "query" : """
			SELECT ?p ?ot (COUNT(?p) AS ?pc) {  
			GRAPH ?g {?s a pe:PE22_Persistent_Dataset .
			  ?o a ?ot .
			  ?s ?p ?o .
			  FILTER(?ot != owl:Class) }
			}
			GROUP BY ?p ?ot
			ORDER BY DESC (?pc)
        """
    },
    {    
        "title" : "PE24_Volatile_Dataset" , 
        "description" : "" , 
        "query" : """
			SELECT ?p ?c (COUNT(?p) AS ?pc) { ?f a pe:PE24_Volatile_Dataset .
			  ?t a ?c .
			  ?f ?p ?t .
			  FILTER(?c != owl:Class)
			} 
			GROUP BY ?p ?c ORDER BY DESC (?pc)
        """
    },
    {    
        "title" : "PE25_RI_Consortium" , 
        "description" : "" , 
        "query" : """
			SELECT ?p ?c (COUNT(?p) AS ?pc) {
			  ?f a pe:PE25_RI_Consortium .
			  ?t a ?c .
			  ?f ?p ?t .
			  FILTER(?c != owl:Class)
			} 
			GROUP BY ?p ?c ORDER BY DESC (?pc)
        """
    },
    {    
        "title" : "PE26_RI_Project" , 
        "description" : "" , 
        "query" : """
			SELECT ?p ?c (COUNT(?p) AS ?pc) {
			  ?f a pe:PE26_RI_Project .
			  ?t a ?c .
			  ?f ?p ?t .
			  FILTER(?c != owl:Class)
			} 
			GROUP BY ?p ?c ORDER BY DESC (?pc)
        """
    },
    {    
        "title" : "PE28_Curation_Plan" , 
        "description" : "" , 
        "query" : """
			SELECT ?p ?c (COUNT(?p) AS ?pc) {
			  ?f a pe:PE28_Curation_Plan .
			  ?t a ?c .
			  ?f ?p ?t .
			  FILTER(?c != owl:Class)
			} 
			GROUP BY ?p ?c ORDER BY DESC (?pc)
        """
    },
    {
        "title" : "PE29_Access_Point" ,
        "description" : "" ,
        "query" : """
			SELECT ?p ?ot (COUNT(?p) AS ?pc) {
                GRAPH ?g { 
                    ?s a pe:PE29_Access_Point .
                    ?s ?p ?o .
                    ?o a ?ot.
                    FILTER(?ot != owl:Class)
			    } 
			}
			GROUP BY ?p ?ot
			ORDER BY DESC (?pc)
        """
    },
    {    
        "title" : "PE34_Team" , 
        "description" : "" , 
        "query" : """
			SELECT ?p ?ot (COUNT(?p) AS ?pc) {
			GRAPH ?g { ?s a crmpe:PE34_Team.
			  ?s ?p ?o .
			  ?o a ?ot.
			  FILTER(?ot != owl:Class)
			} }
			GROUP BY ?p ?ot
			ORDER BY DESC (?pc)
        """
    }, 
    {
        "title": "PE38_Schema",
        "description": "",
        "query": """
			SELECT ?p ?ot (COUNT(?p) AS ?pc) {
                GRAPH ?g { 
                    ?s a http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE38_Schema.
                    ?s ?p ?o .
                    ?o a ?ot.
                    FILTER(?ot != owl:Class)
                } 
			}
			GROUP BY ?p ?ot
			ORDER BY DESC (?pc)
        """
    },
    {    
        "title" : "PE22_Persistent_Dataset" , 
        "description" : "" , 
        "query" : """
			SELECT ?p (count(?p) as ?count) 
			WHERE { [a crmpe:PE22_Persistent_Dataset] ?p ?o } 
			GROUP BY ?p
        """
    }, 
    {    
        "title" : "E39_Actor (outgoing)" , 
        "description" : "As specialisation of Q1, just looking at the distinct properties and object-classes of the instances of class E39_Actor:" , 
        "query" : """
			SELECT ?p ?ot (COUNT(?p) as ?pCount)
			  WHERE {?s ?p ?o. ?s a crm:E39_Actor. ?o a ?ot.}
			  GROUP BY ?p ?ot
			ORDER BY DESC(?pCount)
        """
    }, 
    {    
        "title" : "E39_Actor (incoming)" , 
        "description" : "" , 
        "query" : """
			SELECT ?p ?st (COUNT(?p) as ?pCount)
			  WHERE {
			GRAPH ?g {?s ?p ?o. ?o a crm:E39_Actor. ?s a ?st.} }
			  GROUP BY ?p ?st
			ORDER BY DESC(?pCount)
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


