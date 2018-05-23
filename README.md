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

An extensive and extendable script for executing multiple queries against a SPARQL-endpoint of your choice, returning the result-data either in different data formats or uploaded as a google sheets files into a public google folder or inserted into existing google sheets file.

There is no fancyness yet at all to this script; it just provides the core logic for the described purpose, in a minimalistic manner in order to be extensible for any kind of interface to be wrapped around it later on. 

In the folder ./scripts/querPy/ you can find executables and the source code

### stand-alone executables for windows and linux

These executables are entirely self-contained and are packaged with a python-interpreter, the libraries and the script in one single file, which is run in a terminal.

There are two options available: 
* '-t' creates a template config file where the user can edit all necessary information (what queries to be run, titles, description, output format, output destination, etc.)
* '-r' runs the specified config file; e.g. '-r template.py' would run all queries provided in the template.py file

On Windows, run for example:

```querPy_bin_windows.exe -t```

or 

```querPy_bin_windows.exe  -r template.py```

On Linux, run for example:

```querPy_bin_linux -t```

or 

```querPy_bin_linux  -r template.py```




### run the source code with your own python interpreter

To run the source code with your own python interpreter you need to install the following:

```
pip install SPARQLWrapper
pip install google-api-python-client
```

Then run the source (assuming template.py again to be a config file):
```
python querPy.py -r template.py
```

(Should your pip and python commands be pointing to older versions, you might need to explicitely run 'pip3' or 'python3' instead or install them.)


### Building stand-alone executables for your platform

To make an executable on your own for your platform, you need to install the necessary libraries and pyinstaller:

```
pip install SPARQLWrapper
pip install google-api-python-client
pip install pyinstaller
pyinstaller --onefile querPy.py
```

after these commands, several folders were created; within the dist folder you would find a single executable file which should contain everything needed to run the script (which includes a dedicated python interpreter, all the imported libraries and the script itself).

This single executable file you can run as outlined before.


### structure of the config file

The config file fed with the '-r' command is itself actually a python module (due to problems having arisen when using other formats), thus basic python syntax is to be respected. There is a ready-made template file included in the querPy folder.

Within the file there are several variables (most of which are actually optional):

#### title
defines the title of the whole set of queries

OPTIONAL, if not set, timestamp will be used

#### description
defines the textual and human-intended description of the purpose of these queries

OPTIONAL, if not set, nothing will be used or displayed

#### output_destination
defines where to save the results, input can be: 

* a local path to a folder 

* a URL for a public google sheets document  

* a URL for a public google drive folder

NOTE: On windows, folders in a path use backslashes, in such a case it is mandatory to attach a 'r' in front of the quotes, e.g. r"C:\Users\sresch\.."
In the other cases the 'r' is simply ignored; thus best would be to always leave it there.

OPTIONAL, if not set, folder of executed script will be used

#### output_format
defines the format in which the result data shall be saved (currently available: csv, tsv, xml, json, xlsx)

OPTIONAL, if not set, csv will be used

#### summary_sample_limit
defines how many rows shall be displayed in the summary

OPTIONAL, if not set, 5 will be used

#### endpoint
defines the SPARQL endpoint against which all the queries are run

MANDATORY

#### queries
defines the set of queries to be run. 

MANDATAORY

##### query

###### title

OPTIONAL, if not set, timestamp will be used

###### description

OPTIONAL, if not set, nothing will be used or displayed

###### query
the sparql query itself

MANDATORY
