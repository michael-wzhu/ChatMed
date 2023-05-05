import json
import time

import torch
from transformers import AutoConfig, LlamaForCausalLM, LlamaTokenizer, AutoModelForCausalLM

import sys
sys.path.append("./")

# model_path = "/public/home/xlwang2/codes/Med_Prompts/models--BelleGroup--BELLE-7B-2M/snapshots/a9076d928eff1d94fe6b4372ba2bd3a800dc10a1"
# model_path = "./resources/chinese-llama-alpaca-plus-lora-7b"
from peft import LoraConfig, TaskType, get_peft_model

model_path = "./resources/chinese-llama-alpaca-plus-lora-7b"

config = AutoConfig.from_pretrained(
    model_path,
)
print(config)

with torch.no_grad():
    torch_dtype = torch.float16
    # model = LlamaForCausalLM.from_pretrained(
    #     model_path,
    #     config=config,
    #     torch_dtype=torch_dtype,
    #     # low_cpu_mem_usage=True
    # )
    model = AutoModelForCausalLM.from_config(
        config,
        torch_dtype=torch_dtype
    )
    print(model)
    model = model.cuda()

    tokenizer = LlamaTokenizer.from_pretrained(
        model_path,
    )
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.eos_token_id
    model.resize_token_embeddings(len(tokenizer))

    # 加载lora
    trainable = "q_proj,v_proj,k_proj,o_proj,gate_proj,down_proj,up_proj"
    target_modules = trainable.split(',')
    modules_to_save = None
    lora_rank = 8
    lora_dropout = 0.1
    lora_alpha = 32
    print(target_modules)
    print(lora_rank)
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        target_modules=target_modules,
        inference_mode=False,
        r=lora_rank,
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout,
        modules_to_save=None)
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    # 加载训练后的参数
    path = "./medical_prompts/experiments/output/chatmed-llama-7b-pt-v0/checkpoint-100-32"
    state_dict = torch.load(path)
    model.load_state_dict(state_dict, strict=False)
    model.print_trainable_parameters()
    for n, p in model.named_parameters():
        print(n, p.requires_grad)

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


@app.route("/llama_generate", methods=["POST"])
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

CUDA_VISIBLE_DEVICES=2 python web_demos/chatmed_llama_v0/web_service_simple.py


'''
