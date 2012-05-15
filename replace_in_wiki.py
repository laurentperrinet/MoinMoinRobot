"""
    WikiRpc Search-and-replace tool for MoinMoin 

    Modifications on the original script to achieve wiki-wide search and replace task.
    I used it to change the name Category* to Tag*.
    For safety, everything was done on a local copy of my remote wiki.

    Copyright 2010 Laurent Perrinet <laurent.perrinet@gmail.com>
    

    Copyright 2008 Remco Boerma <r.boerma@drenthecollege.nl>

    Purpose: 
        Using this script you can search-and-replace in multiple wiki pages at once. 
        {{{ preformatted }}}, `text` and = level 1 titles = are preserved at will.

        There are several parameters to be used, some of them set using environment
        variables ('username' and 'password' for example). While sometimes one wants 
        to change every occurence of a needle, at times it's very imported not to 
        change just-everything. The user is asked when running if Save replacement 
        should be used or not. 

    Configuration:
        Environment variables: 
            username :: the username to be used for xmlrpc 
            password :: the password to be used for xmlrpc <optional>
            moin_url :: the hostname of your moinmoin server

        Hardcoded:
            MOIN_URL :: set this to your site's hostname if you don't want to use 
                        the environment variable
            RPC_URL  :: normally set using your MOIN_URL, but this allows for 
                        complex urls
            sever regular expressions used in get_save_regions :: 
                        regular expressions used to test what lines not to touch

    Usage: 
        1. Set the username and moin_url environment variables. If you like, 
        set the password variable as well (or retype this at every execution). 
        2. start replace_in_wiki.py 
        3. enter the expression to select the pages to appy this search-and-replace on
        4. enter the regular expression (FORCED) to search for in the pages
        5. enter the replacement expressions (can use \1 and \2 etc)
        6. enter yes,y or simply hit enter to enable SaveReplacer (and keep 
           {{{preformatted}}} `text` = intact = ) or enter anything else to replace
           every occurence per page. 
        7. Examen the result of diff comparison on the old and new content and decide: 
        8. Either accept the change (yes, y, or simply enter) and upload this new 
           page to the server, or enter any other value (and enter) to not upload the
           new version. 
        
    Notes: 
        1. The regular expression search is performed with re.MULTILINE and re.DOTALL 
           as default options: this allows for multiline matches, as well as using ^ and
           $ in your expression on a line basis. 


    Verified to work with: 
      * Python 2.5
      * MoinMoin 1.5.6 (using plain http authentication)

    @copyright: GPL v2

"""
import xmlrpclib
import getpass,os,re,difflib,sys

WIKIURL = "http://localhost:8080/"

RPC_URL = WIKIURL + "?action=xmlrpc2"

DEBUG = 0 # use this for SaveReplacer debugging... 

class SaveReplacer(object):
    def __init__(self,text):
        self.text = text

    def _is_a_save_region(self,start,end):
        global DEBUG
        if DEBUG>2: print 'Checking %d,%d in %s'%(start,end,self._save_regions)
        for save_start,save_end in self._save_regions:
            if (start >= save_start and start <= save_end) or \
                (end >= save_start and end <= save_end): 
                  return True
        else :
            return False

    def _do_replace(self,match):
        global DEBUG
        start = match.start()
        end = match.end()
        text = match.string
        newtext = match.expand(self.replacement)
        if not self._is_a_save_region(start,end):
            if DEBUG: print 'Changing',`text[start:end]`,'@ %d-%d' % (start,end),'to',`newtext`
            return newtext
        else:
            if DEBUG: print 'PREVENTED',`self.text[start:end]`,'@ %d-%d' % (start,end),'to',`newtext`
            return match.string[start:end]

    def get_save_regions(self):
        regions  = [match.span() for match in re.finditer(r'^=\s.*?\s+=\s*$',self.text,re.MULTILINE)] # multiline to work per line with ^ and $
        regions += [match.span() for match in re.finditer('{{{.*?}}}',self.text,re.DOTALL)] # dotall for . being all including newlines
        regions += [match.span() for match in re.finditer('`.*?`',self.text)]
        return regions

    def run(self,needle,replacement,options=0):
        self.replacement = replacement
        self._save_regions = self.get_save_regions()
        self.text = needle.sub(self._do_replace,self.text,options)
        del self._save_regions
        del self.replacement

if __name__ == '__main__':
    assert sys.version_info[0:2]>=(2,5), "\n\nThis script requires python 2.5 or higher .. \n\n(re.finditer() method should accept options...)"
    username = os.environ.get('username', None)
    print 'Using username:',username
    password = os.environ.get('password', None)

    if not password: 
        password = getpass.getpass('password for '+username+' : ')

    server = xmlrpclib.ServerProxy(RPC_URL)# % (username,password))
    auth_token = server.getAuthToken(username, password)

    print 'searching...',
    pagelist = [pagename for pagename, junk in server.searchPages(raw_input('Page search:'))]
    maxcount = len(pagelist)
    print 'Found', maxcount, 'pages...'
    needle = re.compile(unicode(raw_input('Needle: ')))
    replacement = unicode(raw_input('Replace with: '))
    wants_safe_replace = raw_input('Safe replace  yes/no [yes]:').lower().strip() in ['yes','y','']
    for count,pagename in enumerate(pagelist):
        print '--[%d/%d]------[%s]----' % (count+1,maxcount,pagename)
        text = unicode(server.getPage(pagename))
        if wants_safe_replace:
            save = SaveReplacer(text)
            save.run(needle,replacement,re.MULTILINE + re.DOTALL)
            patched = save.text
        else:
            patched = needle.sub(replacement,text,re.MULTILINE + re.DOTALL)
        if patched == text:
            print 'NO Changes'
            continue 
        lines = list(difflib.Differ().compare(text.splitlines(1),patched.splitlines(1)))
        for line in lines:
            if line[0] in '-+?':
                print line.encode('utf-8'),
        update_answer=raw_input('Update wiki? yes/no [yes] ').lower().strip()
        if update_answer in ['yes','y','',' ']:
            print 'Updating',
            updated =  server.putPage(pagename,patched)
            print `updated`
        else:
            print 'Skipped'
            
