import scrapy.crawler

from examtopics_scraper.exporters import (ExamtopicsExamsExportPipeline,
                                          ExamtopicsQuestionsExportPipeline,
                                          generate_questions_html_exporter)
from examtopics_scraper.spiders import ExamtopicsExamsSpider, ExamtopicsQuestionsSpider


def scrape_exams(provider: str, verbose: bool = False):
    process = scrapy.crawler.CrawlerProcess(settings={
        "ITEM_PIPELINES": {ExamtopicsExamsExportPipeline: 300},
        "LOG_LEVEL": "DEBUG" if verbose else "ERROR"},
    )
    process.crawl(ExamtopicsExamsSpider, provider=provider)
    process.start()


def scrape_questions(provider: str, exam: str, output: str, verbose: bool = False):
    settings = {"LOG_LEVEL": "DEBUG" if verbose else "ERROR"}
    if output:
        settings["ITEM_PIPELINES"] = {
            generate_questions_html_exporter(provider, exam, output): 300}
    else:
        settings["ITEM_PIPELINES"] = {ExamtopicsQuestionsExportPipeline: 300}

    process = scrapy.crawler.CrawlerProcess(settings=settings)
    process.crawl(ExamtopicsQuestionsSpider, provider=provider, exam=exam)
    process.start()
