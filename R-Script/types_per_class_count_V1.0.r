library(SPARQL)
library(ggplot2)
library(reshape)
library(scales)
library(RColorBrewer)
library(colorRamps)

endpoint <- "https://virtuoso.parthenos.d4science.org/sparql"

#Q4 - all used Subject types + frequencies

q <- " select  
?type  
(str(?type_label) as ?type_label)
#(replace(str(?type),\"(^.*/)\",  \"\", \"i\" ) as ?type_label)
?class
(replace(str(?class),\"(^.*/)\",  \"\", \"i\" ) as ?class_label)
?instanceClass
(replace(str(?instanceClass),\"(^.*/)\",  \"\", \"i\" ) as ?instanceClass_label)
(COUNT(distinct ?instanceURI) as ?instanceCount)
(str(?ds) as ?ds)
where{

graph ?gRecord  {
?type a ?class.
optional {?type rdfs:label ?type_label .
FILTER ( langmatches(lang(?type_label), \"en\") || langmatches(lang(?type_label), \"\") ) 
}
{?instanceURI crm:P2_has_type ?type} union {?type crm:P2i_is_type_of ?instanceURI}
}

values ?classE55 { <http://www.cidoc-crm.org/cidoc-crm/E55_Type> }
?class rdfs:subClassOf* ?classE55 .


optional{ ?instanceURI a ?instanceClass }

GRAPH <provenance> {
values ?ds { \"PARTHENOS\"^^<http://www.w3.org/2001/XMLSchema#string> }
?gRecord <dnetcollectedFrom> ?api . ?api <dnetisApiOf> ?ds}

} 

group by ?ds ?class ?instanceClass ?type ?type_label
order by ?ds ?type
"

res <- SPARQL(url = endpoint, q)$results

#display.brewer.all()

colourCount = length(unique(res$type_label))
getPalette = colorRampPalette(brewer.pal(12, "Paired"))

ggplot(data = res, aes(x = instanceClass_label, y = instanceCount, fill = type_label)) + 
  geom_bar(stat="identity")+
  theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5))+
  #theme(legend.position="bottom") +
  theme(plot.margin=unit(c(0,0,0,0),"cm"))+
  theme(legend.text=element_text(size=6))+
  scale_fill_manual(values = colorRampPalette(brewer.pal(12, 
                                                         "Set3"))(colourCount))




  
