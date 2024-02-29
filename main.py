import re
import os
import datetime

def format_contents(input_path):
    with open(input_path, "r") as file:
        start = "begin"
        end = "end"
        data = file.read()

        start_index = 0
        last_end_pos = 0
        result = []
        while start_index < len(data):
            start_pos = data.find(start, start_index)
            if start_pos == -1:
                section = data[last_end_pos:].strip()
                section = re.sub(r'(\d{4,})(\.\d+)?', lambda m: re.sub(r'(\d{3})', r'\1\:', m.group(0)), section)
                section = re.sub(r'(\d),', r'\1\:', section)
                result.append(section)
                break
            end_pos = data.find(end, start_pos)
            if end_pos == -1:
                section = data[last_end_pos:start_pos].strip()
                section = re.sub(r'(\d{4,})(\.\d+)?', lambda m: re.sub(r'(\d{3})', r'\1\:', m.group(0)), section)
                section = re.sub(r'(\d),', r'\1\:', section)
                result.append(section)
                break

            result.append(data[last_end_pos:start_pos].strip())
            result.append(data[start_pos + len(start): end_pos])

            start_index = end_pos + len(end)
            last_end_pos = start_index

        output = "\t".join(result)

        dir_path = os.path.dirname(os.path.dirname(input_path))

        out_dir = os.path.join(dir_path, 'out')
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        filename = os.path.basename(input_path)

        output_path = os.path.join(out_dir, f'_{filename}_{current_time}.txt')

        with open(output_path, 'w') as output_file:
            output_file.write(output)

if __name__ == "__main__":
    parent_dir = os.path.dirname(os.path.abspath(__file__))

    src_dir = os.path.join(parent_dir, "src")

    count = 0
    for filename in os.listdir(src_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(src_dir, filename)
            format_contents(file_path)
            count += 1
            
    print(f"Formatted {count} files")