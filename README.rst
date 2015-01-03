Wraps `Alexa Web Information Service`_.

Usage
=====

Making ``UrlInfo`` requests::


    api = AwisApi(ACCESS_ID, SECRET_ACCESS_KEY)
    tree = api.url_info("www.domain.com", "Rank", "LinksInCount")
    elem = tree.find("//{%s}StatusCode" % api.NS_PREFIXES["alexa"])
    assert elem.text == "Success"


Batch ``UrlInfo`` requests::


    tree = api.url_info(("example1.com", "example2.com", "example3.com"), "Rank", "LinksInCount")


Making ``SitesLinkingIn`` requests::


    api = AwisApi(ACCESS_ID, SECRET_ACCESS_KEY)
    tree = api.sites_linking_in('metmuseum.org', count=20, start=0)
    for element in tree.findall('//awis:SitesLinkingIn/awis:Site', api.NS_PREFIXES):
        print element.find('awis:Title', api.NS_PREFIXES).text
        print element.find('awis:Url', api.NS_PREFIXES).text


Batch ``SitesLinkingIn`` requests::


    tree = api.sites_linking_in(['metmuseum.org', 'wikipedia.org'])


Making ``CategoryListings`` requests::

    api = AwisApi(ACCESS_ID, SECRET_ACCESS_KEY)
    tree = api.category_listings("Top/Business/Financial_Services")
    for item in tree.findall("//{%s}DataUrl" % api.NS_PREFIXES["awis"]):
        print(item.text)


Changelog
=========

Changes since version 1.0
-------------------------

- Added support for batch requests.
- Added ``SitesLinkingIn`` request support.

Changes since version 1.1
-------------------------

- Added ``CategoryListings`` request support.


.. _Alexa Web Information Service: http://aws.amazon.com/awis/
