import requests
import json

def generate_result(data_dir, results_dir):
    """
    Generate the result of the sample html files
    
    Args:
    data_dir (str): The directory containing the sample html files
    results_dir (str): The directory to save the result json files
    """
    for i in range(1, 4):
        with open(f"{data_dir}/sample_{i}.html", "r") as file:
            raw_html = file.read()
        
        response = requests.post("http://localhost:8000/extract-attributes-and-selectors/", headers={"Content-Type": "text/html"}, data=raw_html.encode('utf-8'))

        with open(f"{results_dir}/sample_{i}_result.json", "w") as file:
            file.write(json.dumps(response.json(), indent=4))

if __name__ == "__main__":
    data_dir = "data"
    results_dir = "results"
    generate_result(data_dir, results_dir)