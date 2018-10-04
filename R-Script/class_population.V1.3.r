library(SPARQL)
library(ggplot2)
library(plotly)
library(reshape)
library(scales)



res <-  read.csv("class_population.V1.3.csv")



 plot_ly(res, labels = ~class, values = ~count, type = 'pie',
             textposition = 'inside',
             textinfo = 'label+percent',
             insidetextfont = list(color = '#FFFFFF'),
             hoverinfo = 'text',
             text = ~paste('nr.', count, ' class population'),
             marker = list(colors = colors,
                           line = list(color = '#FFFFFF', width = 1))
             #The 'pull' attribute can also be used to create space between the sectors
             ) %>%
  layout(title = 'Class population',
         xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
         yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
         legend = list(x = 100, y = 0.5),
         font = list(color = '#000000', size = 7))
  

