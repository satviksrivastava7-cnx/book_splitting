import os
import json

def create_syllabus_json(board, class_name, book_name, output_dir, parsed_json_dir, log_message):
    try:
        for subject_folder in os.listdir(output_dir):
            subject_output_path = os.path.join(output_dir, subject_folder)

            if os.path.isdir(subject_output_path):
                subject_json_path = os.path.join(parsed_json_dir, f"{subject_folder}.json")
                
                if not os.path.exists(subject_json_path):
                    if log_message:
                        log_message(f"Subject-specific JSON for {subject_folder} not found in {subject_json_path}.")
                    continue

                with open(subject_json_path, 'r') as f:
                    subject_data = json.load(f)

                syllabus = {
                    "board": board,
                    "class": class_name,
                    "subject": subject_folder,
                    "book_name": book_name,
                    "topics": []
                }

                for chapter in subject_data:
                    topic = {
                        "title": chapter["chapter_title"],
                        "topics": [{"name": subtopic} for subtopic in chapter["chapter_topics_list"]]
                    }
                    syllabus["topics"].append(topic)

                syllabus_json_path = os.path.join(subject_output_path, "syllabus.json")
                with open(syllabus_json_path, 'w') as f:
                    json.dump([syllabus], f, indent=4)

                if log_message:
                    log_message(f"Syllabus JSON created for subject: {subject_folder} at {syllabus_json_path}")

    except Exception as e:
        if log_message:
            log_message(f"Error in create_syllabus_json: {str(e)}")
        else:
            print(f"Error in create_syllabus_json: {str(e)}")
