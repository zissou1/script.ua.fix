import xbmcaddon
import xbmc
import xbmcgui
import urllib2
import time
from contextlib import closing

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
settings = xbmcaddon.Addon(id='script.ua.fix')
username = addon.getSetting('username')
password = addon.getSetting('password')
m3upath = addon.getSetting('m3upath')
output = addon.getSetting('output')
new_useragent = ('Kodi/17.1 (Macintosh; Intel Mac OS X 10_11_6) App_Bitness/64 Version/16.1-Git:2016-04-24-c327c5')
dialog = xbmcgui.Dialog()
__language__ = settings.getLocalizedString
note_time = 10000
note_error = 'error'

#Language strings
note_success = __language__(30011)
note_reboot =__language__(30012)
note_urlerr = __language__(30013)
note_usrpass = __language__(30020)
note_connerr = __language__(30021)
note_yes = __language__(30022)
note_no = __language__(30023)
note_abort_reboot = __language__(30024)

def uafix():
    try:
        req = urllib2.Request('http://clientportal.link:8080/get.php?username='+username+'&password='+password+'&type=m3u_plus&output='+output,headers={'User-Agent': 'Mozilla/5.0'})

        with closing(urllib2.urlopen(req)) as response:
            m3u_response = response.read().decode('ascii', 'ignore')

            with closing(open(m3upath+'iptv_original.m3u', 'w+')) as infile, closing(open(m3upath+'iptv_all.m3u', 'w')) as fileall:
                infile.write(m3u_response)
                infile.seek(0)
                '''ignoreLines = False'''
                for line in infile:
                    '''if '#EXTM3U' in line:
                        fileswe.write(line)
                        ignoreLines = True
                    if 'tvg-name=\" Sweden [SE] \"' in line:
                        ignoreLines = False
                    if 'group-title=\"Switzerland\"' in line:
                        ignoreLines = True
                    if not ignoreLines:
                        fileswe.write(line.replace('.m3u8', '.m3u8|User-agent='+new_useragent))'''
                    fileall.write(line.replace('.m3u8', '.m3u8|User-agent='+new_useragent))

            if dialog.yesno(addon.getAddonInfo('name'), note_success, note_reboot, note_abort_reboot , yeslabel=note_yes, nolabel=note_no, autoclose=13000):
                xbmc.executebuiltin('ActivateWindow(10000,return)')
            else:
                xbmc.restart()

    except urllib2.URLError:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(note_urlerr.encode('utf-8'), note_usrpass.encode('utf-8'), note_time, note_error))
        time.sleep(2)
        addon.openSettings('script.ua.fix')

try:
    urllib2.urlopen("http://www.google.com").close()
except urllib2.URLError:
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, note_connerr.encode('utf-8'), note_time, note_error))
else:
    uafix()
