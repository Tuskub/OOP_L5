import sys
from parsers.xml_parser import XMLParser
from xml.etree import ElementTree as ET
from datetime import datetime


def channel_templates(name: str) -> ET.Element:
    div = ET.Element('div', attrib={'class': 'channel_item_info'})
    label = ET.Element('label')
    label.text = str(name)
    div.append(label)
    return div


def event_templates(start: datetime, end: datetime, name: str) -> ET.Element:
    div = ET.Element('div', attrib={'class': 'programm-item'})
    start_time = ET.Element('span')
    end_time = ET.Element('span')
    title = ET.Element('span')
    start_time.text = str(start.time()) + ' - '
    end_time.text = str(end.time()) + ' '
    title.text = str(name)
    div.append(start_time)
    div.append(end_time)
    div.append(title)
    return div


class XMLToHTML:
    parser: XMLParser = XMLParser()

    def __init__(self, path: str):
        self.xml = self.parser.open_file(path)

    def convert_xml_to_html(self):
        self.xml = self.parser.extract_data(self.xml)
        self.xml = self.parser.parse_data(self.xml)
        # После этих преобразований получил xml = List[EPGChannel]
        html = ET.Element('html')
        header = ET.Element('header')
        meta = ET.Element('meta', attrib={'charset': 'UTF-8'})
        body = ET.Element('body')
        main_div = ET.Element('div')
        html.append(header)
        html.append(body)
        body.append(main_div)
        header.append(meta)
        for channel in self.xml:
            channel_div = ET.Element('div', attrib={'class': 'channel_item'})
            channel_div.append(channel_templates(channel.name))
            programme_div = ET.Element('div', attrib={'class': 'programs_items'})
            channel_div.append(programme_div)
            for event in channel.programme:
                programme_div.append(event_templates(event.time_start, event.time_end, event.name))
            main_div.append(channel_div)
        ET.ElementTree(html).write('test.html', encoding='UTF-8', method='html')
