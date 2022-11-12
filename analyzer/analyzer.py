#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

class Analyzer(object):
    def __init__(self):
        pass

    def analyze(self,serverity,rules,paths):
        #print("rules:",rules)       
        report = {}
        

        report['serverity'] = serverity


        file_analyzed_list = []
        findings_per_rule_list = []
        
        for rule in rules:
            findings_per_rule_dict = {}
            
            findings_list = []
            findings_per_rule_dict['rule_identifier'] = rule['identifier']
            findings_per_rule_dict['rule_title'] = rule['title']
            findings_per_rule_dict['rule_description'] = rule['description']
            findings_per_rule_dict['rule_recommendation'] = rule['recommendation']

            for file_name, path in paths.items():
                
                file_analyzed_list.append(path)
                
                #self.analyze_file(path,rules)
            
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
            
                    pattern = rule['pattern']
                    rule_regex = re.compile(pattern)
                    findings =rule_regex.findall(code)
                    #print("Pattern:",pattern)
                    
                    if len(findings) > 0:
                        for finding in findings:
                            finding_dict = {}
                            
                            finding_dict['file_name'] = file_name
                            finding_dict['line_number'] = code_dict[finding.strip()]
                            finding_dict['line_code'] = finding.strip()
                            findings_list.append(finding_dict)
                            
                    
            findings_per_rule_dict['findings'] = findings_list
            findings_per_rule_list.append(findings_per_rule_dict)
                    
                            
        report['files_analyzed'] = file_analyzed_list 
        report['findings_per_rule'] = findings_per_rule_list
        
        return report
    


