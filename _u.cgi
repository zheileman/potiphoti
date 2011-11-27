#!/usr/local/bin/perl

#################################################################################
#  _U.CGI
#
#  Author 	: Zheileman (zheileman at gmail.com)
#  URL		: http://github.com/zheileman/potiphoti
#
#  Copyright 2003-2011, Zheileman.
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
use GD;
use lib::Thumbnail;
use lib::BASE;

my $big = $BASE::big;
my $img = $BASE::img;
my $xml = $BASE::xml;

my $charset  = $BASE::charset;
my $password = $BASE::password;


print "Content-type: text/html\n\n";

my $q = new CGI;

my $step = $q->param('step') || 0;


if (!$step) {

    &printForm;

} else {

    my $pass	= $q->param('pass')    || 0;
    my $file	= $q->param('file')    || 0;
    my $comment = $q->param('comment') || 0;

    if (!$file || !$comment || !$pass) {
	&printForm("<p>$BASE::nullparms</p>");
    } else {

	if ($password eq 'changeme' || $pass ne $password) {
	    &printForm("<p>$BASE::passerror</p>");
	    exit;
	}

	$comment =~ s/<.+?>//g;
	my $id = BASE::getFecha();
	my $fecha = BASE::getFecha($id);
	my $remoteimg = "$img$id.jpg";
	my $remoteimg_original = "$big$id.jpg";
	my $osizeX = 0;
	my $osizeY = 0;

	if (!open ARCH, "> $remoteimg_original") {
		&printForm("<p>$BASE::outputerror $remoteimg_original ($!)</p>");
	} else {

	    my $ReadBytes;
	    my $Buffer;
	    my $Bytes;

	    binmode(ARCH);
	    while ($Bytes=read($file,$Buffer,1024)){
		print ARCH $Buffer;
	    }
	    close ARCH;

	    # Resize the uploaded image
	    if (open IN, "< $remoteimg_original") {
		my $srcImage = GD::Image->newFromJpeg(*IN);
		close IN;

		# Create a thumbnail where the biggest side is X
		# Save original size for later reference
		my $maxthumbsize = $BASE::thumbsize1;
		($osizeX, $osizeY) = $srcImage->getBounds();
		if ($osizeX > $maxthumbsize || $osizeY > $maxthumbsize) {
		    my ($thumbb,$x,$y) = Thumbnail::create($srcImage, $maxthumbsize);

		    # Save the thumbnail
		    if (open OUT, "> $remoteimg") {
			binmode OUT;
			print OUT $thumbb->jpeg;
			close OUT;
		    } else {
			&printForm("<p>$BASE::outputerror $remoteimg ($!)</p>");
		    }
		} else {
		    # We do not need to resize image, so a hardlink will be used to
		    # reference the original image.
		    link("$remoteimg_original", "$remoteimg") || &printForm("<p>$BASE::outputerror $remoteimg ($!)</p>");
		}
	    }

	    my $remotexml = "$xml$id.xml";
	    if (!open XML, "> $remotexml") {
		    &printForm("<p>$BASE::outputerror $remotexml ($!)</p>");
	    } else {

		print XML "<?xml version=\"1.0\" encoding=\"$charset\"?>
<?xml-stylesheet type=\"text/xsl\" href=\"../transform.xsl\"?>
<Foto>
  <Archivo>../$remoteimg</Archivo>
  <Original>../$remoteimg_original</Original>
  <OriginalSizeX>$osizeX</OriginalSizeX>
  <OriginalSizeY>$osizeY</OriginalSizeY>
  <ID>$id</ID>
  <Fecha>$fecha</Fecha>
  <Texto><![CDATA[$comment]]></Texto>
</Foto>
";
		close(XML);
		&printForm("<p>$BASE::uploadok</p>");
	    }

	}

    }

}



sub printForm {
    my $html = BASE::joinTemplate("template_u.txt");
    my $replace = (!$_[0] ? "<p>&nbsp;</p>" : $_[0]);
    $html =~ s/<!--<ERRORES>-->/$replace/;
    print $html;
    exit(0);
}

