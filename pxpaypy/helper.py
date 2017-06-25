"""Helper methods"""
# This file is part of PxPayPy.
#
# PxPayPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# PxPayPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public
# License along with PxPayPy. If not, see
# <http://www.gnu.org/licenses/>.

from defusedxml.ElementTree import fromstring as parseXML


def get_xml(response):
    """Returns XML object from web response"""
    if response.status_code != 200:
        raise(Exception("Server responded with {status}: {reason}".format(
            status=response.status_code, reason=response.reason)))
    else:
        try:
            et = parseXML(response.text)
        except Exception as e:
            raise(Exception("Error parsing response: {description}".format(
                description=str(e))))
        return et


def process_status(et, pxpost=False):
    """Returns transaction status"""
    if not pxpost:
        if (int(et.get("valid")) != 1):
            raise(Exception("Invalid request."))
    try:
        return xml_to_dir(et)
    except Exception as e:
        raise(Exception("Error parsing status: {}".format(str(e))))


def xml_to_dir(et):
    """Return a dictionary from XML.
    NOTE: This method ignores attributes"""
    result = {}
    for element in et.getchildren():
        if len(element.getchildren()) > 0:
            result[element.tag] = xml_to_dir(element)
        else:
            result[element.tag] = element.text
    return result
