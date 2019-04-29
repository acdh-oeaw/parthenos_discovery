


# -------------------- OPTIONAL SETTINGS --------------------

# title
# defines the title of the whole set of queries
# OPTIONAL, if not set, timestamp will be used
title = "urn_url_count"


# description
# defines the textual and human-intended description of the purpose of these queries
# OPTIONAL, if not set, nothing will be used or displayed


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

# queries
# defines the set of queries to be run.
# MANDATAORY
queries = [
    {
        "title" : "count subjects" ,
        "query" : r"""
            SELECT (count(distinct ?s) as ?count) WHERE {
                ?s [] [] .
            }
        """
    },
    {
        "title" : "count subjects starting with \"http://\"" ,
        "query" : r"""
            SELECT (count(distinct ?s) as ?count) WHERE {
                ?s [] [] .
                filter ( strStarts( lcase(str(?s)), "http://") )
            }
        """
    },
    {
        "title" : "count subjects not starting with \"http://\"" ,
        "query" : r"""
            SELECT (count(distinct ?s) as ?count) WHERE {
                ?s [] [] .
                filter ( !strStarts( lcase(str(?s)), "http://") )
            }
        """
    },
    {
        "title" : "count subjects starting with \"urn:uuid\"" ,
        "query" : r"""
            SELECT (count(distinct ?s) as ?count) WHERE {
                ?s [] [] .
                filter ( strStarts( lcase(str(?s)), "urn:uuid") )
            }
        """
    },
    {
        "title" : "count subjects not starting with \"urn:uuid\"" ,
        "query" : r"""
            SELECT (count(distinct ?s) as ?count) WHERE {
                ?s [] [] .
                filter ( !strStarts( lcase(str(?s)), "urn:uuid") )
            }
        """
    },


    {
        "title" : "count properties",
        "query" : r"""
            SELECT (count(distinct ?p) as ?count) WHERE {
                [] ?p [] .
            }
        """
    },
    {
        "title" : "count properties starting with \"http://\"" ,
        "query" : r"""
            SELECT (count(distinct ?p) as ?count) WHERE {
                [] ?p [] .
                filter ( strStarts( lcase(str(?p)), "http://") )
            }
        """
    },
    {
        "title" : "count properties not starting with \"http://\"" ,
        "query" : r"""
            SELECT (count(distinct ?p) as ?count) WHERE {
                [] ?p [] .
                filter ( !strStarts( lcase(str(?p)), "http://") )
            }
        """
    },
    {
        "title" : "count properties starting with \"urn:uuid\"" ,
        "query" : r"""
            SELECT (count(distinct ?p) as ?count) WHERE {
                [] ?p [] .
                filter ( strStarts( lcase(str(?p)), "urn:uuid") )
            }
        """
    },
    {
        "title" : "count properties not starting with \"urn:uuid\"" ,
        "query" : r"""
            SELECT (count(distinct ?p) as ?count) WHERE {
                [] ?p [] .
                filter ( !strStarts( lcase(str(?p)), "urn:uuid") )
            }
        """
    },


    {
        "title" : "count objects" ,
        "query" : r"""
            SELECT (count(distinct ?o) as ?count) WHERE {
                [] [] ?o .
            }
        """
    },
    {
        "title" : "count objects starting with \"http://\"" ,
        "query" : r"""
            SELECT (count(distinct ?o) as ?count) WHERE {
                [] [] ?o .
                filter ( strStarts( lcase(str(?o)), "http://") )
            }
        """
    },
    {
        "title" : "count objects not starting with \"http://\"" ,
        "query" : r"""
            SELECT (count(distinct ?o) as ?count) WHERE {
                [] [] ?o .
                filter ( !strStarts( lcase(str(?o)), "http://") )
            }
        """
    },
    {
        "title" : "count objects starting with \"urn:uuid\"" ,
        "query" : r"""
            SELECT (count(distinct ?o) as ?count) WHERE {
                [] [] ?o .
                filter ( strStarts( lcase(str(?o)), "urn:uuid") )
            }
        """
    },
    {
        "title" : "count objects not starting with \"urn:uuid\"" ,
        "query" : r"""
            SELECT (count(distinct ?o) as ?count) WHERE {
                [] [] ?o .
                filter ( !strStarts( lcase(str(?o)), "urn:uuid") )
            }
        """
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

    all_query_data_objects = results.queries


    # subjects

    count_subjects = all_query_data_objects[0].results_matrix[1][0]
    count_subjects_with_http = all_query_data_objects[1].results_matrix[1][0]
    count_subjects_without_http = all_query_data_objects[2].results_matrix[1][0]
    count_subjects_with_urnUuid = all_query_data_objects[3].results_matrix[1][0]
    count_subjects_without_urnUuid = all_query_data_objects[4].results_matrix[1][0]

    if count_subjects - count_subjects_with_http != count_subjects_without_http:
        raise ValueError(
            "This should not happen!\n" +
            "Count of subjects: " + str(count_subjects) +
            "Count of subjects with http: " + str(count_subjects_with_http) +
            "Count of subjects without http: " + str(count_subjects_without_http)
        )

    if count_subjects - count_subjects_with_urnUuid != count_subjects_without_urnUuid:
        raise ValueError(
            "This should not happen!\n" +
            "Count of subjects: " + str(count_subjects) +
            "Count of subjects with \"urn:uuid\" : " + str(count_subjects_with_urnUuid) +
            "Count of subjects without \"urn:uuid\" : " + str(count_subjects_without_urnUuid)
        )

    percentage_subjects_with_http = 100 / count_subjects * count_subjects_with_http
    percentage_subjects_with_urnUuid = 100 / count_subjects * count_subjects_with_urnUuid


    # properties

    count_properties = all_query_data_objects[5].results_matrix[1][0]
    count_properties_with_http = all_query_data_objects[6].results_matrix[1][0]
    count_properties_without_http = all_query_data_objects[7].results_matrix[1][0]
    count_properties_with_urnUuid = all_query_data_objects[8].results_matrix[1][0]
    count_properties_without_urnUuid = all_query_data_objects[9].results_matrix[1][0]

    if count_properties - count_properties_with_http != count_properties_without_http:
        raise ValueError(
            "This should not happen!\n" +
            "Count of properties: " + str(count_properties) +
            "Count of properties with http: " + str(count_properties_with_http) +
            "Count of properties without http: " + str(count_properties_without_http)
        )

    if count_properties - count_properties_with_urnUuid != count_properties_without_urnUuid:
        raise ValueError(
            "This should not happen!\n" +
            "Count of properties: " + str(count_properties) +
            "Count of properties with \"urn:uuid\" : " + str(count_properties_with_urnUuid) +
            "Count of properties without \"urn:uuid\" : " + str(count_properties_without_urnUuid)
        )

    percentage_properties_with_http = 100 / count_properties * count_properties_with_http
    percentage_properties_with_urnUuid = 100 / count_properties * count_properties_with_urnUuid


    # objects

    count_objects = all_query_data_objects[10].results_matrix[1][0]
    count_objects_with_http = all_query_data_objects[11].results_matrix[1][0]
    count_objects_without_http = all_query_data_objects[12].results_matrix[1][0]
    count_objects_with_urnUuid = all_query_data_objects[13].results_matrix[1][0]
    count_objects_without_urnUuid = all_query_data_objects[14].results_matrix[1][0]

    if count_objects - count_objects_with_http != count_objects_without_http:
        raise ValueError(
            "This should not happen!\n" +
            "Count of objects: " + str(count_objects) +
            "Count of objects with http: " + str(count_objects_with_http) +
            "Count of objects without http: " + str(count_objects_without_http)
        )

    if count_objects - count_objects_with_urnUuid != count_objects_without_urnUuid:
        raise ValueError(
            "This should not happen!\n" +
            "Count of objects: " + str(count_objects) +
            "Count of objects with \"urn:uuid\" : " + str(count_objects_with_urnUuid) +
            "Count of objects without \"urn:uuid\" : " + str(count_objects_without_urnUuid)
        )

    percentage_objects_with_http = 100 / count_objects * count_objects_with_http
    percentage_objects_with_urnUuid = 100 / count_objects * count_objects_with_urnUuid


    # all entities

    count_all_entities = count_subjects + count_properties + count_objects

    count_all_entities_with_http = count_subjects_with_http + count_properties_with_http + count_objects_with_http
    percentage_all_entities_with_http = 100 / count_all_entities * count_all_entities_with_http

    count_all_entities_with_urnUuid = count_subjects_with_urnUuid + count_properties_with_urnUuid + count_objects_with_urnUuid
    percentage_all_entities_with_urnUuid = 100 / count_all_entities * count_all_entities_with_urnUuid


    print(
        "\n",
        "count of all entities :", count_all_entities, "\n",
        "percentage of all entities starting with \"http://\" :", round(percentage_all_entities_with_http, 1), "\n",
        "percentage of all entities starting with \"urn:uuid\" :", round(percentage_all_entities_with_urnUuid, 1), "\n",
        "\n",
        "count of all subjects :", count_subjects, "\n",
        "percentage of subjects starting with \"http://\" :", round(percentage_subjects_with_http, 1), "\n",
        "percentage of subjects starting with \"urn:uuid\" :", round(percentage_subjects_with_urnUuid, 1), "\n",
        "\n",
        "count of all properties :", count_properties, "\n",
        "percentage of properties starting with \"http://\" :", round(percentage_properties_with_http, 1), "\n",
        "percentage of properties starting with \"urn:uuid\" :", round(percentage_properties_with_urnUuid, 1), "\n",
        "\n",
        "count of all objects :", count_objects, "\n",
        "percentage of objects starting with \"http://\" :", round(percentage_objects_with_http, 1), "\n",
        "percentage of objects starting with \"urn:uuid\" :", round(percentage_objects_with_urnUuid, 1), "\n",
    )
