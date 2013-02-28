"""
Copyright 2011, Atamert \xd6l\xe7gen (muhuk@muhuk.com)

This file is part of python-awis.

Python-awis is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Python-awis is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import base64
import datetime
import hashlib
import hmac
import urllib
try:
    from lxml import etree as ET
except ImportError:
    try:
        from xml.etree import cElementTree as ET
    except ImportError:
        raise
        from xml.etree import ElementTree as ET


__author__ = u'Atamert \xd6l\xe7gen'
__copyright__ = u'Copyright 2011, Atamert \xd6l\xe7gen'
__credits__ = [u'Atamert \xd6l\xe7gen']


__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = u'Atamert \xd6l\xe7gen'
__email__ = 'muhuk@muhuk.com'
__status__ = 'Production'


class AwisApi(object):
    """
    Wraps Alexa Web Information Service.

    Usage::

        api = AwisApi(ACCESS_ID, SECRET_ACCESS_KEY)
        tree = api.url_info("www.domain.com", "Rank", "LinksInCount")
        elem = tree.find("//{%s}StatusCode" % api.NS_PREFIXES["alexa"])
        assert elem.text == "Success"
    """
    AWIS_HOST = "awis.amazonaws.com"
    PATH = "/"
    NS_PREFIXES = {
        "alexa": "http://alexa.amazonaws.com/doc/2005-10-05/",
        "awis": "http://awis.amazonaws.com/doc/2005-07-11",
    }

    def __init__(self, access_id, secret_access_key):
        self.access_id = access_id
        self.secret_access_key = secret_access_key

    def sign(self, params):
        msg = "\n".join(["GET",
                         self.AWIS_HOST,
                         self.PATH,
                         self._urlencode(params)])
        hmac_signature = hmac.new(self.secret_access_key, msg, hashlib.sha1)
        signature = base64.b64encode(hmac_signature.digest())
        return signature

    def request(self, params, tries=3, as_xml=True):
        params.update({
            "AWSAccessKeyId": self.access_id,
            "SignatureMethod": "HmacSHA1",
            "SignatureVersion": 2,
            "Timestamp": self._get_timestamp(),
        })
        params["Signature"] = self.sign(params)
        url = "http://%s%s?%s" % (self.AWIS_HOST,
                                  self.PATH,
                                  self._urlencode(params))
        failed_requests = 0
        while failed_requests < tries:
            response = urllib.urlopen(url)
            if response.code == 200:
                if as_xml:
                    return ET.parse(response)
                else:
                    return response.read()
            failed_requests += 1
        raise IOError(
          "All %d requests failed, latest response code is %d" % (
              failed_requests,
              response.code,
           ),
        )

    def url_info(self, urls, *response_groups, **kwargs):
        urls = map(urllib.quote, urls)
        params = { "Action": "UrlInfo" }
        if not isinstance(urls, (list, tuple)):
            params.update({
                "Url": urls,
                "ResponseGroup": ",".join(response_groups),
             })
        else:
            if len(urls) > 5:
                raise RuntimeError, "Maximum number of batch URLs is 5."

            params.update({ "UrlInfo.Shared.ResponseGroup": ",".join(response_groups), })    
            
            for i, url in enumerate(urls):
                params.update({"UrlInfo.%d.Url" % (i + 1): url})
        
        return self.request(params, **kwargs)

    @staticmethod
    def _get_timestamp():
        return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")

    @staticmethod
    def _urlencode(params):
        params = [(key, params[key]) for key in sorted(params.keys())]
        return urllib.urlencode(params)
