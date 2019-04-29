from operator import itemgetter

title = "metadata_validation_against_ontologies"

output_destination = r"./results"


output_format = "xlsx"


summary_sample_limit = 100


cooldown_between_queries = 0


write_empty_results = False


count_the_results = False



endpoint = "http://blazegraph.herkules.arz.oeaw.ac.at/parthenos-dev/sparql"
# endpoint = "http://localhost:8890/sparql"




global_data_container = {}


def remove_crm_identifier(value):

    if type(value) is str:

        value = value \
            .replace('http://www.cidoc-crm.org/cidoc-crm/', '') \
            .replace('http://www.cidoc-crm.org/cidoc-crm/CRMsci/', '') \
            .replace('CRMsci/', '') \
            .replace('CRMgeo/', '') \
            .replace('CRMarchaeo/', '') \
            .replace('http://parthenos.d4science.org/CRMext/CRMpe.rdfs/', '') \
            .replace('http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/', '') \
            .replace('http://www.ics.forth.gr/isl/CRMdig/', '') \
            .replace('http://iflastandards.info/ns/fr/frbr/frbroo/', '') \
            .replace('http://www.w3.org/2000/01/rdf-schema#', '') \
            .replace('http://www.w3.org/2001/XMLSchema#', '') \
            .replace('http://www.w3.org/2004/02/skos/core#', '')

        value = value.split('_')[0]

        return value

    else:
        return value


def save_result_in_global_data_container(query_data_object):

    global_data_container['overall_instance_count'] = query_data_object.results_matrix[1][0]



