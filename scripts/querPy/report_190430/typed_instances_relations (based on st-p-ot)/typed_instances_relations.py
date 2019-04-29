
# -------------------- OPTIONAL SETTINGS --------------------

# title
# defines the title of the whole set of queries
# OPTIONAL, if not set, timestamp will be used
title = "typed_instances_relations"


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
# endpoint = "https://virtuoso.parthenos.d4science.org/sparql"
endpoint = "http://blazegraph.herkules.arz.oeaw.ac.at/parthenos-dev/sparql"


global_data_list = []

types = [
    "http://www.cidoc-crm.org/cidoc-crm/E1_CRM_Entity",
    "http://www.cidoc-crm.org/cidoc-crm/E2_Temporal_Entity",
    "http://www.cidoc-crm.org/cidoc-crm/E3_Condition_State",
    "http://www.cidoc-crm.org/cidoc-crm/E4_Period",
    "http://www.cidoc-crm.org/cidoc-crm/E5_Event",
    "http://www.cidoc-crm.org/cidoc-crm/E6_Destruction",
    "http://www.cidoc-crm.org/cidoc-crm/E7_Activity",
    "http://www.cidoc-crm.org/cidoc-crm/E8_Acquisition",
    "http://www.cidoc-crm.org/cidoc-crm/E9_Move",
    "http://www.cidoc-crm.org/cidoc-crm/E10_Transfer_of_Custody",
    "http://www.cidoc-crm.org/cidoc-crm/E11_Modification",
    "http://www.cidoc-crm.org/cidoc-crm/E12_Production",
    "http://www.cidoc-crm.org/cidoc-crm/E13_Attribute_Assignment",
    "http://www.cidoc-crm.org/cidoc-crm/E14_Condition_Assessment",
    "http://www.cidoc-crm.org/cidoc-crm/E15_Identifier_Assignment",
    "http://www.cidoc-crm.org/cidoc-crm/E16_Measurement",
    "http://www.cidoc-crm.org/cidoc-crm/E17_Type_Assignment",
    "http://www.cidoc-crm.org/cidoc-crm/E18_Physical_Thing",
    "http://www.cidoc-crm.org/cidoc-crm/E19_Physical_Object",
    "http://www.cidoc-crm.org/cidoc-crm/E20_Biological_Object",
    "http://www.cidoc-crm.org/cidoc-crm/E21_Person",
    "http://www.cidoc-crm.org/cidoc-crm/E22_Man-Made_Object",
    "http://www.cidoc-crm.org/cidoc-crm/E24_Physical_Man-Made_Thing",
    "http://www.cidoc-crm.org/cidoc-crm/E25_Man-Made_Feature",
    "http://www.cidoc-crm.org/cidoc-crm/E26_Physical_Feature",
    "http://www.cidoc-crm.org/cidoc-crm/E27_Site",
    "http://www.cidoc-crm.org/cidoc-crm/E28_Conceptual_Object",
    "http://www.cidoc-crm.org/cidoc-crm/E29_Design_or_Procedure",
    "http://www.cidoc-crm.org/cidoc-crm/E30_Right",
    "http://www.cidoc-crm.org/cidoc-crm/E31_Document",
    "http://www.cidoc-crm.org/cidoc-crm/E32_Authority_Document",
    "http://www.cidoc-crm.org/cidoc-crm/E33_Linguistic_Object",
    "http://www.cidoc-crm.org/cidoc-crm/E34_Inscription",
    "http://www.cidoc-crm.org/cidoc-crm/E35_Title",
    "http://www.cidoc-crm.org/cidoc-crm/E36_Visual_Item",
    "http://www.cidoc-crm.org/cidoc-crm/E37_Mark",
    "http://www.cidoc-crm.org/cidoc-crm/E38_Image",
    "http://www.cidoc-crm.org/cidoc-crm/E39_Actor",
    "http://www.cidoc-crm.org/cidoc-crm/E40_Legal_Body",
    "http://www.cidoc-crm.org/cidoc-crm/E41_Appellation",
    "http://www.cidoc-crm.org/cidoc-crm/E42_Identifier",
    "http://www.cidoc-crm.org/cidoc-crm/E44_Place_Appellation",
    "http://www.cidoc-crm.org/cidoc-crm/E45_Address",
    "http://www.cidoc-crm.org/cidoc-crm/E46_Section_Definition",
    "http://www.cidoc-crm.org/cidoc-crm/E47_Spatial_Coordinates",
    "http://www.cidoc-crm.org/cidoc-crm/E48_Place_Name",
    "http://www.cidoc-crm.org/cidoc-crm/E49_Time_Appellation",
    "http://www.cidoc-crm.org/cidoc-crm/E50_Date",
    "http://www.cidoc-crm.org/cidoc-crm/E51_Contact_Point",
    "http://www.cidoc-crm.org/cidoc-crm/E52_Time-Span",
    "http://www.cidoc-crm.org/cidoc-crm/E53_Place",
    "http://www.cidoc-crm.org/cidoc-crm/E54_Dimension",
    "http://www.cidoc-crm.org/cidoc-crm/E55_Type",
    "http://www.cidoc-crm.org/cidoc-crm/E56_Language",
    "http://www.cidoc-crm.org/cidoc-crm/E57_Material",
    "http://www.cidoc-crm.org/cidoc-crm/E58_Measurement_Unit",
    "http://www.cidoc-crm.org/cidoc-crm/E63_Beginning_of_Existence",
    "http://www.cidoc-crm.org/cidoc-crm/E64_End_of_Existence",
    "http://www.cidoc-crm.org/cidoc-crm/E65_Creation",
    "http://www.cidoc-crm.org/cidoc-crm/E66_Formation",
    "http://www.cidoc-crm.org/cidoc-crm/E67_Birth",
    "http://www.cidoc-crm.org/cidoc-crm/E68_Dissolution",
    "http://www.cidoc-crm.org/cidoc-crm/E69_Death",
    "http://www.cidoc-crm.org/cidoc-crm/E70_Thing",
    "http://www.cidoc-crm.org/cidoc-crm/E71_Man-Made_Thing",
    "http://www.cidoc-crm.org/cidoc-crm/E72_Legal_Object",
    "http://www.cidoc-crm.org/cidoc-crm/E73_Information_Object",
    "http://www.cidoc-crm.org/cidoc-crm/E74_Group",
    "http://www.cidoc-crm.org/cidoc-crm/E75_Conceptual_Object_Appellation",
    "http://www.cidoc-crm.org/cidoc-crm/E77_Persistent_Item",
    "http://www.cidoc-crm.org/cidoc-crm/E78_Collection",
    "http://www.cidoc-crm.org/cidoc-crm/E79_Part_Addition",
    "http://www.cidoc-crm.org/cidoc-crm/E80_Part_Removal",
    "http://www.cidoc-crm.org/cidoc-crm/E81_Transformation",
    "http://www.cidoc-crm.org/cidoc-crm/E82_Actor_Appellation",
    "http://www.cidoc-crm.org/cidoc-crm/E83_Type_Creation",
    "http://www.cidoc-crm.org/cidoc-crm/E84_Information_Carrier",
    "http://www.cidoc-crm.org/cidoc-crm/E85_Joining",
    "http://www.cidoc-crm.org/cidoc-crm/E86_Leaving",
    "http://www.cidoc-crm.org/cidoc-crm/E87_Curation_Activity",
    "http://www.cidoc-crm.org/cidoc-crm/E89_Propositional_Object",
    "http://www.cidoc-crm.org/cidoc-crm/E90_Symbolic_Object",
    "http://www.cidoc-crm.org/cidoc-crm/E92_Spacetime_Volume",
    "http://www.cidoc-crm.org/cidoc-crm/E93_Presence",
    "http://www.cidoc-crm.org/cidoc-crm/E78_Curated_Holding",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE1_Service",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE2_Hosting_Service",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE3_Curating_Service",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE5_Digital_Hosting_Service",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE6_Software_Hosting_Service",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE7_Data_Hosting_Service",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE8_E-Service",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE10_Digital_Curating_Service",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE11_Software_Curating_Service",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE12_Data_Curating_Service",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE13_Software_Computing_E-Service",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE14_Software_Delivery_E-Service",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE15_Data_E-Service",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE16_Curated_Software_E-Service",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE17_Curated_Data_E-Service",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE18_Dataset",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE19_Persistent_Digital_Object",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE20_Volatile_Digital_Object",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE21_Persistent_Software",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE22_Persistent_Dataset",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE23_Volatile_Software",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE24_Volatile_Dataset",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE25_RI_Consortium",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE26_RI_Project",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE28_Curation_Plan",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE29_Access_Point",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE32_Curated_Thing",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE33_E-Access_Brokering_Service",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE34_Team",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE35_Project",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE36_Competency_Type",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE37_Protocol_Type",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE38_Schema",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE39_Availability_Type",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE40_Programing_Language",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE41_Award_Activity",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE42_Funding_Activity",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE43_Encoding_Type",
    "http://parthenos.d4science.org/CRMext/CRMpe.rdfs/PE44_Audience_Type",
    "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D1_Digital_Object",
    "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D2_Digitization_Process",
    "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D3_Formal_Derivation",
    "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D7_Digital_Machine_Event",
    "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D8_Digital_Device",
    "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D9_Data_Object",
    "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D10_Software_Execution",
    "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D11_Digital_Measurement_Event",
    "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D12_Data_Transfer_Event",
    "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D13_Digital_Information_Carrier",
    "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D14_Software",
    "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D21_Person_Name",
    "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D23_Room",
    "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D29_Annotation_Object",
    "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D30_Annotation_Event",
    "http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/D35_Area",
]

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

        # value = value.split('_')[0]
        value = value.split('\">')[0]

        return value

    else:
        return value


