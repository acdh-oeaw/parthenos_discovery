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


## querPy

Script for querying multiple queries against an endpoint of your choice, returned in either different data formats or uploaded as google sheets files into a public folder / sheets file.
There is no fancyness yet at all to this script; it just provides the core logic for the described purpose, in a minimalistic manner in order to be extensible for any kind of interface later on. 

In the folder ./scripts/querPy/ you can find executables and the source code

### executable stand-alone binaries for windows and linux

the executables need to be run in the terminal with two options available:

```querPy -t```

Creating a template config file where you can edit all the necessary sparql-queries, endpoints, descriptions etc.

```querPy -r template.py```

Runs the script and executes all the queries defined in the config file 'template.py'


### source code of script

To run the source code with your own python interpreter you need to install the following:

```
pip install SPARQLWrapper
pip install google-api-python-client
```

To make an executable on your own for your platform you need to install pyinstaller and run it:

```
pip install pyinstaller
pyinstaller --onefile querPy.py
```
