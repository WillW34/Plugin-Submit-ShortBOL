import requests
import urllib


eval_url = "http://127.0.0.1:8080/evaluate"
run_url = "http://127.0.0.1:8080/run"
succeed_url = "http://127.0.0.1:5000/public/plugintest.txt"
manifest = """{"manifest": 
                {"files": 
                [{"url": "http://localhost:5000/public/Test.dna", "filename": "Test.dna", "type": "application/vnd.dna"}, 
                {"url": "http://localhost:5000/public/plugintest.txt", "filename": "plugintest.txt", "type": "text/plain"}, 
                {"url": "http://localhost:5000/public/darpa_template.xlsx", "filename": "darpa_template.xlsx", "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}]}}"""

#data should be returned from http://127.0.0.1:5000/public/plugintest.txt
run_data = requests.post(succeed_url)


def test():
    eval_response = requests.post(eval_url,data=manifest)
    run_response = requests.post(run_url, data=run_data)
    print(eval_response.text)
    print(run_response.text)


if __name__ == "__main__":test()