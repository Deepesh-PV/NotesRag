from FaissOllm import generate_prompt_and_query

import os
import time
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def model(query):
    if os.path.isfile("tezvec.npy"):
        print("wait for answer")
        return generate_prompt_and_query(query, "llama3:latest", "tezvec.npy", "tez1.json","dummy.txt")
    else:
        return "Wait Till Document is being Embedded"


