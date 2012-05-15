#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

    Modifications on the original script to achieve wiki-wide search and replace task.
    I used it to change the name Category* to Tag*.

    Copyright 2010 Laurent Perrinet <laurent.perrinet@gmail.com>
    
"""

wikiurl = "http://localhost:8080"
username = os.environ.get('username', None)
print 'Using username:', username
password = os.environ.get('password', None)

import xmlrpclib
#from MoinMoin.support.BasicAuthTransport import BasicAuthTransport
#
#srcwiki = xmlrpclib.ServerProxy("http://moinmo.in/?action=xmlrpc2")
#badcontent = srcwiki.getPage("BadContent")
#print badcontent
#authtran = BasicAuthTransport(username, password)
#dstwiki = xmlrpclib.ServerProxy(wikiurl, transport=authtran)
##dstwiki = xmlrpclib.ServerProxy(wikiaddr)
#MatchingPursuit = dstwiki.getPage("MatchingPursuit")
#print MatchingPursuit
#dstwiki.putPage("BadContent", badcontent)

# From http://moinmo.in/MoinAPI/Examples?highlight=%28xmlrpc%29

if False: # read
    pagename = u'NewsEvents' # not protected
    pagename = u'Publications/Perrinet06ciotat' # protected
    homewiki = xmlrpclib.ServerProxy(wikiurl + "?action=xmlrpc2", allow_none=True)
    auth_token = homewiki.getAuthToken(username, password)
    mc = xmlrpclib.MultiCall(homewiki)
    mc.applyAuthToken(auth_token)
    mc.getPage(pagename)
    result = mc()
    success, raw = tuple(result)
    if isinstance(result, tuple) and tuple(result)[0] == "SUCCESS":
        print "reading page '%s' : %s" % (pagename, tuple(result)[0])
    else:
        print tuple(result)[0]

if False: # True: # write
    pagename = u'TestingPage'
    text = """
    This is a line of TEXT

