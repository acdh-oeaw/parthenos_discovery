title = "Measurements of provenances and sources of datasets, comparing them to the overall count of triples in virtuoso"

description = "As designed in Parthenos, the origin of a triple is encoded by its respective graph (the fourth part in the quadruple). The graph then again is itself in a relation to its specific provenance (datasets by a provider) as well as its source (the provider). This set of queries produces an overview of how many triples originate from how many provenances and sources."

output_destination = r"https://drive.google.com/drive/folders/1Ha18gd_QqQKrK3TmZcwitb068H2kP6ya"

summary_sample_limit = 30

endpoint = "https://virtuoso.parthenos.d4science.org/sparql"

queries = [
    {
        "title": "Percentage of all triples which are associated with a provenance graph compared to overall numbers of triples",
        "query": """
			PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
			SELECT ?countAll ?countHavingSource (xsd:double(xsd:float(?countHavingSource)/xsd:float(?countAll)) AS ?percentageHavingSource) WHERE {
				{
					SELECT COUNT(*) as ?countHavingSource WHERE {
						GRAPH ?g { ?s ?p ?o } .
						GRAPH <dnet:graph> { ?g <dnet:collectedFrom> ?source }
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
        "query": """
            SELECT ?source ?sourceLabel COUNT(*) AS ?count WHERE {
                GRAPH ?g { ?s ?p ?o } .
                GRAPH <dnet:graph> { ?g <dnet:collectedFrom> ?source }
				OPTIONAL {
					GRAPH <dnet:graph> { ?source <dnet:isApiOf> ?sourceLabel }
				}
            }
            GROUP BY ?source ?sourceLabel
            ORDER BY DESC ( ?count )
        """
    },
    {
        "title": "All graphs which are not related to provenance",
        "description": "The number produced here is exactly what is missing in first query",
        "query": """
            SELECT ?g COUNT(?p) AS ?count WHERE {
                GRAPH ?g { ?s ?p ?o }
                FILTER NOT EXISTS { GRAPH <dnet:graph> { ?g <dnet:collectedFrom> ?source } } 
            }
            GROUP BY ?g
            ORDER BY DESC(?count)
        """
    },
    {
        "title": "Count of all triples which are associated with a provenance graph, grouped by provenance graph",
        "query": """
            SELECT ?g COUNT(*) AS ?count WHERE {
                GRAPH ?g { ?s ?p ?o } .
                GRAPH <dnet:graph> { ?g <dnet:collectedFrom> ?source }
            }
            GROUP BY ?g
            ORDER BY DESC ( ?count )
        """
    },
    {
        "title": "Count of all triples which are associated with a provenance graph",
        "query": """
            SELECT COUNT(?g) AS ?count WHERE {
                GRAPH <dnet:graph> { ?g <dnet:collectedFrom> ?source }
            }
        """
    },
    {
        "title": "All relations used in triples of provenance graph",
        "query": """
            SELECT DISTINCT ?p COUNT(?p) AS ?count WHERE {
                GRAPH <dnet:graph> { [] ?p [] }
            }
        """
    },
]
