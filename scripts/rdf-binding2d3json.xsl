<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:my="myFunctions"
    xmlns:s="http://www.w3.org/2005/sparql-results#" 
    exclude-result-prefixes="xs"
    version="2.0">

<xsl:variable name="ns">
    <namespaces>
        <ns prefix="crm">http://www.cidoc-crm.org/cidoc-crm/</ns>
        <ns prefix="dig">http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/</ns>
        <ns prefix="pe">http://parthenos.d4science.org/CRMext/CRMpe.rdfs/</ns>
    </namespaces>
</xsl:variable>
<xsl:output method="text" indent="yes"></xsl:output>
    <!-- 
        { "nodes": 
    [{"position":"1","id":"node1","key":"node1","name":"node1_name","type":"TypeA","count":"5"},
     {"position":"2","id":"node2","key":"node2","name":"node2_name","type":"TypeB","count":"10"},
     {"position":"3","id":"node3","key":"node3","name":"node3_name","type":"TypeC","count":"8"}
],
    "links": [{"source":"node1", "target":"node2", "label":"test"},
    {"source":"node2", "target":"node3"}
    ]}
    
    <tt_header><st>st</st><p>p</p><ot>ot</ot><cnt>pCount</cnt></tt_header>
<tt><st>crm:PC14_carried_out_by</st><p>crm:P14.1_in_the_role_of</p><ot>crm:E55_Type</ot><cnt>315301</cnt></tt>
    -->
  
<xsl:template match="/">    
    {"nodes": [
    <xsl:for-each-group select="/s:sparql/s:results/s:result/s:binding[@name = ('st','p','ot')]" group-by=".">
        <xsl:variable name="id" select="my:normalize(.)"/>
        <xsl:variable name="cnt" select="sum(current-group()/../s:binding[@name='count']/s:literal)"/>
        {"id":"<xsl:value-of select="$id"/>","key":"<xsl:value-of select="$id"/>","name":"<xsl:value-of select="my:shorten(.)"/>","count":"<xsl:value-of select="$cnt"/>","type":"entity" }
        <xsl:if test="not(position()=last())"><xsl:text>, </xsl:text></xsl:if>        
    </xsl:for-each-group>
    ],
    "links": [    
    <xsl:for-each select="/s:sparql/s:results/s:result" >
        <xsl:variable name="p_normalized" select="my:normalize(s:binding[@name='p'])" />
        {"source":"<xsl:value-of select="my:normalize(s:binding[@name='st'])" />", "target":"<xsl:value-of select="$p_normalized" />", "value":"<xsl:value-of select="s:binding[@name='count']/s:literal" />"},
        {"source":"<xsl:value-of select="$p_normalized" />", "target":"<xsl:value-of select="my:normalize(s:binding[@name='ot'])" />", "value":"<xsl:value-of select="s:binding[@name='count']/s:literal" />"}
        <xsl:if test="not(position()=last())"><xsl:text>, </xsl:text></xsl:if>
        <!-- <xsl:value-of select="st"/> ->  <xsl:value-of select="p"/>;
        <xsl:value-of select="p"/> ->  <xsl:value-of select="ot"/>; -->
    </xsl:for-each>
    ] }
</xsl:template>

    <xsl:function name="my:shorten">
        <xsl:param name="value" />		
            <xsl:choose>
                <xsl:when test="$ns/namespaces/ns[starts-with($value,.)]">
            <xsl:for-each select="$ns/namespaces/ns">
                <xsl:if test="starts-with($value,.)">
                    <xsl:value-of select="replace($value,.,concat(@prefix,'_'))"/>
                </xsl:if>
            </xsl:for-each>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="$value"/>
                </xsl:otherwise>
            </xsl:choose>
        
    </xsl:function>
    
    <xsl:function name="my:normalize">
        <xsl:param name="value" />
        <xsl:variable name="prefixed" select="my:shorten($value)" />
        <xsl:value-of select="translate($prefixed,'*/-.'',$@={}:[]()#>&lt; ','XZ__')" />		
    </xsl:function>
    

</xsl:stylesheet>