library(SPARQL)
library(ggplot2)
library(reshape)
library(scales)
library(RColorBrewer)
library(colorRamps)
library(dplyr)

res <-  read.csv("types_per_class_V1.2_complete.csv")

res %>% count (instanceClass, class_label) %>% 
    ggplot(aes(x = class_label, y = n, fill = instanceClass)) + 
    geom_bar(stat="identity")+
    theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5))+
    scale_fill_brewer(palette="Paired") +
    theme(legend.text=element_text(size=7))




 



  

