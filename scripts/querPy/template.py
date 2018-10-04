# title
# defines the title of the whole set of queries
# OPTIONAL, if not set, timestamp will be used
title = "dati.culturaitalia.it SPARQL test"


# description
# defines the textual and human-intended description of the purpose of these queries
# OPTIONAL, if not set, nothing will be used or displayed
description = "SPARQL query divise tra generali e specifiche per entità e proprietà"


# output_destination
# defines where to save the results, input can be: 
# * a local path to a folder 
# * a URL for a google sheets document  
# * a URL for a google folder
# NOTE: On windows, folders in a path use backslashes, in such a case it is mandatory to attach a 'r' in front of the quotes, e.g. r"C:\Users\sresch\.."
# In the other cases the 'r' is simply ignored; thus best would be to always leave it there.
# OPTIONAL, if not set, folder of executed script will be used
output_destination = r"https://docs.google.com/spreadsheets/d/1Q-HilLKieerZojyF1qytcnCuV3C7GtEOk02padGHpFQ/edit?usp=sharing"


# output_format
# defines the format in which the result data shall be saved (currently available: csv, tsv, xml, json, xlsx)
# OPTIONAL, if not set, csv will be used
output_format = "xlsx"


# summary_sample_limit
# defines how many rows shall be displayed in the summary
# OPTIONAL, if not set, 5 will be used
summary_sample_limit = 3


# endpoint
# defines the SPARQL endpoint against which all the queries are run
# MANDATORY
endpoint = "http://sta-dati-culturaitalia.gruppometa.it/sparql"


