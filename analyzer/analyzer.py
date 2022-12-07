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
                # scode_dict = self.create_line_code_dict(path)
                
                # read whole contract file
                code = ""
                with open(path, 'r') as f:
                    code = f.read() # read whole contract file
                    pattern = rule['pattern']
                    print("pattern:",pattern)
                    rule_regex = re.compile(pattern)
                                            
                    # Using normal regex and .findall() method
                    if pattern_type == "Normal":
                        
                        findings = rule_regex.findall(code)
        
                        if len(findings) > 0:    
                            # remove empty space front and back in findings
                            findings = [finding.strip() for finding in findings]
                            findings = set(findings) # remove duplicate findings  
             
                            for finding in findings:
                                finding_dict_list=[] # dictionary for finding, initialize must in the loop
                                finding_dict_list = self.add_finding_item(finding,file_name,path)
                                #print("finding_dict_list:",finding_dict_list)
                                #findings_list.append(finding_dict)
                                findings_list.extend(finding_dict_list)
                            # remove duplicate findings
                            #findings_list = [dict(t) for t in {tuple(d.items()) for d in findings_list}]
                                
                                
                    # Using regex with group and .findall() method
                    if pattern_type == "Group":
                        #result = re.search(r"(if.*revert..*;)", code)
                        findings = rule_regex.findall(code)
                        
                        if len(findings) > 0:
                            findings = [finding.strip() for finding in findings]
                            findings = set(findings) # remove duplicate findings
                            for finding in findings:
                                finding_dict_list=[]
                                finding_dict = self.add_finding_item(finding,file_name,path)
                                #findings_list.append(finding_dict)
                                findings_list.extend(finding_dict_list)
                            
                    # Using Multi-lines matching regex and .findall() method
                    if pattern_type == "Multi":
                        
                        findings = rule_regex.findall(code)
                        #print("Multi findings:",findings)
                        if len(findings) > 0:
                            # remove empty space front and back in findings
                            findings = [finding.strip() for finding in findings]
                            findings = set(findings) # remove duplicate findings
                            for finding in findings:
                                finding_dict_list=[] # dictionary for finding, initialize must in the loop
                                # One Line
                                #print("Multi splitliens length:",len(finding.splitlines()))
                                if len(finding.splitlines()) == 1:
                                    finding_dict_list = self.add_finding_item(finding,file_name,path)
                                    #findings_list.append(finding_dict)
                                    findings_list.extend(finding_dict_list)
                                    
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
                                    
                                    contract_file = open(path, 'r')
                                    second_line_number_list = []
                                    for m_line_number, m_line in enumerate(contract_file):
                                        m_head, m_sep, m_tail = m_line.partition('//')
                                        if m_head.strip() == second_line:
                                            second_line_number_list.append(m_line_number+1)
                                    contract_file.close()
                                    
                                    for second_line_number in second_line_number_list:
                                        finding_dict = {}
                                        first_line_number = second_line_number - back_number
                                    
                                        finding_dict['file_name'] = file_name
                                        # Line number for Multi-lines
                                        finding_dict['line_number'] = str(first_line_number)+"-"+str(first_line_number+len(finding.splitlines(False))-1)
                                    #print("finding_dict['line_number']:",str(first_line_number)+"-"+str(first_line_number+len(finding.splitlines(False))-1))
                                        finding_dict['line_code'] = finding
                                    #print("finding_dict['line_code']:",finding)
                                        findings_list.append(finding_dict)
                                    #print("findings_list:",findings_list)
                                    
                                    

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
                            # remove empty space front and back in findings
                            sub_finding_list = [sub_finding.strip() for sub_finding in sub_finding_list]
                            # remove duplicate findings
                            sub_finding_list = set(sub_finding_list)
                            #print("sub_finding_list:",sub_finding_list)
                            for sub_finding in sub_finding_list:
                                #print("sub_finding:",sub_finding)
                                #print("sub_pattern_key:",len(sub_pattern_key))
                                
                                #sub_pattern = '.*\(.*,[\x20]'+sub_finding+'\);|.*=[\x20]'+sub_finding+'[;|,|)].*'
                                #sub_finding = sub_finding.replace('(','\(')
                                #sub_finding = sub_finding.replace(')','\)')
                                if len(sub_pattern_key) > 0:
                                    sub_key = sub_finding[int(sub_pattern_key[0]):sub_finding.find(sub_pattern_key[1])]
                                    
                                else:
                                    sub_key = sub_finding
                                    sub_key = sub_finding.replace('(','\(')
                                    sub_key = sub_finding.replace(')','\)')
                                #print("Before sub_pattern:",sub_pattern_string)
                                #print("sub_key:",sub_key)
                                sub_pattern = sub_pattern_string.replace('SUB_PATTERN',sub_key)
                                print("sub_pattern:",sub_pattern)
                                sub_rule_regex = re.compile(sub_pattern)
                                sub_findings = sub_rule_regex.findall(code)
                                
                                if sub_pattern_type == "One":
                                    if len(sub_findings) == 1:
                                        sub_finding_dict_list = []
                                        sub_finding_dict_list = self.add_finding_item(sub_finding,file_name,path)
                                        # findings_list.append(sub_finding_dict)
                                        findings_list.extend(sub_finding_dict_list)

                                if sub_pattern_type == "Two":
                                    if len(sub_findings) == 2:
                                        sub_finding_dict_list = []
                                        sub_finding_dict_list = self.add_finding_item(sub_finding,file_name,path)
                                        #findings_list.append(sub_finding_dict)
                                        findings_list.extend(sub_finding_dict_list)
                                
                                if sub_pattern_type == "Sub_Normal":
                                    if len(sub_findings) > 0:
                                        for sub_find in sub_findings:
                                            sub_finding_dict_list = [] # dictionary for finding, initialize must in the loop
                                            sub_finding_dict_list = self.add_finding_item(sub_find,file_name,path)
                                            #findings_list.append(sub_finding_dict) 
                                            findings_list.extend(sub_finding_dict_list)
                                    

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
    
    def add_finding_item(self,finding,file_name,path):
        _findying_dict_list = []
        
        #print("In add_finding_item:",finding)
        head, sep, tail = finding.partition('//')
        #print("head:",head)
        finding = head.strip()
        #line_number = code_dict[finding]
        line_numbers = self.get_code_line_numbers(path,finding)
        # print("line_numbers:",line_numbers)
        for line_number in line_numbers:
            _findying_dict = {}
            # Add finding information
            _findying_dict['file_name'] = file_name
            _findying_dict['line_number'] = str(line_number)
            _findying_dict['line_code'] = finding
            _findying_dict_list.append(_findying_dict)

        return _findying_dict_list

    def get_code_line_numbers(self,path,finding):
        #print("In get_code_line_numbers:",path)
        line_numbers = []
        contract_file = open(path, 'r')
        for line_number, line in enumerate(contract_file):
            #print("line_number:",line_number)
            #print("finding:",finding)
            head, sep, tail = line.partition('//')
            #print("linecod:",head.strip())
            if finding == head.strip():
                #print("finding_line_number:",line_number)
                line_numbers.append(line_number+1)
        contract_file.close()

        return line_numbers

