

本readme目的是准备LlaMA模型底座，使得其可以在huggingface transformers框架下进行参数高效微调。准备工作主要有三步：

### LlaMA模型主干

获取LlaMA模型主干有几种途径：
- 原版LLaMA模型: 在[LlaMA原项目地址](https://github.com/facebookresearch/llama)填写google form申请;
- [LlaMA项目的一个PR](https://github.com/facebookresearch/llama/pull/73/files)
- huggingface的model hub中已经人上传了模型: [decapoda-research/llama-7b-hf](https://huggingface.co/decapoda-research/llama-7b-hf)

### LlaMA模型权重转化

上一步骤的前两种方法需要将LlaMA模型权重转化为huggingface transformers的格式，详见[convert_llama_weights_to_hf](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/convert_llama_weights_to_hf.py))。


### 融合Chinese-LlaMA-Alpaca

[Chinese-LlaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca/blob/main/README_EN.md)项目提供了使得LlaMA模型更适应于中文场景的lora权重和经过继续预训练的embedding权重。我们采用其脚本将其权重合并到模型主干中：

```bash
python src/chatmed_llama_peft/merge_llama_with_chinese_lora.py \
    --base_model yahma/llama-7b-hf \
    --lora_model ziqingyang/chinese-llama-plus-lora-7b,ziqingyang/chinese-alpaca-plus-lora-7b \
    --output_type huggingface \
    --output_dir ./resources/chinese-llama-alpaca-plus-lora-7b

```

注意上述命令中我们合并了[Chinese-LlaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca)的两个lora权重，第一个权重是做了大规模中文语料预训练，第二个权重则是进一步做了基于self-instruct的中文指令微调。两者合并可以得到更会说中国话的LlaMA模型。

