import requests
import urllib

eval_url = "http://localhost:5000/evaluate"
run_url = "http://localhost:5000/run"

manifest = """{"manifest": 
                {"files": [{"url": "http://localhost:5000/testing/plugintest.txt", "filename": "plugintest.txt", "type": "text/plain"}]}}"""

import requests, zipfile, io


def test():
    eval_response = requests.post(eval_url, data=manifest)
    run_response = requests.post(run_url, data=manifest)

    print(eval_response.text)
    z = zipfile.ZipFile(io.BytesIO(run_response.content))
    z.extractall("out")


if __name__ == "__main__": test()
