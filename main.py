import re

def format_contents(path):
    with open(path, "r") as file:
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

        return "\t".join(result)