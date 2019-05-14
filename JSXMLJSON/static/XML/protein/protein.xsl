<?xml version="1.0" encoding="UTF-8"?>
    
    <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="html" encoding="UTF-8"/>

    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="protein">
        <HTML>
            <HEAD>
                <TITLE>Proteine
                    <xsl:value-of select="@name"/>
                </TITLE>
            </HEAD>
            <BODY BGCOLOR="#ffffff">
                <H1>Proteine
                    <xsl:value-of select="@name"/>
                </H1>
                <UL>
                    <LI>Size =
                        <xsl:value-of select="@length"/>
                    </LI>
                    <LI>Gene =
                        <xsl:apply-templates select="GENE"/>
                    </LI>
                    <xsl:if test="INTERACTION">
                        <LI>Interactions =
                            <UL>
                                <xsl:for-each select="INTERACTION">
                                    <LI>
                                        <xsl:apply-templates select="."/>
                                    </LI>
                                </xsl:for-each>
                            </UL>
                        </LI>
                    </xsl:if>
                </UL>
            </BODY>
        </HTML>
    </xsl:template>


    <xsl:template match="GENE">
        <A HREF="{@name}.html">
            <xsl:value-of select="@name"/>
        </A>
    </xsl:template>

    <xsl:template match="INTERACTION">
        <A HREF="{PROTEIN/@name}-{GENE/@name}.html">
            <xsl:value-of select="PROTEIN/@name"/>-
            <xsl:value-of select="GENE/@name"/>
        </A>
    </xsl:template>

</xsl:stylesheet>
