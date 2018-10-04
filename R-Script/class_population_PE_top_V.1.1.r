library(SPARQL)
library(ggplot2)
library(reshape)
library(scales)
library(RColorBrewer)
library(colorRamps)

endpoint <- "https://virtuoso.parthenos.d4science.org/sparql"

#Q4 - all used Subject types + frequencies

q <- " select distinct ?topclass 

(?class as ?specific_class) (count(distinct ?instanceURI) as ?count) 


where{

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



GRAPH <provenance> {?gRecord <dnetcollectedFrom> ?api . ?api <dnetisApiOf> \"PARTHENOS\"^^<http://www.w3.org/2001/XMLSchema#string>}
} 
group by ?topclass ?class
order by ?topclass ?class
"

res <- SPARQL(url = endpoint, q)$results

#display.brewer.all()

colourCount = length(unique(res$specific_class))
getPalette = colorRampPalette(brewer.pal(12, "Paired"))

ggplot(data = res, aes(x = topclass, y = count, fill = specific_class)) + 
  geom_bar(stat="identity")+
  theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5))+
  #theme(legend.position="bottom") +
  theme(plot.margin=unit(c(0,0,0,0),"cm"))+
  theme(legend.text=element_text(size=6))+
  scale_fill_manual(values = colorRampPalette(brewer.pal(12, 
                                                         "Set3"))(colourCount))




  