AND     This is another line of text
    
    """
    homewiki = xmlrpclib.ServerProxy(wikiurl + "?action=xmlrpc2", allow_none=True)
    auth_token = homewiki.getAuthToken(username, password)
    mc = xmlrpclib.MultiCall(homewiki)
    mc.applyAuthToken(auth_token)
    mc.putPage(pagename, text)
    result = mc()
    if isinstance(result, tuple) and tuple(result)[0] == "SUCCESS":
        print "page '%s' created: %s" % (pagename, tuple(result)[0])
    else:
        print 'You did not change the page content, not saved!'

if False: #  replace
#if True: # replace
    pagename = 'Publications/Simoncini11'
#    old, new = '\n= reference =\n', '\n== reference ==\n'
    old, new = 'Category', 'Tag'

#    old, new = '^= reference =$', '^== reference ==$'
#    pagename = u'Publications'

    homewiki = xmlrpclib.ServerProxy(wikiurl + "?action=xmlrpc2", allow_none=True)
    auth_token = homewiki.getAuthToken(username, password)
    mc = xmlrpclib.MultiCall(homewiki)
    mc.applyAuthToken(auth_token)
    mc.getPage(pagename)
    result = mc()
    if tuple(result)[0] == "SUCCESS":
        print "page '%s' to modify: %s" % (pagename, tuple(result)[0])
        raw = tuple(result)[1]
        if raw.find(old)>-1:
            raw = raw.replace(old, new)
#            print raw
            mc.putPage(pagename, raw)
            result = mc()
            print result[0]
        else:
            print 'not modified'
    else:
        print tuple(result)[0]

import os
if True:  # replace
#if False: # False: # rename - not working
#    pagelist = mc.getPageList()#searchPages('ublic')
    old, new = '= reference =\n', '== reference ==\n'
#    old, new = '^= reference =$', '^== reference ==$'
#    old, new = '=== abstract ===\n', '== abstract ==\n'
#    old, new = 'Category', 'Tag'
#    old, new = 'TagPublications11', 'TagYear11'
#    old, new = 'Tag11', 'TagYear11'
#    old, new = 'TagPublications10', 'TagYear10'
#    old, new = 'TagPublications09', 'TagYear09'
#    old, new = 'TagPublications08', 'TagYear08'
#    old, new = 'TagPublications07', 'TagYear07'
#    old, new = 'TagPublications06', 'TagYear06'
#    old, new = 'TagPublications05', 'TagYear05'
#    pagelist = homewiki.searchPages('= reference =')
#    pagelist = homewiki.searchPages(old)
##    pagelist = homewiki.searchPages('= abstract =')
#    pagelist = homewiki.searchPages('Cat')
#    for pagename, pagetext in pagelist:
    homewiki = xmlrpclib.ServerProxy(wikiurl + "?action=xmlrpc2", allow_none=True)
    auth_token = homewiki.getAuthToken(username, password)
    mc = xmlrpclib.MultiCall(homewiki)
    mc.applyAuthToken(auth_token)
    mc.getAllPages()#opts={'include_system':False, 'include_underlay':False})
    result = mc()
    pagelist = tuple(result)[1]
#    pagelist = os.listdir('/Users/lup//Sites/localmoin/perrinet/data/pages')
#    pagelist = [ page.replace('(2d)', '-') for page in pagelist]
#    pagelist = [ page.replace('(2f)', '/') for page in pagelist]
#    pagelist = [ page.replace('(c3a9)', 'é') for page in pagelist]
##    pagelist = [ page.replace('(c380)', 'à') for page in pagelist]
#   
#    print pagelist
    for pagename in pagelist:
        homewiki = xmlrpclib.ServerProxy(wikiurl + "?action=xmlrpc2", allow_none=True)
        auth_token = homewiki.getAuthToken(username, password)
#        if pagename == 'Publications/SanzLeon11': print 'hop'
        mc = xmlrpclib.MultiCall(homewiki)
        mc.applyAuthToken(auth_token)
        mc.getPage(pagename)
        try: 
            result = mc()
#            print pagename
            if tuple(result)[0] == "SUCCESS":
    #            print 'Processing page ', pagename #, pagetext
    #            print "page '%s' to modify: %s" % (pagename, tuple(result)[0])
                raw = tuple(result)[1]
    #            print 'raw = ', raw
    #            print raw, raw.find(old)
                if raw.find(old)>-1:
                    raw = raw.replace(old, new)
        #            print raw
                    mc.applyAuthToken(auth_token)
                    mc.putPage(pagename, raw)
                    result = mc()
                    print ":-) page '%s' modified: %s" % (pagename, tuple(result)[0])
    #                print result[0]
    #            else:
    #                print ")-: page '%s' NOT modified: %s" % (pagename, tuple(result)[0])
            else:
                print tuple(result)[0]
        except:
            print 'failed', pagename


if False: # False: # rename - not working
    homewiki = xmlrpclib.ServerProxy(wikiurl + "?action=xmlrpc2", allow_none=True)
    auth_token = homewiki.getAuthToken(username, password)
    mc = xmlrpclib.MultiCall(homewiki)
    mc.applyAuthToken(auth_token)
    mc.renamePage(u'TestingPage', u'TestPage2')
    result = mc()
    print result[0]
    
#if True:  # rename 
if False: 
    homewiki = xmlrpclib.ServerProxy(wikiurl + "?action=xmlrpc2", allow_none=True)
    auth_token = homewiki.getAuthToken(username, password)
    mc = xmlrpclib.MultiCall(homewiki)
    old, new = 'Category', 'Tag'
#    pagelist = homewiki.searchPages(old)
#    for pagename, pagetext in pagelist:
    for pagename in homewiki.getAllPages():
        if pagename.find(old)>-1:
            mc = xmlrpclib.MultiCall(homewiki)
            mc.applyAuthToken(auth_token)
            mc.renamePage(pagename, pagename.replace(old, new))
            result = mc()

            print ":-) page '%s' modified: %s" % (pagename, tuple(result)[0])
#                print result[0]
#        else:
#            print ")-: page '%s' NOT modified: %s" % (pagename, tuple(result)[0])
