


# title
# defines the title of the whole set of queries
# OPTIONAL, if not set, timestamp will be used
title = "Analysis by Property"


# description
# defines the textual and human-intended description of the purpose of these queries
# OPTIONAL, if not set, nothing will be used or displayed
description = "Queries extracted from google doc: https://docs.google.com/document/d/1aJnpoMIr2MUOLlGKk3ZvLTE5mEGk6fzaixunrMF4HhE/edit#heading=h.nruhl4b7h4vx"


# output_destination
# defines where to save the results, input can be: 
# * a local path to a folder 
# * a URL for a google sheets document  
# * a URL for a google folder
# NOTE: On windows, folders in a path use backslashes, in such a case it is mandatory to attach a 'r' in front of the quotes, e.g. r"C:\Users\sresch\.."
# In the other cases the 'r' is simply ignored; thus best would be to always leave it there.
# OPTIONAL, if not set, folder of executed script will be used
output_destination = r"https://drive.google.com/drive/folders/1dbC698XgXpMUQzDeq29UrXMWalaL7XLN"


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
        "title" : "QP1 - P3_has_note - Description" , 
        "description" : "" , 
        "query" : """
			SELECT ?s ?type ?Description
			WHERE { ?s crm:P3_has_note ?Description;
					rdf:type ?type .}
        """
    },
    {
        "title": "QP2 - Description summary",
        "description": "",
        "query": """
			SELECT ?type COUNT(?Description) as ?count WHERE { 
			    ?s crm:P3_has_note ?Description;
				a ?type .
            }
			GROUP BY ?type
			ORDER BY DESC(?count)
        """
    }, 
    {    
        "title" : "QP3 - Access Point" , 
        "description" : "" , 
        "query" : """
			SELECT COUNT(?f) as ?cnt_s {
			  ?f <pe:PP28_has_designated_access_point> ?t .
			}			
        """
    }, 
    {    
        "title" : "QP4a - crm:P2_has_type - E55_Type" , 
        "description" : "" , 
        "query" : """
			SELECT ?st (count(DISTINCT ?e55t) as ?e55_cnt) (COUNT(?s) AS ?pc) {
			GRAPH ?g { ?s a ?st.
			  ?s crm:P2_has_type ?e55t.
			  ?e55t  a crm:E55_Type.
			} }
			GROUP BY ?st
			ORDER BY ?st DESC (?pc)
        """
    }, 
    {    
        "title" : "QP4b - distinct Class / E55_Type" , 
        "description" : "" , 
        "query" : """
			SELECT ?st ?e55t (COUNT(?s) AS ?pc) {
			GRAPH ?g { ?s a ?st.
			  ?s crm:P2_has_type ?e55t.
			  ?e55t  a crm:E55_Type.
			} }
			GROUP BY ?st ?e55t
			ORDER BY ?st DESC (?pc)
        """
    }, 
    {
        "title": "QP4c - count distinct Class / E55_Type",
        "description": "",
        "query": """
			SELECT (COUNT (distinct ?e55t) as ?e55t_cnt) (COUNT(?s) AS ?pc) WHERE {
                GRAPH ?g { 
                    ?s a ?st.
                    ?s crm:P2_has_type ?e55t.
                    ?e55t a crm:E55_Type.
                } 
            }
        """
    },
    {    
        "title" : "QP4d - E55_Type in correct namespace" , 
        "description" : "" , 
        "query" : """
			SELECT (COUNT (distinct ?e55t) as ?e55t_cnt) (COUNT(?s) AS ?pc) {
			GRAPH ?g { ?s a ?st.
				?s crm:P2_has_type ?e55t.
				?e55t  a crm:E55_Type.
				FILTER(STRSTARTS(STR(?e55t), "http://parthenos.d4science.org/handle/Parthenos/REG/Concept/")) 
			} } 
        """
    }, 
    {    
        "title" : "QP4e - E55_Type  / ST / CVs" , 
        "description" : "" , 
        "query" : """
			SELECT ?st ?cv (count(DISTINCT ?e55t) as ?e55t_cnt) (count(?cv) as ?cnt) WHERE {
				SELECT ?st ?e55t (STRBEFORE(STRAFTER(STR(?e55t), "http://parthenos.d4science.org/handle/Parthenos/REG/Concept/"),'/') as ?cv) WHERE {
					GRAPH ?g { ?s a ?st.
					  ?s crm:P2_has_type ?e55t.
					  ?e55t  a crm:E55_Type.
					} 
				} 
			}
			GROUP BY ?st ?cv
			ORDER BY ?st ?cv
        """
    }, 
    {    
        "title" : "QP4f - E55_Type: CVs" , 
        "description" : "" , 
        "query" : """
			SELECT ?cv (count(DISTINCT ?e55t) as ?e55t_cnt) (count(?cv) as ?cnt) WHERE {
			SELECT ?st ?e55t (STRBEFORE(STRAFTER(STR(?e55t), "http://parthenos.d4science.org/handle/Parthenos/REG/Concept/"),'/') as ?cv) WHERE {
			GRAPH ?g { ?s a ?st.
			  ?s crm:P2_has_type ?e55t.
			  ?e55t  a crm:E55_Type.
			} } }
			GROUP BY ?cv
			ORDER BY ?cv
        """
    }, 
    {    
        "title" : "QP4g - E55_Type: ST / CVs / Terms" , 
        "description" : "" , 
        "query" : """
			SELECT ?st ?e55t (STRBEFORE(STRAFTER(STR(?e55t), "http://parthenos.d4science.org/handle/Parthenos/REG/Concept/"),'/') as ?cv)
			(STRAFTER(STRAFTER(STR(?e55t), "http://parthenos.d4science.org/handle/Parthenos/REG/Concept/"),'/') as ?term) WHERE {
			GRAPH ?g { ?s a ?st.
			  ?s crm:P2_has_type ?e55t.
			  ?e55t  a crm:E55_Type.
			} }			
        """
    }, 
    {    
        "title" : "QP4h - E55_Type: CVs / Terms" , 
        "description" : "" , 
        "query" : """
			SELECT (count(DISTINCT ?st) as ?st_cnt) (count(?cv) as ?cnt)  ?cv ?term WHERE {
			SELECT ?st ?e55t (STRBEFORE(STRAFTER(STR(?e55t), "http://parthenos.d4science.org/handle/Parthenos/REG/Concept/"),'/') as ?cv)
			(STRAFTER(STRAFTER(STR(?e55t), "http://parthenos.d4science.org/handle/Parthenos/REG/Concept/"),'/') as ?term) WHERE {
			GRAPH ?g { ?s a ?st.
			  ?s crm:P2_has_type ?e55t.
			  ?e55t  a crm:E55_Type.
			} } }
			GROUP BY ?cv ?term
			ORDER BY ?cv ?term			
        """
    }, 
    {    
        "title" : "QP5b - missing rdfs:label" , 
        "description" : "" , 
        "query" : """
			SELECT count( distinct ?s )
			WHERE {
			   ?s ?p ?o.
			   FILTER NOT EXISTS {
				?s rdfs:label ?x
			   }
			 }			
        """
    },
    {    
        "title" : "QP6 - crm:P129_is_about" , 
        "description" : "" , 
        "query" : """
			SELECT ?t count(distinct ?s) as ?cnt_s count(distinct ?term) as ?cnt_t count(?s) as ?cnt WHERE {
			GRAPH ?g {
			  ?s crm:P129_is_about ?term.
			  ?s a ?t
			} }
			group by ?t			
        """
    },
    {    
        "title" : "QP6b - is_about by subject-type and term type" , 
        "description" : "" , 
        "query" : """
			SELECT ?t ?tterm count(distinct ?s) as ?cnt_s count(distinct ?term) as ?cnt_t count(?s) as ?cnt WHERE {
			GRAPH ?g {
			  ?s crm:P129_is_about ?term.
			  ?s a ?t.
			  ?term a ?tterm.
			} }
			group by ?t ?tterm
			ORDER BY  ?t ?tterm			
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


