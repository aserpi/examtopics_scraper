import argparse
import sys
from typing import TypedDict

import scrapy.crawler

from examtopics_scraper.exporters import (ExamtopicsExamsStdoutPipeline,
                                          ExamtopicsQuestionsStdoutPipeline,
                                          generate_questions_html_exporter, ScrapyPipeline)
from examtopics_scraper.spiders import ExamtopicsExamsSpider, ExamtopicsQuestionsSpider


class CrawlerSettings(TypedDict):
    ITEM_PIPELINES: dict[type[ScrapyPipeline], int]
    LOG_LEVEL: str


def run():
    parser = argparse.ArgumentParser(prog="examtopics_scraper",
                                     description="Simple scraper for question discussions on "
                                                 "ExamTopics")
    parser.add_argument("provider", help="exam provider")
    parser.add_argument("-e", "--exam", help="exam code")
    parser.add_argument("-o", "--output", help="output path for question discussions")
    parser.add_argument("-v", "--verbose", action="store_true", help="enable debug logging")
    args = parser.parse_args()

    if args.exam:
        scrape_questions(args.provider, args.exam, args.output, args.verbose)
    elif args.output:
        print("Cannot save output of provider scraper.")
        sys.exit(64)
    else:
        scrape_exams(args.provider, args.verbose)


def scrape_exams(provider: str, verbose: bool = False):
    """Scrape exams on ExamTopics for a given provider."""
    settings: CrawlerSettings = {
        "ITEM_PIPELINES": {ExamtopicsExamsStdoutPipeline: 300},
        "LOG_LEVEL": "DEBUG" if verbose else "ERROR"
    }
    process = scrapy.crawler.CrawlerProcess(settings=settings)
    process.crawl(ExamtopicsExamsSpider, provider=provider)
    process.start()


def scrape_questions(provider: str, exam: str, output: str, verbose: bool = False):
    """Scrape question discussions on ExamTopics."""
    settings: CrawlerSettings = {"LOG_LEVEL": "DEBUG" if verbose else "ERROR"}
    if output:
        settings["ITEM_PIPELINES"] = {
            generate_questions_html_exporter(provider, exam, output): 300}
    else:
        settings["ITEM_PIPELINES"] = {ExamtopicsQuestionsStdoutPipeline: 300}

    process = scrapy.crawler.CrawlerProcess(settings=settings)
    process.crawl(ExamtopicsQuestionsSpider, provider=provider, exam=exam)
    process.start()