def check_valid_properties(query_data_object):

    def main_check_valid_properties(query_data_object):

        global_data_container['all_properties_and_types'] = merge_relations_with_inverses(query_data_object.results_matrix)
        create_queries_from_properties_and_types(global_data_container['all_properties_and_types'])


    def merge_relations_with_inverses(results_matrix):

        all_properties_and_types = []
        number_properties_out = 0
        number_properties_in = 0

        for i in range(1, len(results_matrix)):

            row = results_matrix[i]

            base_type = row[0]
            base_type_shortened = remove_crm_identifier(base_type)
            if base_type == '':
                base_type = None
                base_type_shortened = None

            super_type = row[1]
            super_type_shortened = remove_crm_identifier(super_type)
            if super_type == '':
                super_type = None
                super_type_shortened = None

            property = row[2]
            property_shortened = remove_crm_identifier(property)
            if property == '':
                raise ValueError("This should never happen!\n", row)

            subject_type = row[3]
            subject_type_shortened = remove_crm_identifier(subject_type)
            if subject_type == '':
                subject_type = None
                subject_type_shortened = None

            object_type = row[4]
            object_type_shortened = remove_crm_identifier(object_type)
            if object_type == '':
                object_type = None
                object_type_shortened = None

            property_out = None
            property_out_shortened = None
            property_in = None
            property_in_shortened = None

            if object_type is not None:
                # use object_type as other_type

                number_properties_out += 1

                other_type = object_type
                other_type_shortened = object_type_shortened
                property_out = property
                property_out_shortened = property_shortened


            elif subject_type is not None:
                # use subject_type as other_type

                number_properties_in += 1

                other_type = subject_type
                other_type_shortened = subject_type_shortened
                property_in = property
                property_in_shortened = property_shortened


            else:
                raise ValueError("This should never happen!\nCurrent row:", row)

            found = False
            for properties_and_types in all_properties_and_types:

                if property_out_shortened is not None:

                    if \
                            properties_and_types['property_in_shortened'] is not None and (
                                    properties_and_types['property_in_shortened'] == property_out_shortened + "i" or
                                    properties_and_types['property_in_shortened'] + "i" == property_out_shortened):

                        found = True

                        if properties_and_types['property_out'] is not None or properties_and_types[
                            'other_type'] is None:
                            raise ValueError("This should never happen!\nCurrent properties_and_types:",
                                             properties_and_types)

                        properties_and_types['property_out'] = property_out
                        properties_and_types['property_out_shortened'] = property_out_shortened


                elif property_in_shortened is not None:

                    if \
                            properties_and_types['property_out_shortened'] is not None and (
                                    properties_and_types['property_out_shortened'] == property_in_shortened + "i" or
                                    properties_and_types['property_out_shortened'] + "i" == property_in_shortened):

                        found = True

                        if properties_and_types['property_in'] is not None or properties_and_types[
                            'other_type'] is None:
                            raise ValueError("This should never happen!\nCurrent properties_and_types:",
                                             properties_and_types)

                        properties_and_types['property_in'] = property_in
                        properties_and_types['property_in_shortened'] = property_in_shortened


                else:
                    raise ValueError("This should never happen!")

            if not found:
                all_properties_and_types.append({
                    'base_type': base_type,
                    'base_type_shortened': base_type_shortened,
                    'super_type': super_type,
                    'super_type_shortened': super_type_shortened,
                    'property_out': property_out,
                    'property_out_shortened': property_out_shortened,
                    'property_in': property_in,
                    'property_in_shortened': property_in_shortened,
                    'other_type': other_type,
                    'other_type_shortened': other_type_shortened,
                })

        if \
                (number_properties_out + number_properties_in) != (len(results_matrix) - 1):
            raise ValueError("This should never happen!")

        print("\nFound " + str(len(all_properties_and_types)) + " properties\n")


        return all_properties_and_types





    def create_queries_from_properties_and_types(all_properties_and_types):

        for properties_and_types in all_properties_and_types:

        # for i in {6, 17, 18}:
        #     properties_and_types = all_properties_and_types[i]


            base_type = properties_and_types['base_type']
            base_type_shortened = properties_and_types['base_type_shortened']
            property_out = properties_and_types['property_out']
            property_out_shortened = properties_and_types['property_out_shortened']
            property_in = properties_and_types['property_in']
            property_in_shortened = properties_and_types['property_in_shortened']
            other_type = properties_and_types['other_type']
            other_type_shortened = properties_and_types['other_type_shortened']



            # create title

            if property_out_shortened is not None and property_out_shortened[-1] != "i":

                title_correct_type = \
                    base_type_shortened + "-" +\
                    property_out_shortened + "->" + \
                    other_type_shortened

                title_incorrect_type = \
                    base_type_shortened + "-" +\
                    property_out_shortened + "->" + \
                    "Not" + other_type_shortened

            elif property_in_shortened is not None and property_in_shortened[-1] != "i":

                title_correct_type = \
                    other_type_shortened + "-" + \
                    property_in_shortened + "->" + \
                    base_type_shortened

                title_incorrect_type = \
                    "Not" + other_type_shortened + "-" + \
                    property_in_shortened + "->" + \
                    base_type_shortened

            else:
                raise ValueError("This should never happen!\n", properties_and_types)





            # create query

            if properties_and_types['other_type_shortened'] == "Literal":

                query_string_correct_type = r"""
                    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

                    select
                    (count( distinct ?base_instance ) as ?base_instance_count)
                    (count(*) as ?relations_count)
                    (count( distinct ?literal_instance ) as ?literal_instance_count)
                    where {

                        select
                        distinct ?base_instance ?literal_instance
                        where {
                            ?base_instance  rdf:type  ?base_intermediate_type .
                            ?base_intermediate_type  rdfs:subClassOf*  <""" + base_type + r"""> .

                            ?base_instance  <""" + property_out + r""">   ?literal_instance .

                            filter ( isLiteral( ?literal_instance ) )
                        }
                    }
                """

                query_string_incorrect_type = r"""
                    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

                    select
                    (count( distinct ?base_instance ) as ?base_instance_count)
                    (count(*) as ?relations_count)
                    (count( distinct ?literal_instance ) as ?literal_instance_count)
                    where {

                        select
                        distinct ?base_instance ?literal_instance ?other_intermediate_type
                        where {
                            ?base_instance  rdf:type  ?base_intermediate_type .
                            ?base_intermediate_type  rdfs:subClassOf*  <""" + base_type + r"""> .

                            ?base_instance  <""" + property_out + r""">   ?literal_instance .
                            
                            filter ( !isLiteral( ?literal_instance ) )
                        }
                    }
                """

            else:

                relation_query_substring = ""

                if property_out is not None and property_in is not None:
                    relation_query_substring = r"""
                            { ?base_instance  <""" + property_out + r""">   ?other_instance . } union
                            { ?other_instance  <""" + property_in + r""">   ?base_instance . }"""

                elif property_out is not None and property_in is None:
                    relation_query_substring = r"""
                            ?base_instance  <""" + property_out + r""">   ?other_instance . """

                elif property_out is None and property_in is not None:
                    relation_query_substring = r"""
                            ?other_instance  <""" + property_in + r""">   ?base_instance . """
                else:
                    raise ValueError("This should never happen!\n", properties_and_types)



                query_string_correct_type = r"""
                    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
                    select
                    (count( distinct ?base_instance ) as ?base_instance_count)
                    (count(*) as ?relations_count)
                    (count( distinct ?other_instance ) as ?other_instance_count)
                    where {
        
                        select
                        distinct ?base_instance ?other_instance
                        where {
                            ?base_instance  rdf:type  ?base_intermediate_type .
                            ?base_intermediate_type  rdfs:subClassOf*  <""" + base_type + r""">  .
                            
                            """ \
                            + relation_query_substring + \
                            r"""
                            
                            ?other_instance  rdf:type  ?other_intermediate_type .
                            ?other_intermediate_type  rdfs:subClassOf*  <""" + other_type + r"""> . 
                        }
                    }
                """

                query_string_incorrect_type = r"""
                    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
                    select
                    (count( distinct ?base_instance ) as ?base_instance_count)
                    (count(*) as ?relations_count)
                    (count( distinct ?other_instance ) as ?other_instance_count)
                    where {
        
                        select
                        distinct ?base_instance ?other_instance
                        where {
                            ?base_instance  rdf:type  ?base_intermediate_type .
                            ?base_intermediate_type  rdfs:subClassOf*  <""" + base_type + r""">  .
                            
                            """ \
                            + relation_query_substring + \
                            r"""
        
                            ?other_instance  rdf:type  ?other_intermediate_type .
                            
                            filter not exists {
                                ?other_intermediate_type  rdfs:subClassOf*  <""" + other_type + r"""> .
                            } 
                            
                        }
                    }
                """


            queries.append({
                "title": title_correct_type,
                "query": query_string_correct_type,
                "custom_data_container" : properties_and_types,
                "custom_meta_function": attach_correct_results_to_global_container
            })

            queries.append({
                "title": title_incorrect_type,
                "query": query_string_incorrect_type,
                "custom_data_container" : properties_and_types,
                "custom_meta_function": attach_incorrect_results_to_global_container
            })



    main_check_valid_properties(query_data_object)



