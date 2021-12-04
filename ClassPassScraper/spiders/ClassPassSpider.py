# -*- coding: utf-8 -*-
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from ClassPassScraper.items import Studios
import json
import logging


class ClassPassspiderSpider(SitemapSpider):
    name = 'ClassPassSpider'
    allowed_domains = ['classpass.com']
    sitemap_urls = ['https://classpass.com/sitemap-studios-partial.xml']


    def __init__(self):
        SitemapSpider.__init__(self)
        rootLogger = logging.getLogger()
        rootLogger.setLevel(logging.DEBUG)

        logFormatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

        # file handler
        fileHandler = logging.FileHandler("Output.log")
        fileHandler.setLevel(logging.DEBUG)
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)

        # console handler
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)


    def parse(self, response):
        # Parse each page. If information does not exist, insert a blank.
        script = response.css('script#store::text').get()
        data = json.loads(script)
        itemLoader = ItemLoader(item=Studios(),response=response)
        for i in data['entities']['venueByIdV2']['data']:
            itemLoader.add_value('Studio', data['entities']['venueByIdV2']['data'][i]['name'])
            itemLoader.add_value('City', data['entities']['venueByIdV2']['data'][i]['address']['city']) if 'city' in data['entities']['venueByIdV2']['data'][i]['address'] \
                else itemLoader.add_value('City', '')
            itemLoader.add_value('State', data['entities']['venueByIdV2']['data'][i]['address']['state']) if 'state' in data['entities']['venueByIdV2']['data'][i]['address'] \
                else itemLoader.add_value('State', '')
            itemLoader.add_value('ZipCode', data['entities']['venueByIdV2']['data'][i]['address']['zip_code']) if 'zip_code' in data['entities']['venueByIdV2']['data'][i]['address'] \
                else itemLoader.add_value('ZipCode', '')
            itemLoader.add_value('Website', data['entities']['venueByIdV2']['data'][i]['website']) if 'website' in data['entities']['venueByIdV2']['data'][i] \
                else itemLoader.add_value('Website', '')
            address = response.css('span._7PFYNQ5sk4nOrtcbS_Kfr::text').getall()[0]
            telephone = ''
            if len(response.css('span._7PFYNQ5sk4nOrtcbS_Kfr::text').getall()) > 1:
                telephone = response.css('span._7PFYNQ5sk4nOrtcbS_Kfr::text').getall()[1]
            itemLoader.add_value('Address', address)
            itemLoader.add_value('Telephone', telephone)
            if 'contact_emails' in data['entities']['venueByIdV2']['data'][i]:
                itemLoader.add_value('Email', data['entities']['venueByIdV2']['data'][i]['contact_emails'])
            elif 'alternate_contact_emails' in data['entities']['venueByIdV2']['data'][i]:
                for alt_email in 'alternate_contact_emails' in data['entities']['venueByIdV2']['data'][i]:
                    itemLoader.add_value('Email', data['entities']['venueByIdV2']['data'][i]['alternate_contact_emails'][alt_email])
            else:   
                 itemLoader.add_value('Email', '')
            itemLoader.add_value('Instagram', data['entities']['venueByIdV2']['data'][i]['instagram_handle']) if 'instagram_handle' in data['entities']['venueByIdV2']['data'][i] \
                else itemLoader.add_value('Instagram', '')
            itemLoader.add_value('Facebook', data['entities']['venueByIdV2']['data'][i]['facebook_page_url']) if 'facebook_page_url' in data['entities']['venueByIdV2']['data'][i] \
                else itemLoader.add_value('Facebook', '')
            itemLoader.add_value('Twitter', data['entities']['venueByIdV2']['data'][i]['twitter']) if 'twitter' in data['entities']['venueByIdV2']['data'][i] \
                else itemLoader.add_value('Twitter', '')
            itemLoader.add_value('Rating', f"{data['entities']['venueByIdV2']['data'][i]['ratings']['mean']}") if 'mean' in data['entities']['venueByIdV2']['data'][i]['ratings'] \
                else itemLoader.add_value('Rating', '')
            itemLoader.add_value('ReviewCount', f"{data['entities']['venueByIdV2']['data'][i]['ratings']['count']['total']}") if 'count' in data['entities']['venueByIdV2']['data'][i]['ratings'] \
                else itemLoader.add_value('ReviewCount', '')
            itemLoader.add_value('Link', response.url)
            yield itemLoader.load_item()
