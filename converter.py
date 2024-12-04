import json
import requests

def parse_m3u(file_content):
    """
    Parse an M3U content string and extract details into a dictionary.

    Args:
        file_content (str): Content of the M3U file.

    Returns:
        list: A list of dictionaries containing the extracted information.
    """
    data = []
    lines = file_content.splitlines()
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
    print("hi")
    # URL of the M3U file
    m3u_file_url = input("http://starshare.org:8080/get.php?username=varun98&password=9876&type=m3u_plus&output=ts").strip()
    output_json_path = 'playlist.json'

    try:
        # Download the M3U file
        print("Downloading the M3U file...")
        response = requests.get(m3u_file_url)
        response.raise_for_status()

        # Parse the M3U content
        file_content = response.text
        extracted_data = parse_m3u(file_content)
        print(f"Extracted Data: {extracted_data}")

        # Save the extracted data as JSON
        save_to_json(extracted_data, output_json_path)
        print(f"Data has been saved to {output_json_path}")
    except requests.RequestException as e:
        print(f"Error downloading the file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
