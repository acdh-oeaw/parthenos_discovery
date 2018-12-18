

# variable datasources, individual values of this variable will be injected into the queries where used.
datasources=["CLARIN", "PARTHENOS", "Huma-Num - Nakala", "Huma-Num - Isidore", "PARTHENOS WP3", "PARTHENOS WP4", "PARTHENOS WP8"]


# title
# defines the title of the whole set of queries
# OPTIONAL, if not set, timestamp will be used
title = [
datasources,
" : JRR_Quality_Test_Queries_V1.2.1_PerDatasource"
]


# description
# defines the textual and human-intended description of the purpose of these queries
# OPTIONAL, if not set, nothing will be used or displayed
description = r"Queries updated by Anastasia. Documented here: https://docs.google.com/document/d/1l4mzvSkWljwyj4wuOznk6OxXttDd0aYoQWPJRdcUTC8/edit?ts=5b9ba964"


# output_destination
# defines where to save the results, input can be:
# * a local path to a folder
# * a URL for a google sheets document
# * a URL for a google folder
# NOTE: On windows, folders in a path use backslashes, in such a case it is mandatory to attach a 'r' in front of the quotes, e.g. r"C:\Users\sresch\.."
# In the other cases the 'r' is simply ignored; thus best would be to always leave it there.
# OPTIONAL, if not set, folder of executed script will be used
output_destination = r"https://drive.google.com/drive/folders/1GQPLj15BJ0xZ5cvc_u_bJUV8Um6N80DK"


# summary_sample_limit
# defines how many rows shall be displayed in the summary
# OPTIONAL, if not set, 5 will be used
summary_sample_limit = 10


