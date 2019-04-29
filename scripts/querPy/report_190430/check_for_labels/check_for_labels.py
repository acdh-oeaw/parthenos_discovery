
# -------------------- OPTIONAL SETTINGS --------------------

# title
# defines the title of the whole set of queries
# OPTIONAL, if not set, timestamp will be used
title = "check_for_labels"


# description
# defines the textual and human-intended description of the purpose of these queries
# OPTIONAL, if not set, nothing will be used or displayed
description = ""


# output_destination
# defines where to save the results, input can be: 
# * a local path to a folder 
# * a URL for a google sheets document  
# * a URL for a google folder
# NOTE: On windows, folders in a path use backslashes, in such a case it is mandatory to attach a 'r' in front of the quotes, e.g. r"C:\Users\sresch\.."
# In the other cases the 'r' is simply ignored; thus best would be to always leave it there.
# OPTIONAL, if not set, folder of executed script will be used
output_destination = r"./results"


# output_format
# defines the format in which the result data shall be saved (currently available: csv, tsv, xml, json, xlsx)
# OPTIONAL, if not set, csv will be used
output_format = "xlsx"


# summary_sample_limit
# defines how many rows shall be displayed in the summary
# OPTIONAL, if not set, 5 will be used
summary_sample_limit = 100


# cooldown_between_queries
# defines how many seconds should be waited between execution of individual queries in order to prevent exhaustion of Google API due to too many writes per time-interval
# OPTIONAL, if not set, 0 will be used
cooldown_between_queries = 0


# write_empty_results
# Should tabs be created in a summary file for queries which did not return results? Possible values are python boolean values: True, False
# OPTIONAL, if not set, False will be used
write_empty_results = False

count_the_results = False


# -------------------- MANDATORY SETTINGS -------------------- 

# endpoint
# defines the SPARQL endpoint against which all the queries are run
# MANDATORY
# endpoint = "http://localhost:8890/sparql"
endpoint = "https://virtuoso.parthenos.d4science.org/sparql"
# endpoint = "http://blazegraph.herkules.arz.oeaw.ac.at/parthenos-dev/sparql"


global_data_list = [[
	"description",
	"number of results",
	"percentage of results"
]]

def save_count_of_all(query_data_object):
	
	global_data_list.append([
		query_data_object.title, 
		int(query_data_object.results_matrix[1][0]),
		100.0
	])
	
	
def calculate_percentage(query_data_object):
	
	count_of_all = global_data_list[1][1]

	results_matrix = query_data_object.results_matrix
	if len(results_matrix) > 1:
		count_total = int(query_data_object.results_matrix[1][0])
	else:
		count_total = 0
	
	count_percentage = round(100 / count_of_all * count_total, 1)
	
	global_data_list.append([
		query_data_object.title, 
		count_total,
		count_percentage
	])


def calculate_percentage_of_properties(query_data_object):

	count_of_all = global_data_list[1][1]

	results_matrix = query_data_object.results_matrix
	if len(results_matrix) > 1:

		for result in results_matrix[1:]:

			property = result[0]
			property_count_total = int(result[1])
			property_count_percentage = round(100 / count_of_all * property_count_total, 1)

			global_data_list.append([
				"count where object is literal of property: " + property,
				property_count_total,
				property_count_percentage
			])

	

# queries
# defines the set of queries to be run. 
# MANDATAORY
queries = [
	{
		"title": "count of all subjects in general",
		"query": r"""
			select (count(distinct ?s) as ?count) where {
				?s ?p ?o 
			}
		""",
		"custom_meta_function": save_count_of_all
	},
    {
		"title": "count of subjects that have property rdfs:label",
		"query": r"""
			select (count(distinct ?s) as ?count) where {
				?s <http://www.w3.org/2000/01/rdf-schema#label> ?o 
			}
			
		""",
		"custom_meta_function": calculate_percentage
    },
    {
		"title": "count of subjects that have property rdfs:label and the object is literal",
		"query": r"""
			select (count(distinct ?s) as ?count) where {
				?s <http://www.w3.org/2000/01/rdf-schema#label> ?o .
				filter isLiteral ( ?o )
			}
		""",
		"custom_meta_function": calculate_percentage
    },
    {
		"title": "count of properties where the object is of type string",
		"query": r"""
			select ?p (count (distinct ?s) as ?count) where {
				?s ?p ?o .
				filter isLiteral ( ?o )
			}
			group by ?p
			order by desc(?count)
		""",
		"custom_meta_function": calculate_percentage_of_properties
    },
    
]

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
print(results[1].results_matrix)
'''

# UNCOMMENT THE FOLLOWING LINES FOR A QUICKSTART:
def custom_post_processing(results):

	import csv
	
	for line in global_data_list:
		print(line)


	with open(output_destination + "/results.csv", "w") as f:
		writer = csv.writer(f)
		writer.writerows(global_data_list)
