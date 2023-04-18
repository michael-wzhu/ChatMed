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

我们主要对比了目前在开源社区常用的Bloomz模型。

| 输入 | Bloomz输出  | ChatMed输出 |
| -- | -- | -- | -- | 
| 颈柱病是如何引起的\n我是坐办公室的，经常有不明因素或病因的落枕，最近还有耳鸣，不太严重。这是不是颈柱问题，怎么预防。| - | 你好！根据你说的症状有可能是与颈椎病有关的，建议到医院查一查，应当做一下X线片检查和颈部血管彩超等等，首先应当注意防止受寒，多吃蔬菜水果，可以试试理疗的方法如按摩针灸等，不要过度劳累紧张，要好好休息 |
| 胃胀气怎么缓解和治疗？ | - | 你好，根据你的描述是属于腹胀,建议你服用吗丁啉、乳酸菌素片调理看看。必要时到医院消化内科就诊检查确诊病因对症治疗。 |
| 怎样防止乳腺癌 | - | 你好，以下几点建议可供参考：一、保持良好的心态与情绪。精神因素对乳房健康有密切关系。据调查，大多数乳癌患者在患病前都曾有过一段时间的精神紧张期，如遇重大创伤、工作变动等，使本人心理上发生矛盾冲突，社会适应能力遭遇到打击，易怒、郁闷、忧愁或悲伤等，而长期的情绪不稳定、心情不舒畅也会导致癌症的发生和发展。二、坚持体育锻炼，积极参加社交活动，避免单独运动伤害。三、养成良好的饮食习惯。戒烟限酒；忌食腌制食品、烧烤食物等；食用富含维生素和蛋白质的营养食品，多吃新鲜蔬菜水果；饮用绿茶可以保护乳房，等等。四、定期进行乳房自检。了解自己的乳房如何健康状况，学会识别异常现象，发现问题及时处理。 | 



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







