[**中文**](./README.md) | [**English**](./README_EN.md)

<p align="center">
    <br>
    <img src="https://github.com/michael-wzhu/ChatMed/blob/main/pics/ChatMed.png" width="355"/>
    <br>
</p>
<p align="center">
    <img alt="GitHub" src="https://img.shields.io/github/license/ymcui/Chinese-LLaMA-Alpaca.svg?color=blue&style=flat-square">
    <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/ymcui/Chinese-LLaMA-Alpaca">
</p>

以ChatGPT、GPT-4等为代表的大语言模型（Large Language Model, LLM）掀起了新一轮自然语言处理领域的研究浪潮，展现出了类通用人工智能（AGI）的能力，受到业界广泛关注。

为推动LLM在中文医疗领域的发展和落地，提升LLM的医疗知识与回答医学咨询的能力，我们现推出**ChatMed**系列中文医疗大规模语言模型:

- 🚀 [ChatMed-Consult](https://huggingface.co/michaelwzhu/ChatMed-Consult) : 基于[中文医疗在线问诊数据集ChatMed_Consult_Dataset](https://huggingface.co/datasets/michaelwzhu/ChatMed_Consult_Dataset)的50w+在线问诊+ChatGPT回复作为训练集。模型主干为[LlaMA-7b](https://github.com/facebookresearch/llama),融合了[Chinese-LlaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca)的LoRA权重与中文扩展词表，然后再进行基于LoRA的参数高效微调。我们将全部数据和代码都进行了公开。我们也将部署一个在线Gradio demo, 敬请关注。
- ⏳ [ChatMed-TCM](https://huggingface.co/michaelwzhu/ChatMed-TCM) : 大模型赋能中医药传承。这一模型的训练数据为[中医药指令数据集ChatMed_TCM_Dataset](https://huggingface.co/datasets/michaelwzhu/ChatMed_TCM_Dataset)。以我们开源的[中医药知识图谱](https://github.com/ywjawmw/TCM_KG)为基础，采用以实体为中心的自指令方法(entity-centric self-instruct)，调用ChatGPT得到2.6w+的围绕中医药的指令数据。ChatMed-TCM模型也是以LlaMA为底座，采用LoRA微调得到。


----

[Text2DT](https://github.com/michael-wzhu/Text2DT_Baseline) | [中文医疗大模型评测基准PromptCBLUE](https://github.com/michael-wzhu/PromptCBLUE) | [中文医疗在线问诊数据集ChatMed_Consult_Dataset](https://huggingface.co/datasets/michaelwzhu/ChatMed_Consult_Dataset) | [中医药指令数据集ChatMed_TCM_Dataset](https://huggingface.co/datasets/michaelwzhu/ChatMed_Consult_Dataset) | [中医药知识图谱](https://github.com/ywjawmw/TCM_KG)


## 更新

2023/5/05 开源[ChatMed-Consult](https://huggingface.co/michaelwzhu/ChatMed-Consult)模型;


## ChatMed-Consult模型介绍

### 模型介绍

- 训练数据：[中文医疗在线问诊数据集ChatMed_Consult_Dataset](https://huggingface.co/datasets/michaelwzhu/ChatMed_Consult_Dataset)的50w+在线问诊+ChatGPT回复作为训练集。我们发现，在线爬取的问诊数据，虽然可以反映真实世界的用户/患者的问诊需求，但是一般网上的回答良莠不齐。所以我们调用ChatGPT (`gpt-3.5-turbo`)得到问诊的回复。 (⏳ todo: 实现一个评估模型，给人工回复进行评分。调用大模型的token毕竟烧钱)
- 模型基座：目前我们开源了基于LlaMA-7b的[ChatMed-Consult](https://huggingface.co/michaelwzhu/ChatMed-Consult)模型。后续我们将会尝试不同的模型底座，比如LlaMA-13b，MOSS等。
- 代码：模型训练所需要的全部代码见[ChatMed-Consult 训练代码](https://github.com/michael-wzhu/ChatMed/blob/main/src/chatmed_llama_peft)。训练中我们借助DeepSpeed(ZeRO stage 3)实现分布式训练。
- 模型权重下载：由于我们目前采用模型是基于Llama-7b进行参数高效微调，所以我们只上传了参数高效微调模块的权重，见[ChatMed-Consult模型权重](https://huggingface.co/michaelwzhu/ChatMed-Consult)。

### 快速上手

在使用[ChatMed-Consult](https://huggingface.co/michaelwzhu/ChatMed-Consult)之前，大家需要准备好LlaMA-7b底座模型，详细操作见[LlaMA-7b模型准备](https://github.com/michael-wzhu/ChatMed/blob/main/src/chatmed_llama_peft/LlaMA-7b%E6%A8%A1%E5%9E%8B%E5%87%86%E5%A4%87.md)。

LlaMA-7b底座模型准备好后，下载[ChatMed-Consult的LoRA权重](https://huggingface.co/michaelwzhu/ChatMed-Consult)，在3090显卡(或者更强的显卡) 运行以下命令，启动一个简单的基于flask的web service:

```bash
python src/web_services/web_service_simple.py
```

然后运行 
```bash
python src/web_services/web_service_test.py
```

上面的脚本主要是运行了test_examples.json文件中提供了测试用例。在使用自己的测试用例时，请注意保持格式一致。

### 训练

首先，大家需要准备好LlaMA-7b底座模型，保存于`resources/chinese-llama-alpaca-plus-lora-7b`路径。数据集采用[中文医疗在线医疗咨询数据集ChatMed_Consult_Dataset](https://huggingface.co/datasets/michaelwzhu/ChatMed_Consult_Dataset)。我们采用deepspeed实现分布式训练：

```bash
./src/chatmed_llama_peft/run_train.sh
```

训练脚本中使用的是4张显卡，大家根据自己的服务器情况调整超参数。




## 效果对比

我们对比了经过权重转化与合并的[中文LlaMA-7b](https://github.com/michael-wzhu/ChatMed/blob/main/src/chatmed_llama_peft/LlaMA-7b%E6%A8%A1%E5%9E%8B%E5%87%86%E5%A4%87.md)，以及经过了[ChatMed_Consult_Dataset](https://huggingface.co/datasets/michaelwzhu/ChatMed_Consult_Dataset) 和LoRA微调的[ChatMed-Consult](https://huggingface.co/michaelwzhu/ChatMed-Consult)模型。下面是五个典型例子的对比。更多测试样例见[More test examples](https://github.com/michael-wzhu/ChatMed/blob/main/src/web_services/test_examples/ChatMed-Consult_test.json)


| 问诊问题 | 中文LlaMA-7b | ChatMed-Consult |
|------|------------|-----------------|
| 天气温度越来越高，对于有宝宝的家庭来说，室内空调开到几度合适，以前我都是开二十七，那医生说开错了。    | "A. 二十七摄氏度；B. 三十二八摄氏度；C.三十六二十四摄氏度；D.四十一九摄氏度；E. 四十一九摄氏度。"          | "在夏天的时候，为了保持良好的健康和舒适的环境，建议您将房间内的空气调节器调至26-28摄氏度左右即可。如果您想让婴儿更加舒服地睡觉，可以把室温降低1-2个台阶（比如从27升至22），这样可以让孩子更容易入睡并提高睡眠质量。同时，也要注意定期清洁空调过滤网以及避免过度使用空调等措施以保证室内通风良好、干燥清新。"              |
| 这两天关节痛，昨天贴了膏药好一点。昨晚吹了一下风扇，今天早上起床都起不了，走不了路。    | "可能是风湿性关节炎引起的疼痛和僵硬症状。建议您去医院做进一步检查以确定诊断并制定治疗方案。"          | 您的症状可能是风湿性疾病引起的疼痛和僵硬感。建议您尽快就医并接受专业的诊断治疗。在等待看医生的过程中，可以尝试以下措施缓解痛苦：保持休息、避免过度活动或剧烈运动；使用热敷或者冷敷来减轻肿胀和疼痛；按摩局部肌肉以促进血液循环等。同时请注意保暖，穿暖和的衣服，以免加重病情。"            |
| 癫痫病25年了，这些年病情一直都比较稳定，发作次数也很少，现在开始频繁发作了该怎么办？有没有什么针对的办法可以解决啊？    | 建议您及时就医并进行检查。如果确诊为癫痫持续状态（EPS）或阵发性间歇期发作等需要药物治疗的情况，可以考虑使用抗惊厥药、镇静催眠剂和神经营养素类药物来控制症状；同时注意饮食卫生及生活习惯的调整也是很重要的。          | "如果您的癫痫症状越来越多、更频繁或更加严重，建议您尽快就医。以下是一些可能有助于缓解您的情况的方法和注意事项:\n\n1.保持规律的生活方式，包括充足睡眠时间、饮食健康等；\n2.避免过度疲劳或者精神紧张的情况发生；\n3.定期进行体检和其他必要的检查以确保身体健康状况良好；\n4.遵从医生开具的药物治疗方案并按时服药；\n5.在紧急情况下及时拨打急救电话寻求帮助。\n\n请注意，以上方法只是一般性的指导原则，具体治疗方法需要根据个人实际情况而定，最好咨询专业医师的意见。"               |
| 上牙床外凸，牙齿还是较整齐的，微笑时会露出很大的牙床，已经21岁了，带牙套会有用吗，需要带多久，多少钱啊。    | "建议您去口腔医院进行检查和治疗，因为这属于比较严重的问题之一。"          | "如果您想矫正您的下颌骨和牙齿问题，可以考虑戴牙套来达到这个目的。但是需要注意的是，佩戴牙套的时间长短取决于问题的严重程度以及个人的情况。一般来说，如果情况比较轻微或不影响日常生活的话，可能只需要几个月就可以看到明显的效果；但如果情况较为复杂或者影响到生活质量，可能会更长时间才能完成治疗过程。此外，价格也会因地区、医院等因素而有所不同，建议您咨询当地口腔医生进行详细了解并制定个性化方案。"               |
| 医生您好，我想给爷爷奶奶在美国买保健品/药，奶奶有长期冠心病，爷爷有缺血性心脏病，以前还做过白内障手术，请问有哪些药适合买?我看到的有鱼油，欧米茄（omega）3-6-9,还有烟酸，叶黄素，亚麻油.    | 建议购买含有硝酸甘油、维生素E和钙片等成分的产品。          | "很抱歉听到您的家人健康问题。对于老年人来说，选择合适的药物非常重要。以下是一些可能有用的产品和建议供参考:\n\n1. Omega-3脂肪酸补充剂 - 这些产品通常含有丰富的Omega-3脂肪酸和其他营养成分，可以帮助降低血液中的胆固醇水平并预防心血管疾病。但是请注意，如果您正在服用其他抗凝或降脂药物，最好先咨询专业医师的意见是否需要调整剂量或者停止使用这些药品。\n\n2. Smart Heart Plus – 这是一种针对心脏问题的复合物，包括多种天然植物提取物、维生素B群等物质，能够改善血液循环、增强心肌功能以及保护血管壁等等。不过需要注意的是，这种产品的效果因人而异，所以在购买前一定要仔细阅读说明书并且遵循医嘱进行用药。\n\n3. CoQ10 - 这种辅酶是一种重要的能量代谢产物，它可以在细胞中提供电子流来支持ATP合成过程。CoQ10缺乏可能会导致疲劳感、肌肉疼痛等问题。因此，如果老人的身体状况允许，可以考虑添加适量的CoQ10以提高身体机能。"               |

我们可以看到：
- 在线问诊，由于用户输入错字或者语音转文字带来噪音，问诊问题可能不会很规整。在这种情况下，中文LlaMA-7b模型可能会产生没有意义的回答。而ChatMed-Consult可以有效的从干扰中理解用户问题，做出相应的回答；
- ChatMed-Consult的回答会更加具有人性关怀一些，而中文LlaMA-7b模型的回复可能会比较生硬；
- ChatMed-Consult相较于中文LlaMA-7b模型的回答会更加丰富，具有更多可行的建议。
- 大模型作为医生的辅助，其可以多列举可能性和建议，但是不能太过武断的下结论。中文LlaMA-7b模型面对问诊问题会比较容易下直接下结论，似乎是有一些过度自信。ChatMed-Consult一般会说"以下是一些可能..."，相对更加谨慎。



## 免责声明

- 本项目相关资源仅供学术研究之用，严禁用于商业用途。
- ChatMed-Consult作为基于语言模型的智能助手，其不能代替医生进行医学诊断和给出医学建议。如有需要，请咨询专业医生或前往医院就诊。
- ChatMed系列模型正在快速迭代中，模型权重会定期进行更新。
- ChatMed系列模型基于开源数据，其训练数据的质和量都是有限的，其掌握的医学知识肯定是存在各种各样的缺陷。我们将会不断进行改进和更新。


## 致谢

本项目基于开源项目进行开发，在此对相关项目和研究开发人员表示感谢。

- [LlaMA](https://github.com/facebookresearch/llama)
- [Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca)
- [Chinese-LlaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca)

Logo中的小学霸羊驼是由[midjourney](http://midjourney.com)自动生成。


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







