
# title
# defines the title of the whole set of queries
# OPTIONAL, if not set, timestamp will be used
title = "ARIADNE: Metadata quality on virtuoso"

# description
# defines the textual and human-intended description of the purpose of these queries
# OPTIONAL, if not set, nothing will be used or displayed
description = r"As originally defined here: https://services.d4science.org/group/d4science-services-gateway/workspace?itemid=84e187f3-44aa-4df2-8e83-a92957455be0&operation=gotofolder , descriptions available here: https://docs.google.com/document/d/1diQQmN8tCXohNtHYqf-KVatb1jhTiILoBXHspF2c-y0/edit"


# output_destination
# defines where to save the results, input can be: 
# * a local path to a folder 
# * a URL for a google sheets document  
# * a URL for a google folder
# NOTE: On windows, folders in a path use backslashes, in such a case it is mandatory to attach a 'r' in front of the quotes, e.g. r"C:\Users\sresch\.."
# In the other cases the 'r' is simply ignored; thus best would be to always leave it there.
# OPTIONAL, if not set, folder of executed script will be used
output_destination = r"https://drive.google.com/drive/folders/1EvG4xew3RqX-l_Nh6f2RlTn3TVy-uNgl"


# output_format
# defines the format in which the result data shall be saved (currently available: csv, tsv, xml, json, xlsx)
# OPTIONAL, if not set, csv will be used
output_format = ""


# summary_sample_limit
# defines how many rows shall be displayed in the summary
# OPTIONAL, if not set, 5 will be used
summary_sample_limit = 10


# endpoint
# defines the SPARQL endpoint against which all the queries are run
# MANDATORY
endpoint = "https://virtuoso.parthenos.d4science.org/sparql"


