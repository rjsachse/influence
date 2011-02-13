"""
    Simple addon installer for skinner
"""


#Modules General
import os
import sys
import urllib
from traceback import print_exc

#Modules XBMC
import xbmc
import xbmcgui
from xbmcaddon import Addon

# addon constants
#__addonID__   = "script.addon.installer" # get addon id
#__settings__  = Addon( __addonID__ ) # get Addon object

SILENT = True
DIALOG_PROGRESS = xbmcgui.DialogProgress()


def download( url, destination="special://home/addons/packages/" ):
    try:
        if not SILENT:
            DIALOG_PROGRESS.create( __settings__.getAddonInfo( "name" ) )
        destination = xbmc.translatePath( destination ) + os.path.basename( url )
        def _report_hook( count, blocksize, totalsize ):
            if not SILENT: 
                percent = int( float( count * blocksize * 100 ) / totalsize )
                DIALOG_PROGRESS.update( percent, "Downloading: %s " % url, "to: %s" % destination )
        fp, h = urllib.urlretrieve( url, destination, _report_hook )
        print fp, h
        return fp
    except:
        print_exc()
    if not SILENT:
        DIALOG_PROGRESS.close()
    return ""


def install( filename ):
    from resources.lib.extractor import extract
    print "extract : %s %s " % (filename, xbmc.translatePath( "special://skin" ) )
    return extract( filename, xbmc.translatePath( "special://skin" ) )


def notification( header="", message="", sleep=5000, icon="" ):
    """ Will display a notification dialog with the specified header and message,
        in addition you can set the length of time it displays in milliseconds and a icon image. 
    """
    xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i,%s)" % ( header, message, sleep, icon ) )


if ( __name__ == "__main__" ):
    try: zipview = sys.argv[ 1 ]
    except: print_exc()
    else:
        try: SILENT = sys.argv[ 2 ] != "false"
        except: print_exc()

        if zipview:
            ListView = ['1001','1002','1003','1004','1005','1006','1007','1008','1009','1010']
            ViewOK=False
            for v in ListView:
                print v;
                if xbmc.getCondVisibility("!Skin.HasSetting(ViewCustom%s_IsInstall)" % (v) ):
                    print zipview
                    fp, ok = install( zipview )
                    SrcView=open('special://skin/720p/View_Custom.xml','r')
                    NewView=open('special://skin/720p/View_Custom%s.xml' % (v),'w')
                    f=SrcView.readlines()
                    SrcView.close
                    for l in f:
                        NewView.write(l.replace("##@@##",v))
                    NewView.close
                    ViewOK=True
                    xbmc.executebuiltin( "Skin.SetBool(ViewCustom%s_IsInstall)" % ( v ) )
                    break	        

            if ViewOK:
                xbmcgui.Dialog().ok(  "View %s installed" % (v), "XBMC requires restart!" )
            else:
                xbmcgui.Dialog().ok(  "Error","No more custom view available" )    
