import config, lang, pb, misc

from xml.dom import minidom
import urllib2
import time
import os
import urlnorm
from collections import OrderedDict
import sys

def crawl_subcats():
	dirpath = "data/site/%s/" % config.start_cat
	filepath = dirpath + "%s/subcats.txt"

	if os.path.exists(filepath):
		subcats = misc.read_file(filepath)
	else:
		subcats = get_subcats(config.start_cat)
		subcats = [subcat for subcat in subcats if lang.can_subcat(subcat)]
		
		misc.write_file(dirpath + "subcats.txt", subcats)
	return subcats

def crawl_pages(subcats):
	dirpath = "data/site/%s/" % config.start_cat
	pages = []

	counter = 0
	for subcat in subcats:
		counter += 1
		pb.update(counter, len(subcats))

		subcat_dirpath = dirpath + subcat + "/"
		misc.mkdir_p(subcat_dirpath)

		filepath = subcat_dirpath + "pages.txt"
		if os.path.exists(filepath):
			subcat_pages = misc.read_file(filepath)
		else:
			subcat_pages = get_subcat_pages(subcat)
			misc.write_file(filepath, subcat_pages)

		pages.extend(subcat_pages)

	pages = [page for page in pages if lang.can_page(page)]
	pages = OrderedDict.fromkeys(pages).keys() # unique
	return pages

def crawl_all_pages(pages):
	dirpath = "data/pages/%s/" % config.start_cat

	counter = 0
	for page in pages:
		counter += 1
		pb.update(counter, len(pages))

		filepath = dirpath + page + ".html"
		if not os.path.exists(filepath):
			htmldoc = get_page(page)

			f = open(filepath, 'w')
			f.write(htmldoc)
			f.close()

def get_subcats(category):
	while True:
		try:
			subcats = dl_subcats(category)
			break
		except:
			e = sys.exc_info()[0]
			print(e)

	return subcats

def get_subcat_pages(subcat):
	while True:
		try:
			subcat_pages = dl_pages(subcat)
			break
		except:
			e = sys.exc_info()[0]
			print(e)

	return subcat_pages

def get_page(page):
	while True:
		try:
			htmldoc = dl_html(page)
			break
		except:
			e = sys.exc_info()[0]
			print(e)
	return htmldoc

def dl_subcats(category):
	subcats = []
	cmcontinue = True
	cmcontinue_str = ""

	while cmcontinue:
		xml = dl_subcats_xml(category, cmcontinue_str)

		xmldoc = minidom.parseString(xml)
		subcatlist = xmldoc.getElementsByTagName('cm')
		subcatlist = [subcat.attributes['title'].value.encode("utf8") for subcat in subcatlist]
		subcats.extend(subcatlist)

		list = xmldoc.getElementsByTagName('query-continue')
		if list:
			categorymembers = list[0].getElementsByTagName('categorymembers')[0]
			cmcontinue_str = categorymembers.attributes["cmcontinue"].value
		else:
			cmcontinue = False

	return subcats

def dl_subcats_xml(category, cmcontinue):
	if cmcontinue:
		return dl_xml({"action": "query", 
			"list": "categorymembers",
			"cmtitle": category,
			"cmtype": "subcat",
			"cmlimit": "500",
			"cmcontinue": cmcontinue})
	else:
		return dl_xml({"action": "query", 
			"list": "categorymembers",
			"cmtitle": category,
			"cmtype": "subcat",
			"cmlimit": "500"})

def dl_pages(subcat):
	pages = []
	cmcontinue = True
	cmcontinue_str = ""

	while cmcontinue:
		xml = dl_pages_xml(subcat, cmcontinue_str)

		xmldoc = minidom.parseString(xml)
		pagelist = xmldoc.getElementsByTagName('cm')
		pagelist = [page.attributes['title'].value.encode("utf8") for page in pagelist]
		pages.extend(pagelist)

		list = xmldoc.getElementsByTagName('query-continue')
		if list:
			categorymembers = list[0].getElementsByTagName('categorymembers')[0]
			cmcontinue_str = categorymembers.attributes["cmcontinue"].value
		else:
			cmcontinue = False

	return pages

def dl_pages_xml(subcat, cmcontinue):
	if cmcontinue:
		return dl_xml({"action": "query", 
			"list": "categorymembers",
			"cmtitle": subcat,
			"cmtype": "page",
			"cmlimit": "500",
			"cmcontinue": cmcontinue})
	else:
		return dl_xml({"action": "query", 
			"list": "categorymembers",
			"cmtitle": subcat,
			"cmtype": "page",
			"cmlimit": "500"})

def dl_xml(params):
	url = "http://en.wiktionary.org/w/api.php?format=xml"
	for key, val in params.iteritems():
		url += "&%s=%s" % (key, val)
	url = urlnorm.norm(url)

	# We're permitted to crawl any page with the API regardless
	# of robots.txt since we're using the API
	response = urllib2.urlopen(url.encode("utf8"), timeout=5)

	time.sleep(config.api_crawl_delay)
	return response.read()

def dl_html(page):
	url = "http://en.wiktionary.org/wiki/%s" % page
	url = urlnorm.norm(url)

	# we should be able to crawl any page from the links we obtained
	# and we're obeying crawling delays here
	response = urllib2.urlopen(url.encode("utf8"), timeout=5)

	time.sleep(config.page_crawl_delay)
	return response.read()
