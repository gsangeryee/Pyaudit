#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

class Analyzer(object):
    def __init__(self):
        pass

    def analyze(self,rules,paths):
        #print("rules:",rules)        
        
        for file_name, path in paths.items():
            #self.analyze_file(path,rules)
            print("file_name:",file_name)
            # create line-code dictionary
            code_dict = {} # key: line code, value: line number
            with open(path,'r') as f:
                for line_number, line_code in enumerate(f):
                    line_code = line_code.strip()
                    code_dict[line_code] = line_number
                    
            
            # read whole contract file
            code = ""
            with open(path, 'r') as f:
                code = f.read()
                for rule in rules:
                    #print(rule)
                    #print(rule['pattern'])
                    pattern = rule['pattern']
                    rule_regex = re.compile(pattern)
                    findings =rule_regex.findall(code)
                    
                    if len(findings) > 0:
                        for finding in findings:
                            print(finding.strip())
                            print(code_dict[finding.strip()])
            

        pass
    


