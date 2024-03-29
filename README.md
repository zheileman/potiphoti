PotiPhoti, Yet another simple photolog
======================================

Copyright 2003-2011, Zheileman (zheileman at gmail.com)  
http://github.com/zheileman/potiphoti

Software published under the terms of the GNU General Public License.


DESCRIPTION
-----------

This is a simple photolog system I wrote in Perl several years ago (around 2003) just to have fun and learn a bit of a new language. No database is needed because all data is saved in XML format.  
This photolog will run in any perl-enabled webserver, UNIX-like system.

Pages of the photolog are generated from XML and XSL, and a lot of parameters can be configurated by the user with the simple edition of a configuration file in plane text format.

The main differences from others similar photologs are:

* Technologies: Perl, XML, XSL.
* It is full compatible with Mozilla, Opera and IE.
* Easy installation: it can be installed by uploading a directory to the web server.
* Focused to users with simple necessities in order to begin managing the photolog in 5 minutes.

**Disclaimer:** Please note that the code is ugly, the functionality is very limited and it's probably full of bugs. I was learning perl at the same time I was coding this so the quality is poor and I'm not maintaining the project anymore.  
Use at your own risk.


INSTALLATION
------------

1. Untar potiphoti-xxx.tar.gz to your local hard disk (tar zxvf potiphoti-xxx.tar.gz)

2. Edit `config.txt` in order to configure some parameters like administration password and photolog name.  
You can't use the default password. You need to change it!

3. Optional: edit `template_x` files and make your very personal layout :)  
DO NOT REMOVE `<!--<xxxx>-->` tags, ONLY change their location. Also edit photostyles.css accordly to the new layout.  
Replace logo.jpg with your prefer image. If you want other size for the logo image, do not forget to edit #banner in photostyles.css.

4. You could want to edit `.htaccess` and make it fit your necessities.

5. Upload all to your site and set permissions: `chmod 755 *.cgi`

6. You are done!


**PotiPhoti is not working?**

Check the first line of *.cgi files for the path to your perl interpreter. The default path in the script is `/usr/local/bin/perl`  
If you don't know this path, you can check it out under telnet by entering the command `whereis perl`

Check *.cgi files are in UNIX format. Convert them if necessary.

Check the dir where PotiPhoti files were put has 755 permits.

**IMPORTANT**
PotiPhoti requires GD.pm perl module installed in your server in order to run! Contact your server admin if you don't have it.  
You can download it from http://search.cpan.org/src/LDS/GD-2.11/GD.pm


UPGRADING
---------

If you are upgrading PotiPhoti, remember NOT to remove the /data directory. You can move that directory across different installations of PotiPhoti.
Config.txt, template_x, photostyles.css and transform.xsl shouldn't be overwritten in order to leave current configuration unchanged, but due to the early stage of PotiPhoti development, they could change in next releases, so it's good to make a backup before you upload the new ones, and make manual changes.


HOW TO USE POTIPHOTI
--------------------

The upload system is located in `_u.cgi`, so http://www.yoursite.com/photos/_u.cgi will carry you to it.

Fill in your password, browse your local disk for a good image and write down a brief description for it. Then press upload button and... voila!
The image will be automatically resized with the parametes located in the config.txt file:

``` html
[THUMBSIZE1]=275 (max width for main thumbnail)
[THUMBSIZE2]=50  (max width for mini thumbnails)
```

Original photo with original size is also saved for later visualization.
It's important to know that in the current state of the project, PotiPhoti has only support for JPEG files. Sorry for inconvenience.

Now go to the directory where PotiPhoti files were uploaded (like http://www.yourserver.com/photos/) and enjoy!


**And what about deleting photos already uploaded?**

Well... You can't. This is another of the features that will be developed as soon as possible. Sorry again.
But you can allways remove files from your server through FTP/shell. In order to delete an image, you need to remove the next files:
Check the file name of the image to remove because you'll need it.

``` html
Remove the following:
* In data/ the XML file with that date in filename.
* In data/big/ the image file with that date in filename.
* In data/thumb/ idem.
* In data/img/ idem.
```

FREQUENTLY ASKED QUESTIONS
--------------------------

**Could I change the name of the main directory?**

Yes, it's safe to change it. You can upload PotiPhoti files to any directory.
