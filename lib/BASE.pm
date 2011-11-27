package BASE;

#################################################################################
#  BASE.pm
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

use IO::File;

use vars qw($version $charset $datadir $big $img $thumb $xml $password $thumbsize1 $thumbsize2 $iframestyle $sphotostyle $extrainfo);
use vars qw($totalphotos $totalsize $showall $upload $nullparms $passerror $outputerror $uploadok $noid $invalidtext $commentok $commenterror $labelname $labelemail $labelcancel $labelsend);


# It's good to leave default directories unchanged
$datadir = "data/";

$big   = $datadir . "big/";
$img   = $datadir . "img/";
$thumb = $datadir . "thumb/";
$xml   = $datadir;

$version = "Powered by Poti<b>Photi</b> v0.6";

# Make necessary directories
my $oldmask = umask(0); # Needed to set 777 permits correctly
mkdir($datadir, 0777) if (!-e $datadir);
mkdir($big, 	0777) if (!-e $big);
mkdir($img, 	0777) if (!-e $img);
mkdir($thumb, 	0777) if (!-e $thumb);
umask($oldmask); # Put umask back

if (!-e $datadir || !-w $datadir) {
    # Critical error
    print "Content-type: text/html\n\n";
    print "ERROR: no data directory found, or 777 permits not set.";
    exit(1);
}

# Extract config #################################################################

my %config;
my $configfile = new IO::File("config.txt");
my $configdata = join('', <$configfile>);

$configdata =~ m/\[CHARSET\]=(.*)/;      $config{'charset'} = $charset = $1;
$configdata =~ m/\[TITLE\]=(.*)/;        $config{'title'} = $1;
$configdata =~ m/\[DESCRIPTION\]=(.*)/;  $config{'description'} = $1;
$configdata =~ m/\[KEYWORDS\]=(.*)/;     $config{'keywords'} = $1;

$configdata =~ m/\[LANGUAGE\]=(.*)/;     my $language = "$1.language";
$configdata =~ m/\[PASSWORD\]=(.*)/;     $password = $1;
$configdata =~ m/\[THUMBSIZE1\]=(.*)/;   $thumbsize1 = $1;
$configdata =~ m/\[THUMBSIZE2\]=(.*)/;   $thumbsize2 = $1;
$configdata =~ m/\[IFRAMESTYLE\]=(.*)/;  $iframestyle = $1;
$configdata =~ m/\[SPHOTOSTYLE\]=(.*)/;  $sphotostyle = $1;
$configdata =~ m/\[EXTRAINFO\]=(.*)/;    $extrainfo = ($1 eq 'yes' ? 1 : 0);

##################################################################################


# Languages
require (-e $language ? $language : "es-ES.language");

sub getFecha {
	if (!$_[0]) {
        my ($_seg,$_min,$_hora,$_dia,$_mes,$_anio) = localtime(time);
        $_anio += 1900; $_mes++;
        $_seg  = (sprintf "%02d", $_seg);
        $_min  = (sprintf "%02d", $_min);
        $_hora = (sprintf "%02d", $_hora);
        $_dia  = (sprintf "%02d", $_dia);
        $_mes  = (sprintf "%02d", $_mes);
        return "$_anio$_mes$_dia$_hora$_min";
    } else {
    	my $data = &getID($_[0]);
        if ($data < 12) {
            return "Foto";
        } else {
            my $d1 = substr($data,0,4);  # year
            my $d2 = substr($data,4,2);  # month
            my $d3 = substr($data,6,2);  # day
            my $d4 = substr($data,8,2);  # hour
            my $d5 = substr($data,10,2); # minutes
            return "$d3/$d2/$d1 @ $d4:$d5";
        }
    }
}


sub joinTemplate {
    my $templatefile = new IO::File($_[0]);
    my $templatedata = join('', <$templatefile>);

    $templatedata =~ s/<!--<CHARSET>-->/$config{'charset'}/e;
    $templatedata =~ s/<!--<TITLE>-->/$config{'title'}/eg;
    $templatedata =~ s/<!--<DESCRIPTION>-->/$config{'description'}/e;
    $templatedata =~ s/<!--<KEYWORDS>-->/$config{'keywords'}/e;

    return $templatedata;
}


sub joinSide {
    my $templatefile = new IO::File($_[0]);
    my $templatedata = join('', <$templatefile>);
    my $total1 = "$totalphotos " . $_[1];
    my $total2 = "$totalsize<br />" . $_[2];

    $templatedata =~ s/<!--<SHOWALL>-->/$showall/e;
    $templatedata =~ s/<!--<UPLOAD>-->/$upload/e;
    $templatedata =~ s/<!--<TOTALPHOTOS>-->/$total1/e;
    $templatedata =~ s/<!--<TOTALSIZE>-->/$total2/e;

    return $templatedata;
}

sub getID {
    my $id = shift;
    if (!$id) { return 0; }
    $id =~ s/^.*(\\|\/)//;
    $id =~ s/\.jpg//;
    $id =~ s/\.xml//;
    return $id;
}


sub trim {
    my @out = @_;
    for (@out) {
        s/^\s+//;
        s/\s+$//;
    }
    return wantarray ? @out : $out[0];
}


sub validate {
    # Remove all but numbers
    my $string = shift;
    $string =~ s/[^0-9]//g;
    return $string;
}


1;