def attach_correct_results_to_global_container(query_data_object):

    properties_and_types = query_data_object.custom_data_container

    results_matrix = query_data_object.results_matrix

    if len(results_matrix) != 2:
        raise ValueError("This should never happen!\n", results_matrix)

    properties_and_types["base_instance_count_correct"] = results_matrix[1][0]

    properties_and_types["relations_count_correct"] = results_matrix[1][1]
    properties_and_types["other_instance_count_correct"] = results_matrix[1][2]

    if global_data_container['overall_instance_count'] != 0:
        properties_and_types['ratio_correct'] = properties_and_types["relations_count_correct"] / global_data_container['overall_instance_count']
    else:
        properties_and_types['ratio_correct'] = 0


def attach_incorrect_results_to_global_container(query_data_object):

    properties_and_types = query_data_object.custom_data_container

    results_matrix = query_data_object.results_matrix

    if len(results_matrix) != 2:
        raise ValueError("This should never happen!\n", results_matrix)

    properties_and_types["base_instance_count_incorrect"] = results_matrix[1][0]

    properties_and_types["relations_count_incorrect"] = results_matrix[1][1]
    properties_and_types["other_instance_count_incorrect"] = results_matrix[1][2]

    if global_data_container['overall_instance_count'] != 0:
        properties_and_types['ratio_incorrect'] = properties_and_types["relations_count_incorrect"] / global_data_container['overall_instance_count']
    else:
        properties_and_types['ratio_incorrect'] = 0




