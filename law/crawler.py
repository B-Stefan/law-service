from scrapy.crawler import CrawlerProcess
from law.crawler import LawCrawler
from law.service import LawService

if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(LawCrawler)
    process.start()  # the script will block here until the crawling is finished

    service = LawService()
    service.merge_laws(LawCrawler.laws)

