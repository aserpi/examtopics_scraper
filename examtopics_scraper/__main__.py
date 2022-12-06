import argparse
import sys

from examtopics_scraper.scrapers import scrape_exams, scrape_questions


def main():
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


main()
