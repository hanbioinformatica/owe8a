<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="html" encoding="UTF-8"/>

 

    <xsl:template match="/">
        <html>
            <head>
                <title>CV - <xsl:value-of select="cv/personalia/naam"/></title>
            </head>
            <body style="font-family: helvetica; font-size: 14px;">
                <h1>Curriculum Vitae</h1>
                <h2>Personalia</h2>
                <table bgcolor="lightgray" border="0">
                    <tr>
                        <td width="250">Naam</td>
                        <td width="250">
                            <xsl:value-of select="cv/personalia/naam"/>
                        </td>
                    </tr>
                    <tr>
                        <td>Geboorte Datum</td>
                        <td>
                            <xsl:value-of select="cv/personalia/gebdatum"/>
                        </td>
                    </tr>
                    <tr>
                        <td>Geslacht</td>
                        <td>
                            <xsl:value-of select="cv/personalia/geslacht"/>
                        </td>
                    </tr>
                    <tr>
                        <td>Burg. Staat</td>
                        <td>
                            <xsl:value-of select="cv/personalia/burgstaat"/>
                        </td>
                    </tr>
                    <tr>
                        <td>Nationaliteit</td>
                        <td>
                            <xsl:value-of select="cv/personalia/nationaliteit"/>
                        </td>
                    </tr>
                    <tr>
                        <td>E-mail</td>
                        <td>
                            <xsl:value-of select="cv/personalia/email"/>
                        </td>
                    </tr>
                </table>
                <h2>Studie</h2>
                <table bgcolor="lightgray" border="0">
                    <xsl:for-each select="cv/studie/opleiding">
                        <tr>
                            <td valign="top" width="250">
                                <xsl:value-of select="periode"/>
                            </td>
                            <td width="250">
                                <xsl:value-of select="naam"/>
                                <xsl:value-of select="school"/>
                                <xsl:value-of select="diploma"/>
                                <xsl:value-of select="plaatje"/>
                            </td>
<td><img>   		
    		<xsl:attribute name="src">
    			<xsl:copy-of select="plaatje"/>
    		</xsl:attribute>
    	</img></td>


                        </tr>
                    </xsl:for-each>
                </table>
                <h2>Werk</h2>
                <table bgcolor="lightgray" border="0">
                    <xsl:for-each select="cv/werk/baan">
                        <tr>
                            <td valign="top" width="250">
                                <xsl:value-of select="periode"/>
                            </td>
                            <td width="250">
                                <xsl:value-of select="functie"/> bij
                                <xsl:value-of select="bedrijf"/>
                            </td>
                        </tr>
                    </xsl:for-each>
                </table>
                <h2>Referenties</h2>
                <xsl:for-each select="cv/referenties/referentie">
                    <table bgcolor="lightgray" border="0">
                        <tr>
                            <tr>
                                <td width="250">
                                    Organisatie
                                </td>
                                <td width="250">
                                    <xsl:value-of select="bedrijf"/>
                                </td>
                            </tr>
                            <tr>
                                <td width="250">
                                    Naam
                                </td>
                                <td>
                                    <xsl:value-of select="naam"/>
                                </td>
                            </tr>
                            <tr>
                                <td width="250">
                                    Telefoon
                                </td>
                                <td>
                                    <xsl:value-of select="telefoon"/>
                                </td>
                            </tr>
                            <tr>
                                <td width="250">
                                    Email
                                </td>
                                <td>
                                    <xsl:value-of select="email"/>
                                </td>
                            </tr>
                        </tr>
                    </table>
                </xsl:for-each>
                <h2>Hobbies</h2>
                <table bgcolor="lightgray" border="0">
                    <xsl:for-each select="cv/hobbies/hobby">
                        <tr>
                            <td width="250">
                                <xsl:value-of select="naam"/>
                            </td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>
