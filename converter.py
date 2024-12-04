import json

def parse_m3u(file_path):
    """
    Parse an M3U file and extract details into a dictionary.
    
    Args:
        file_path (str): Path to the M3U file.
    
    Returns:
        list: A list of dictionaries containing the extracted information.
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        current_entry = {}

        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Metadata line (starts with #EXTINF)
            if line.startswith('#EXTINF:'):
                # Parse the metadata
                try:
                    duration, title = line[8:].split(',', 1)
                    current_entry['duration'] = int(duration)
                    current_entry['title'] = title
                except ValueError:
                    # If split fails, just record the entire line
                    current_entry['info'] = line[8:]
            
            # URL line
            elif line.startswith('http') or line.startswith('https'):
                current_entry['url'] = line
                data.append(current_entry)
                current_entry = {}
    
    return data

def save_to_json(data, output_path):
    """
    Save extracted data to a JSON file.
    
    Args:
        data (list): Extracted data from the M3U file.
        output_path (str): Path to save the JSON file.
    """
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == '__main__':
    # Path to the M3U file
    m3u_file_path = '/Users/mohitbendale/Desktop/M3u to Json/tv_channels_shannon98_plus.m3u'  # Replace with your M3U file path
    output_json_path = 'playlist.json'

    # Parse the M3U file
    extracted_data = parse_m3u(m3u_file_path)
    print(f"Extracted Data: {extracted_data}")
    
    # Save the extracted data as JSON
    save_to_json(extracted_data, output_json_path)
    print(f"Data has been saved to {output_json_path}")