def attach_invalid_properties_to_global_container(query_data_object):

    global_data_container['all_invalid_properties'] = query_data_object.results_matrix







def custom_pre_processing():

    print("CALLING custom_pre_processing")

    global_data_container.clear()
    queries.clear()

    # types = ["http://www.cidoc-crm.org/cidoc-crm/E39_Actor"]
    # types = ["http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE13_Software_Computing_E-Service"]
    # types = ["http://www.cidoc-crm.org/cidoc-crm/E4_Period"]
    # types = [ "http://www.cidoc-crm.org/cidoc-crm/E53_Place", "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE13_Software_Computing_E-Service" ]

    # types = ["http://www.cidoc-crm.org/cidoc-crm/E53_Place", "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE13_Software_Computing_E-Service"]
    # types = ["http://www.cidoc-crm.org/cidoc-crm/E53_Place", "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE13_Software_Computing_E-Service", "http://www.cidoc-crm.org/cidoc-crm/E39_Actor"]

    types = [
        "http://www.cidoc-crm.org/cidoc-crm/E53_Place",
        "http://www.cidoc-crm.org/cidoc-crm/E39_Actor",
        "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE18_Dataset",
        "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE1_Service",
        "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D14_Software",
    ]

    queries.append({
        "title": "Get count of instances of given type",
        "query": [r"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            select (count(distinct ?base_instance) as ?base_instance_count) where {
            
                ?base_instance  rdf:type  ?base_intermediate_type .
                ?base_intermediate_type  rdfs:subClassOf*  <""", types, r""">   .
            }
        """],
        "custom_meta_function": save_result_in_global_data_container
    })



    queries.append({
        "title": "extract relations from ontologies",
        "query": [r"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT distinct ?base_type ?super_type ?property ?subject_type ?object_type WHERE {
                
              {
                ?property rdfs:domain ?super_type .
                ?base_type rdfs:subClassOf* ?super_type .
            
                ?property rdfs:range ?object_type .
              }
              union 
              {
                ?property rdfs:range ?super_type .
                ?base_type rdfs:subClassOf* ?super_type .
            
                ?property rdfs:domain ?subject_type .
              }
              
              values ?base_type { <""", types, r""">  }
            }
            order by ?property
        """],
        "custom_meta_function": check_valid_properties
    })



    queries.append({
        "title": "check for invalid properties",
        "query": [r"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            select ?instance_type  ?property_out_wrong ?property_in_wrong ?count where {
              
              filter ( ?property_out_wrong != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> )
              
              filter not exists {
                 ?property_out_wrong  rdfs:domain  ?intermediate_subject_type .
                 ?instance_type  rdfs:subClassOf*  ?intermediate_subject_type .
                
                 ?property_in_wrong  rdfs:range  ?intermediate_object_type .
                 ?instance_type  rdfs:subClassOf*  ?intermediate_object_type
              } 
              
              
              bind ( ?property_out as ?property_out_wrong )
              bind ( ?property_in as ?property_in_wrong )
              
              {
                select ?property_out ?property_in ?instance_type (count(?instance) as ?count) where {
            
                  ?instance  rdf:type  ?instance_type .
                  ?instance_type  rdfs:subClassOf* <""", types, r""">    .
            
                  { ?instance  ?property_out [] . } union
                  { [] ?property_in  ?instance . }
                }
                group by ?property_out ?property_in ?instance_type
              }
            }    
        """],
        "custom_meta_function": attach_invalid_properties_to_global_container
    })

    



queries = [
]





def custom_post_processing(results):

    def matrix_to_pretty_string(matrix):

        matrix_string = ""

        max_length = 0
        for row in matrix:
            for col in row:
                if col is not None and len(str(col)) > max_length:
                    max_length = len(str(col))
        max_length += 2

        for row in matrix:
            row_string = ""
            for col in row:
                if col is None:
                    row_string += "None".ljust(max_length)
                else:
                    row_string += str(col).ljust(max_length)
            matrix_string += row_string + "\n"

        return matrix_string



    result_summary = ""
    result_csv = []


    all_properties_and_types = global_data_container['all_properties_and_types']


    result_summary += "\n\n####################################################################################"
    message = "Results regarding " + all_properties_and_types[0]['base_type_shortened']
    result_summary += "\n" + message
    result_csv.append([])
    result_csv.append([message])


    overall_instance_count = global_data_container['overall_instance_count']
    message = "Count of instances overall:" + str(overall_instance_count)
    result_summary += "\n\n\n" + message
    result_csv.append([])
    result_csv.append([message])


    message = "Extracted " + str(len(all_properties_and_types)) + \
        " properties and their respective types from ontologies. Compared them to existing instances:\n\n"
    result_summary += "\n\n\n" + message
    result_csv.append([])
    result_csv.append([message])


    properties_and_types_matrix_summary = [[
        "type",
        "property out",
        "property in",
        "other type",
        "relations correct type",
        "ratio_correct",
        "relations incorrect type",
        "ratio_incorrect"
    ]]

    properties_and_types_matrix_csv = [[
        "type_shortened",
        "property_out_shortened",
        "property_in_shortened",
        "other_type_shortened",

        "relations correct type",
        "ratio_correct",
        "relations incorrect type",
        "ratio_incorrect",
        
        "type_full",
        "property_out_full",
        "property_in_full",
        "other_type_full",
    ]]



    for properties_and_types in all_properties_and_types:

    # for i in {6, 17, 18}:
    #     properties_and_types = all_properties_and_types[i]

        properties_and_types_matrix_summary.append([
            properties_and_types['super_type_shortened'],
            properties_and_types['property_out_shortened'],
            properties_and_types['property_in_shortened'],
            properties_and_types['other_type_shortened'],
            properties_and_types["relations_count_correct"],
            round(properties_and_types['ratio_correct'], 2),
            properties_and_types["relations_count_incorrect"],
            round(properties_and_types['ratio_incorrect'], 2),
        ])

        properties_and_types_matrix_csv.append([

            properties_and_types['super_type_shortened'],
            properties_and_types['property_out_shortened'],
            properties_and_types['property_in_shortened'],
            properties_and_types['other_type_shortened'],

            properties_and_types["relations_count_correct"],
            round(properties_and_types['ratio_correct'], 2),
            properties_and_types["relations_count_incorrect"],
            round(properties_and_types['ratio_incorrect'], 2),

            properties_and_types['super_type'],
            properties_and_types['property_out'],
            properties_and_types['property_in'],
            properties_and_types['other_type'],
        ])


    properties_and_types_pretty_string = matrix_to_pretty_string( properties_and_types_matrix_summary )

    result_summary += properties_and_types_pretty_string
    result_csv.append([])
    for row in properties_and_types_matrix_csv:
        result_csv.append(row)




    all_invalid_properties = global_data_container['all_invalid_properties']

    message = "Found " + str(len(all_invalid_properties)-1) + " wrongly assigned properties:\n\n"
    result_summary += "\n\n\n" + message
    result_csv.append([])
    result_csv.append([message])

    all_invalid_properties_pretty_string = matrix_to_pretty_string(all_invalid_properties)

    result_summary += all_invalid_properties_pretty_string
    result_csv.append([])
    result_csv.append(all_invalid_properties[0])
    for row in all_invalid_properties[1:]:

        row_tmp = []

        for column in row:
            row_tmp.append(remove_crm_identifier(column))

        result_csv.append(row_tmp)

    result_csv.append([])
    result_csv.append([])
    result_csv.append([])

    print(result_summary)

    with open(output_destination + "/summary.txt", "w") as output_file:
        output_file.write(result_summary)

    import csv

    with open(output_destination + "/results.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(result_csv)
