from parsers.html_parser import HTMLParser
from parsers.xml_parser import XMLParser
from parsers.xml_to_html import XMLToHTML


# parser = HTMLParser()
# parser.get_epg('https://tv.mail.ru/orenburg')
#
# parser = XMLParser()
# parser.get_epg('parsers/xmltv.xml')
#
# test = parser.get_average_duration()
# for channel in test:
#     print(channel)

html = XMLToHTML('parsers/xmltv.xml')
html.convert_xml_to_html()
