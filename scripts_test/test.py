import subprocess
import re

# Define patterns to identify data sources and workbooks
data_source_pattern = re.compile(r'.*\.datasource$')
workbook_pattern = re.compile(r'.*\.workbook$')

# Function to run git command and get output
def run_git_command(args):
    result = subprocess.run(['git'] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"Git command failed: {result.stderr}")
    return result.stdout

# Function to parse git diff output
def parse_git_diff(diff_output):
    added = {'datasource': [], 'workbook': []}
    modified = {'datasource': [], 'workbook': []}
    deleted = {'datasource': [], 'workbook': []}

    lines = diff_output.split('\n')
    for line in lines:
        if line.startswith('A\t'):
            filepath = line[2:]
            if data_source_pattern.match(filepath):
                added['datasource'].append(filepath)
            elif workbook_pattern.match(filepath):
                added['workbook'].append(filepath)
        elif line.startswith('M\t'):
            filepath = line[2:]
            if data_source_pattern.match(filepath):
                modified['datasource'].append(filepath)
            elif workbook_pattern.match(filepath):
                modified['workbook'].append(filepath)
        elif line.startswith('D\t'):
            filepath = line[2:]
            if data_source_pattern.match(filepath):
                deleted['datasource'].append(filepath)
            elif workbook_pattern.match(filepath):
                deleted['workbook'].append(filepath)

    return added, modified, deleted

# Get the changes from the previous commit
diff_output = run_git_command(['diff', '--name-status', 'HEAD~1'])

# Parse the diff output
added, modified, deleted = parse_git_diff(diff_output)

# Output the results
print("Added Data Sources:", added['datasource'])
print("Added Workbooks:", added['workbook'])
print("Modified Data Sources:", modified['datasource'])
print("Modified Workbooks:", modified['workbook'])
print("Deleted Data Sources:", deleted['datasource'])
print("Deleted Workbooks:", deleted['workbook'])
