#!/usr/bin/python
# -*- coding: utf-8 -*-
from analyzer.analyzer import Analyzer
import datetime

class Report(object):
    def __init__(self):
        pass

    def get_reports(self,serverity_level,rules,contest_paths,base_url):
        
        
        markdown_report_list = []
        grid_table_list = []

        # Get report from Analyzer
        report = Analyzer().analyze(serverity_level, rules, contest_paths)

        # Report Elements
        serverity_level = report['serverity']
        fiels_analyzed_list = report['files_analyzed']
        findings_per_rule_list = report['findings_per_rule']

        # Report Header
        if serverity_level == "GASOP":
            report_title = "Gas Optimizations"
        elif serverity_level == "LOW_NC":
            report_title = "Low Severity and Non Critical Issues"
        elif serverity_level == "HIGH":
            report_title = "High Risk Findings"
        elif serverity_level == "MEDIUM":
            report_title = "Medium Risk Findings"
        markdown_report_list.append("# " + report_title+ " Report\n")
        markdown_report_list.append("\n")
        
        # Add Report datetime from os system

        now = datetime.datetime.now()
        markdown_report_list.append("Report Date: " + now.strftime("%Y-%m-%d %H:%M:%S") + "\n")

        # Report File list
        markdown_report_list.append("## Files Analyzed\n")
        # print length of fiels_analyzed_list
        
        for file in fiels_analyzed_list:
            # file[6:] is to remove the "audit/" folder from the path
            markdown_report_list.append("- " + file[6:] + "\n")

        markdown_report_list.append("\n")
        markdown_report_list.append("Total:"+ str(len(fiels_analyzed_list)) + "\n")
        markdown_report_list.append("\n")

        # Report Grid Table For low_nc And gasop
        if serverity_level == "LOW_NC" or serverity_level == "GASOP":
            grid_table_list.append("| |Issue|Instances|\n")
            grid_table_list.append("|-|:-|:-:|\n")
            grid_table_list.append("|[G-XXX]| Optimize names to save gas|xxx|\n")
        
        # Report Findings
        for findings_per_rule in findings_per_rule_list:
            # Rule informatioin
            rule_identifier = findings_per_rule['rule_identifier']
            #print("Report rule_identifier: " + rule_identifier)
            rule_title = findings_per_rule['rule_title']
            rule_description = findings_per_rule['rule_description']
            rule_recommendation = findings_per_rule['rule_recommendation']
            
            findings_list = findings_per_rule['findings']
            if len(findings_list) == 0:
                continue
            markdown_report_list.append("## " + rule_identifier + " " + rule_title + "\n")
            markdown_report_list.append("\n")

            # Report Grid Table For low_nc And gasop
            if serverity_level == "LOW_NC" or serverity_level == "GASOP":
                grid_table_list.append("|")
                grid_table_list.append(rule_identifier)
                grid_table_list.append("|")
                grid_table_list.append(rule_title)
                grid_table_list.append("|")
                grid_table_list.append(str(len(findings_list)))
                grid_table_list.append("|\n")
            
            # Impact
            markdown_report_list.append("### Impact\n")
            markdown_report_list.append(rule_description + "\n")
            markdown_report_list.append("\n")

            # Findings
            markdown_report_list.append("### Findings\n")
            markdown_report_list.append("Total:" + str(len(findings_list)) + "\n")
            markdown_report_list.append("\n")
            for finding in findings_list:
                markdown_report_list.append(self.finding_details(finding,base_url))
            markdown_report_list.append("\n")

            # Recommendation
            markdown_report_list.append("### Recommendation\n")
            markdown_report_list.append(rule_recommendation + "\n")
            markdown_report_list.append("\n")
        
        # Add Normal Findings
        if serverity_level == "GASOP":
            rule_identifier = "[G-XXX]"
            #print("Report rule_identifier: " + rule_identifier)
            rule_title = "Optimize names to save gas"
            rule_description = "public/external function names and public member variable names can be optimized to save gas. See [this](https://gist.github.com/IllIllI000/a5d8b486a8259f9f77891a919febd1a9) link for an example of how it works. Below are the interfaces/abstract contracts that can be optimized so that the most frequently-called functions use the least amount of gas possible during method lookup. Method IDs that have two leading zero bytes can save 128 gas each during deployment, and renaming functions to have lower method IDs will save 22 gas per call, [per sorted position shifted](). (检查常用 public/external 的公共成员变量和公共函数如get，set它们的Method ID顺序是否从小到大排列，特别是在积累中定义的get，set方法，如果子类应用父类的get/set没有按 Method ID 排序，也可以优化。只需列出合约和方法名。参考signature_extractory.md 和 [https://github.com/code-423n4/2022-12-gogopool-findings/blob/main/data/NoamYakov-G.md#g06--optimize-names-to-save-gas](https://github.com/code-423n4/2022-12-gogopool-findings/blob/main/data/NoamYakov-G.md#g06--optimize-names-to-save-gas) "
            rule_recommendation = ""
            markdown_report_list.append("## " + rule_identifier + " " + rule_title + "\n")
            markdown_report_list.append("\n")
            markdown_report_list.append("### Impact\n")
            markdown_report_list.append(rule_description + "\n")
            markdown_report_list.append("\n")

        markdown_report_list.append("".join(grid_table_list))
        
        return ''.join(markdown_report_list)


    def finding_details(self,finding,base_url):
        #print("finding:",finding)
        finding_details_list = []
        file_name = finding['file_name']
        line_number = finding['line_number']
        # if line_number is a range, replace the "-" with "-L"
        line_number = line_number.replace("-","-L")
        line_code = finding['line_code']
        
        finding_details_list.append("["+file_name+"#L"+str(line_number)+"]("+base_url+"/"+file_name+"#L"+str(line_number)+")\n")
        finding_details_list.append("```solidity\n")
        multi_line = line_code.splitlines(False)
        # Multi line code
        if len(multi_line) > 1:
            #print("multi_line:",multi_line)
            head, sep, tail = line_number.partition('-')
            #print("head:",head)
            start_line_number = int(head)
            for line in multi_line:
                finding_details_list.append(str(start_line_number) + ":    ")
                finding_details_list.append(line + "\n")
                start_line_number = start_line_number + 1
        else:
            finding_details_list.append(str(line_number) + ":    ")
            finding_details_list.append(line_code + "\n")

        finding_details_list.append("```\n")
        return ''.join(finding_details_list)
