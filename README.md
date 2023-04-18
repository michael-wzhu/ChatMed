[**中文**](./README.md) | [**English**](./README_EN.md)

<p align="center">
    <br>
    <img src="./pics/ChatMed.png" width="355"/>
    <br>
</p>
<p align="center">
    <img alt="GitHub" src="https://img.shields.io/github/license/ymcui/Chinese-LLaMA-Alpaca.svg?color=blue&style=flat-square">
    <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/ymcui/Chinese-LLaMA-Alpaca">
</p>

以ChatGPT、GPT-4等为代表的大语言模型（Large Language Model, LLM）掀起了新一轮自然语言处理领域的研究浪潮，展现出了类通用人工智能（AGI）的能力，受到业界广泛关注。

为推动LLM在中文医疗领域的发展和落地，我们现推出**ChatMed**系列中文医疗大规模语言模型:

- 🚀 [ChatMed-FP](https) : 在大规模医疗领域文本(25亿tokens)上对Bloomz-7B模型进行继续预训练(further pretraining).
- 🚀 [ChatMed-Instruct](https) : 基于[PromptCBLUE](https://github.com/michael-wzhu/PromptCBLUE)基准数据，对Bloomz-7B模型进行了全量微调，可用于在处理各种医疗文本挖掘/信息抽取任务.


----

[Text2DT](https://github.com/michael-wzhu/Text2DT_Baseline) | [中文医疗大模型评测基准PromptCBLUE](https://github.com/michael-wzhu/PromptCBLUE)


## 更新

2023/4/18 上传训练了7.2w步的ChatMed-FP模型到HuggingFace Hub. 模型下载链接: [ChatMed-FP]()


## 快速上手

下载模型后，在3090显卡(或者更强的显卡) 运行

```bash

python run_test_examples.py

```

上面的脚本主要是运行了test_examples.json文件中提供了5个测试用例。在使用自己的测试用例时，请注意保持格式一致。


## 生成效果对比

我们主要对比了目前在开源社区大火的LlaMA模型，以及新近开源的[Huatuo](https://github.com/SCIR-HI/Huatuo-Llama-Med-Chinese)

| 输入 | Llama输出 | Huatuo输出 | ChatMed输出 |
| -- | -- | -- | -- | 
| 小张最近感觉身体不适，出现心悸、气促等症状。体检发现心脏扩大、搏动减弱。| Llama输出 | Huatuo输出 | ChatMed输出 |



## 免责声明

本项目相关资源仅供学术研究之用，严禁用于商业用途。


## Citation

如果你使用了本项目的模型，数据或者代码，请声明引用：

```bash
@misc{zhu2023ChatMed,
      title={ChatMed: A Chinese Medical Large Language Model}, 
      author={Wei Zhu and Xiaoling Wang},
      year={2023},
      publisher = {GitHub},
      journal = {GitHub repository},
      howpublished = {\url{https://github.com/michael-wzhu/ChatMed}},
}

```







