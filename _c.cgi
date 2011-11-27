#!/usr/local/bin/perl

#################################################################################
#  _C.CGI
#
#  Author	: Zheileman (zheileman at kalendas.net)
#  URL		: http://potiphoti.sourceforge.net
#
#  Copyright 2003-2004, Zheileman.
#
#
#  This file is part of PotiPhoti.
#
#  PotiPhoti is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  any later version.
#
#  PotiPhoti is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PotiPhoti; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#################################################################################

use strict;

use CGI;
use lib::BASE;

my $img = $BASE::img;
my $xml = $BASE::xml;


print "Content-type: text/html\n\n";

my $q = new CGI;

my $id	 = $q->param('id')   || 0;
my $send = $q->param('send') || 0;

# Remove HTML shit
$id   =~ s/<.+?>//g;
$send =~ s/<.+?>//g;

if (!$id) {
    &printRespuesta($BASE::noid);
    exit;
}

if (!$send) {
    &printForm($id);
} else {
    my $author = BASE::trim($q->param('author')) || 0;
    my $url    = BASE::trim($q->param('url'))	 || 0;
    my $text   = BASE::trim($q->param('text'))	 || 0;

    # Remove HTML shit
    $author =~ s/<.+?>//g;
    $url    =~ s/<.+?>//g;
    $text   =~ s/<.+?>//g;

    # Spam-protect the email address
    $url =~ s/@/\&\#64\;/g;
    $url =~ s/\./\&\#46\;/g;

    if (!$author || !$url || !$text) {
	&printRespuesta($BASE::invalidtext);
    } else {
	if (open XML, "< $xml$id.xml") {
		my @file = <XML>;
		close(XML);

		my $filejoin = join '', @file;
		my $fecha = BASE::getFecha(BASE::getFecha());
	    my $newcomment = "	<Comentario>
    <Fecha>$fecha</Fecha>
    <Autor>$author</Autor>
    <Url>$url</Url>
    <Texto><![CDATA[$text]]></Texto>
  </Comentario>
</Foto>";
	    $filejoin =~ s/<\/Foto>/$newcomment/g;
	    open XML, "> $xml$id.xml";
	    print XML "$filejoin";
	    close(XML);

	    &printRespuesta($BASE::commentok);
	} else {
	    &printRespuesta($BASE::commenterror);
	}
    }
}



sub printForm {
    my $html = BASE::joinTemplate("template_c.txt");
	my $code = "
	<form method=\"post\" action=\"_c.cgi?id=$_[0]\" name=\"comments_form\" onsubmit=\"return formCheck(this)\">

	<input type=\"hidden\" name=\"send\" value=\"1\" />
	<input type=\"hidden\" name=\"id\" value=\"$_[0]\" />

	<div style=\"width:100px; padding-right:15px; margin-right:15px; float:left; text-align:left;\">
		<label for=\"author\">$BASE::labelname</label><br />
		<input tabindex=\"1\" id=\"author\" name=\"author\" /><br /><br />

		<label for=\"url\">$BASE::labelemail</label><br />
		<input tabindex=\"2\" id=\"url\" name=\"url\" /><br /><br />
	</div>

	<br />
	<textarea tabindex=\"3\" id=\"text\" name=\"text\" rows=\"8\" cols=\"29\"></textarea><br /><br />

	<input type=\"button\" onclick=\"window.close()\" value=\"&nbsp; $BASE::labelcancel &nbsp;\" />
	<input style=\"font-weight: bold;\" type=\"submit\" name=\"post\" value=\"&nbsp; $BASE::labelsend &nbsp;\" />

	</form>
	";

    $html =~ s/<!--<CUERPO>-->/$code/;
    print $html;
}


sub printRespuesta {
    my $html = BASE::joinTemplate("template_c.txt");
    my $msg  = "<br /><br />$_[0]";
    $html =~ s/<!--<CUERPO>-->/$msg/;
    print $html;
}

