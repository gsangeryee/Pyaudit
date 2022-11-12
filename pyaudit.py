import os
from fnmatch import fnmatch
import re
import json
import argparse
from enum import Enum
from analyzer.report import Report

def main(contest, serverity_level,base_url):
    
    # Get Contest contracts files path
    contest_paths = {}

    contest_root = 'audit' + os.sep + contest + os.sep
    file_patterns = "*.sol"

    for path, subdirs, files in os.walk(contest_root):
        for name in files:
            if fnmatch(name, file_patterns):
                contest_paths[name] = os.path.join(path, name)
    
    # Get Serverity rules from rule json file
    rules = {}
    rule_root = 'rules' + os.sep + serverity_level.value.lower() +".json"
    
    with open(rule_root) as f:
        rule = json.load(f)
        rules = rule['rules']

    

    # Write report to file with Markdown format
    markdown_report = Report().get_reports(serverity_level, rules, contest_paths, base_url)
    
    repot_file ='audit' + os.sep + serverity_level.value.lower() +  "_" + contest + ".md"
    
    with open(repot_file, 'w') as f:
        f.write(markdown_report)
        f.close()


# command line arguments
class ServerityLevel(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW_NC = "LOW_NC"
    GASOP = "GASOP"


    def __str__(self):
        return self.value
        
if __name__ == "__main__":
    # main()
    parser = argparse.ArgumentParser(description='Run PyAudit.')
    parser.add_argument('-c', '--contest', help='Contest Path', type=str, required=True)
    parser.add_argument('-l', '--serverity-level', choices=list(ServerityLevel), \
                        help='Choice Serverity level', type=ServerityLevel, required=True)
    parser.add_argument('-u', '--url', help='base url', type=str, required=True)
    args = parser.parse_args()
    contest = ""
    serverity_level = ""
    base_url = ""
    if args.contest != None:
        contest = args.contest
    if args.serverity_level != None:
        serverity_level = args.serverity_level
    if args.url != None:
        base_url = args.url

    main(contest, serverity_level, base_url)
        

    
