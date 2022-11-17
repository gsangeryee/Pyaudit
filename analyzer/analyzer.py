#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

class Analyzer(object):
    def __init__(self):
        pass
    
    # Analyze the contest contracts
    # Return a report
    """
        Output report format:
        {
            "serverity": "GASOP",
            "files_analyzed": [
                "audit/2022-05-sturdy/smart-contracts/YieldManager.sol",
                "audit/2022-05-sturdy/smart-contracts/GeneralVault.sol",
                "audit/2022-05-sturdy/smart-contracts/LidoVault.sol",
                "audit/2022-05-sturdy/smart-contracts/YieldManager.sol",
                "audit/2022-05-sturdy/smart-contracts/GeneralVault.sol",
                "audit/2022-05-sturdy/smart-contracts/LidoVault.sol"
            ],
            "findings_per_issue": [
                {
                "issue_identifier": "[G-001]",
                "findings": [
                    {
                    "file_name": "YieldManager.sol",
                    "line_number": 63,
                    "line_code": "function setExchangeToken(address _token) external onlyAdmin {"
                    },
                    {
                    "file_name": "YieldManager.sol",
                    "line_number": 72,
                    "line_code": "function registerAsset(address _asset) external onlyAdmin {"
                    },
                    {
                    "file_name": "YieldManager.sol",
                    "line_number": 95,
                    "line_code": ") external onlyAdmin {"
                    },
                    {
                    "file_name": "YieldManager.sol",
                    "line_number": 117,
                    "line_code": "function distributeYield(uint256 _offset, uint256 _count) external onlyAdmin {"
                    },
                    {
                    "file_name": "GeneralVault.sol",
                    "line_number": 164,
                    "line_code": "function setTreasuryInfo(address _treasury, uint256 _fee) external onlyAdmin {"
                    },
                    {
                    "file_name": "LidoVault.sol",
                    "line_number": 29,
                    "line_code": "function processYield() external override onlyAdmin {"
                    }
                ]
                },
                {
                "issue_identifier": "[G-002]",
                "findings": [
                    {
                    "file_name": "YieldManager.sol",
                    "line_number": 119,
                    "line_code": "for (uint256 i = 0; i < _count; i++) {"
                    },
                    {
                    "file_name": "YieldManager.sol",
                    "line_number": 129,
                    "line_code": "for (uint256 i = 0; i < assetYields.length; i++) {"
                    },
                    {
                    "file_name": "YieldManager.sol",
                    "line_number": 155,
                    "line_code": "for (uint256 i = 0; i < length; i++) {"
                    },
                    {
                    "file_name": "GeneralVault.sol",
                    "line_number": 217,
                    "line_code": "for (uint256 i = 0; i < length; i++) {"
                    }
                ]
                }
            ]
        }
        """
        
    def analyze(self,serverity,rules,paths):
        #print("rules:",rules)   
        # Dicitonary For Report    
        report = {}

        #Add serverity level to report
        report['serverity'] = serverity
        
        file_analyzed_list = set([]) # list of files analyzed
        findings_per_rule_list = [] # list of findings per rule

    

        # Loop through all the rules
        for rule in rules:
            findings_per_rule_dict = {} 
            findings_list = []

            # Add rule information
            findings_per_rule_dict['rule_identifier'] = rule['identifier']
            findings_per_rule_dict['rule_title'] = rule['title']
            findings_per_rule_dict['rule_description'] = rule['description']
            findings_per_rule_dict['rule_recommendation'] = rule['recommendation']
            pattern_type = rule['pattern_type']
            
            # Loop through all the contract files
            for file_name, path in paths.items():
                #print("file_name:",file_name)
                
                #file_analyzed_list.append(path)
                file_analyzed_list.add(path)
                
                # create line-code dictionary
                code_dict = {} # key: line code, value: line number
                with open(path,'r') as f:
                    for line_number, line_code in enumerate(f):
                        #print("line_number:",line_number)
                        #print("line_code:",line_code)
                        # Get rid of the comments (//) in end of the code
                        # There are two ways to get rid of the comments
                        # Way 1: line_code = line_code.split('//')[0]  
                        head, sep, tail = line_code.partition('//') # Way 2
                        #print("head:",head)
                        line_code = head.strip()
                        code_dict[line_code] = line_number

                # read whole contract file
                code = ""
                with open(path, 'r') as f:
                    code = f.read()
            
                    pattern = rule['pattern']
                    rule_regex = re.compile(pattern)

                    # Using group regex model and .search() method
                    if pattern_type == "Sub":
                        #findings_by_group = rule_regex.search(code)
                        sub_pattern_string = rule['sub_pattern']
                        sub_finding_list = rule_regex.findall(code)
                        
                        if len(sub_finding_list) > 0:
                            for sub_finding in sub_finding_list:
                                #sub_pattern = '.*\(.*,[\x20]'+sub_finding+'\);|.*=[\x20]'+sub_finding+'[;|,|)].*'
                                sub_pattern = sub_pattern_string.replace('SUB_PATTERN',sub_finding)
                                #print("sub_pattern:",sub_pattern)
                                sub_rule_regex = re.compile(sub_pattern)
                                sub_findings = sub_rule_regex.findall(code)
                                #print("sub_findings:",sub_findings)
                                if len(sub_findings) > 0:
                                    for sub_find in sub_findings:
                                        #print("sub_find:",sub_find)
                                        sub_find = sub_find.strip()
                                        #print("sub_find:",sub_find)
                                        line_number = code_dict[sub_find]
                                        #print("line_number:",line_number)
                                        findings_dict = {}
                                        findings_dict['file_name'] = file_name
                                        findings_dict['line_number'] = line_number
                                        findings_dict['line_code'] = sub_find
                                        findings_list.append(findings_dict)
                                            
                    # Using normal regex and .findall() method
                    if pattern_type == "Normal":
                        findings = rule_regex.findall(code)        
                        if len(findings) > 0:
                            for finding in findings:
                                
                                finding_dict = {}
                                # Add finding information
                                finding_dict['file_name'] = file_name
                                finding_dict['line_number'] = code_dict[finding.strip()]
                                finding_dict['line_code'] = finding.strip()
                                findings_list.append(finding_dict)
                            
            # Add All findings of this rule from all files to findings_per_rule_dict     
            findings_per_rule_dict['findings'] = findings_list
            # Add a findings per rule to findings_per_rule_list
            findings_per_rule_list.append(findings_per_rule_dict)
                    
                            
        report['files_analyzed'] = file_analyzed_list 
        # Add all findings for all rule to report
        report['findings_per_rule'] = findings_per_rule_list
        
        return report
    


