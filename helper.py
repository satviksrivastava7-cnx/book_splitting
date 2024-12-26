import os
import json
import sys

def log_message(message):
    print(message)
    sys.stdout.flush()

def convert_txt_to_json(txt_file_path, output_dir, log_message, root):
    with open(txt_file_path, 'r') as txt_file:
        lines = txt_file.readlines()

    content = lines[1:-1]
    content_str = ''.join(content)

    try:
        json_content = json.loads(content_str)
    except json.JSONDecodeError as e:
        log_message(f"Error decoding JSON in {txt_file_path}: {e}")
        root.update()
        return

    json_file_path = os.path.join(output_dir, os.path.splitext(os.path.basename(txt_file_path))[0] + '.json')

    with open(json_file_path, 'w') as json_file:
        json.dump(json_content, json_file, indent=4)

    log_message(f"Converted TXT to JSON: {txt_file_path} -> {json_file_path}")
    root.update()
    
def process_txt_files(input_dir, output_dir, log_message, root):
    os.makedirs(output_dir, exist_ok=True)
    txt_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]

    log_message(f"Found {len(txt_files)} TXT files to process in {input_dir}")
    root.update()

    for txt_file in txt_files:
        txt_file_path = os.path.join(input_dir, txt_file)
        log_message(f"Processing: {txt_file}")
        root.update()
        convert_txt_to_json(txt_file_path, output_dir, log_message, root)

