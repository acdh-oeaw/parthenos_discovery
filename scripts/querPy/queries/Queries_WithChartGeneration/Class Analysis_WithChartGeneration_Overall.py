
# -------------------- OPTIONAL SETTINGS --------------------

# title
# defines the title of the whole set of queries
# OPTIONAL, if not set, timestamp will be used
title = "queries for chart generation purposes_Overall"


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
output_destination = r"./results_local/Overall"


# output_format
# defines the format in which the result data shall be saved (currently available: csv, tsv, xml, json, xlsx)
# OPTIONAL, if not set, csv will be used
output_format = "xlsx"


# summary_sample_limit
# defines how many rows shall be displayed in the summary
# OPTIONAL, if not set, 5 will be used
summary_sample_limit = 3


# cooldown_between_queries
# defines how many seconds should be waited between execution of individual queries in order to prevent exhaustion of Google API due to too many writes per time-interval
# OPTIONAL, if not set, 0 will be used
cooldown_between_queries = 0


# write_empty_results
# Should tabs be created in a summary file for queries which did not return results? Possible values are python boolean values: True, False
# OPTIONAL, if not set, False will be used
write_empty_results = False


# variable datasources, individual values of this variable will be injected into the queries where used.
# datasources = ["CLARIN", "PARTHENOS", "Huma-Num - Nakala", "Huma-Num - Isidore", "European Holocaust Research Infrastructure", "ARIADNE", "Cultura Italia", "METASHARE", "LRE MAP"]

# -------------------- MANDATORY SETTINGS --------------------

# endpoint
# defines the SPARQL endpoint against which all the queries are run
# MANDATORY
endpoint = "https://virtuoso.parthenos.d4science.org/sparql"

# queries
# defines the set of queries to be run.
# MANDATAORY
queries = [
    {
        "title": "Instances and their count, overview_Overall",
        "query": r"""
            select ?resourceClass count(?resource) as ?countOfInstances where {
                ?resource a ?resourceClass
            }
            group by ?resourceClass
        """
    },
    {
        "title": "A weighted overview of all instanciated classes and their respective superClass hierarchy path_Overall",
        "description": "This query counts the number of classes which are instantiated by some resource, and then uses this number to give weight to the respective super class chain of the original class-instance. This way we can see which super classes are how often used for instantiation, either directly (a particular class is instantiated, while also having further sub classes) or indirectly (through subClass-relations leading to the original instances). Note that the ?resourceClass column displays where the path stems from, while ?superClass ?superSuperClass displays some edge in the super class hierarchy, ultimately leading to 'E1_CRM_Entity'. Also note in the sankey chart which is generated from this data, sometimes you will see intermediate nodes merging or splitting; when this happens it indicates some multiple inheritance, e.g. E77 isSubClassOf E1, while also E77 isSubClassOf S15 isSubClassOf E1, where then you would see an identical number of flows merging into E77. This does not mean there is double the amount of E77 instances, but only that there are multiple paths to the same superClass somewhere (and vice versa to subClasses).",
        "query": r"""
            select ?count ?resourceClass ?superClass ?superSuperClass where {

            ?resourceClass <http://www.w3.org/2000/01/rdf-schema#subClassOf>* ?superClass .
            ?superClass <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?superSuperClass

            {
                select count(?resource) as ?count ?resourceClass where {
                    ?resource a ?resourceClass
                }

            }
        }
        group by ?resourceClass ?superClass ?superSuperClass
        """
    },
]

# Each query is itself encoded as a python dictionary, and together these dictionaries are collected in a python list. Beginner's note on such syntax as follows:
# * the set of queries is enclosed by '[' and ']'
# * individual queries are enclosed by '{' and '},'
# * All elements of a query (title, description, query) need to be defined using quotes as well as their contents, and both need to be separated by ':'
# * All elements of a query (title, description, query) need to be separated from each other using quotes ','
# * The content of a query needs to be defined using triple quotes, e.g. """ SELECT * WHERE .... """
# * Any indentation (tabs or spaces) do not influence the queries-syntax, they are merely syntactic sugar.


