#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

"""
Just examples for using the xmlrpc calls.

"""
import getpass
import os
import time
import xmlrpclib

wikiurl = "http://localhost:8080"
username = os.environ.get('username', None)
print 'Using username:', username
password = os.environ.get('password', None)


#NAME = username # os.environ.get("WIKIUSER", "")
PAGENAME = u"TestPage"
ATTACHNAME = u"example.zip"
PASSWORD = password # getpass.getpass()
WIKIURL = "http://localhost:8080/"

def get_filelist():
    """"
    this script creates a page PAGENAME
    currently the pagename is hard coded
    username NAME is read from an env var WIKIUSER
    """
    if NAME and PASSWORD:
        xmlrpc_url = "%s?action=xmlrpc2" % WIKIURL
        homewiki = xmlrpclib.ServerProxy(xmlrpc_url, allow_none=True)
        multicall = xmlrpclib.MultiCall(homewiki)
        auth_token = homewiki.getAuthToken(NAME, PASSWORD)
        if auth_token:
            multicall.applyAuthToken(auth_token)
            multicall.listAttachments(PAGENAME)
            result = multicall()
            if tuple(result)[0] == "SUCCESS":
                return tuple(result)[1]
    return []

def put_page():
    """"
    this script creates a page PAGENAME
    currently the pagename is hard coded
    username NAME is read from an env var WIKIUSER
    """
    filelist = get_filelist()
    filelist = [txt for txt in filelist if txt.endswith('.png')]

    if NAME and PASSWORD and ATTACHNAME.endswith('.zip'):
        xmlrpc_url = "%s?action=xmlrpc2" % WIKIURL
        homewiki = xmlrpclib.ServerProxy(xmlrpc_url, allow_none=True)
        multicall = xmlrpclib.MultiCall(homewiki)
        auth_token = homewiki.getAuthToken(NAME, PASSWORD)
        if auth_token:
            multicall.applyAuthToken(auth_token)
            text = [' * {{attachment:%s}} ' % txt for txt in filelist]
            multicall.putPage(PAGENAME, '\n'.join(text))
            result = multicall()
            if isinstance(result, tuple) and tuple(result)[0] == "SUCCESS":
                print "page '%s' created: %s" % (PAGENAME, tuple(result)[0])
            else:
                print 'You did not change the page content, not saved!'

def rename_page():
    """"
    this script renames a page PAGENAME hardcoded to a prefix of Trash_ 
    and a time stamp
    currently the pagename is hard coded
    username NAME is read from an env var WIKIUSER
    """
    if NAME and PASSWORD:
        xmlrpc_url = "%s?action=xmlrpc2" % WIKIURL
        homewiki = xmlrpclib.ServerProxy(xmlrpc_url, allow_none=True)
        multicall = xmlrpclib.MultiCall(homewiki)
        auth_token = homewiki.getAuthToken(NAME, PASSWORD)
        if auth_token:
            multicall.applyAuthToken(auth_token)
            trash_name = 'Trash_%d_%s' % (time.time(), PAGENAME)
            multicall.renamePage(PAGENAME, trash_name)
            result = multicall()
            if tuple(result)[0] == "SUCCESS":
                print "page '%s' renamed to %s: %s" % (PAGENAME,
                trash_name, tuple(result)[0])
            else:
                print tuple(result)[1]

def unzip_attachment():
    """"
    this script unzips an attachment ATTACHNME on a page
    currently the attachment name and the pagename is hard coded
    username NAME is read from an env var WIKIUSER
    """
    if NAME and PASSWORD and ATTACHNAME.endswith('.zip'):
        xmlrpc_url = "%s?action=xmlrpc2&target=%s" % (WIKIURL, ATTACHNAME)
        homewiki = xmlrpclib.ServerProxy(xmlrpc_url, allow_none=True)
        multicall = xmlrpclib.MultiCall(homewiki)
        auth_token = homewiki.getAuthToken(NAME, PASSWORD)
        if auth_token:
            multicall.applyAuthToken(auth_token)
            multicall.unzipAttachment(PAGENAME)
            result = multicall()
            print "zip file '%s' on page '%s' unpacked: %s" % (ATTACHNAME,
                  PAGENAME, tuple(result)[0])

def put_attachment():
    """"
    this script adds an attachment ATTACHNANE to a page
    currently the attachment name and the pagename is hard coded
    username NAME is read from an env var WIKIUSER
    """
    if NAME and PASSWORD and ATTACHNAME:
        xmlrpc_url = "%s?action=xmlrpc2" % WIKIURL
        homewiki = xmlrpclib.ServerProxy(xmlrpc_url, allow_none=True)
        multicall = xmlrpclib.MultiCall(homewiki)
        auth_token = homewiki.getAuthToken(NAME, PASSWORD)
        if auth_token:
            multicall.applyAuthToken(auth_token)
            text = file(ATTACHNAME, 'rb+').read()
            data = xmlrpclib.Binary(text)
            multicall.putAttachment(PAGENAME, ATTACHNAME, data)
            result = multicall()
            print "zip file '%s' on page '%s' saved: %s" % (ATTACHNAME,
                PAGENAME, tuple(result)[0])
        else:
            print 'Wrong name: "%s" or password entered!' % NAME
    else:
        print 'Missing name or password'

def del_attachment():
    """"
    this script deletes the ATTACHNAME from the wiki
    currently the attachment name and the pagename is hard coded
    username NAME is read from an env var WIKIUSER
    """
    if NAME and PASSWORD:
        xmlrpc_url = "%s?action=xmlrpc2" % WIKIURL
        homewiki = xmlrpclib.ServerProxy(xmlrpc_url, allow_none=True)
        multicall = xmlrpclib.MultiCall(homewiki)
        auth_token = homewiki.getAuthToken(NAME, PASSWORD)
        if auth_token:
            multicall.applyAuthToken(auth_token)
            multicall.delAttachment(PAGENAME, ATTACHNAME)
            result = multicall()
            print "file '%s' on page '%s' deleted: %s" % (ATTACHNAME,
                 PAGENAME, tuple(result)[0])
        else:
            print 'Wrong name: "%s" or password entered!' % NAME
    else:
        print 'Missing name or password'

if __name__ == "__main__":
#    put_attachment()
#    unzip_attachment()
    put_page()
#    del_attachment()
#    rename_page()

