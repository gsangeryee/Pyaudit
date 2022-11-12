#!/usr/bin/python
# -*- coding: utf-8 -*-
from analyzer.analyzer import Analyzer

class Report(object):
    def __init__(self):
        pass

    def get_reports(self,serverity_level,rules,contest_paths,base_url):
        
        
        markdown_report_list = []
        grid_table_list = []

        # Get report from Analyzer
        report = Analyzer().analyze(serverity_level.value, rules, contest_paths)

        # Report Elements
        serverity_level = report['serverity']
        fiels_analyzed_list = report['files_analyzed']
        findings_per_rule_list = report['findings_per_rule']

        # Report Header
        markdown_report_list.append("# " + serverity_level+ " Report\n")
        markdown_report_list.append("\n")

        # Report File list
        markdown_report_list.append("## Files Analyzed\n")

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
        
        # Report Findings
        for findings_per_rule in findings_per_rule_list:
            # Rule informatioin
            rule_identifier = findings_per_rule['rule_identifier']
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

        markdown_report_list.append("".join(grid_table_list))

        return ''.join(markdown_report_list)


    def finding_details(self,finding,base_url):
        finding_details_list = []
        file_name = finding['file_name']
        line_number = finding['line_number']
        line_code = finding['line_code']

        finding_details_list.append("["+file_name+"#L"+str(line_number)+"]("+base_url+"/"+file_name+"#L"+str(line_number)+")\n")
        finding_details_list.append("```solidity\n")
        finding_details_list.append(str(line_number) + ":    ")
        finding_details_list.append(line_code + "\n")
        finding_details_list.append("```\n")
        return ''.join(finding_details_list)
