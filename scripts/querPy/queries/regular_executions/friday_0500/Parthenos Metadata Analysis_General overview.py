


# title
# defines the title of the whole set of queries
# OPTIONAL, if not set, timestamp will be used
title = "General overview queries"


# description
# defines the textual and human-intended description of the purpose of these queries
# OPTIONAL, if not set, nothing will be used or displayed
description = "Queries extracted from google doc: https://docs.google.com/document/d/1aJnpoMIr2MUOLlGKk3ZvLTE5mEGk6fzaixunrMF4HhE/edit#heading=h.3i3qrymun2lk"


# output_destination
# defines where to save the results, input can be: 
# * a local path to a folder 
# * a URL for a google sheets document  
# * a URL for a google folder
# NOTE: On windows, folders in a path use backslashes, in such a case it is mandatory to attach a 'r' in front of the quotes, e.g. r"C:\Users\sresch\.."
# In the other cases the 'r' is simply ignored; thus best would be to always leave it there.
# OPTIONAL, if not set, folder of executed script will be used
output_destination = r"https://drive.google.com/drive/folders/13v-SQyeene9-YpUtJPeb79pSqD4DE6rw"


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
        "title" : "Q1 - ?subject-class ?predicate ?object-class" , 
        "description" : "A complete overview/summary of all types of relations in the data." , 
        "query" : """
			SELECT ?st ?p ?ot ( COUNT( ?p ) AS ?pCount ) WHERE {
				GRAPH ?g {
					?s ?p ?o .
					?s a ?st .
					?o a ?ot 
				} 
			}
			GROUP BY ?st ?p ?ot 
			ORDER BY DESC ( ?pCount )
        """
    }, 
    {    
        "title" : "Q2 - ?subject-class ?predicate" , 
        "description" : "Reducing above query (Q1) to just combinations of subject-class and predicate." , 
        "query" : """
			SELECT ?st ?p COUNT(?p) AS ?pCount WHERE {
				GRAPH ?g {
					?s ?p ?o .
					?s a ?st .
				} 
			}
			GROUP BY ?st ?p
			ORDER BY DESC ( ?pCount ) 
        """
    }, 
    {    
        "title" : "Q3 - all used predicates + frequencies" , 
        "description" : "" , 
        "query" : """
			SELECT ?p (COUNT(?p) as ?pCount) WHERE {
				[] ?p []
			}
			GROUP BY ?p
			ORDER BY DESC(?pCount)
        """
    }, 
    {    
        "title" : "Q4 - all used Subject types + frequencies" , 
        "description" : "" , 
        "query" : """
			SELECT ?type (COUNT(?type) as ?typeCount) WHERE {
				[] a ?type
			}
			GROUP BY ?type
			ORDER BY DESC(?typeCount)
        """
    }, 
    {    
        "title" : "Q5 - just CIDOC-CRM types + frequencies" , 
        "description" : "" , 
        "query" : """
			SELECT ?type (COUNT(?type) as ?typeCount) WHERE {
				[] a ?type. 
				FILTER(STRSTARTS(STR(?type), "crm:"))
			}
			GROUP BY ?type
			ORDER BY ?typeCount
        """
    }, 
    {    
        "title" : "Q5a - Why is PC14 an entity type? #11653" , 
        "description" : "" , 
        "query" : """
			SELECT ?p ?ot ( COUNT( ?p ) as ?pCount ) WHERE {
					graph ?g {
							?s ?p ?o .
							?s a <crm:PC14_carried_out_by> .
							?o a ?ot
					}
			}
			GROUP BY ?p ?ot
			ORDER BY DESC ( ?pCount )
        """
    }, 
    {    
        "title" : "Q5a - Why is PC14 an entity type? #11653" , 
        "description" : "" , 
        "query" : """
			SELECT ?g ?s ?p ?o WHERE {
					graph ?g {
							?s ?p ?o .
							?s a <crm:PC14_carried_out_by> .
						 
					}
			}
        """
    }, 
    {    
        "title" : "Q6 -  just CIDOC-PE types + frequencies" , 
        "description" : "" , 
        "query" : """
			SELECT ?type (COUNT(?type) as ?typeCount) WHERE {
				[] a ?type.
				FILTER(STRSTARTS(STR(?type), "pe:"))
			}
			GROUP BY ?type ORDER BY DESC(?typeCount)
        """
    }, 
    {    
        "title" : "Q6b - CIDOC-PE types with inheritance" , 
        "description" : "Same as Q6a but with inference activated:" , 
        "query" : """
			DEFINE input:inference 'parthenos_rules' 
			SELECT ?type (COUNT(?type) as ?typeCount) WHERE {
				[] a ?type.
				FILTER(STRSTARTS(STR(?type), "pe:"))
			}
			GROUP BY ?type ORDER BY DESC(?typeCount)
        """
    }, 
    {    
        "title" : "Q7 Find out all datasets and calculate how many triples there are per graph" , 
        "description" : "" , 
        "query" : """
			SELECT DISTINCT ?g (count(?p) as ?triples) WHERE { 
				GRAPH ?g { ?s ?p ?o }
			} 
			GROUP BY ?g
			ORDER BY DESC (?triples)
        """
    }, 
    {    
        "title" : "Q10 The number of nodes equals to the sum of distinct subjects and objects." , 
        "description" : "" , 
        "query" : """
			SELECT (COUNT (DISTINCT ?node) AS ?vNum) WHERE {
			  { ?node ?p ?obj } UNION
			  { ?obj ?p ?node }
			}
        """
    }, 
    {    
        "title" : "Q11 Number of single triples between two nodes" , 
        "description" : "" , 
        "query" : """
			SELECT ?s ?o (COUNT (*) AS ?tNum) WHERE { 
				{ ?s ?p ?o } UNION 
				{ ?o ?q ?s } 
			}
			GROUP BY ?s ?o ORDER BY DESC (?tNum)
        """
    }, 
    {    
        "title" : "Q12 - Return most connected entities (ignoring related graphs)" , 
        "description" : "" , 
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
        "title" : "Q13 - Return most connected entities while differentiating between incoming and outgoing edges (ignoring related graphs)" , 
        "description" : "" , 
        "query" : """
			SELECT 
			?resource 
			COUNT(?pFrom) AS ?countPredicates_FromResource  
			COUNT(?pTo) AS ?countPredicates_ToResource  
				WHERE {
					{ ?resource ?pFrom ?resourceTo } UNION
					{ ?resourceFrom ?pTo ?resource } 
				}		 
			GROUP BY ?resource
			ORDER BY DESC ( ?countPredicates_FromResource ) 
        """
    }, 
    {    
        "title" : "Q14 - Return most connected entities (including related graphs)" , 
        "description" : "" , 
        "query" : """
			SELECT ?graph ?resource COUNT(*) AS ?countOfConnections WHERE {
				GRAPH ?graph { 
					{ ?resource ?pTo ?resourceTo } UNION
					{ ?resourceFrom ?pFrom ?resource } 
				}
			}	 
			GROUP BY ?graph ?resource
			ORDER BY DESC (?countOfConnections) ?graph 
        """
    }, 
    {    
        "title" : "Q15 - Return most connected entities while differentiating between incoming and outgoing edges (including related graphs)" , 
        "description" : "" , 
        "query" : """
			SELECT ?graph ?resource  COUNT(?pFrom) AS ?countPredicates_FromResource  COUNT(?pTo) AS ?countPredicates_ToResource  WHERE {
				GRAPH ?graph { 
					{ ?resource ?pFrom ?resourceTo } UNION
					{ ?resourceFrom ?pTo ?resource } 
				} 
			} 
			GROUP BY ?graph ?resource
			ORDER BY DESC ( ?countPredicates_FromResource ) 
        """
    }, 
    {    
        "title" : "Q16 - Return identical triples and the number of graphs they are spread over" , 
        "description" : "" , 
        "query" : """
			SELECT ?s ?p ?o COUNT(?g) AS ?count_graphs WHERE {
				GRAPH ?g { ?s ?p ?o }
			}
			GROUP BY ?s ?p ?o
			HAVING ( COUNT( ?g ) > 1)
			ORDER BY DESC ( ?count_graphs )
        """
    }, 
    {    
        "title" : "Q17 - count of graphs grouped by their count of triples" , 
        "description" : "Returns a meta-count, i.e. first the query counts all triples per graphs, resulting in ?triplesInGraphs and then it counts how many graphs have such a ?triplesInGraphs number. So it returns a compressed statistic about the size-distribution of graphs." , 
        "query" : """
			SELECT COUNT(?g) AS ?numberOfGraphs ?triplesInGraphs  WHERE {
				SELECT ?g COUNT(*) AS ?triplesInGraphs WHERE {
					GRAPH ?g { ?s ?p ?o } .
				} 
				GROUP BY ?g 
			}
			GROUP BY ?triplesInGraphs
			ORDER BY ?triplesInGraphs
        """
    }, 
    {    
        "title" : "Q18 Graphs per Provenance " , 
        "description" : "" , 
        "query" : """
			SELECT ?source (COUNT(DISTINCT ?g) as ?gcnt) WHERE { 
				GRAPH ?g {?s ?p ?o  .} . 
				GRAPH <provenance> {?g <dnetcollectedFrom> ?api . ?api <dnetisApiOf> ?source.}
			}
			GROUP BY ?source
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


