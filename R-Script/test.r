library(SPARQL)
library(ggplot2)
library(reshape)
library(scales)



res <-  read.csv("class_population.V1.3.csv")

ggplot(res, aes(x=class, y=count, fill=count)) +
  geom_bar(stat="identity")+theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5))+
  geom_text(aes(label=count), vjust=-0.1, size=2.5)
