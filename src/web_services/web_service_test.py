


# coding=utf-8
# Created by Michael Zhu
# DataSelect AI, 2023

import json
import time

import urllib.request

import sys
sys.path.append("/")


def test_service(input_text):
    header = {'Content-Type': 'application/json'}

    prompt = "<s>问：\n{}\n答：\n".format(input_text.strip())

    data = {
          "query": prompt,
          "max_new_tokens": 1024,
    }
    request = urllib.request.Request(
        # url='http://127.0.0.1:9005/chatmed_generate',
        url='http://219.228.135.162:9005/chatmed_generate',
        headers=header,
        data=json.dumps(data).encode('utf-8')
    )
    response = urllib.request.urlopen(request)
    res = response.read().decode('utf-8')
    result = json.loads(res)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, indent=2))

    return result


if __name__ == "__main__":

    f_out = open("src/web_services/test_examples/ChatMed-Consult_test.json", "a", encoding="utf-8", buffering=1)
    with open("src/web_services/test_examples/ChatMed_Consult-v0.3-1.jsonl", "r", encoding="utf-8") as f:

        for line in f:
            line = line.strip()
            if not line:
                continue

            line = json.loads(line)
            print(line)

            t0 = time.time()
            result = test_service(line["query"])
            t1 = time.time()
            print("time cost: ", t1 - t0)

            f_out.write(
                json.dumps(result, ensure_ascii=False) + "\n"
            )

