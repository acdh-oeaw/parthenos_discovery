
# datasources = ["Huma-Num - Nakala", "Huma-Num - Isidore", "LRE MAP", "PARTHENOS", "Cultura Italia", "European Holocaust Research Infrastructure", "ARIADNE", "METASHARE", "CLARIN"]
datasources = ["Huma-Num - Nakala", "Huma-Num - Isidore", "PARTHENOS", "METASHARE", "Cultura Italia", "LRE MAP", "European Holocaust Research Infrastructure", "CLARIN", "ARIADNE"] # orderd by number of E55 instances

    
# -------------------- OPTIONAL SETTINGS -------------------- 

# title
# defines the title of the whole set of queries
# OPTIONAL, if not set, timestamp will be used
title = ["E39_Actor_neighbourhood_", datasources]


# description
# defines the textual and human-intended description of the purpose of these queries
# OPTIONAL, if not set, nothing will be used or displayed
description = "Expanding the neighbourhoods with two hops from the specified inner query, here surrounding E39_Actor."


# output_destination
# defines where to save the results, input can be: 
# * a local path to a folder 
# * a URL for a google sheets document  
# * a URL for a google folder
# NOTE: On windows, folders in a path use backslashes, in such a case it is mandatory to attach a 'r' in front of the quotes, e.g. r"C:\Users\sresch\.."
# In the other cases the 'r' is simply ignored; thus best would be to always leave it there.
# OPTIONAL, if not set, folder of executed script will be used
output_destination = r"https://drive.google.com/drive/folders/14R3K44ap63Z0qD4N8aYGMpGUVIdvds7R"


# output_format
# defines the format in which the result data shall be saved (currently available: csv, tsv, xml, json, xlsx)
# OPTIONAL, if not set, csv will be used
output_format = "csv"


# summary_sample_limit
# defines how many rows shall be displayed in the summary
# OPTIONAL, if not set, 5 will be used
summary_sample_limit = 100


# cooldown_between_queries
# defines how many seconds should be waited between execution of individual queries in order to prevent exhaustion of Google API due to too many writes per time-interval
# OPTIONAL, if not set, 0 will be used
cooldown_between_queries = 10


# write_empty_results
# Should tabs be created in a summary file for queries which did not return results? Possible values are python boolean values: True, False
# OPTIONAL, if not set, False will be used
write_empty_results = False


# -------------------- MANDATORY SETTINGS -------------------- 

# endpoint
# defines the SPARQL endpoint against which all the queries are run
# MANDATORY
endpoint = "https://virtuoso.parthenos.d4science.org/sparql"

