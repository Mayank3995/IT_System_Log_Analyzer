import re

def parse_logs(file_path):
    parsed_data = []
    # Regex pattern: Matches "YYYY-MM-DD HH:MM:SS LEVEL Message"
    # Adjust this pattern if your log file format is different
    log_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(\w+)\s+(.*)')

    try:
        with open(file_path, 'r') as file:
            for line in file:
                match = log_pattern.search(line)
                if match:
                    # Extract groups: (Timestamp, Severity, Message)
                    parsed_data.append(match.groups())
    except Exception as e:
        print(f"Error reading file: {e}")

    return parsed_data