def save_results_in_global_data_list(query_data_object):

    results_matrix = query_data_object.results_matrix

    type_shortened = query_data_object.custom_data_container
    title = query_data_object.title

    print(type_shortened)
    global_data_list.append([])
    global_data_list.append([])
    global_data_list.append([type_shortened + ": relations to and from other instances which have types assigned"])

    print(title)
    global_data_list.append([title])

    if len(results_matrix) > 1:

        tmp_list = []
        for line in results_matrix:
            tmp_list.append(line[:-1])

        global_data_list.extend(tmp_list)

    else:

        global_data_list.append(["No relations to typed instances found"])






def custom_pre_processing():

    for type in types:
    # for i in range(1,10):
    #     type = types[i]

        type_shortend = remove_crm_identifier(type)

        title = "s_type -p_in-> " + type_shortend + " -p_out-> o_type"

        query = r"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            select ?s_type ?p_in ?p_out ?o_type (count( distinct *) as ?count) ?custom_order where {

                {
                    ?i  ?p_out  ?o_instance .
                    ?o_instance  rdf:type  ?o_type .
                    ?i  rdf:type  <""" + type + r"""> .

                    filter ( ?p_out != rdf:type )
                    values ?custom_order { 2 }
                }
                union {
                    ?s_instance  ?p_in  ?i .
                    ?s_instance  rdf:type  ?s_type .
                    ?i  rdf:type  <""" + type + r"""> .
                    values ?custom_order { 1 }
                }

            }
            group by ?s_type ?p_in ?p_out ?o_type ?custom_order  
            order by ?custom_order desc( ?count )
        """

        query_object = {
            "title": title,
            "query": query,
            "custom_data_container": type_shortend,
            "custom_meta_function": save_results_in_global_data_list
        }

        queries.append(query_object)


# queries
# defines the set of queries to be run.
# MANDATAORY
queries = [
]



def custom_post_processing(results):

    import csv

    with open( output_destination + "output.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(global_data_list)