# queries
queries = [
    {
        "title" : [datasources, "_i -> ir"],
        
        "description" : r"""
            meanings of variables: 
                'i' = the instance of the specified CRM class, 
                'i_p_ir' = the relations from i to ir, 
                'ir' = the instances to the right of i (outgoing relations from i), 
                'ir_type : the type (if it exists) of ir """,
                
        "query" : [r"""
            
            select 
            
            <i> as ?id_subject_group
            count( distinct ?i ) as ?subject_group_count
            
            ?i_p_ir as ?relation
            count(?i_p_ir) as ?relation_count
            
            <ir> as ?id_object_group
            count( distinct ?ir ) as ?object_group_count
            ?ir_type
            
            where {
                graph ?sourceGraph {
                
                    # subquery (also with graph context, important for performance!), to get the correct distinct i without having the rest of the sub result intefering with the rest:
                    {
                        
                        select distinct ?i where {
                            graph ?sourceGraph {
                                ?i <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.cidoc-crm.org/cidoc-crm/E39_Actor> .
                            }
                            graph <dnet:graph> {
                                ?sourceGraph <dnet:collectedFrom> ?api .
                                ?api <dnet:isApiOf> '""", datasources, r"""'^^<http://www.w3.org/2001/XMLSchema#string>
                            }
                        } 
                    }
                    
                    # path from i to ir:
                    ?i ?i_p_ir ?ir .
                    
                    # cut away unneccesary results:
                    filter (
                        ?i_p_ir != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> && 
                        ?ir != <http://www.cidoc-crm.org/cidoc-crm/E39_Actor>
                    )
                    
                    # if there is a type for ir, get it:
                    optional {
                        ?ir a ?ir_type .
                    }
                } 
                graph <dnet:graph> {
                    ?sourceGraph <dnet:collectedFrom> ?api .
                    ?api <dnet:isApiOf> '""", datasources, r"""'^^<http://www.w3.org/2001/XMLSchema#string>
                }   
            }
            group by ?i_p_ir ?ir_type
        """]
    },
    {
        "title": [datasources, "_il -> i"],
        
        "description" : r"""
            meanings of variables: 
                'i' = the instance of the specified CRM class, 
                'il_p_i' = the relations from il to i, 
                'il' = the instances to the left of i (incoming relations to i), 
                'il_type : the type (if it exists) of il """,
                
        "query": [r"""

            select 

            <il> as ?id_subject_group
            count( distinct ?il ) as ?subject_group_count
            ?il_type

            ?il_p_i as ?relation
            count( ?il_p_i ) as ?relation_count

            <i> as ?id_object_group
            count( distinct ?i ) as ?object_group_count

            where {

                graph ?sourceGraph {
                    # subquery (also with graph context, important for performance!), to get the correct distinct i without having the rest of the sub result intefering with the rest:
                    {
                        select distinct ?i where {
                            graph ?sourceGraph {
                                ?i <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.cidoc-crm.org/cidoc-crm/E39_Actor> .
                            } 
                            graph <dnet:graph> {
                                ?sourceGraph <dnet:collectedFrom> ?api .
                                ?api <dnet:isApiOf> '""", datasources, r"""'^^<http://www.w3.org/2001/XMLSchema#string>
                            }
                        }
                    }
                    
                    # path from il to i:
                    ?il ?il_p_i ?i .
                    
                    # if there is a type for il, get it:
                    optional {
                        ?il a ?il_type .
                    }
                } 
                graph <dnet:graph> {
                    ?sourceGraph <dnet:collectedFrom> ?api .
                    ?api <dnet:isApiOf> '""", datasources, r"""'^^<http://www.w3.org/2001/XMLSchema#string>
                }   
            }
            group by ?il_p_i ?il_type
        """]
    },
    {
        "title": [datasources, "_ir -> irr"],
        
        "description" : r"""
            meaing of variables: 
                'i' = the instance of the specified CRM class, 
                'i_p_ir' = the relation from i to ir, 
                'ir' = the instances to the right of i (outgoing relations from i), 
                'ir_p_irr' = the relations from ir to irr, 
                'irr'  = the instances to the right of ir (outgoing relations from ir), 
                'irr_type : the type (if it exists) of irr """,
            
        "query": [r"""

            select

            <ir> as ?id_subject_group
            count( distinct ?ir ) as ?subject_group_count

            ?ir_p_irr as ?relation
            count( ?ir_p_irr ) as ?relation_count

            <irr> as ?id_object_group
            count( distinct ?irr ) as ?object_group_count
            ?irr_type

            where {

                graph ?sourceGraph {

                    # subquery (also with graph context, important for performance!), to get the correct distinct ir without having the rest of the sub result intefering with the rest:
                    {
                        select distinct ?ir where {
                            graph ?sourceGraph {

                                ?i <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.cidoc-crm.org/cidoc-crm/E39_Actor> .

                                ?i ?i_p_ir ?ir .
                            }
                            graph <dnet:graph> {
                                ?sourceGraph <dnet:collectedFrom> ?api .
                                ?api <dnet:isApiOf> '""", datasources, r"""'^^<http://www.w3.org/2001/XMLSchema#string>
                            }                                
                        }
                    }

                    # path from ir to irr:
                    ?ir ?ir_p_irr ?irr .
                    
                    # if there is a type for irr, get it:
                    optional {
                        ?irr a ?irr_type .
                    }

                }
                graph <dnet:graph> {
                    ?sourceGraph <dnet:collectedFrom> ?api .
                    ?api <dnet:isApiOf> '""", datasources, r"""'^^<http://www.w3.org/2001/XMLSchema#string>
                }
            }
            group by ?ir_p_irr ?irr_type
        """]
    },
    {
        "title": [datasources, "_irl -> ir"],
        
        "description" : r"""
            meaing of variables: 
                'i' = the instance of the specified CRM class, 
                'i_p_ir' = the relations from i to ir, 
                'ir' = the instances to the right of i (outgoing relations from i), 
                'irl_p_ir' = the relations from irl to ir, 
                'irl'  = the instances to the left of ir (incoming relations to ir), 
                'irl_type : the type (if it exists) of irl """,
            
        "query": [r"""

            select

            <irl> as ?id_subject_group
            count( distinct ?irl ) as ?subject_group_count
            ?irl_type

            ?irl_p_ir as ?relation
            count( ?irl_p_ir ) as ?relation_count

            <ir> as ?id_object_group
            count( distinct ?ir ) as ?object_group_count

            where {

                graph ?sourceGraph {

                    # subquery (also with graph context, important for performance!), to get the correct distinct ir without having the rest of the sub result intefering with the rest:
                    {
                        select distinct ?ir where {

                            graph ?sourceGraph {
                                ?i <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.cidoc-crm.org/cidoc-crm/E39_Actor> .

                                ?i ?i_p_ir ?ir .
                            }
                            graph <dnet:graph> {
                                ?sourceGraph <dnet:collectedFrom> ?api .
                                ?api <dnet:isApiOf> '""", datasources, r"""'^^<http://www.w3.org/2001/XMLSchema#string>
                            }                                
                        }
                    }

                    # path from irl to ir, minus the paths which we have already explored in the subquery before
                    ?irl ?irl_p_ir ?ir .
                    minus {
                            ?irl <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.cidoc-crm.org/cidoc-crm/E39_Actor> .
                            ?irl ?irl_p_ir ?ir .
                    }
                    
                    # if there is a type for irl, get it:
                    optional {
                        ?irl a ?irl_type .
                    }
                }
                graph <dnet:graph> {
                    ?sourceGraph <dnet:collectedFrom> ?api .
                    ?api <dnet:isApiOf> '""", datasources, r"""'^^<http://www.w3.org/2001/XMLSchema#string>
                }
            }
            group by ?irl_p_ir ?irl_type

        """]
    },
    {
        "title": "il -> ilr",
        
        "description" : r"""
            meaing of variables: 
                'i' = the instance of the specified CRM class, 
                'il_p_i' = the relations from il to i, 
                'il' = the instances to the left of i (incoming relations to i), 
                'il_p_ilr' = the relations from il to ilr, 
                'ilr'  = the instances to the right of il (outgoing relations from il), 
                'ilr_type : the type (if it exists) of ilr """,
            
        "query": [r"""

            select

            <il> as ?id_subject_group
            count( distinct ?il ) as ?subject_group_count

            ?il_p_ilr as ?relation
            count( ?il_p_ilr ) as ?relation_count

            <ilr> as ?id_object_group
            count( distinct ?ilr ) as ?object_group_count
            ?ilr_type

            where {

                graph ?sourceGraph {

                    # subquery (also with graph context, important for performance!), to get the correct distinct il without having the rest of the sub result intefering with the rest:
                    {
                        select distinct ?il where {
                            graph ?sourceGraph {
                                ?i <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.cidoc-crm.org/cidoc-crm/E39_Actor> .

                                ?il ?il_p_i ?i .
                            }
                            graph <dnet:graph> {
                                ?sourceGraph <dnet:collectedFrom> ?api .
                                ?api <dnet:isApiOf> '""", datasources, r"""'^^<http://www.w3.org/2001/XMLSchema#string>
                            }                                
                        }
                    }

                    # path from il to ilr, minus the paths which we have already explored in the subquery before
                    ?il ?il_p_ilr ?ilr .
                    minus {
                        ?il ?il_p_ilr ?ilr .
                        ?ilr <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.cidoc-crm.org/cidoc-crm/E39_Actor> .
                    }
                    
                    # if there is a type for ilr, get it:
                    optional {
                        ?ilr a ?ilr_type .
                    }

                }
                graph <dnet:graph> {
                    ?sourceGraph <dnet:collectedFrom> ?api .
                    ?api <dnet:isApiOf> '""", datasources, r"""'^^<http://www.w3.org/2001/XMLSchema#string>
                }
            }
            group by ?il_p_ilr ?ilr_type
        """]
    },
    {
        "title": "ill -> il",
        
        "description" : r"""
            meaing of variables: 
                'i' = the instance of the specified CRM class, 
                'il_p_i' = the relations from il to i, 
                'il' = the instances to the left of i (incoming relations to i), 
                'ill_p_il' = the relations from ill to il, 
                'ill'  = the instances to the left of il (incoming relations to il), 
                'ill_type : the type (if it exists) of ill """,
            
        "query": [r"""

            select

            <ill> as ?id_subject_group
            count( distinct ?ill ) as ?subject_group_count
            ?ill_type

            ?ill_p_il as ?relation
            count( ?ill_p_il ) as ?relation_count

            <il> as ?id_object_group
            count( distinct ?il ) as ?object_group_count

            where {

                graph ?sourceGraph {
                    # subquery (also with graph context, important for performance!), to get the correct distinct il without having the rest of the sub result intefering with the rest:
                    {
                        select distinct ?il where {
                            graph ?sourceGraph {
                                ?i <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.cidoc-crm.org/cidoc-crm/E39_Actor> .

                                ?il ?il_p_i ?i .
                            }
                            graph <dnet:graph> {
                                ?sourceGraph <dnet:collectedFrom> ?api .
                                ?api <dnet:isApiOf> '""", datasources, r"""'^^<http://www.w3.org/2001/XMLSchema#string>
                            }                                
                        }
                    }

                    # path from ill to il
                    ?ill ?ill_p_il ?il .
                    
                    # if there is a type for ill, get it:
                    optional {
                        ?ill a ?ill_type .
                    }

                }
                graph <dnet:graph> {
                    ?sourceGraph <dnet:collectedFrom> ?api .
                    ?api <dnet:isApiOf> '""", datasources, r"""'^^<http://www.w3.org/2001/XMLSchema#string>
                }
            }
            group by ?ill_p_il ?ill_type
        """]
    },
]
# defines the set of queries to be run.
# MANDATAORY

