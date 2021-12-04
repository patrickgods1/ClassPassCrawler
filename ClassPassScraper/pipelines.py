# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from pydispatch import dispatcher

class ClassPassscraperPipeline(object):
    def process_item(self, item, spider):
        return item

def item_type(item):
    # return type(item).__name__.replace('Item','').lower()  # TeamItem => team
    return type(item).__name__

class MultiCSVItemPipeline(object):
    fileNamesCsv = ['Studios']

    def __init__(self):
        self.files = {}
        self.exporters = {}
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)


    def spider_opened(self, spider):
        self.files = dict([ (name, open(f'{name}.csv','ab')) for name in self.fileNamesCsv])
        for name in self.fileNamesCsv:
            self.exporters[name] = CsvItemExporter(self.files[name])

            # if name == 'ImageItem':
            #     self.exporters[name].fields_to_export = ['brand', 'model', 'department', 'image_names', 'image_urls']
            #     self.exporters[name].start_exporting()
            if name == 'Studios':
                self.exporters[name].fields_to_export = ['Studio', 'Address', 'City', 'State', 'ZipCode', 'Telephone', 'Email', 'Website', 'Instagram', 
                    'Facebook', 'Twitter', 'Link', 'Rating', 'ReviewCount']
                self.exporters[name].start_exporting()

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        typesItem = item_type(item)
        if typesItem in set(self.fileNamesCsv):
            self.exporters[typesItem].export_item(item)

        return item