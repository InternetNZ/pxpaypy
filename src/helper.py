"""Helper methods"""
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
    if (et.get("valid") != "1"):
        raise(Exception("Invalid request."))

    result = {}
    for element in et.getchildren():
        result[element.tag] = element.text

    return result
