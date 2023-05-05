import json
import time

import torch
from transformers import AutoConfig, LlamaForCausalLM, LlamaTokenizer, AutoModelForCausalLM

import sys
sys.path.append("./")

from peft import LoraConfig, TaskType, get_peft_model, PeftModel

model_path = "./resources/chinese-llama-alpaca-plus-lora-7b"
config = AutoConfig.from_pretrained(
    model_path,
)
print(config)

with torch.no_grad():
    torch_dtype = torch.float16
    model = LlamaForCausalLM.from_pretrained(
        model_path,
        config=config,
        torch_dtype=torch_dtype,
        # low_cpu_mem_usage=True
    )
    model = model.cuda()

    tokenizer = LlamaTokenizer.from_pretrained(
        model_path,
    )
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.eos_token_id
    model.resize_token_embeddings(len(tokenizer))

    # 加载lora
    # peft_model_path = "resources/ChatMed-Consult_llama_lora_pt_v0"
    peft_model_path = "michaelwzhu/ChatMed-Consult"
    model = PeftModel.from_pretrained(model, peft_model_path)
    model.eval()


generation_config = dict(
    temperature=0.2,
    # top_k=40,
    top_p=0.9,
    do_sample=True,
    num_beams=1,
    repetition_penalty=1.3,
    max_new_tokens=400
)

from flask import Flask, request

app = Flask(__name__)


@app.route("/chatmed_generate", methods=["POST"])
def cough_predict():
    input_data = json.loads(
        request.get_data().decode("utf-8")
    )

    query = input_data.get("query")
    max_new_tokens = input_data.get("max_new_tokens", 256)

    t0 = time.time()
    with torch.no_grad():
        device = torch.device("cuda")
        inputs = tokenizer(query, return_tensors="pt", add_special_tokens=False)  # add_special_tokens=False ?
        generation_output = model.generate(
            input_ids=inputs["input_ids"].to(device),
            attention_mask=inputs['attention_mask'].to(device),
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
            **generation_config
        )
        s = generation_output[0]
        print(s)
        output = tokenizer.decode(s, skip_special_tokens=True)

        response = output.split("答：\n")[1].strip()

    print(output)

    t1 = time.time()
    print("time cost: ", t1 - t0)

    return {
        "query": query,
        "response": response
    }


app.run(host="0.0.0.0", port=9005, debug=False)

'''

CUDA_VISIBLE_DEVICES=2 python src/web_services/web_service_simple.py


'''