# Each query is itself encoded as a python dictionary, and together these dictionaries are collected in a python list. 
# Beginner's note on such syntax as follows:
# * the set of queries is enclosed by '[' and ']'
# * individual queries are enclosed by '{' and '},'
# * All elements of a query (title, description, query) need to be defined using quotes as well as their contents, and both need to be separated by ':'
# * All elements of a query (title, description, query) need to be separated from each other using quotes ','
# * The content of a query needs to be defined using triple quotes, e.g. """ SELECT * WHERE .... """
# * Any indentation (tabs or spaces) do not influence the queries-syntax, they are merely syntactic sugar.



# --------------- CUSTOM POST-PROCESSING METHOD --------------- 
'''
The method 'custom_post_processing(results)' is a stump for custom post processing which is always called if present and to which
result data from the query execution is passed. This way you can implement your own post-processing steps there.

The incoming 'results' argument is a list, where each list-element is a dictionary represting all data of a query.

This dictionary has the following keys and respective values:

* most likely to be needed are these two keys and values:
'query_title' - title of an individual query, as defined above.
'results_matrix' - the result data organized as a two dimensional list, where the first row contains the headers. 
This value is what you would most likely need to post process the result data.  

* other than these two, each query dictionary also contains data from and for querPy, which might be of use:
'query_description' - description of an individual query, as defined above.
'query_text' - the sparql query itself.
'results_execution_duration' - the duration it took to run the sparql query.
'results_lines_count' - the number of lines the sparql query produced at the triplestore.
'results_raw' - the result data in the specified format, encapsulated by its respective python class (e.g. a python json object).
'query_for_count' - an infered query from the original query, is used to get number of result lines at the triplestore.

As an example to print the raw data from the second query defined above, write:
print(results[1]['results_matrix'])
'''