# queries
# defines the set of queries to be run. 
# MANDATAORY
queries = [


    {
        # title
        # OPTIONAL, if not set, timestamp will be used
        "title" : "types_per_class_V1.0" ,
        
        # description
        # OPTIONAL, if not set, nothing will be used or displayed
        "description" : "This query gives the list of instances of E55 existing in a data source and for what class they stand as type." ,

        # query
        # the sparql query itself
        # MANDATORY
        "query" : [r"""
			#DEFINE input:inference 'parthenos_rules'
			select distinct 
			?type  (str(?type_label) as ?type_label)
			?classE55
			( GROUP_CONCAT(distinct ?class_label, "/") as ?class_label )

			?instanceClass
			( GROUP_CONCAT(distinct str(?instanceClass_labelX) , "/") as ?instanceClass_label )

			(str(?ds) as ?ds) 
			?gRecord
			where{

			values ?classE55 { <http://www.cidoc-crm.org/cidoc-crm/E55_Type> }
			optional{
			?classE55 rdfs:label ?class_label.
			}

			graph ?gRecord  {
			?type a ?classE55.
			optional{?type rdfs:label ?type_label.}
			{?instanceURI crm:P2_has_type ?type} union {?type crm:P2i_is_type_of ?instanceURI}
			optional{ ?instanceURI a ?instanceClass.}
			}

			?instanceClass rdfs:label ?instanceClass_labelX.

			GRAPH <provenance> {
			values ?ds { 'ARIADNE'^^<http://www.w3.org/2001/XMLSchema#string> }
            ?gRecord <dnetcollectedFrom> ?api . ?api <dnetisApiOf> ?ds}
			} 
			order by ?type ?ds
        """]
    }, 
    {
        # title
        # OPTIONAL, if not set, timestamp will be used
        "title" : "place_instances_V.1.0" ,

        # description
        # OPTIONAL, if not set, nothing will be used or displayed
        "description" : "This query gives the list of instances of E53 class existing in a data source." ,

        # query
        # the sparql query itself
        # MANDATORY
        "query" : [r"""
			#DEFINE input:inference 'parthenos_rules'
			select
			?classE53
			( GROUP_CONCAT(distinct ?class_label, "/") as ?class)
			?instanceURI
			( GROUP_CONCAT(distinct ?instance_labelX, "/") as ?instance_label)

			(str(?ds) as ?ds)
			#?gRecord
			where{

			values ?classE53 { <http://www.cidoc-crm.org/cidoc-crm/E53_Place> }
			optional{
			?classE53 rdfs:label ?class_label.
			}

			graph ?gRecord  {
			?instanceURI a ?classE53.
			optional {?instanceURI rdfs:label ?instance_labelX.}
			}

			GRAPH <provenance> {
			values ?ds { 'ARIADNE'^^<http://www.w3.org/2001/XMLSchema#string> }
			?gRecord <dnetcollectedFrom> ?api . ?api <dnetisApiOf> ?ds}

			}
			order by ?ds ?instanceURI
        """]
    },
    {
        # title
        # OPTIONAL, if not set, timestamp will be used
        "title" : "periods_and_events_V1.0" ,

        # description
        # OPTIONAL, if not set, nothing will be used or displayed
        "description" : "This query gives the list of instances of E4 Period and E5 Event existing in a data source." ,

        # query
        # the sparql query itself
        # MANDATORY
        "query" : [r"""
			#DEFINE input:inference 'parthenos_rules'
			select distinct
			?class
			( GROUP_CONCAT(distinct ?class_labelX, "/") as ?class_label)

			?instanceURI
			str(?instance_labelX) as ?instance_label

			(str(?ds) as ?ds)
			?gRecord
			where{

			values ?class { <http://www.cidoc-crm.org/cidoc-crm/E4_Period> <http://www.cidoc-crm.org/cidoc-crm/E5_Event>}
			?class rdfs:label ?classlabelX. bind (str(?classlabelX) as ?class_labelX).

			graph ?gRecord  {
			?instanceURI a ?class.
			}

			optional {?instanceURI rdfs:label ?labelX. bind (str(?labelX) as ?instance_labelX).}

			GRAPH <provenance> {
			values ?ds { 'ARIADNE'^^<http://www.w3.org/2001/XMLSchema#string> }
			?gRecord <dnetcollectedFrom> ?api . ?api <dnetisApiOf> ?ds}

			}
			#group by ?ds ?gRecord ?class
			order by ?ds ?gRecord ?instanceURI
        """]
    },
    {
        # title
        # OPTIONAL, if not set, timestamp will be used
        "title" : "tmp_class_population.V1.0" ,

        # description
        # OPTIONAL, if not set, nothing will be used or displayed
        "description" : "This query gives the density of population of classes by instances for a particular named graph in the registry." ,

        # query
        # the sparql query itself
        # MANDATORY
        "query" : [r"""
			#3 ######### Counts instances per class per record. To have the instances per class replace count(distinct ?instanceURI) with ?instanceURI in 'select' clause #########
			######### Result is the same as in https://beta-parthenos.d4science.org/aggregator/mvc/ui/lightui.do?ui=parthenos#/doc/objidentifier/parthenos___%253A%253A8d777f385d3dfec8815d20f7496026dc #########

			#DEFINE input:inference 'parthenos_rules'
			select distinct ?class count(distinct ?instanceURI) {
			graph ?gRecord  {
			?instanceURI a ?class.
			}

			#optional {?subclass rdfs:subClassOf ?class . }
			#filter (!bound(?subclass ))

			GRAPH <provenance> {?gRecord <dnetcollectedFrom> ?api . ?api <dnetisApiOf> 'ARIADNE'^^<http://www.w3.org/2001/XMLSchema#string>}
			}
			group by ?gRecord ?class
        """]
    },
    {
        # title
        # OPTIONAL, if not set, timestamp will be used
        "title" : "tmp_class_population_PE_top.V1.0" ,

        # description
        # OPTIONAL, if not set, nothing will be used or displayed
        "description" : "This query gives the density of population of classes by instances grouped by Parthenos Top Level Entities (Projects, Services, Actors, Datasets and Software) for a particular named graph in the registry." ,

        # query
        # the sparql query itself
        # MANDATORY
        "query" : [r"""
			#DEFINE input:inference 'parthenos_rules'
			select distinct ?topclass (?class as ?excplicit_class) (count(distinct ?instanceURI) as ?count) {

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
			GRAPH <provenance> {?gRecord <dnetcollectedFrom> ?api . ?api <dnetisApiOf> 'ARIADNE'^^<http://www.w3.org/2001/XMLSchema#string>}
			}
			#group by ?gRecord  ?topclass ?class
			group by ?topclass ?class
			order by ?topclass ?class
        """]
    },
    {
        # title
        # OPTIONAL, if not set, timestamp will be used
        "title" : "tmp___all_project_min_data_gen_query_counts_v2.0" ,

        # description
        # OPTIONAL, if not set, nothing will be used or displayed
        "description" : "This query is designed to test a top level Parthenos Entity (Projects, Services, Actors, Datasets and Software) for which minimal metadata has been specified and return, per instance of that entity, the count of paths that fulfill the defined minimal metadata for that entity. The query returns a COUNT of the paths that meet the minimal metadata requirements for that entity. The query is designed to be run on a named graph loaded into the registry, therefore allowing the testing of information density per loaded dataset." ,

        # query
        # the sparql query itself
        # MANDATORY
        "query" : [r"""
			DEFINE input:inference 'parthenos_rules'

			PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
			PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
			PREFIX parthenos: <http://parthenos.d4science.org/CRMext/CRMpe.rdfs/>
			PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
			PREFIX crmdig: <http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/>


			select distinct
			#?gRecord
			( COALESCE(str(?instance_label), ?instanceURI) as ?instance )
			( COALESCE(str(?ID_label), ?ID) as ?id)
			( COALESCE(str(?Name_label), ?Name) as ?name )
			#( COALESCE(str(?Service_label), ?Service) as ?service )
			( COALESCE(str(?Team_label), ?Team) as ?team )

			( COUNT(?Member) as ?member )
			( COUNT(?Member_address) as ?member_address )
			( COUNT(?Member_address_type) as ?member_address_type )

			( COUNT(?Time_span) as ?time_span )
			( COUNT(?Time_actual) as ?time_actual )


			where {

			#source
			GRAPH <provenance> {?gRecord <dnetcollectedFrom> ?api . ?api <dnetisApiOf> 'ARIADNE'^^<http://www.w3.org/2001/XMLSchema#string>.}

			#Gets all Projects per source-record
			GRAPH ?gRecord {#

			#Gets the Project
			?instanceURI a parthenos:PE35_Project .

			#Gets the Label of Project
			?instanceURI rdfs:label ?instance_label .

			#Gets ID of Project
			OPTIONAL { ?instanceURI crm:P1_is_identified_by ?ID .
			 ?ID a crm:E42_Identifier; rdfs:label ?ID_label. }

			#Gets Value of Name of Project
			OPTIONAL { ?instanceURI crm:P1_is_identified_by ?Name.
			 ?Name a crm:E41_Appellation; rdfs:label ?Name_label. }

			#Gets the Service currently offered by Project
			#OPTIONAL { ?instanceURI parthenos:PP1_currently_offers ?Service .
			# OPTIONAL { ?Service rdfs:label ?Service_label. }  }

			#Gets the Team currently maintaining Project
			OPTIONAL { ?instanceURI parthenos:PP44_has_maintaining_team ?Team .
			 OPTIONAL { ?Team rdfs:label ?Team_label.}

			 #Gets the Members of the Team
			 OPTIONAL { ?Team crm:P107_has_current_or_former_member ?Member .
			  OPTIONAL { ?Member rdfs:label ?Member_label. }

			   #Gets the Address of Actor
			   OPTIONAL { ?Member crm:P76_has_contact_point ?Member_address.
				OPTIONAL { ?Member_address rdfs:label ?Member_address_label. }

				#Gets the type of Address of Actor
				OPTIONAL { ?Member_address crm:P2_has_type ?Member_address_type.
				 OPTIONAL { ?Member_address_type rdfs:label ?Member_address_type_label. }
				}#Member_address_type --end
			   }#Member_address --end
			  }#Member --end
			 }#Team --end


			#Gets the Time since when project has been run
			OPTIONAL { ?instanceURI crm:P4_has_time-span ?Time_span .
			 OPTIONAL { ?Time_span rdfs:label ?Time_span_label. }
			 OPTIONAL { ?Time_span crm:P82a_begin_of_the_begin ?Time_actual .}
			}

			}#?gRecord --end

			}
			order by  ?instance ?id ?name ?team #?service
        """]
    },
    {
        # title
        # OPTIONAL, if not set, timestamp will be used
        "title" : "tmp___all_project_min_data_gen_query_counts_v3.0" ,

        # description
        # OPTIONAL, if not set, nothing will be used or displayed
        "description" : "This query is designed to test a top level Parthenos Entity (Projects, Services, Actors, Datasets and Software) for which minimal metadata has been specified and return, per instance of that entity, the count of paths that fulfill the defined minimal metadata for that entity. The query returns a BOOLEAN of the paths that meet the minimal metadata requirements for that entity. The query is designed to be run on a named graph loaded into the registry, therefore allowing the testing of information completeness per loaded dataset. It is envisioned that this query could be loaded into a data analysis and visualization software (e.g. Excel) in order to generate overview data for data providers indicating the strengths and weaknesses of the aggregated data in order to track down quality problems in the graph. N.B.: There is a unique instance of this query for each of the Parthenos Top Level Entities tracking its specific minimal metadata requirements. In order to test a particular kind of entity you must use the appropriate query as indicated by the query name." ,

        # query
        # the sparql query itself
        # MANDATORY
        "query" : [r"""
			DEFINE input:inference 'parthenos_rules'

			PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
			PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
			PREFIX parthenos: <http://parthenos.d4science.org/CRMext/CRMpe.rdfs/>
			PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
			PREFIX crmdig: <http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/>


			select distinct
			#?gRecord
			( COALESCE(str(?instance_label), ?instanceURI) as ?instance )
			( COALESCE(str(?ID_label), ?ID) as ?id)
			( COALESCE(str(?Name_label), ?Name) as ?name )
			#( COALESCE(str(?Service_label), ?Service) as ?service )
			( COALESCE(str(?Team_label), ?Team) as ?team )

			( COUNT(?Member)>0 as ?member )
			( COUNT(?Member_address)>0 as ?member_address )
			( COUNT(?Member_address_type)>0 as ?member_address_type )

			( COUNT(?Time_span)>0 as ?time_span )
			( COUNT(?Time_actual)>0 as ?time_actual )


			where {

			#source
			GRAPH <provenance> {?gRecord <dnetcollectedFrom> ?api . ?api <dnetisApiOf> 'ARIADNE'^^<http://www.w3.org/2001/XMLSchema#string>.}

			#Gets all Projects per source-record
			GRAPH ?gRecord {#

			#Gets the Project
			?instanceURI a parthenos:PE35_Project .

			#Gets the Label of Project
			?instanceURI rdfs:label ?instance_label .

			#Gets ID of Project
			OPTIONAL { ?instanceURI crm:P1_is_identified_by ?ID .
			 ?ID a crm:E42_Identifier; rdfs:label ?ID_label. }

			#Gets Value of Name of Project
			OPTIONAL { ?instanceURI crm:P1_is_identified_by ?Name.
			 ?Name a crm:E41_Appellation; rdfs:label ?Name_label. }

			#Gets the Service currently offered by Project
			#OPTIONAL { ?instanceURI parthenos:PP1_currently_offers ?Service .
			# OPTIONAL { ?Service rdfs:label ?Service_label. }  }

			#Gets the Team currently maintaining Project
			OPTIONAL { ?instanceURI parthenos:PP44_has_maintaining_team ?Team .
			 OPTIONAL { ?Team rdfs:label ?Team_label.}

			 #Gets the Members of the Team
			 OPTIONAL { ?Team crm:P107_has_current_or_former_member ?Member .
			  OPTIONAL { ?Member rdfs:label ?Member_label. }

			   #Gets the Address of Actor
			   OPTIONAL { ?Member crm:P76_has_contact_point ?Member_address.
				OPTIONAL { ?Member_address rdfs:label ?Member_address_label. }

				#Gets the type of Address of Actor
				OPTIONAL { ?Member_address crm:P2_has_type ?Member_address_type.
				 OPTIONAL { ?Member_address_type rdfs:label ?Member_address_type_label. }
				}#Member_address_type --end
			   }#Member_address --end
			  }#Member --end
			 }#Team --end


			#Gets the Time since when project has been run
			OPTIONAL { ?instanceURI crm:P4_has_time-span ?Time_span .
			 OPTIONAL { ?Time_span rdfs:label ?Time_span_label. }
			 OPTIONAL { ?Time_span crm:P82a_begin_of_the_begin ?Time_actual .}
			}

			}#?gRecord --end

			}
			order by  ?instance ?id ?name ?team #?service
        """]
    },
    {
        # title
        # OPTIONAL, if not set, timestamp will be used
        "title" : "tmp___all_project_min_data_gen_query_v4.0" ,

        # description
        # OPTIONAL, if not set, nothing will be used or displayed
        "description" : "This query is designed to test a top level Parthenos Entity (Projects, Services, Actors, Datasets and Software) for which minimal metadata has been specified and return, per instance of that entity, the values for the qualifying data paths fulfilling the minimal metadata requirements for that entity. It is envisioned that this query can be used for spot testing of data in order to understand in a synoptic view of some sample records, what the actual data looks like to an end user. N.B.: There is a unique instance of this query for each of the Parthenos Top Level Entities tracking its specific minimal metadata requirements. In order to test a particular kind of entity you must use the appropriate query as indicated by the query name." ,

        # query
        # the sparql query itself
        # MANDATORY
        "query" : [r"""
			DEFINE input:inference 'parthenos_rules'

			PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
			PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
			PREFIX parthenos: <http://parthenos.d4science.org/CRMext/CRMpe.rdfs/>
			PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
			PREFIX crmdig: <http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/>


			select distinct
			#?gRecord
			( COALESCE(str(?instance_label), ?instanceURI) as ?instance )
			( COALESCE(str(?id_label), ?id) as ?ID)
			( COALESCE(str(?name_label), ?name) as ?Name )

			(GROUP_CONCAT (DISTINCT COALESCE(str(?service), ?service), "\n") as ?Services )
			(GROUP_CONCAT (DISTINCT COALESCE(str(?service_label), ?service), "\n") as ?Services_Label )
			(GROUP_CONCAT (DISTINCT COALESCE(str(?team_label), ?team), "\n") as ?Team )

			(GROUP_CONCAT (DISTINCT CONCAT (
			STRAFTER( str(?actorRelation), str(crm:)), ": ",
			COALESCE(str(?member_label), ?member),
			?delim1,
			COALESCE(str(?member_address_type_label), ?member_address_type),
			?delim2, COALESCE(str(?member_address_label), ?member_address)
			),"\n") as ?Team_Members)

			(GROUP_CONCAT (DISTINCT CONCAT(
			COALESCE(str(?time_span_label), ?time_span), ?delim3, str(?time_actual)
			),"\n") as ?Time_Span_of_Project )




			where {

			#source
			GRAPH <provenance> {?gRecord <dnetcollectedFrom> ?api . ?api <dnetisApiOf> 'ARIADNE'^^<http://www.w3.org/2001/XMLSchema#string>.}

			#Gets all Projects per source-record
			GRAPH ?gRecord {#

			#Gets the Project
			?instanceURI a parthenos:PE35_Project .

			#Gets the Label of Project
			?instanceURI rdfs:label ?instance_label .

			#Gets id of Project
			OPTIONAL { ?instanceURI crm:P1_is_identified_by ?id .
			 ?id a crm:E42_Identifier; rdfs:label ?id_label. }

			#Gets Value of Name of Project
			OPTIONAL { ?instanceURI crm:P1_is_identified_by ?name.
			 ?name a crm:E41_Appellation; rdfs:label ?name_label. }

			#Gets the Service currently offered by Project
			OPTIONAL { ?instanceURI parthenos:PP1_currently_offers ?service .
			 OPTIONAL { ?service rdfs:label ?service_label. }  }

			#Gets the Team currently maintaining Project
			OPTIONAL { ?instanceURI parthenos:PP44_has_maintaining_team ?team .
			 OPTIONAL { ?team rdfs:label ?team_label.}

			 #Gets the Members of the Team
			 OPTIONAL { ?team ?actorRelation ?member . #crm:P107_has_current_or_former_member
			 ?member a crm:E39_Actor.

			  OPTIONAL { ?member rdfs:label ?member_label. }

			   #Gets the Address of Actor
			   OPTIONAL { ?member crm:P76_has_contact_point ?member_address.
				OPTIONAL { ?member_address rdfs:label ?member_address_label. }

				#Gets the type of Address of Actor
				OPTIONAL { ?member_address crm:P2_has_type ?member_address_type.
				 OPTIONAL { ?member_address_type rdfs:label ?member_address_type_label. }
				}#Member_address_type --end
			   }#Member_address --end
			  }#Member --end
			 }#Team --end


			#Gets the Time since when project has been run
			OPTIONAL { ?instanceURI crm:P4_has_time-span ?time_span .
			 OPTIONAL { ?time_span rdfs:label ?time_span_label. }
			 OPTIONAL { ?time_span crm:P82a_begin_of_the_begin ?time_actual .}
			}

			}#?gRecord --end

			Bind(if(Bound(?member),", ","") as ?delim1)
			Bind(if(Bound(?member_address_type),": ","") as ?delim2)
			Bind(if(Bound(?time_actual),": ","") as ?delim3)

			}
			group by  ?instanceURI ?instance_label ?id ?id_label ?name ?name_label
			#order by  ?instance ?ID ?Name
        """]
    },
]

# Notes on syntax of queries-set:
# * the set of queries is enclosed by '[' and ']'
# * individual queries are enclosed by '{' and '},'
# * All elements of a query (title, description, query) need to be defined using quotes as well as their contents, and both need to be separated by ':'
# * All elements of a query (title, description, query) need to be separated from each other using quotes ','
# * The content of a query needs to be defined using triple quotes, e.g. """ SELECT * WHERE .... """
# * Any indentation (tabs or spaces) do not influence the queries-syntax, they are merely syntactic sugar.
