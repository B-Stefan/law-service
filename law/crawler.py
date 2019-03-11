from law.service.law_service import LawService
from law.crawler.law_crawler import LawCrawler
from scrapy.crawler import CrawlerProcess
from law.utils import get_neo4j_driver_instance

if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(LawCrawler)
    process.start()  # the script will block here until the crawling is finished

