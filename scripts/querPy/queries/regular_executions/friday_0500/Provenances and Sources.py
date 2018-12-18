title = "Measurements of provenances and sources of datasets, comparing them to the overall count of triples in virtuoso"

description = "As designed in Parthenos, the origin of a triple is encoded by its respective graph (the fourth part in the quadruple). The graph then again is itself in a relation to its specific provenance (datasets by a provider) as well as its source (the provider). This set of queries produces an overview of how many triples originate from how many provenances and sources."

output_destination = r"https://drive.google.com/drive/folders/1Ha18gd_QqQKrK3TmZcwitb068H2kP6ya"

summary_sample_limit = 30

endpoint = "https://virtuoso.parthenos.d4science.org/sparql"

queries = [
    {
        "title": "All current source apis and their labels",
        "query": r"""
            select ?api ?source_label where {
                graph <http://www.d-net.research-infrastructures.eu/provenance/graph> { 
                    ?source_graph <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?api .
                    ?api <http://www.d-net.research-infrastructures.eu/provenance/isApiOf> ?source_label .
                }
            }
            group by ?api ?source_label
        """
    },
    {
        "title": "All current source labels",
        "query": r"""
            select distinct ?source_label where {
                graph <http://www.d-net.research-infrastructures.eu/provenance/graph> { 
                    ?source_graph <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?api .
                    ?api <http://www.d-net.research-infrastructures.eu/provenance/isApiOf> ?source_label .
                }
            }
        """
    },
    {
        "title": "Percentage of all triples which are associated with a provenance graph compared to overall numbers of triples",
        "query": r"""
			PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
			SELECT ?countAll ?countHavingSource (xsd:double(xsd:float(?countHavingSource)/xsd:float(?countAll)) AS ?percentageHavingSource) WHERE {
				{
					SELECT COUNT(*) as ?countHavingSource WHERE {
						GRAPH ?g { ?s ?p ?o } .
						GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> {
                            ?g <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom>  ?source 
                        }
					}
				}
				{
					SELECT COUNT(*) as ?countAll WHERE {
						?s ?p ?o
					}
				}
            }
        """
    },
    {
        "title": "Count of all triples which are associated with a provenance graph, grouped by source graph",
        "query": r"""
            SELECT ?source ?sourceLabel COUNT(*) AS ?count WHERE {
                GRAPH ?g { ?s ?p ?o } .
                GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> { ?g <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?source }
				OPTIONAL {
					GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> { ?source <http://www.d-net.research-infrastructures.eu/provenance/isApiOf> ?sourceLabel }
				}
            }
            GROUP BY ?source ?sourceLabel
            ORDER BY DESC ( ?count )
        """
    },
    {
        "title": "All graphs which are not related to provenance",
        "description": "The number produced here is exactly what is missing in first query",
        "query": r"""
            SELECT ?g COUNT(?p) AS ?count WHERE {
                GRAPH ?g { ?s ?p ?o }
                FILTER NOT EXISTS { GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> { ?g <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?source } } 
            }
            GROUP BY ?g
            ORDER BY DESC(?count)
        """
    },
    {
        "title": "Count of all triples which are associated with a provenance graph, grouped by provenance graph",
        "query": r"""
            SELECT ?g COUNT(*) AS ?count WHERE {
                GRAPH ?g { ?s ?p ?o } .
                GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> { ?g <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?source }
            }
            GROUP BY ?g
            ORDER BY DESC ( ?count )
        """
    },
    {
        "title": "Count of all triples which are associated with a provenance graph",
        "query": r"""
            SELECT COUNT(?g) AS ?count WHERE {
                GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> { ?g <http://www.d-net.research-infrastructures.eu/provenance/collectedFrom> ?source }
            }
        """
    },
    {
        "title": "All relations used in triples of provenance graph",
        "query": r"""
            SELECT DISTINCT ?p COUNT(?p) AS ?count WHERE {
                GRAPH <http://www.d-net.research-infrastructures.eu/provenance/graph> { [] ?p [] }
            }
        """
    },
]
