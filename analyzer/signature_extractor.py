#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
from web3 import Web3



def keccak256(text):
    keccak_hash = Web3.keccak(text=text)
    return keccak_hash

def get_function_signature(function_signature):
    keccak_hash = Web3.keccak(text=function_signature).hex()
    return keccak_hash[:8]

def read_sol_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def get_function_names(file_content):
    function_regex = r'function\s+(([^\s]+)\s*\([^()]*\))\s+(public|external|internal|private)'
    matches = re.findall(function_regex, file_content)
    return [match[0] for match in matches]

def generate_markdown(functions):
    markdown = "| Function Signature | Function Name |\n|--------------------|---------------|\n"
    for function in functions:
        
        function_signature = get_function_signature(function)
        markdown += f"| {function_signature} | {function} |\n"
    return markdown

def save_markdown(file_name, markdown_content):
    with open(file_name, 'w') as file:
        file.write(markdown_content)

def generate_signature_md(sol_file_path):
    # Get contest name from the sol file path, e.g. 'audit/contest_name/contract.sol'
    contest_name = sol_file_path.split(os.sep)[1]+"_report"
    # Contest report folder path e.g. 'audit/contest_name_report'
    contest_report_folder_path = os.path.join('audit', contest_name)
    # Check if the contest report folder exists, if not, create it
    if not os.path.exists(contest_report_folder_path):
        os.makedirs(contest_report_folder_path)

    file_content = read_sol_file(sol_file_path)
    function_names = get_function_names(file_content)
    markdown_content = generate_markdown(function_names)
    
    sol_file_name = Path(sol_file_path).stem
    markdown_file_name = f"{sol_file_name}_signature_extractory.md"
    
    # output markdonw file to contest report folder
    output_path = os.path.join(contest_report_folder_path, markdown_file_name)
    save_markdown(output_path, markdown_content)

    return output_path