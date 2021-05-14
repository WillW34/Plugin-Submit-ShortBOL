import requests
import urllib


url = "http://127.0.0.1:5000/evaluate"
manifest = """{"manifest": {"files":[
            {"url": "http://synbiohub.org/expose/b41e63d6-10f4-4cac-b1c8-285f71156b56", "filename": "asdfasdf.xls", "type": "application/vnd.ms-excel"},
            {"url": "http://synbiohub.org/expose/jkl9d8s7ufjqhoer8u709s", "filename": "file_name1.dna", "type": "application/xml"},
            {"url": "http://synbiohub.org/expose/basdf-11230948f4-12344cac", "filename": "file_name2.xml", "type": "application/xml"},
            {"url": "http://synbiohub.org/expose/09uj2k3j0", "filename": "file_name3.shb", "type": "application/xml"},
            {"url": "http://synbiohub.org/expose/asdfasdf56", "filename": "file_name4.xml", "type": "application/xml"}]}}"""


def test():
    response = requests.post(url,data=manifest)
    print(response.text)


if __name__ == "__main__":test()