# write_empty_results
# Should tabs be created in a summary file for queries which did not return results? Possible values are python boolean values: True, False
# OPTIONAL, if not set, False will be used
write_empty_results = True


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
        "title" : "class_population.V1.4",
        "description" : "This query gives the density of population of classes by instances for a particular named graph in the registry.",
        "query" : [
			r"""
			#3 ######### Counts instances per class ignoring the record. To have the instances per class replace count(distinct ?instanceURI) with ?instanceURI in 'select' clause #########

			#DEFINE input:inference 'parthenos_rules'
			select ?class (count(distinct ?instanceURI) as ?count)
			( STR(?class_label) as ?class_label)
			( STR(?ds) as ?ds)
			where{
			graph ?gRecord  {
			?instanceURI a ?class.
			}

			optional{
			?class rdfs:label ?class_label.
			FILTER(langmatches(lang(?class_label), "en") || langmatches(lang(?class_label), ""))
			}

			values ?ds { '""",
			datasources,
			r"""'^^<http://www.w3.org/2001/XMLSchema#string>}
			GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> {?gRecord <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?api . ?api <http://www.d-net.research-infrastructures.eu/provenance/isApiOf> ?ds}
			}
			group by ?ds ?class ?class_label
			order by ?ds ?class
			"""
		]
    },
    {
		"title" : "class_population_PE_top.V1.2",
		"description" : "This query gives the density of population of classes by instances grouped by Parthenos Top Level Entities (Projects, Services, Actors, Datasets and Software) for a particular named graph in the registry.",
		"query" : [
			r"""
			#4 ######### The top categories and the count of instances per specific class #########

			select distinct ?topclass
			( STR(?topclass_label) as ?topclass_label)
			#( GROUP_CONCAT(distinct ?topclass_label, "/") as ?topclass_label )
			(?class as ?specific_class) 
			( STR(?class_label) as ?specific_class_label)
			#( GROUP_CONCAT(distinct ?class_labelX, "/") as ?specific_class_label )
			(count(distinct ?instanceURI) as ?count) 

			( STR(?ds) as ?ds)
			where{

			graph ?gRecord {
			?instanceURI a ?class.
			}
			optional { ?class rdfs:subClassOf*  ?topclass. }
			filter(
			?topclass = crmpe:PE35_Project ||
			?topclass = crmpe:PE1_Service ||
			?topclass = crm:E39_Actor ||
			?topclass = crmpe:PE18_Dataset ||
			?topclass = crmdig:D14_Software
			)

			optional { ?class rdfs:label ?class_label . FILTER(langmatches(lang(?class_label), "en") || langmatches(lang(?class_label), "")) }
			optional { ?topclass rdfs:label ?topclass_label . FILTER(langmatches(lang(?topclass_label), "en") || langmatches(lang(?topclass_label), "")) }

			values ?ds { '""",
			datasources,
			r"""'^^<http://www.w3.org/2001/XMLSchema#string>}
			GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> {?gRecord <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?api . ?api <http://www.d-net.research-infrastructures.eu/provenance/isApiOf> ?ds}
			}
			group by ?ds ?topclass ?class ?topclass_label ?class_label
			order by ?ds ?topclass ?class
			"""
		]
    },
    {
		"title" : "types_per_class_V1.3",
		"description" : "This query gives the list of instances of E55 existing in a data source and for what class they stand as type.",
		"query" : [
			r"""
			#6 ############ Get Types related to Classes, per Datasource ###########

			#DEFINE input:inference 'parthenos_rules'
			select distinct
			?type  
			(STR(?type_label) as ?type_label)
			?class
			#( GROUP_CONCAT(distinct ?class_label, "/") as ?class_label )
			(STR(?class_label) as ?class_label)
			?instanceClass
			#( GROUP_CONCAT(distinct ?instanceClass_label , "/") as ?instanceClass_label )
			(STR(?instanceClass_label) as ?instanceClass_label)
			(STR(?ds) as ?ds) 

			where{

			graph ?gRecord  {
			?type a ?class.
			optional{?type rdfs:label ?type_label . 
				FILTER(langmatches(lang(?type_label), "en") || langmatches(lang(?type_label), ""))
			}
			{?instanceURI crm:P2_has_type ?type} union {?type crm:P2i_is_type_of ?instanceURI}
			}

			values ?classE55 { <http://www.cidoc-crm.org/cidoc-crm/E55_Type> }
			?class rdfs:subClassOf* ?classE55 .
			optional{?class rdfs:label ?class_label . 
				FILTER(langmatches(lang(?class_label), "en") || langmatches(lang(?class_label), ""))
			}

			optional{ ?instanceURI a ?instanceClass.
				optional {?instanceClass rdfs:label ?instanceClass_label . 
					FILTER(langmatches(lang(?instanceClass_label), "en") || langmatches(lang(?instanceClass_label), ""))
				}
			}

			values ?ds { '""",
			datasources,
			r"""'^^<http://www.w3.org/2001/XMLSchema#string>}
			GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> {?gRecord <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?api . ?api <http://www.d-net.research-infrastructures.eu/provenance/isApiOf> ?ds}
			} 
			group by ?ds ?class ?instanceClass ?type  ?class_label ?instanceClass_label ?type_label 
			order by ?ds ?type
			"""
		]
    },
    {
		"title" : "types_per_class_count.V1.1",
		"description" : "A modification of query 'types_per_class_V1.3', where the types of the classes are counted.",
		"query" : [
			r"""
			#6 ############ Get Types related to Classes, per Datasource ###########
			#Note: the class labels (i.e. ?class_label, ?instanceClass_label) could be replaced with the class names for better performance#

			#DEFINE input:inference 'parthenos_rules'
			select  
			?type  
			#(replace(str(?type),"(^.*/)",  "", "i" ) as ?type_label)
			(STR(?type_label) as ?type_label)
			?class
			#(replace(str(?class),"(^.*/)",  "", "i" ) as ?class_label)
			(STR(?class_label) as ?class_label)
			?instanceClass
			#(replace(str(?instanceClass),"(^.*/)",  "", "i" ) as ?instanceClass_label)
			(STR(?instanceClass_label) as ?instanceClass_label)
			(COUNT(distinct ?instanceURI) as ?instanceCount)
			(STR(?ds) as ?ds)
			where{

			graph ?gRecord  {
			?type a ?class.
			optional {?type rdfs:label ?type_label .
				FILTER ( langmatches(lang(?type_label), "en") || langmatches(lang(?type_label), "") ) 
			}
			{?instanceURI crm:P2_has_type ?type} union {?type crm:P2i_is_type_of ?instanceURI}
			}

			values ?classE55 { <http://www.cidoc-crm.org/cidoc-crm/E55_Type> }
			?class rdfs:subClassOf* ?classE55 .
			optional{?class rdfs:label ?class_label . 
				FILTER(langmatches(lang(?class_label), "en") || langmatches(lang(?class_label), ""))
			}

			optional{ ?instanceURI a ?instanceClass.
				optional {?instanceClass rdfs:label ?instanceClass_label . 
					FILTER(langmatches(lang(?instanceClass_label), "en") || langmatches(lang(?instanceClass_label), ""))
				}
			}

			values ?ds { '""",
			datasources,
			r"""'^^<http://www.w3.org/2001/XMLSchema#string> }
			GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> {?gRecord <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?api . ?api <http://www.d-net.research-infrastructures.eu/provenance/isApiOf> ?ds}
			} 
			group by ?ds ?class ?instanceClass ?type ?class_label ?instanceClass_label ?type_label
			#group by ?ds ?class ?instanceClass ?type ?type_label
			order by ?ds ?type

			#---end of query ----
			"""
		]
    },
    {
		"title" : "all_types.V1.1",
		"description" : "This query returns all instances of type in a dataset given by a provider.",
		"query" : [
			r"""
			#5 ############ Discovering the redundant values of all the Types ###########

			#DEFINE input:inference 'parthenos_rules'
			select distinct (?instanceURI as ?type)
			( STR(?label) as ?label)
			( STR(?ds) as ?ds)
			where{
			values ?classE55 { <http://www.cidoc-crm.org/cidoc-crm/E55_Type> }

			graph ?gRecord  {
			?instanceURI a ?class.
			optional{
			?instanceURI rdfs:label ?label.
			FILTER(langmatches(lang(?label), "en") || langmatches(lang(?label), ""))
			}
			}

			?class rdfs:subClassOf* ?classE55.

			values ?ds {'""",
			datasources,
			r"""'^^<http://www.w3.org/2001/XMLSchema#string>}
			GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> {?gRecord <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?api . ?api <http://www.d-net.research-infrastructures.eu/provenance/isApiOf> ?ds}
			} 
			order by  ?instanceURI


			#---end of query ----
			"""
		]
    },
    {
		"title" : "place_instances_count.V1.1",
		"description" : "This query gives the list of instances of E53 class existing in a data source and the number of times it is used.",
		"query" : [
			r"""
			#7b ############ Get the Places instances COUNT per Datasource ###########

			select 
			(?instanceURI as ?place)
			#( GROUP_CONCAT(distinct ?place_labelX, "/") as ?place_label)
			(STR(?place_label) as ?place_label)
			(COUNT(distinct ?resource) as ?placeAppearance)
			(STR(?ds) as ?ds) 
			where{

			values ?classE53 { <http://www.cidoc-crm.org/cidoc-crm/E53_Place> }
			?class rdfs:subClassOf* ?classE53 .

			graph ?gRecord {
			?instanceURI a ?class.
			optional{
			?instanceURI rdfs:label ?place_label. FILTER(langmatches(lang(?place_label), "en") || langmatches(lang(?place_label), ""))
			}
			?resource ?relatedto ?instanceURI.
			}

			values ?ds { '""",
			datasources,
			r"""'^^<http://www.w3.org/2001/XMLSchema#string> }
			GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> {?gRecord <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?api . ?api <http://www.d-net.research-infrastructures.eu/provenance/isApiOf> ?ds}
			} group by ?ds ?instanceURI ?place_label
			order by ?ds

			#---end of query ----
			"""
		]
    },
    {
		"title" : "periods_and_events_count.V1.1",
		"description" : "This query gives the list of instances of E4 Period and E5 Event existing in a data source and their counts.",
		"query" : [
			r"""
			#8a ############ Get the Periods/Events/Activities instances COUNT per Datasource ###########

			#DEFINE input:inference 'parthenos_rules'
			select 
			(?instanceURI as ?instance)
			#( GROUP_CONCAT(distinct ?instance_label, "/") as ?instance_label)
			(STR(?instance_label) as ?instance_label)
			(COUNT(distinct ?resource) as ?instanceAppearance)
			(STR(?ds) as ?ds) 
			where{


			graph ?gRecord {
			?instanceURI a ?class.
			optional{
			?instanceURI rdfs:label ?instance_label.
			FILTER(langmatches(lang(?instance_label), "en") || langmatches(lang(?instance_label), ""))
			}
			?resource ?relatedto ?instanceURI.
			}

			filter (?class = <http://www.cidoc-crm.org/cidoc-crm/E4_Period> || ?class = <http://www.cidoc-crm.org/cidoc-crm/E5_Event>)
			#optional{?class rdfs:label ?class_label. FILTER(langmatches(lang(?class_label), "en") || langmatches(lang(?class_label), ""))}

			values ?ds { '""",
			datasources,
			r"""'^^<http://www.w3.org/2001/XMLSchema#string> }
			GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> {?gRecord <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?api . ?api <http://www.d-net.research-infrastructures.eu/provenance/isApiOf> ?ds}
			} 
			group by ?ds ?class ?instanceURI ?instance_label
			order by ?ds ?class

			#---end of query ----
			"""
		]
    },
]

# Notes on syntax of queries-set:
# * the set of queries is enclosed by '[' and ']'
# * individual queries are enclosed by '{' and '},'
# * All elements of a query (title, description, query) need to be defined using quotes as well as their contents, and both need to be separated by ':'
# * All elements of a query (title, description, query) need to be separated from each other using quotes ','
# * The content of a query needs to be defined using triple quotes, e.g. """ SELECT * WHERE .... """
# * Any indentation (tabs or spaces) do not influence the queries-syntax, they are merely syntactic sugar.
