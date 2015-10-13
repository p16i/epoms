#!/usr/local/bin/python
import sys
import requests
from epoms.spotsig import SpotSig
from bs4 import BeautifulSoup
# from lxml import etree
import eatiht.v2 as v2


spotsig = SpotSig()
url = sys.argv[1]
text = v2.extract(url)

text = """
As part of Internet.org, its initiative to bring billions of people around the world online, Facebook will partner with Eutelsat to launch a new satellite that will provide Internet access to parts of Sub-Saharan Africa.
Internet.org's network infrastructure already includes drones and a laser communication system that are now undergoing lab tests, but this is its first project to provide Internet access from space, said Facebook chief executive officer Mark Zuckerberg in a post.
The Facebook-Eutelsat satellite, called AMOS-6, is currently under construction and scheduled to launch in 2016. After it begins orbiting, the satellite will be able to connect "millions of people" in west, east, and south Africa. Zuckerberg wrote that Internet.org will work with local partners to help users get online using AMOS-6's coverage, but it's unclear if he meant carriers. TechCrunch has emailed Facebook for clarification.The company begin working directly with local carriers in October 2014 to fix their networks and provide speedier connections.
As our Ingrid Lunden pointed out at the time, however, the move wasn't made purely out of altruism. Forming alliances with carriers in countries like Indonesia, where Facebook is already popular, gives it more leverage when trying to convince them to implement services like zero-rating, which has landed Facebook in hot water with net neutrality advocates.
"""
print spotsig.signature(text)
print '->>>>>>>'

text = """
Facebook Inc. is teaming with French satellite operator Eutelsat Communications SA to deliver Internet coverage to 14 countries in Africa beginning next year.

The companies said they would tap communications capability on the Amos-6 satellite, which is expected to be launched in 2016. Amos-6 is being built by Spacecom.

Facebook and Eutelsat said they expect to begin beaming Internet coverage to parts of west, east and southern Africa in the second half of next year. South Africa, Nigeria, Uganda and Kenya are among the countries that will be covered.

The partnership is part of Facebook's Internet.org initiative to extend Internet access to many areas of the developing world where it isn't now available.

To connect people living in remote regions, traditional connectivity infrastructure is often difficult and inefficient, so we need to invent new technologies," Chief Executive Mark Zuckerberg said in a Facebook post. Mr. Zuckerberg said Facebook will work with local partners "to help communities begin accessing Internet services provided through satellite.

Facebook and Eutelsat said they have a multiyear agreement with Spacecom to use Amos-6's broadband capacity.

Eutelsat said it is establishing a new company based in London to lead its African broadband business, focusing initially on premium consumer and professional segments, according to a statement. The company aims to target small-business owners, the spokeswoman said. The company will partner with telecom companies and service providers.


"""

# data = etree.HTML(page.text)
# article = data.xpath('//article/text()')
# print article

# soup = BeautifulSoup(page.text,'html.parser')
# print soup.get_text()
# # print BeautifulSoup(soup.find('article'), 'html.parser' ).string
print spotsig.signature(text)