# queries
# defines the set of queries to be run. 
# MANDATAORY
queries = [

# GENERALI

{
	"title" : "Q1 Classi e superclassi" ,
	#"description" : "Optional description of first query, used to describe the purpose of the query." ,
	"query" : """
		SELECT distinct ?super ?sub

		WHERE {?sub rdfs:subClassOf ?super }
	"""
},

{    

	"title" : "Q2 Frequanze dei predicati in ordine decrescente" ,
	"query" : """
	  SELECT ?predicate (COUNT(*)AS ?frequency)

  WHERE {?subject ?predicate ?object}

  GROUP BY ?predicate

  ORDER BY DESC(?frequency)
	"""
},  

{    
	"title" : "Q3 Oggetti che contengono DIPINTO con S / O / P " , 
	"query" : """
		 SELECT ?s ?p ?o

			  WHERE

			  { ?s ?p ?o .FILTER regex(str(?s), "dipinto") .

		}
	"""
},

{    
	"title" : "Q4 Tutti i dataset e calcolo delle triple per grafo" , 
	"query" : """
	   SELECT DISTINCT ?g (count(?p) as ?triples)

	WHERE { GRAPH ?g { ?s ?p ?o } }

	GROUP BY ?g
	ORDER BY DESC(?triples)
	"""
},

{    
	"title" : "Q5 Tutte le classi in uso" , 
	"query" : """
	  SELECT ?class (count(?s) as ?count)

	WHERE { ?s a ?class }

	GROUP BY ?class
   
	ORDER BY DESC(?count)
	"""
},

 {    
	"title" : "Q6 Numero di grafi presenti nello SPARQL endpoint" ,     
	"query" : """
		SELECT (COUNT (DISTINCT ?g) AS ?gNum)
  WHERE { GRAPH ?g
	{ ?s ?p ?o }

  }
	"""
},

{    
	"title" : "Q7 Numero di nodi (vertici)" ,     
	"query" : """
	   SELECT (COUNT (DISTINCT ?node) AS ?vNum)
  WHERE {
	{ ?node ?p ?obj }
	UNION
	{ ?obj ?p ?node }
  }
	"""
},


{    
	"title" : "Q8 Numero di triple tra due nodi" ,     
	"query" : """
   SELECT ?s ?o (COUNT (*) AS ?tNum)
  WHERE {
	{ ?s ?p ?o }
	UNION
	{ ?o ?q ?s }
  }
  GROUP BY ?s ?o
	"""
},

{    
	"title" : "Q9 Tutti gli oggetti di tipo Opere" ,  
	"description" : "Specifica per E22_Man_Made_Object" ,   
	"query" : """
	 SELECT ?oggetto ?tipo

	WHERE { ?oggetto a crm:E22_Man-Made_Object;
					crm:P2_has_type ?tipo.
			?tipo a crm:E55_Type;
				 rdfs:label "Opere".}
	"""
},

{    
	"title" : "Q10 Predicati utilizzati dalla classe E22_Man_Made_Object" ,  
	"description" : "Specifica per E22_Man_Made_Object" ,   
	"query" : """
	  SELECT ?p (count(?p) as ?count) 

	  WHERE { [a crm:E22_Man-Made_Object ] ?p ?o } 

	  GROUP BY ?p
	"""
},

{    
	"title" : "Q11 Elenco delle classi e predicati collegati ad una determinata classe e numero di istanze collegate rispetto alla classe determinata" ,  
	"description" : "Specifica per E22_Man_Made_Object" ,   
	"query" : """
	  SELECT ?p ?c (COUNT(?p) AS ?pc) {
	  ?f a crm:E22_Man-Made_Object .
	  ?t a ?c .
	  ?f ?p ?t .
	  FILTER(?c != owl:Class)
	} GROUP BY ?p ?c
  ORDER BY DESC(?pc)
	"""
},

{    
	"title" : "Q12 Query federata Oggetti che hanno come tipologia Kantaros e la defizione di Kantaros dal Getty Thesaurus" ,  
   "description" : "Specifica per E22_Man_Made_Object" ,   
	"query" : """
  SELECT *

			  WHERE {{  ?oggetto crm:P2_has_type ?type .

					  ?type a crm:E55_Type;

						   rdfs:label "kantharos" .
					}

					SERVICE <http://vocab.getty.edu/sparql> {

					  SELECT ?gco

	WHERE {?gco rdfs:label "kantharos"@en}

						}}
	"""
},

{    
	"title" : "Q13 Tutti i Man Made Object di tipo Dipinto" ,  
   "description" : "Specifica per E22_Man_Made_Object" ,   
	"query" : """
	SELECT ?oggetto ?type WHERE {

					  ?oggetto a crm:E22_Man-Made_Object;
							crm:P2_has_type ?type.

					  ?type a crm:E55_Type;

						   rdfs:label "dipinto" .

						}
	"""
},

{    
	"title" : "Q14 Opere fatte da Vasari" ,  
   "description" : "Specifica per E22_Man_Made_Object" ,   
	"query" : """
  SELECT ?oggetto ?actor

	WHERE {?oggetto a crm:E22_Man-Made_Object;
				crm:P94i_was_created_by ?creation.
		   ?creation a crm:E65_Creation;
				  crm:P14_carried_out_by ?actor.
		   ?actor a crm:E39_Actor;
				  crm:P48_has_preferred_identifier ?appellation.
			?appellation a crm:E82_Actor_Appellation;
				  rdfs:label "Vasari"
		  }

	"""
},

{    
	"title" : "Q14a Opere e attori" ,  
   "description" : "Specifica per E22_Man_Made_Object" ,   
	"query" : """
  SELECT ?oggetto ?actor ?label
  WHERE {?oggetto a crm:E22_Man-Made_Object;
			  crm:P94i_was_created_by ?creation.
		 ?creation a crm:E65_Creation;
				crm:P14_carried_out_by ?actor.
		 ?actor a crm:E39_Actor;
				crm:P48_has_preferred_identifier ?appellation.
		  ?appellation a crm:E82_Actor_Appellation;
				rdfs:label ?label .
		}


	"""
},

{    
	"title" : "Q15 Opere intitolate Battesimo di Cristo" ,  
   "description" : "Specifica per E22_Man_Made_Object" ,   
	"query" : """
  SELECT ?oggetto ?title

	WHERE {?oggetto a crm:E22_Man-Made_Object;
				crm:P1_is_identified_by ?title.
			?title a crm:E35_Title;
				   rdfs:label "Battesimo di Cristo"}

	"""
},

{    
	"title" : "Q16 Opere che nel titolo contengono Cristo" ,  
   "description" : "Specifica per E22_Man_Made_Object" ,   
	"query" : """
  SELECT ?oggetto ?label

	WHERE {?oggetto a crm:E22_Man-Made_Object;
				crm:P1_is_identified_by ?title.
			?title a crm:E35_Title;
					 rdfs:label ?label.
			?label  bif:contains "'Cristo'" .
		   }
	"""
},

{    
	"title" : "Q17 Collezioni e titoli delle Collezioni" ,  
  "description" :  "Specifica per E78_Collection" ,   
	"query" : """
 SELECT ?collection ?title ?label

  WHERE {?collection a crm:E78_Collection;
			 crm:P1_is_identified_by ?title.
		 ?title a crm:E35_Title;
			 rdfs:label ?label }
	"""
},

{    
	"title" : "Q18 Legal Body del Piemonte e contatti" ,  
   "description" : "Specifica per E40_Legal_Body" ,   
	"query" : """
  SELECT ?lo ?cp ?label

  WHERE {?lo a    crm:E40_Legal_Body; 
				 
				  crm:P76_has_contact_point ?cp.
	  
		 ?cp a    crm:E51_Contact_Point;
				  rdfs:label ?label.
		 ?label   bif:contains "'Piemonte'" .}
	"""
},

{    
	"title" : "Q19 Luoghi della cultura in Piemonte con indirizzo e contatti" ,  
   "description" : "Specifica per E40_Legal_Body" ,   
	"query" : """
  SELECT ?lc ?ente ?indirizzo ?tipologia ?contatti

  WHERE {?lc a crm:E40_Legal_Body;
			   crm:P1_is_identified_by ?appellation;
			   crm:P76_has_contact_point ?cp;
			   crm:P2_has_type ?type;
			   crm:P53_has_former_or_current_location ?luogo.
		   ?appellation a <http://www.openarchives.org/OAI/2.0/E82_Actor_Appellation>;
			   rdfs:label ?ente.
		 ?luogo a crm:E53_Place;

				crm:P1_is_identified_by ?address.

		 ?address a crm:E45_Address;
					  rdf:value ?indirizzo.
		 ?indirizzo bif:contains "'Piemonte'".

		 ?type a    crm:E55_Type;
				  rdfs:label ?tipologia.
		 ?tipologia   bif:contains "'Luoghi della cultura'" .

	   ?cp a    crm:E51_Contact_Point;
				  rdfs:label ?contatti}
	"""
},

{    
	"title" : "Q20 Luoghi della cultura in Lombardia e indirizzo" ,  
   "description" : "Specifica per E40_Legal_Body" ,   
	"query" : """
   SELECT ?lc ?ente ?indirizzo

  WHERE {?lc a crm:E40_Legal_Body;
			   crm:P1_is_identified_by ?appellation;
			   crm:P53_has_former_or_current_location ?luogo.
		   ?appellation a <http://www.openarchives.org/OAI/2.0/E82_Actor_Appellation>;
			   rdfs:label ?ente.
		  ?luogo a crm:E53_Place;

				crm:P1_is_identified_by ?address.

		 ?address a crm:E45_Address;
					  rdf:value ?indirizzo.
		 ?indirizzo bif:contains "'Lombardia'".}
	"""
},

{    
	"title" : "Q21 Luoghi della cultura in Lombardia con indirizzo e contatti" ,  
  "description" :  "Specifica per E40_Legal_Body" ,   
	"query" : """
	SELECT ?lc ?ente ?indirizzo ?tipologia ?contatti

  WHERE {?lc a crm:E40_Legal_Body;
			   crm:P1_is_identified_by ?appellation;
			   crm:P76_has_contact_point ?cp;
			   crm:P2_has_type ?type;
			   crm:P53_has_former_or_current_location ?luogo.
		   ?appellation a <http://www.openarchives.org/OAI/2.0/E82_Actor_Appellation>;
			   rdfs:label ?ente.
		 ?luogo a crm:E53_Place;

				crm:P1_is_identified_by ?address.

		 ?address a crm:E45_Address;
					  rdf:value ?indirizzo.
		 ?indirizzo bif:contains "'Lombardia'".

		 ?type a    crm:E55_Type;
				  rdfs:label ?tipologia.
		 ?tipologia   bif:contains "'Luoghi della cultura'" .

	   ?cp a    crm:E51_Contact_Point;
				  rdfs:label ?contatti}
	"""
},

{    
	"title" : "Q22 Tipologie di enti e label" ,  
  "description" :  "Specifica per E40_Legal_Body" ,   
	"query" : """
	 SELECT ?ente ?tipologia

  WHERE {?ente a crm:E40_Legal_Body;
			   crm:P2_has_type ?type.
		 ?type a crm:E55_Type;
				rdfs:label ?tipologia.}

	"""
},

{    
	"title" : "Q23 Diritti posseduti da un ente" ,  
  "description" :  "Specifica per E30_Right" ,   
	"query" : """
  SELECT ?diritti ?lb ?label

	WHERE {?diritti a crm:E30_Right;
				  crm:P75i_is_possessed_by ?lb.
			?lb a crm:E40_Legal_Body;
				  rdfs:label ?label}

	"""
},

{    
	"title" : "Q24 Tipologie di diritti per le singole risorse" ,  
  "description" :  "Specifica per E30_Right" ,   
	"query" : """
 SELECT ?risorsa ?titolo ?proprietà

	WHERE {?risorsa a crm:E22_Man-Made_Object;
					  crm:P104_is_subject_to ?diritti;
						 crm:P1_is_identified_by ?title.
			?title a crm:E35_Title;
				   rdfs:label ?titolo.
					  
		   ?diritti a crm:E30_Right;
					 crm:P75i_is_possessed_by ?lb.
			?lb a crm:E40_Legal_Body;
				  rdfs:label ?proprietà.}

	"""
},

{    
	"title" : "Q25 Ente e label" ,  
  "description" :  "Specifica per E30_Right" ,   
	"query" : """
 SELECT ?risorsa ?label

   WHERE {?risorsa a crm:E40_Legal_Body;
					rdfs:label ?label.}

	"""
},

{    
	"title" : "Q26 Tutte le fotografie PICO thesaurus" ,  
  "description" :  "integrazione PICO THesaurus" ,   
	"query" : """
SELECT ?risorsa ?titolo ?tipo

WHERE { ?risorsa a crm:E22_Man-Made_Object;
  crm:P2_has_type ?tipo;
  crm:P1_is_identified_by ?title. 
  ?title a crm:E35_Title;
  rdfs:label ?titolo.

	?tipo a crm:E55_Type;
		a <http://culturaitalia.it/pico/thesaurus/4.1#fotografie>.}

	"""
},

{    
	"title" : "Q27 Oggetti di tipo FOTOGRAFIA" ,  
  "description" :  "integrazione PICO THesaurus" ,   
	"query" : """
SELECT ?s 

WHERE

{ ?s   a <http://culturaitalia.it/pico/thesaurus/4.1#fotografie> 

}

	"""
},

{    
	"title" : "Q28 Concetti thesaurus e label" ,  
  "description" :  "PICO Thesaurus" ,   
	"query" : """
SELECT ?concept ?prefLabel
WHERE {
  ?concept a skos:Concept .
  ?concept skos:prefLabel ?prefLabel.
 
} 
ORDER BY ?prefLabel

	"""
},

{    
	"title" : "Q29 Tutte le proprietà di un concetto" ,  
  "description" :  "PICO Thesaurus" ,   
	"query" : """
SELECT DISTINCT ?property ?value
WHERE {
  <http://culturaitalia.it/pico/thesaurus/4.1#fotografie>  ?property ?value .
}

	"""
},


{    
	"title" : "Q30 Tutti i broader del concetto ARTISTI" ,  
  "description" :  "PICO Thesaurus" ,   
	"query" : """
SELECT ?concetto 

 WHERE {?concetto a <http://www.w3.org/2004/02/skos/core#Concept> ;
				  skos:broader <http://culturaitalia.it/pico/thesaurus/4.1#artisti>. }

	"""
},

]

# Notes on syntax of queries-set:
# * the set of queries is enclosed by '[' and ']'
# * individual queries are enclosed by '{' and '},'
# * All elements of a query (title, description, query) need to be defined using quotes as well as their contents, and both need to be separated by ':'
# * All elements of a query (title, description, query) need to be separated from each other using quotes ','
# * The content of a query needs to be defined using triple quotes, e.g. """ SELECT * WHERE .... """
# * Any indentation (tabs or spaces) do not influence the queries-syntax, they are merely syntactic sugar.


