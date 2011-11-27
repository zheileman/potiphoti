<?xml version="1.0" encoding="ISO-8859-1" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" />
<xsl:template match="/">
    <html>
    <head>
      <link rel="stylesheet" href="../photostyles.css" type="text/css" />
      <script type="text/javascript">
	function resizeIframe() {
		i = parent.document.getElementById(window.name);
		iHeight = document.body.scrollHeight;
		i.style.height = iHeight + 15 + "px";
	}
	function OpenComments(c) {
	    window.open(c,'photocomments','width=320,height=390,scrollbars=no,status=yes');
	}
	function openBigPhoto(p,w,h) {
	    ww = w + 10;
	    wh = h + 20;
	    window.open(p,'bigphoto','width='+ww+',height='+wh+',scrollbars=no,status=yes');
	}
      </script>
    </head>
    <body onload="resizeIframe()">
    <xsl:for-each select="Foto">
      <center>
      <div class="photocentral">
		<xsl:choose>
			<xsl:when test="Original">
				<a href="{Original}" onclick="javascript:openBigPhoto(this.href,{OriginalSizeX},{OriginalSizeY}); return false;">
					<img src="{Archivo}" alt="" title="" border="0" />
				</a>
			</xsl:when>
			<xsl:otherwise>
				<img src="{Archivo}" alt="" title="" border="0" />
			</xsl:otherwise>
		</xsl:choose>
      </div>
      </center>
      <br />
      <div class="photobodyiframe">
	<xsl:value-of select="Texto"/>
	<br /><br />
      </div>
      <div class="posted">
	<a href="../?id={ID}" target="newwindow">permalink</a> :: <a href="../_c.cgi?id={ID}" onclick="OpenComments(this.href); return false">comment</a> ..
	<xsl:value-of select="Fecha"/>
      </div>
      <xsl:for-each select="Comentario">
	<div class="commentbody">
	  <xsl:value-of select="Texto"/>
	</div>
	<div class="commentposted">
	  <a href="mailto:{Url}">
	    <xsl:value-of select="Autor"/>
	  </a>
	   |
	  <xsl:value-of select="Fecha"/>
	</div>
      </xsl:for-each>
    </xsl:for-each>
    </body>
    </html>
</xsl:template>
</xsl:stylesheet>
