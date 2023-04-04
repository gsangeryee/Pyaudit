import os
from fnmatch import fnmatch
import re
import json
import argparse
from enum import Enum
from analyzer.report import Report


def main(contest, base_url):

    # Get Contest contracts files path
    #contest_paths = {}
    contest_paths = []

    contest_root = 'audit' + os.sep + contest + os.sep

    scope_paths = []
    with open('scope.txt') as f:
        # read file by line
        for line in f:
            path = contest_root + line.strip()
            contest_paths.append(path)
            #name = line.strip().split(os.sep)[-1]
            #contest_paths[name] = path
        f.close()

    #serverity_levels = ["HIGH", "MEDIUM", "LOW_NC", "GASOP"]
    serverity_levels = ["HIGH", "MEDIUM", "GASOP"]
    # each serverity_level
    for serverity_level in serverity_levels:
        # Get Serverity rules from rule json file
        rules = {}
        rule_root = 'rules' + os.sep + serverity_level.lower() + ".json"

        with open(rule_root) as f:
            rule = json.load(f)
            rules = rule['rules']
        # Write report to file with Markdown format
        markdown_report = Report().get_reports(
            serverity_level, rules, contest_paths, base_url)
        
        # crate report folder if not exist
        if not os.path.exists("audit" + os.sep + contest + "_report"):
            os.makedirs("audit" + os.sep + contest + "_report")
            
        # report file in audit/contest+"_report"/contest + "_" + serverity_level.lower() + ".md"
        report_file = "audit" + os.sep + contest + "_report" + os.sep + contest + "_" + serverity_level.lower() + ".md"
        
        with open(report_file, 'w') as f:
            f.write(markdown_report)
            f.close()

    def __str__(self):
        return self.value


if __name__ == "__main__":
    # main()
    parser = argparse.ArgumentParser(description='Run PyAudit.')
    # add parser arguments for contest and url
    parser.add_argument('-c', '--contest',
                        help='Contest Path', type=str, required=True)
    parser.add_argument('-u', '--url', help='base url',
                        type=str, required=True)
    args = parser.parse_args()
    contest = args.contest
    base_url = args.url
    # add err comment
    if not contest:
        print("Error: Contest is required")
        exit(1)
    if not base_url:
        print("Error: Base URL is required")
        exit(1)
    main(contest, base_url)
