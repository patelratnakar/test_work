import subprocess
import re

# Get the previous commit hash
prev_commit = subprocess.check_output(["git", "rev-parse", "HEAD~1"]).decode("utf-8").strip()

# Get the current commit hash
curr_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()

# Get the diff between the previous and current commits
diff = subprocess.check_output(["git", "diff", "--name-status", prev_commit, curr_commit]).decode("utf-8").splitlines()

# Initialize dictionaries to store the changes
added_data_sources = {}
added_workbooks = {}
modified_data_sources = {}
modified_workbooks = {}
deleted_data_sources = {}
deleted_workbooks = {}

# Iterate through the diff and filter the changes
for line in diff:
    status, path = line.split("\t")
    if re.match(r"data sources/.+\.tds$", path):
        if status == "A":
            added_data_sources[path] = True
        elif status == "M":
            modified_data_sources[path] = True
        elif status == "D":
            deleted_data_sources[path] = True
    elif re.match(r"workbooks/.+\.twb$", path):
        if status == "A":
            added_workbooks[path] = True
        elif status == "M":
            modified_workbooks[path] = True
        elif status == "D":
            deleted_workbooks[path] = True

# Print the changes
print("Added Data Sources:")
for path in added_data_sources:
    print(f"  - {path}")

print("\nAdded Workbooks:")
for path in added_workbooks:
    print(f"  - {path}")

print("\nModified Data Sources:")
for path in modified_data_sources:
    print(f"  - {path}")

print("\nModified Workbooks:")
for path in modified_workbooks:
    print(f"  - {path}")

print("\nDeleted Data Sources:")
for path in deleted_data_sources:
    print(f"  - {path}")

print("\nDeleted Workbooks:")
for path in deleted_workbooks:
    print(f"  - {path}")