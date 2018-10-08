# title
# defines the title of the whole set of queries
# OPTIONAL, if not set, timestamp will be used
title = "JRR_Quality_Test_Queries_V1.2.1_Overall"


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
output_destination = r"https://drive.google.com/drive/folders/1hAA4_r-PWA-hyYCZYgMY0XQsvKoPNHLY"


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
		"title" : "class_population_overall.V1.5",
		"description" : "This query gives the density of population of classes by instances for all providers giving data to the registry, grouping by provider.",
		"query" : [
			r"""
            #3 ######### Counts instances per class ignoring the record. To have the instances per class replace count(distinct ?instanceURI) with ?instanceURI in 'select' clause #########

			#DEFINE input:inference 'parthenos_rules'
			select ?class (count(distinct ?instanceURI) as ?count)
			#(replace(str(?class),"(^.*/)",  "", "i" ) as ?class_label)
			( STR(?class_label) as ?class_label)
			( STR(?ds) as ?ds )
			where{
			graph ?gRecord  {
			?instanceURI a ?class.
			}

			optional{
			?class rdfs:label ?class_label.
			FILTER(langmatches(lang(?class_label), "en") || langmatches(lang(?class_label), ""))
			}

			#values ?ds { "PARTHENOS"^^<http://www.w3.org/2001/XMLSchema#string> }
			GRAPH <dnet:graph> {?gRecord <dnet:collectedFrom> ?api . ?api <dnet:isApiOf> ?ds}
			} 
			group by ?ds ?class ?class_label
			order by ?ds ?class
			"""
		]
    },
    {
		"title" : "class_population_PE_top_overall.V1.2",
		"description" : "This query gives the density of population of classes by instances grouped by Parthenos Top Level Entities (Projects, Services, Actors, Datasets and Software)  for all providers giving data to the registry, grouping by provider.",
		"query" :
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

			#values ?ds { "PARTHENOS"^^<http://www.w3.org/2001/XMLSchema#string>}
			GRAPH <dnet:graph> {?gRecord <dnet:collectedFrom> ?api . ?api <dnet:isApiOf> ?ds}
			} 
			group by ?ds ?topclass ?class ?topclass_label ?class_label
			order by ?ds ?topclass ?class
			"""
    },
    {
		"title" : "all_types_overall.V1.1",
		"description" : "This query returns all instances of type in all datasets in kb given by providers, grouped by provider.",
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

			GRAPH <dnet:graph> {?gRecord <dnet:collectedFrom> ?api . ?api <dnet:isApiOf> ?ds}
			} 
			order by  ?ds ?instanceURI


			#---end of query ----
			"""
		]
    },
    {
		"title" : "place_instances_count_overall.V1.1",
		"description" : "This query gives the list of instances of E53 class existing in a data source and the number of times it is used.",
		"query" : [
			r"""
            #7b ############ Get the Places instances COUNT per Datasource ###########

			select 
			(?instanceURI as ?place)
			#( GROUP_CONCAT(distinct ?place_labelX, "/") as ?place_label)
			(STR(?place_label) as ?place_label)
			(COUNT(distinct ?resource) as ?placeAppearance)
			(str(?ds) as ?ds) 
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

			#values ?ds { "PARTHENOS"^^<http://www.w3.org/2001/XMLSchema#string> }
			GRAPH <dnet:graph> {?gRecord <dnet:collectedFrom> ?api . ?api <dnet:isApiOf> ?ds}

			} group by ?ds ?instanceURI ?place_label
			order by ?ds

			#---end of query ----
			"""
		]
    },
    {
		"title" : "periods_and_events_count_overall.V1.2",
		"description" : "This query gives the list of instances of E4 Period and E5 Event existing in all data sources and their counts.",
		"query" :
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

			#values ?ds { "PARTHENOS"^^<http://www.w3.org/2001/XMLSchema#string> }
			GRAPH <dnet:graph> {?gRecord <dnet:collectedFrom> ?api . ?api <dnet:isApiOf> ?ds}
			} 
			group by ?ds ?class ?instanceURI ?instance_label
			order by ?ds ?class

			#---end of query ----
			"""
    }
]

# Notes on syntax of queries-set:
# * the set of queries is enclosed by '[' and ']'
# * individual queries are enclosed by '{' and '},'
# * All elements of a query (title, description, query) need to be defined using quotes as well as their contents, and both need to be separated by ':'
# * All elements of a query (title, description, query) need to be separated from each other using quotes ','
# * The content of a query needs to be defined using triple quotes, e.g. """ SELECT * WHERE .... """
# * Any indentation (tabs or spaces) do not influence the queries-syntax, they are merely syntactic sugar.
