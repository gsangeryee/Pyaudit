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
        { => store in report{} dirctioary
            "serverity": "GASOP",
            "files_analyzed": [ => store in file_analyzed_list set
                "audit/2022-05-sturdy/smart-contracts/YieldManager.sol",
                "audit/2022-05-sturdy/smart-contracts/GeneralVault.sol",
                "audit/2022-05-sturdy/smart-contracts/LidoVault.sol",
                "audit/2022-05-sturdy/smart-contracts/YieldManager.sol",
                "audit/2022-05-sturdy/smart-contracts/GeneralVault.sol",
                "audit/2022-05-sturdy/smart-contracts/LidoVault.sol"
            ],
            "findings_per_issue": [ => store in findings_per_rule_list list, each serverity repot has a findings_per_rule_list
                { ==> store in findings_per_rule_dict dictionary, each rule has a findings_per_rule_dict
                "issue_identifier": "[G-001]",
                "findings": [ => store in findings_list list, each rule has a findings_list
                    { => store in finding_dict dictionary, each finding has a finding_dict
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
        
        file_analyzed_list = set([]) # list of smart contests
        findings_per_rule_list = [] # list of findings per rule

        # Loop through all the rules
        for rule in rules:
            print("rule:",rule['identifier'])
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
                print("file_name index:",path[path.find(path.split('/')[2]):])
                # file name with path
                file_name = path[path.find(path.split('/')[2]):]
                file_analyzed_list.add(path)
                
                # create line-code dictionary
                code_dict = self.create_line_code_dict(path)
                
                # read whole contract file
                code = ""
                with open(path, 'r') as f:
                    code = f.read() # read whole contract file
                    pattern = rule['pattern']
                    rule_regex = re.compile(pattern)
                                            
                    # Using normal regex and .findall() method
                    if pattern_type == "Normal":
                        
                        findings = rule_regex.findall(code)        
                        if len(findings) > 0:                            
                            for finding in findings:
                                finding_dict={} # dictionary for finding, initialize must in the loop
                                finding_dict = self.add_finding_item(finding,code_dict,file_name)
                                findings_list.append(finding_dict)
                                
                    # Using regex with group and .findall() method
                    if pattern_type == "Group":
                        #result = re.search(r"(if.*revert..*;)", code)
                        findings = rule_regex.findall(code)
                        
                        if len(findings) > 0:
                            findings = set(findings) # remove duplicate findings
                            for finding in findings:
                                finding_dict={}
                                finding_dict = self.add_finding_item(finding,code_dict,file_name)
                                findings_list.append(finding_dict)
                            
                    # Using Multi-lines matching regex and .findall() method
                    if pattern_type == "Multi":
                        
                        findings = rule_regex.findall(code)
                        if len(findings) > 0:
                            for finding in findings:
                                finding_dict={} # dictionary for finding, initialize must in the loop
                                # One Line
                                if len(finding.splitlines()) == 1:
                                    finding_dict = self.add_finding_item(finding,code_dict,file_name)
                                    findings_list.append(finding_dict)
                                    
                                # Multiple Lines
                                if len(finding.splitlines()) > 1:
                                    # Cause some cases, the first line is only require keyword, so we need to skip it 
                                    second_line = finding.splitlines(False)[1]
                                    back_number = 1
                                    # skip the seconde line if it is a blank line
                                    if second_line.strip() == "":
                                        second_line = finding.splitlines(False)[2] # Get the third line
                                        back_number = 2
                                        # skip the third line,using the fourth line  if it is a comment line
                                        if second_line.strip().find('//') == 0:
                                            second_line = finding.splitlines(False)[3]
                                            back_number = 3
                                    else:
                                        # skip the seconde line,using the third line  if it is a comment line
                                        if second_line.strip().find('//') == 0:
                                            second_line = finding.splitlines(False)[2]
                                            back_number = 2

                                    head, sep, tail = second_line.partition('//')
                                    second_line = head.strip()
                                    second_line_number = code_dict[second_line]
                                    first_line_number = second_line_number - back_number
                                    
                                    finding_dict['file_name'] = file_name
                                    # Line number for Multi-lines
                                    finding_dict['line_number'] = str(first_line_number)+"-"+str(first_line_number+len(finding.splitlines(False))-1)
                                    #print("finding_dict['line_number']:",str(first_line_number)+"-"+str(first_line_number+len(finding.splitlines(False))-1))
                                    finding_dict['line_code'] = finding
                                    #print("finding_dict['line_code']:",finding)
                                    findings_list.append(finding_dict) 
                                    

                    # Using two steps regex
                    # 1. Using regex to Step One find.
                    # 2. Extract keywords from the matching results according to the rules of the sub_pattern's key.
                    # 3. Replace the keywords with the pattern of the sub_pattern to form a second matching regular expression.
                    # 4. Use the second matching regular expression for second matching.
                    # 5. According to the rules of the sub_pattern's type, process the results of the second matching.
                    #    5.1 If type is One, it means that the keyword only appears once in the second matching, such as the function is not called.
                    #    5.2 If type is Two, it means that the keyword appears twice in the second matching, such as the function is only called once.
                    if pattern_type == "Sub":
                        #findings_by_group = rule_regex.search(code)
                        sub_pattern_dict = rule['sub_pattern']
                        sub_pattern_string = sub_pattern_dict['pattern']
                        sub_pattern_key = sub_pattern_dict['key']
                        sub_pattern_type = sub_pattern_dict['type']
                        
                        sub_finding_list = rule_regex.findall(code)
                        
                        if len(sub_finding_list) > 0:
                            for sub_finding in sub_finding_list:
                                
                                #sub_pattern = '.*\(.*,[\x20]'+sub_finding+'\);|.*=[\x20]'+sub_finding+'[;|,|)].*'
                                #sub_finding = sub_finding.replace('(','\(')
                                #sub_finding = sub_finding.replace(')','\)')
                                if len(sub_pattern_key) > 0:
                                    sub_key = sub_finding[int(sub_pattern_key[0]):sub_finding.find(sub_pattern_key[1])]
                                    
                                else:
                                    sub_key = sub_finding
                                    sub_key = sub_finding.replace('(','\(')
                                    sub_key = sub_finding.replace(')','\)')
                                
                                sub_pattern = sub_pattern_string.replace('SUB_PATTERN',sub_key)
                                print("sub_pattern:",sub_pattern)
                                sub_rule_regex = re.compile(sub_pattern)
                                sub_findings = sub_rule_regex.findall(code)
                                
                                
                                if sub_pattern_type == "One":
                                    if len(sub_findings) == 1:
                                        sub_finding_dict = {}
                                        sub_finding_dict = self.add_finding_item(sub_finding,code_dict,file_name)
                                        findings_list.append(sub_finding_dict)

                                if sub_pattern_type == "Two":
                                    if len(sub_findings) == 2:
                                        sub_finding_dict = {}
                                        sub_finding_dict = self.add_finding_item(sub_finding,code_dict,file_name)
                                        findings_list.append(sub_finding_dict)

                                """
                                if len(sub_findings) > 0:
                                    # remove duplicate findings
                                    sub_findings = set(sub_findings)
                                
                                    for sub_find in sub_findings:
                                        sub_finding_dict = {} # dictionary for finding, initialize must in the loop
                                        sub_finding_dict = self.add_finding_item(sub_find,code_dict,file_name)
                                        findings_list.append(sub_finding_dict)
                                """       
                                               
                  
            # Add All findings of this rule from all files to findings_per_rule_dict     
            findings_per_rule_dict['findings'] = findings_list
            # Add a findings per rule to findings_per_rule_list
            findings_per_rule_list.append(findings_per_rule_dict)
                    
        # End of for loop for all rules
                         
        report['files_analyzed'] = file_analyzed_list 
        # Add all findings for all rule to report
        report['findings_per_rule'] = findings_per_rule_list
        #print("report:",report)
        
        return report
    
    def add_finding_item(self,finding,code_dict,file_name):
        _findying_dict = {}
        head, sep, tail = finding.partition('//')
        finding = head.strip()
        line_number = code_dict[finding]
        # Add finding information
        _findying_dict['file_name'] = file_name
        _findying_dict['line_number'] = str(line_number)
        _findying_dict['line_code'] = finding
        return _findying_dict
    
    def create_line_code_dict(self,path):
        _code_dict = {}
        with open(path, 'r') as f:
            for line_number, line_code in enumerate(f):
                #print("line_number:",line_number)
                #print("line_code:",line_code)
                head, sep, tail = line_code.partition('//')
                line_code = head.strip()
                _code_dict[line_code] = line_number+1
        return _code_dict

