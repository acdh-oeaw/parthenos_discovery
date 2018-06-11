title = "Measurements of provenances and sources of datasets, comparing them to the overall count of triples in virtuoso"

description = "As designed in Parthenos, the origin of a triple is encoded by its respective graph (the fourth part in the quadruple). The graph then again is itself in a relation to its specific provenance (datasets by a provider) as well as its source (the provider). This set of queries produces an overview of how many triples originate from how many provenances and sources."

output_destination = r"https://drive.google.com/drive/folders/1Ha18gd_QqQKrK3TmZcwitb068H2kP6ya"

summary_sample_limit = 30

endpoint = "https://virtuoso.parthenos.d4science.org/sparql"

queries = [
    {
        "title": "Q1: Count of all triples in Virtuoso (including virtuoso system specifics)",
        "query": """
            SELECT COUNT(*) WHERE {
                GRAPH ?g { ?s ?p ?o }
            }
        """
    },
    {
        "title": "Q2: Count of all triples in Virtuoso (only triples are counted which are associated with a provenance graph)",
        "query": """
            SELECT COUNT(*) WHERE {
                GRAPH ?g { ?s ?p ?o } .
                GRAPH <provenance> { ?g <dnetcollectedFrom> ?source }
            }
        """
    },
    {
        "title": "Q3: Count of all triples grouped by source graph in Virtuoso (only triples are counted which are associated with a provenance graph)",
        "query": """
            SELECT ?source  COUNT(*) AS ?count WHERE {
                GRAPH ?g { ?s ?p ?o } .
                GRAPH <provenance> { ?g <dnetcollectedFrom> ?source }
            }
            GROUP BY ?source
            ORDER BY DESC ( ?count )
        """
    },
    {
        "title": "Q4: Sum of count of all triples grouped by source graph in Virtuoso (only triples are counted which are associated with a provenance graph)",
        "description": "Maybe redundant, but still to be very sure: To verify that query Q3 indeed returns only triples coming from certain sources, a sum of all the counts of Q3 is produced, which then can be compared to the value of Q2.",
        "query": """
            SELECT SUM(?count) AS ?totalCount WHERE {
                SELECT ?source  COUNT(*) AS ?count WHERE {
                    GRAPH ?g { ?s ?p ?o } .
                    GRAPH <provenance> { ?g <dnetcollectedFrom> ?source }
                }
                GROUP BY ?source
                ORDER BY DESC ( ?count )
            }
        """
    },
    {
        "title": "Q5: Count of all triples grouped by provenance graph in Virtuoso (only triples are counted which are associated with a provenance graph)",
        "query": """
            SELECT ?g  COUNT(*) AS ?count WHERE {
                GRAPH ?g { ?s ?p ?o } .
                GRAPH <provenance> { ?g <dnetcollectedFrom> ?source }
            }
            GROUP BY ?g
            ORDER BY DESC ( ?count )
        """
    },
    {
        "title": "Q6: Sum of count of all triples grouped by provenance graph in Virtuoso (only triples are counted which are associated with a provenance graph)",
        "description": "Maybe redundant, but still to be very sure: To verify that query Q5 indeed returns only triples coming from certain provenances, a sum of all the counts of Q5 is produced, which then can be compared to the value of Q2.",
        "query": """
            SELECT SUM(?count) AS ?totalCount WHERE {
                SELECT ?g  COUNT(*) AS ?count WHERE {
                    GRAPH ?g { ?s ?p ?o } .
                    GRAPH <provenance> { ?g <dnetcollectedFrom> ?source }
                }
                GROUP BY ?g
                ORDER BY DESC ( ?count )
            }
        """
    },
    {
        "title": "Q7: All graphs in virtuoso which do not encode provencance",
        "query": """
            SELECT ?g COUNT(?p) AS ?count WHERE {
                GRAPH ?g { ?s ?p ?o }
                FILTER NOT EXISTS { GRAPH <provenance> { ?g <dnetcollectedFrom> ?source } } 
                FILTER ( ?g != <provenance> )
            }
            GROUP BY ?g
            ORDER BY DESC(?count)
        """
    },
    {
        "title": "Q8: All graphs in virtuoso which do not encode provencance (though including the provenance graph itself (the meta-statement about provenance as I understood it), which seems weird but makes sense if you compare it to Q7 and Q3. This way the numbers all match up)",
        "query": """
            SELECT ?g COUNT(?p) AS ?count WHERE {
                GRAPH ?g { ?s ?p ?o }
                FILTER NOT EXISTS { GRAPH <provenance> { ?g <dnetcollectedFrom> ?source } } 
            }
            GROUP BY ?g
            ORDER BY DESC(?count)
        """
    },
]
