# parthenos_discovery
Various scripts and data related to resource discovery in project Parthenos

## Visualize SPARQL results

`scripts/rdf-binding2d3json.xsl` converts result coming from SPARQL endpoint (in generic xml format to json as expected by the graphviewer[1] (specific [d3][2]-json dialect).

[1] http://graphviewer.acdh.oeaw.ac.at/
[2] https://d3js.org/

```xml
<sparql xmlns="http://www.w3.org/2005/sparql-results#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/2001/sw/DataAccess/rf1/result2.xsd">
 <head>
  <variable name="st"/>
  <variable name="p"/>
  <variable name="ot"/>
  <variable name="count"/>
 </head>
 <results distinct="false" ordered="true">
  <result>
   <binding name="st"><uri>http://www.cidoc-crm.org/cidoc-crm/E84_Information_Carrier</uri></binding>
   <binding name="p"><uri>http://www.cidoc-crm.org/cidoc-crm/P128_carries</uri></binding>
   <binding name="ot"><uri>http://www.cidoc-crm.org/cidoc-crm/E89_Propositional_object</uri></binding>
   <binding name="count"><literal datatype="http://www.w3.org/2001/XMLSchema#integer">428147</literal></binding>
  </result>
```