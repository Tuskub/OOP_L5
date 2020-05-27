from datetime import datetime, timedelta
from lxml import html, etree
import requests
from parsers.epg_parser import EPGParser
from typing import List

from egp.epgchannel import EPGChannel
from egp.epgevent import EPGEvent


class HTMLParser(EPGParser):

    def open_file(self, path: str) -> 'file':
        re = requests.get(path)
        return re

    def parse_data(self, raw_data) -> List[EPGChannel]:
        data: List[EPGChannel] = list()
        tree = html.fromstring(raw_data)
        get_start_time = etree.XPath('.//span[@class="p-programms__item__time-value"]/text()')
        get_channel_name = etree.XPath('.//div[@class = "p-channels__item__info"]/div/a/text()')
        get_events = etree.XPath('.//div[@class = "p-programms__item__inner"]')
        get_title = etree.XPath('.//span[@class="p-programms__item__name-link"]/text()')
        all_channel = tree.xpath('//div[starts-with(@class, "p-channels__item js-channel-item")]')
        for channel in all_channel:
            channel_programme: List[EPGEvent] = list()
            channel_name = get_channel_name(channel)[0]
            events = get_events(channel)
            events_start_time = list()
            for event in events:
                start_time = get_start_time(event)[0].split(':')
                events_start_time.append(datetime(1, 1, 1, int(start_time[0]), int(start_time[1])))
            buf_time = events_start_time + [events_start_time[-1] + timedelta(hours=1, minutes=10)]
            events_end_time = [a + (b - a) for a, b in zip(buf_time, buf_time[1:])]
            for event, start_time, end_time in zip(events, events_start_time, events_end_time):
                event_desc = EPGEvent(start_time, end_time, get_title(event)[0])
                channel_programme.append(event_desc)
            data.append(EPGChannel(channel_name, channel_programme))
        return data

    def extract_data(self, file):
        return file.content
