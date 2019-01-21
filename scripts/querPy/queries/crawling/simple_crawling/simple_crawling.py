
title = "simple_crawling v1.0"

description = """
Simple crawling utilizing manual recursion of sparql queries. 

This can be tweaked in a crude way by changing the variable 'start_query' and the depth when the MetaFunctionManager object is created 'meta_functions_manager'. Both are marked with the comment 'MODIFIABLE'

The crawling is started from a given start_query, from which querPy reuses the results to generate new queries so that it 'branches out' from the original query, which is done by following all relations and counting their numbers. All of this crawling logic is done by the class MetaFunctionsManager below. The 'crawling depth' defines the number of relation-steps from the original query results and can be adjusted. 

Also a text file is written locally ('results.txt') which contains a more compressed view on the results."""


output_destination = r"https://drive.google.com/drive/folders/17YIw327UaATOSfAN1pWwVIVBpCSJKUw-?usp=sharing"

summary_sample_limit = 100

cooldown_between_queries = 3

write_empty_results = False

count_the_results = False

endpoint = "https://virtuoso.parthenos.d4science.org/sparql"



# The MetaFunctionsManager class, encapsulating all the crawling logic 

class MetaFunctionsManager:

    def __init__(self, depth_limit = None):

        self.depth_limit = depth_limit
        self.helper = self.HelperFunctions()
        self.file_writer = open("./results.txt", 'w')
        self._id_current = 0

    @property
    def get_current_id(self):
        self._id_current += 1
        return self._id_current


    def crawl_further(self, query_data_object):

        def main():
            print("\nCALL META FUNCTION: crawl_further\n")
            try:
                for i in range(1, len( query_data_object.results_matrix )):
                    current_depth = query_data_object.custom_data_container['current_depth'] + 1
                    create_crawling_query( query_data_object.results_matrix[i], current_depth)
            except KeyError as ex:
                print("ERROR: " + str(ex))


        def create_crawling_query(results_row, current_depth):


            ### get resulting relations for query and output

            nodeset_current = results_row[0]
            nodeset_next = results_row[1]
            nodeset_current_count = results_row[2]
            nodeset_next_count = results_row[3]
            relation_outgoing = results_row[4]
            relation_outgoing_count = results_row[5]
            relation_incoming = results_row[6]
            relation_incoming_count = results_row[7]
            id_query_current = query_data_object.custom_data_container['id']
            id_query_next = self.get_current_id


            ### write resulting relation details to output

            if relation_outgoing != '':
                result_message = \
                    nodeset_current + " (id:" + str(id_query_current) + ", count: " + str(nodeset_current_count) + ")" + \
                    "    --" + relation_outgoing + " (count: " + str(relation_outgoing_count) + ")->    " + \
                    nodeset_next + " (id:" + str(id_query_next) + ", count: " + str(nodeset_next_count) + ") \n"
            elif relation_incoming != '':
                result_message = \
                    nodeset_current + " (id:" + str(id_query_current) + ", count: " + str(nodeset_current_count) + ")" + \
                    "    <-" + relation_incoming + " (count: " + str(relation_incoming_count) + ")--    " + \
                    nodeset_next + " (id:" + str(id_query_next) + ", count: " + str(nodeset_next_count) + ") \n"
            else:
                raise ValueError('No relation found.')

            print(result_message)
            self.file_writer.write(result_message)
            self.file_writer.flush()


            ### construct query for further crawling

            if relation_outgoing != '':
                relation_query_string = "?n__Y <" + relation_outgoing + "> ?n__X ."
            elif relation_incoming != '':
                relation_query_string = "?n__X <" + relation_incoming + "> ?n__Y ."
            else:
                raise ValueError('No relation found.')


            nodes_query_string = r"""

                select ?n__X ?n__Y where {

                    """ + relation_query_string + r"""

                    filter ( ?n__X != ?n__Z )

                    {""" + "\n" + query_data_object.custom_data_container['sub_query'] + r"""
                    }
                }

            """


            nodes_query_string = \
                self.helper.insert_current_depth(nodes_query_string, current_depth)

            crawling_query_string = \
                self.helper.create_crawling_query(nodes_query_string, current_depth + 1)

            queries.append({
                "query": crawling_query_string,
                "custom_meta_function": meta_functions_manager.crawl_further,
                "custom_data_container": {
                    "sub_query": nodes_query_string,
                    "current_depth": current_depth,
                    "id": id_query_next
                }
            })


        main()



    class HelperFunctions:

        def insert_current_depth(self, query_string, current_depth):

            # query_string = query_string.replace("?n_p_nr__X", "?n_p_nr__" + str(current_depth))
            # query_string = query_string.replace("?nl_p_n__X", "?nl_p_n__" + str(current_depth))
            # query_string = query_string.replace("?nr__X", "?nr__" + str(current_depth))
            # query_string = query_string.replace("?nl__X", "?nl__" + str(current_depth))
            if current_depth >= 2:
                query_string = query_string.replace("n__Z", "n__" + str(current_depth - 2))
            else:
                query_string = query_string.replace("n__Z", "n__Y")
            query_string = query_string.replace("n__X", "n__" + str(current_depth))
            query_string = query_string.replace("n__Y", "n__" + str(current_depth - 1))
            query_string = query_string.replace("#subquery__Y", "#subquery__" + str(current_depth - 1))
            query_string.replace("#filter__X", "#filter__" + str(current_depth))

            return query_string


        def create_crawling_query(self, query_string, current_depth):

            crawling_query = r"""
                select 
                
                    '?n__Y' as ?nodeset_current
                    '?n__X' as ?nodeset_next
                
                    count( distinct ?n__Y) as ?n__Y_count
                    count( distinct ?n__X) as ?n__X_count
                     
                    ?relation_outgoing 
                    count(?relation_outgoing) as ?relations_count_outgoing
                    ?relation_incoming
                    count(?relation_incoming) as ?relations_count_incoming 
                    
                where {
                    
                    {
                        ?n__Y ?relation_outgoing ?n__X
                    } union {
                        ?n__X ?relation_incoming ?n__Y
                    }
                    filter ( ?n__Z != ?n__X )

                    {
                        """ + "\n" + query_string + r"""
                    }          
                }
            """

            crawling_query = self.insert_current_depth(crawling_query, current_depth)
            return crawling_query





# MODIFIABLE: define a custom starting query here

start_query = r"""
    select distinct ?n__0 where {
        ?n__0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.cidoc-crm.org/cidoc-crm/E39_Actor> .
    }
"""


# MODIFIABLE: creating an instance of MetaFunctionsManager

meta_functions_manager = MetaFunctionsManager(depth_limit=1)


# Do not change this list
queries = [
    {
        "query": meta_functions_manager.helper.create_crawling_query(start_query, 1),
        "custom_meta_function": meta_functions_manager.crawl_further,
        "custom_data_container": {
            "current_depth": 0,
            "sub_query": start_query,
            "id": meta_functions_manager.get_current_id
        }
    },
]
