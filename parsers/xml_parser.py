from datetime import datetime
from lxml import etree, objectify
from parsers.epg_parser import EPGParser
from typing import List

from egp.epgchannel import EPGChannel
from egp.epgevent import EPGEvent


class XMLParser(EPGParser):

    def open_file(self, path: str) -> 'file':
        with open(path, 'rb') as fobj:
            xlm = fobj.read()
        return xlm

    def parse_data(self, raw_data):
        channels = raw_data.channel
        current_program_guide = objectify.Element('program_guide')
        search_day_programme = etree.XPath('//programme[starts-with(@start, "20200504")]')
        for event in search_day_programme(raw_data):
            current_program_guide.append(event)
        search_program = etree.XPath('//programme[@channel = $channel_id]')
        data: List[EPGChannel] = list()
        for channel in channels:
            channel_id = channel.attrib['id']
            channel_events: List[EPGEvent] = list()
            events = search_program(current_program_guide, channel_id=channel_id)
            if not events:
                continue
            for event in events:
                event_disc = EPGEvent(
                    datetime(1, 1, 1, int(event.attrib['start'][8:10]), int(event.attrib['start'][10:12])),
                    datetime(1, 1, 1, int(event.attrib['stop'][8:10]), int(event.attrib['stop'][10:12])),
                    event.title
                )
                channel_events.append(event_disc)
            data.append(EPGChannel(channel['display-name'], channel_events))
        return data

    def extract_data(self, file):
        tree = objectify.fromstring(file)
        return tree
