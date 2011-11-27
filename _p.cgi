#!/usr/local/bin/perl

#################################################################################
#  _P.CGI
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

my $img   = $BASE::img;
my $thumb = $BASE::thumb;
my $xml   = $BASE::xml;

my $initimg;
my $totalfotos = 0;
my $totalsize  = 0;
my $extrainfo  = $BASE::extrainfo;


print "Content-type: text/html\n\n";

my $q = new CGI;

my $id     = $q->param('id')     || 0;
my $offset = $q->param('offset') || 1;
my $all    = $q->param('all')    || 0;

# Remove all but numbers
$id     = BASE::validate($id);
$offset = BASE::validate($offset);
$all    = BASE::validate($all);

if ($id < 0) { $id = 0; }
if ($offset < 0) { $offset = 1; }
if ($all < 0) { $all = 0; }

&printHTML($id, $offset, $all);



sub printHTML {
    my $html = BASE::joinTemplate("template_p.txt");
    my $minifotos   = &getMinifotos($_[0], $_[1], $_[2]);
    my $fotoactual  = &getFoto($_[0], $_[1], $_[2]);
    my $infolateral = BASE::joinSide("template_s.txt", $totalfotos, $totalsize);
    my $poweredby   = "<div class=\"poweredby\">$BASE::version</div>";
    $html =~ s/<!--<MINIFOTOS>-->/$minifotos/;
    $html =~ s/<!--<FOTOACTUAL>-->/$fotoactual/;
    $html =~ s/<!--<INFOLATERAL>-->/$infolateral/ if $extrainfo;
    $html =~ s/<!--<POWEREDBY>-->/$poweredby/;
    print $html;
}


sub getMinifotos {
    my $ret;
    my $alt;
    my $id = $_[0];
    my $style;
    my $i = 0;
    my $offset = $_[1];
    my $all = $_[2];
    my $newtr = 1;
    my @fotos = <$img*>;
    
    if ($extrainfo) {
        # Complementary information
        $totalfotos = @fotos;
        $totalsize = `du -ch $BASE::thumb $BASE::img $BASE::big`;
        $totalsize =~ s/\n/<br \/>/g;
    }
    
    foreach my $src (reverse sort @fotos) {
    	my $thumbfile = $src;
    	$thumbfile =~ s/$img/$thumb/g;
    	$thumbfile =~ s/\.jpg/m\.jpg/g;

    	if (!-e $thumbfile) {
            if (open IN, "$src") {
                my $srcImage = GD::Image->newFromJpeg(*IN);
                close IN; 

                # Create a thumbnail where the biggest side is X
                my ($thumbb,$x,$y) = Thumbnail::create($srcImage, $BASE::thumbsize2);
     
                # Save the thumbnail
                if (open OUT, "> $thumbfile") {
                    binmode OUT;
                    print OUT $thumbb->jpeg;
                    close OUT;
                }
            } 
        }

    	$style = "style=\"FILTER:alpha(opacity=50);\" onmouseover=\"high(this)\" onmouseout=\"low(this)\"";
    	$i++;
    	
    	if ($all) {
    	    # We are building a table with thumbnails
    	    $ret .= "\r\n<tr>\r\n" if ($newtr == 1);
    	    
        	$alt  = BASE::getFecha($src);
            $ret .= "<td><a href=\"?offset=" . $offset . "&amp;id=" . BASE::getID($src) . "\"><img src=\"$thumbfile\" alt=\"$alt\" title=\"$alt\" border=\"0\" $style /></a></td>\r\n";

    	    $newtr++;
    	    
    	    if ($i == @fotos) {
    	        while ($newtr++ < 5) {
    	            $ret .= "<td>&nbsp;</td>\r\n";
    	        }
    	    }
    	    
    	    if ($newtr >= 5) {
    	        # End of TR
    	        $ret .= "</tr>";
    	        $newtr = 1;
    	    }
    	} else {
        	next if ($i <= ($offset-1)*4);
        	$initimg = $src if (!$initimg); # Get the first photo from each set for later reference
        	if ( ($src eq "$img$id.jpg") || (($id==0) && ($src eq $initimg)) ) { $style = "style=\"$BASE::sphotostyle\""; }
        	$alt  = BASE::getFecha($src);
            $ret .= "&nbsp;<a href=\"?offset=" . $offset . "&amp;id=" . BASE::getID($src) . "\"><img src=\"$thumbfile\" alt=\"$alt\" title=\"$alt\" border=\"0\" $style /></a>\r\n";
            last if ((($i % 4)==0) && ($i < @fotos)); # Exit loop because now we have 4 photos
        }
    }
    
    if ($all) {
        $ret = "\r\n<table width=\"100%\" border=\"0\" cellspacing=\"2\" cellpadding=\"2\">" . $ret . "</table>";
    } else {
        $ret .= "&nbsp;";
        # Add left arrow (go back)
        if ($offset > 1) { $ret .= "<a href=\"?offset=" . ($offset-1) . "\"><img src=\"arrow1.jpg\" alt=\"\" width=\"7\" height=\"9\" border=\"0\" /></a>"; }
        # Add right arrow (next 4 photos)
        if ($i < @fotos) { $ret .= "<a href=\"?offset=" . ++$offset . "\"><img src=\"arrow2.jpg\" alt=\"\" width=\"7\" height=\"9\" border=\"0\" /></a>"; }
    }
    
    $ret = "<center><div class=\"photominis\">$ret</div></center>";
    return $ret;
}


sub getFoto {
    return if ($_[2]);
    my $ret;
    my $xmlfile;
    my $id = $_[0];
    my $offset = $_[1];
    if ($id==0) {
        # There is no photo selected
        $xmlfile = BASE::getID($initimg);
        $xmlfile .= ".xml" if ($xmlfile>0);
    } else {
        $xmlfile = "$id.xml";
    }

    $xmlfile = $xmlfile ? "$xml$xmlfile" : "";
    $xmlfile = "" if (!-e $xmlfile); # File exists?
    
    $ret = "
      <iframe id=\"photolog\" name=\"photolog\" src=\"$xmlfile\" style=\"$BASE::iframestyle\" marginwidth=\"0\" marginheight=\"0\" frameborder=\"0\" scrolling=\"no\"></iframe>
    ";

    return $ret;
}