def custom_post_processing(results):

    import sys

    def main(results):

        print("\nRunning post processing for chart generation.\n")

        create_pieChart_InstancesOverview(results[0])
        create_sankeyChart_InstancesSuperclassesOverview(results[1])



    def create_pieChart_InstancesOverview(query_results):
        import plotly.offline as offline
        import plotly.graph_objs

        results_matrix = query_results['results_matrix']

        labels = []
        values = []
        for i in range(1, len(results_matrix)):
            if results_matrix[i][1] > 10000:
                labels.append(clean_string_of_PE_prefixes(results_matrix[i][0]))
                values.append(results_matrix[i][1])


        offline.plot({
            "data": [
                plotly.graph_objs.Pie(
                    labels=labels,
                    values=values,
                    textinfo='label+value'
                )
            ],
            "layout" : dict( title=query_results['query_title'] )
        }, filename=query_results['query_title'] + ".html")




    def create_sankeyChart_InstancesSuperclassesOverview(query_result):
        import plotly.offline as offline

        def start_method(query_result):

            chart_data = process_data(query_result['results_matrix'])
            print("Created sankey flow chart data, number of such flows: " + str(len(chart_data['source'])))
            create_chart(chart_data, query_result['query_title'])

        def process_data(results_matrix):

            def make_flow_array(source, target, count, chart_data_local):

                try:
                    index_target = chart_data_local['label'].index(target)
                except ValueError:
                    chart_data_local['label'].append(target)
                    index_target = chart_data_local['label'].index(target)

                try:
                    index_source = chart_data_local['label'].index(source)
                except ValueError:
                    chart_data_local['label'].append(source)
                    index_source = chart_data_local['label'].index(source)

                pre_existing = False
                for i in range(0, len(chart_data_local['source'])):
                    if chart_data_local['source'][i] == index_source and chart_data_local['target'][i] == index_target:
                        chart_data_local['value'][i] = chart_data_local['value'][i] + count
                        pre_existing = True

                if not pre_existing:
                    chart_data_local['source'].append(index_source)
                    chart_data_local['target'].append(index_target)
                    chart_data_local['value'].append(count)

                return chart_data_local

            chart_data = {
                'label': [],
                'source': [],
                'target': [],
                'value': [],
            }

            end_nodes = []
            for i in range(1, len(results_matrix)):

                row = results_matrix[i]
                count = int(row[0])
                if (count > 10000):

                    instance = clean_string_of_PE_prefixes(row[1])
                    target = clean_string_of_PE_prefixes(row[2])
                    source = clean_string_of_PE_prefixes(row[3])

                    chart_data = make_flow_array(source, target, count, chart_data)
                    if (instance == target):
                        if not [instance, count] in end_nodes:
                            end_nodes.append([instance, count])

            ##### check if potential end nodes are indeed end nodes or have further children.

            # find indices of classes which have subclasses and direct instances
            sources_to_add_target_to_indices = []
            for end_node in end_nodes:

                instance_string = end_node[0]
                instance_count = end_node[1]

                instance_label_index = -1
                check_count = 0
                for i in range(0, len(chart_data['label'])):
                    if instance_string == chart_data['label'][i]:
                        instance_label_index = i
                        check_count += 1
                if check_count != 1:
                    sys.exit("THIS SHOULD NEVER HAPPEN!")

                if instance_label_index in chart_data['source']:
                    # if label_index in source list, then there is some flows going from instance to yet other instances or classes,
                    # thus for these instances at hand, new target instances must be created, with dedicated new labels, and indices
                    sources_to_add_target_to_indices.append([instance_label_index, instance_count])

            # find indices of instance targets to rename
            target_to_rename_indices = []
            for end_node in end_nodes:

                instance_string = end_node[0]
                instance_count = end_node[1]

                instance_label_index = -1
                check_count = 0
                for i in range(0, len(chart_data['label'])):
                    if instance_string in chart_data['label'][i]:
                        instance_label_index = i
                        check_count += 1
                if check_count != 1:
                    sys.exit("THIS SHOULD NEVER HAPPEN!")

                if instance_label_index in chart_data['target'] and instance_label_index not in chart_data['source']:
                    # if label index is not in source list, then there is no further instances subclassing this instance at hand
                    # thus save this index to replace the label values from "class-name" to "class-name + (instances)"
                    target_to_rename_indices.append([instance_label_index, instance_count])

            # add instance targets to classes which have subclasses and direct instances
            for sources_to_add_target_to_index_and_count in sources_to_add_target_to_indices:
                sources_to_add_target_to_index = sources_to_add_target_to_index_and_count[0]
                sources_to_add_target_to_count = sources_to_add_target_to_index_and_count[1]

                # get string
                source_string = chart_data['label'][sources_to_add_target_to_index]
                target_string = source_string + " (" + "{:,}".format(sources_to_add_target_to_count) + " instances)"
                chart_data['label'].append(target_string)
                target_index = chart_data['label'].index(target_string)

                # create flow manually here
                chart_data['source'].append(sources_to_add_target_to_index)
                chart_data['target'].append(target_index)
                chart_data['value'].append(sources_to_add_target_to_count)

            # edit instance targets where there are no further subclasses
            for target_to_rename_indices in target_to_rename_indices:
                target_to_rename_index = target_to_rename_indices[0]
                target_to_rename_count = target_to_rename_indices[1]

                target_to_rename_string = chart_data['label'][target_to_rename_index]
                chart_data['label'][target_to_rename_index] = target_to_rename_string + " (" + "{:,}".format(
                    target_to_rename_count) + " instances)"

            if len(chart_data['source']) != len(chart_data['target']) or len(chart_data['target']) != len(
                    chart_data['value']):
                sys.exit("THIS SHOULD NEVER HAPPEN!")

            # print data as expressed in original data
            # for i in range(0, len(chart_data['source'])):
            #     try:
            #         print(
            #             str(chart_data['value'][i]) + ", " + \
            #             str(chart_data['target'][i]) + " - " + \
            #             chart_data['label'][chart_data['target'][i]] + ", " + \
            #             str(chart_data['source'][i]) + " - " + \
            #             chart_data['label'][chart_data['source'][i]] + \
            #             "\n"
            #         )
            #     except Exception as ex:
            #         print("THIS SHOULD NEVER HAPPEN!" + ex)

            return chart_data

        def create_chart(chart_data, query_title):

            data = dict(
                type='sankey',
                # orientation = "v",
                node=dict(
                    label=chart_data['label']
                ),
                link=dict(
                    source=chart_data['source'],
                    target=chart_data['target'],
                    value=chart_data['value']
                ))

            layout = dict(
                title=query_title,
            )

            fig = dict(data=[data], layout=layout)
            offline.plot(fig, filename=query_title + ".html", auto_open=True)


        start_method(query_result)


    def clean_string_of_PE_prefixes(value):
        return value \
            .replace('http://www.cidoc-crm.org/cidoc-crm/', '') \
            .replace('CRMsci/', '') \
            .replace('http://parthenos.d4science.org/CRMext/CRMpe.rdfs/', '') \
            .replace('http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/', '')


    main(results)