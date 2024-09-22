import re

# Make all of the links clickable
def process_file(input_file, output_file):
    # Define the regex pattern to find URLs surrounded by <p> and </p>
    pattern = re.compile(r'<p>(http[s]?://[^\s]+)</p>')

    # Read the content of the file
    with open(input_file, 'r') as file:
        content = file.read()

    # Replace <p> and </p> with HTML anchor tags
    updated_content = pattern.sub(r'<a href="\1">\1</a>', content)

    # Write the updated content back to the file
    with open(output_file, 'w') as file:
        file.write(updated_content)

# Specify your input and output file paths
input_file_path = 'intel.txt'   # Change this to your actual input file path
output_file_path = 'intel2.txt' # Change this to your desired output file path

# Call the function to process the file
process_file(input_file_path, output_file_path)








# same thing but for the first occurance




def process_file(input_file, output_file):
    # Define the regex pattern to find <p>...</p>
    pattern = re.compile(r'(<p>)(.*?)(</p>)', re.DOTALL)
    
    # Read the content of the file
    with open(input_file, 'r') as file:
        content = file.read()

    # Find all matches
    matches = pattern.findall(content)
    
    # Replace every 4th occurrence and the first occurrence
    count = 0
    def replacement(match):
        nonlocal count
        count += 1
        # Replace the first occurrence and every 4th occurrence with <h1>...</h1>
        if count == 1 or count % 4 == 0:
            return f'<h1>{match.group(2)}</h1>'
        else:
            return f'<p>{match.group(2)}</p>'

    # Replace <p>...</p> with <h1>...</h1> for the first and every 4th occurrence
    updated_content = pattern.sub(lambda m: replacement(m), content)

    # Write the updated content back to the file
    with open(output_file, 'w') as file:
        file.write(updated_content)

# Specify your input and output file paths
input_file_path = 'intel2.txt'   # Change this to your actual input file path
output_file_path = 'final.txt' # Change this to your desired output file path

# Call the function to process the file
process_file(input_file_path, output_file_path)

