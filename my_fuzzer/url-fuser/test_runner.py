import os
import requests
import json

# Configuration
DIRECTORY_PATH = '/home/youssef/github/wttr.in/my_fuzzer/url-fuser/test-cases' 
MD_OUTPUT_FILE = 'test_results.md'

def test_backend_urls(directory_path):
    results_list = [] # List to store all our test results
    
    if not os.path.exists(directory_path):
        print(f"Error: The directory '{directory_path}' does not exist.")
        return results_list

    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            
            with open(file_path, 'r') as file:
                url = file.read().strip() 
            
            if not url:
                print(f"[{filename}] is empty. Skipping...")
                continue
            
            # Create a dictionary to store the result for this specific file
            test_data = {
                "filename": filename,
                "url": url,
                "status": "",
                "status_code": None,
                "error_message": None
            }

            print(f"Testing: {url}")
            try:
                response = requests.get(url, timeout=10) 
                test_data["status_code"] = response.status_code
                
                if response.status_code == 200:
                    test_data["status"] = "SUCCESS"
                else:
                    test_data["status"] = "WARNING"
                    
            except requests.exceptions.Timeout:
                test_data["status"] = "ERROR"
                test_data["error_message"] = "Request timed out"
            except requests.exceptions.ConnectionError:
                test_data["status"] = "ERROR"
                test_data["error_message"] = "Failed to connect"
            except requests.exceptions.RequestException as e:
                test_data["status"] = "ERROR"
                test_data["error_message"] = str(e)
            
            # Add the dictionary to our master list
            results_list.append(test_data)

    return results_list


def save_to_markdown(data, output_filepath):
    """Exports the results to a Markdown file formatted as a table."""
    with open(output_filepath, 'w') as md_file:
        md_file.write("# Backend API Test Results\n\n")
        # Write Table Headers
        md_file.write("| Filename | URL | Status | Status Code | Error Message |\n")
        md_file.write("|----------|-----|--------|-------------|---------------|\n")
        
        # Write Table Rows
        for item in data:
            # Replace None with empty strings or 'N/A' for cleaner markdown
            code = item['status_code'] if item['status_code'] else "N/A"
            error = item['error_message'] if item['error_message'] else "-"
            
            md_file.write(f"| {item['filename']} | {item['url']} | {item['status']} | {code} | {error} |\n")
            
    print(f"✅ Markdown results successfully saved to: {output_filepath}")

if __name__ == "__main__":
    # 1. Run the tests and gather data
    test_results = test_backend_urls(DIRECTORY_PATH)
    
    # 2. Export the data if we have any results
    if test_results:
        print("\n--- Exporting Results ---")
        
        # You can keep both, or comment out the one you don't need:
        save_to_markdown(test_results, MD_OUTPUT_FILE)