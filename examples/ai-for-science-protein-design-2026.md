# AI for Science：蛋白设计基础模型与工作流
## 2026 技术调研简报

**报告分类：** 公开技术调研 | **发布时间：** 2026 年 | **领域：** 计算生物学 · AI for Science

---

## 执行摘要

人工智能驱动的蛋白质设计正经历一场范式革命。从 AlphaFold2 奠定结构预测的精度基准，到以 RFdiffusion、ESM3、AlphaFold3 为代表的生成式基础模型相继涌现，蛋白质工程正从"经验试错"转向"计算优先、实验验证"的全新模式。

本简报面向计算生物学、药物研发及生物技术领域的技术决策者，系统梳理截至 2026 年上半年的主流 AI 蛋白设计基础模型、标准化工作流及工程实践要点，并给出模型选型建议与关键风险提示。

**核心发现：**

- **结构预测**已基本成熟：AlphaFold3、Chai-1、Boltz-1 在蛋白质 - 配体、蛋白质 - 核酸、抗体 - 抗原等复合体预测上达到或超越传统实验精度。
- **生成式设计**快速成熟：RFdiffusion / RFdiffusion2 + ProteinMPNN / LigandMPNN 已成为主流从头设计流水线；ESM3 实现了序列 - 结构 - 功能的统一多模态推理。
- **标准工作流**已形成：骨架生成 → 序列设计 → 结构验证 → 功能筛选的四阶段流水线被广泛采用，成功率较传统方法提升 10–100 倍。
- **实验验证仍是瓶颈**：计算成功率与湿实验成功率之间仍存在显著差距，复杂靶点（GPCR、离子通道）的设计能力仍受限于结构数据稀缺。

---

## 技术背景

### 1.1 蛋白质设计的核心挑战

蛋白质由氨基酸序列（一级结构）折叠而成具有特定三维构象（二 / 三 / 四级结构）的功能分子。**蛋白质设计**旨在"逆向工程"这一过程——即从功能需求出发，设计出能实现该功能的氨基酸序列与结构。

传统蛋白设计方法（如 Rosetta）依赖物理能量函数与大量专家经验，需筛查数万甚至数十万候选分子才能找到一个可行设计，周期长、成本高、泛化能力有限。

### 1.2 AI 的革命性突破

2020 年，DeepMind 发布 [AlphaFold2](https://www.nature.com/articles/s41586-021-03819-2)，将蛋白质结构预测精度从竞赛冠军水平大幅提升，将预测时间从数月压缩至数小时。这一里程碑奠定了深度学习在蛋白质科学中的核心地位，并于 2024 年获得诺贝尔化学奖。

此后，基于预训练大模型的**蛋白质语言模型（PLM）**、**扩散生成模型**、**多模态基础模型**相继涌现，形成覆盖"结构预测 → 序列设计 → 功能注释"全链路的 AI 工具生态。

### 1.3 市场与应用背景

据 [DataM Intelligence（2026）](https://www.datamintelligence.com/research-report/ai-protein-design-market) 的行业分析，AI 蛋白设计市场竞争持续升温，主要参与者包括 DeepMind、Generate:Biomedicines、Insilico Medicine、Cradle、Profluent 等。行业估计 AI 赋能工具可将早期研发周期缩短 40–60%，药物发现与先导优化占最大应用份额（约 33.7%）。

---

## 主流基础模型与工具全景

### 2.1 结构预测类模型

#### AlphaFold3（Google DeepMind & Isomorphic Labs，2024）

AlphaFold3 是 AlphaFold 系列的第三代，于 2024 年 5 月发表于 [*Nature*](https://www.nature.com/articles/s41586-024-07487-w)，同年 11 月开放学术源代码。其核心创新在于将预测范围从蛋白质单体扩展至**所有生命分子**——蛋白质、DNA、RNA、小分子配体（药物）、翻译后修饰及离子的联合三维结构均可预测。

技术架构上，AlphaFold3 保留了改进的 Evoformer 模块，并引入**扩散网络**（类似于图像生成中的 DALL-E / Stable Diffusion）进行最终原子坐标的生成。在 PoseBusters 基准测试中，AlphaFold3 对蛋白质 - 配体互作的预测精度比最佳传统方法高出 **50%**，是首个在生物分子结构预测上超越物理方法的 AI 系统。[AlphaFold Server](https://alphafold.ebi.ac.uk) 提供免费在线访问，AlphaFold 蛋白结构数据库已覆盖逾 **2.14 亿**个蛋白质结构。

#### Chai-1（Chai Discovery，2024）

[Chai-1](https://github.com/chaidiscovery/chai-lab) 是一个完全开源的多模态生物分子结构预测基础模型，权重和推理代码以 Python 包形式发布，非商业免费使用，商业药物发现场景亦可通过网络界面免费访问。

Chai-1 在蛋白质 - 配体预测（PoseBusters 基准成功率 **77%**，与 AlphaFold3 的 76% 相当）、蛋白质多聚体预测（DockQ 成功率 **0.751** vs. AF-Multimer2.3 的 **0.677**）以及抗体 - 抗原复合体预测上均达到或超越当时最优水平。此外，Chai-1 支持**实验约束提示**（如交叉连接质谱、表位图谱数据），可显著提升困难靶点的预测精度。

#### Boltz-1（MIT CSAIL & Jameel Clinic，2024）

[Boltz-1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11601547/) 是 MIT 开发的完全开源生物分子互作建模系统，预测能力与 AlphaFold3 相当，是目前学术界最具可访问性的高精度多分子结构预测工具之一。[ABCFold](https://academic.oup.com/bioinformatics/article-abstract/5/1/vbaf153/8176613) 工具进一步提供了 AlphaFold3、Boltz-1、Chai-1 的标准化统一接口，便于横向比较。

### 2.2 生成式骨架设计模型

#### RFdiffusion（Baker Lab，华盛顿大学，2023）

[RFdiffusion](https://www.bakerlab.org/2023/07/11/diffusion-model-for-protein-design/) 基于 RoseTTAFold 结构预测网络，通过扩散模型对蛋白质骨架生成任务进行微调，发表于 [*Nature*](https://www.nature.com/articles/s41586-023-06415-8)。它在从头单体设计、拓扑约束蛋白设计、**蛋白质结合剂设计**、对称寡聚体设计、酶活性位点脚手架及对称 Motif 脚手架等多类任务上全面超越既有方法，并经数百个 AI 生成蛋白质的实验验证。单个计算成功设计的实验成功率相比传统方法提升了 **1–2 个数量级**。

#### RFdiffusion2（Baker Lab + MIT，2025）

[RFdiffusion2](https://www.ipd.uw.edu/2025/04/introducing-rfdiffusion2/)（2025 年 4 月发布）在原版基础上引入**流匹配训练**（Flow Matching）、旋转异构体推断及残基索引推断能力，专注于**酶活性位点设计**。RFdiffusion2 仅需输入化学反应描述，即可生成带有定制活性位点的完整蛋白质骨架，无需专家预设原子级细节。

在包含 41 个挑战性酶设计问题的 AME 基准测试中，RFdiffusion2 解决了**全部 41 个**案例，而此前最优方法仅解决 16 个。实验室测试表明，每个案例测试不足 100 个设计即可获得活性酶，锌水解酶设计活性比此前方法高出数个数量级。

#### FrameDiff / SE(3) Diffusion（MIT CSAIL，2023）

[FrameDiff](https://news.mit.edu/2023/generative-ai-imagines-new-protein-structures-0712) 是 RFdiffusion 的简化替代方案，基于 SE(3) 刚体不变扩散框架，无需依赖预训练结构预测网络，可独立生成最长约 500 个氨基酸的新颖蛋白质骨架，并与 RoseTTAFold2 结合演化为 RFdiffusion。

### 2.3 序列设计模型

#### ProteinMPNN（Baker Lab，2022）

[ProteinMPNN](https://www.science.org/doi/10.1126/science.add2187) 是当前最广泛使用的固定骨架序列设计模型，基于消息传递神经网络（MPNN）图神经网络架构，输入蛋白质骨架坐标（PDB 格式），输出氨基酸序列。每条序列生成约需 **1–2 秒**（GPU），在天然蛋白单体上的序列回收率约 **50–55%**。ProteinMPNN 支持单链、多链、对称约束等多种设计场景，是 RFdiffusion 骨架生成后标准的序列设计工具。

#### LigandMPNN（Baker Lab，2025）

[LigandMPNN](https://www.ipd.uw.edu/2025/03/introducing-ligandmpnn/)（2025 年 3 月发布，成果发表于 [*Nature Methods*](https://www.nature.com/articles/s41592-025-02626-1)）是 ProteinMPNN 的扩展版本，显式建模非蛋白原子（小分子、核苷酸、金属离子）的空间与化学上下文。在蛋白质 - 小分子（序列回收率 **63.3% vs. ProteinMPNN 的 50.5%**）、蛋白质 - 核酸（50.5% vs. 34.0%）和蛋白质 - 金属（77.5% vs. 40.6%）场景下均大幅优于 ProteinMPNN 和 Rosetta。已用于设计逾 **100 个**经实验验证的小分子和 DNA 结合蛋白。

### 2.4 蛋白质语言模型（PLM）

#### ESM3（EvolutionaryScale，2024–2025）

[ESM3](https://www.evolutionaryscale.ai/blog/esm3-release) 是 EvolutionaryScale 发布的前沿多模态生成式语言模型，旗舰版本参数量达 **980 亿**，在超过 **10^24 FLOPS** 的算力下训练，发表于 [*Science*](https://www.science.org/doi/10.1126/science.ads0018)（2025 年 1 月）。ESM3 同时对蛋白质**序列、结构和功能**三个模态进行推理，使用离散化词表将三维结构和功能关键词编码为标记序列，以掩码语言建模（MLM）目标训练。

ESM3 能生成与已知蛋白质序列相似度低于 **20%**、TM-score 约 **0.52** 的新型折叠结构，并通过类 RLHF 的自我对齐进一步提升生成质量。其突破性案例 **esmGFP** 与自然界最近荧光蛋白序列相似度仅 **58%**（58% 序列相同 = 42% 突变），相当于"模拟 5 亿年进化"。开源版 ESM3 1.4B 权重可免费获取。

#### ESM2 + ESMFold（Meta AI，2022–2023）

[ESMFold](https://www.science.org/doi/10.1126/science.ade2574) 是基于 ESM2 蛋白质语言模型的端到端结构预测工具，以语言模型嵌入替代多序列比对（MSA）检索，速度比 AlphaFold2 快约 **60 倍**，适合大规模快速筛查。ESM2（规模从 8M 到 15B 参数）在蛋白质进化尺度数据上训练，其嵌入被广泛用于下游结构预测、功能预测和序列设计管线中。

### 2.5 功能预测工具

**DeepGO-SE** 基于 ESM2 嵌入结合神经符号推理，将蛋白质功能预测形式化为语义蕴含问题，在基因本体（GO）功能注释上取得显著提升，发表于 [*Nature Machine Intelligence*](https://www.nature.com/articles/s42256-024-00795-w)（2024）。

**ProteinGym** 是蛋白质适应性（fitness）预测领域最权威的大规模基准集，提供 2000 余个深度突变扫描（DMS）数据集，用于比较不同模型在突变效应预测任务上的性能，发表于 [NeurIPS 2023](https://papers.nips.cc/paper_files/paper/2023/hash/cac723e5ff29f65e3fcbb0739ae91bee-Abstract-Datasets_and_Benchmarks.html)。

---

## 序列 - 结构 - 功能标准工作流

当前 AI 蛋白设计领域已形成较为成熟的**四阶段计算工作流**，如下所示：

```
┌─────────────────────────────────────────────────────────┐
│         AI 蛋白设计四阶段工作流（2025–2026 标准）        │
│                                                         │
│  阶段一：骨架生成                                        │
│  RFdiffusion / RFdiffusion2 / FrameDiff                 │
│  输入：功能约束（结合位点、活性位点、对称性）             │
│  输出：蛋白质三维骨架坐标（.pdb）                        │
│              ↓                                          │
│  阶段二：序列设计                                        │
│  ProteinMPNN / LigandMPNN（含配体场景）                  │
│  输入：固定骨架 + 约束（配体、金属、核酸）               │
│  输出：氨基酸序列（FASTA）                               │
│              ↓                                          │
│  阶段三：结构验证                                        │
│  AlphaFold2 / AlphaFold3 / ESMFold / Chai-1            │
│  指标：自洽 TM-score（scTM ≥ 0.8）、pLDDT、ipTM        │
│  过滤：RMSD < 2 Å（与设计骨架比较）                     │
│              ↓                                          │
│  阶段四：功能注释 & 适应性预测                           │
│  ESM3 功能标记 / DeepGO-SE / ProteinGym DMS 模型        │
│  输出：功能评分、GO 注释、突变效应预测                   │
│              ↓                                          │
│  优先级排序 → 合成表达 → 湿实验验证                      │
└─────────────────────────────────────────────────────────┘
```

### 3.1 阶段一：骨架生成

在给定设计目标（结合特定靶蛋白的 binder、具备特定活性位点的酶、对称纳米粒子等）后，使用 RFdiffusion 或 RFdiffusion2 从噪声中迭代去噪生成满足约束的蛋白质骨架。典型参数：长度 50–400 个氨基酸，单次生成数十至数千条骨架。

### 3.2 阶段二：序列设计

使用 ProteinMPNN 对每条骨架在约束下生成多条候选氨基酸序列（每条骨架通常生成 8–32 条序列）。若设计目标涉及小分子、核酸或金属离子的结合，应改用 LigandMPNN 以显式建模非蛋白原子上下文，可将序列回收率提升 **10–40%**。

### 3.3 阶段三：结构验证（自洽过滤）

将设计序列输入独立的结构预测模型（AlphaFold2 / AlphaFold3 / ESMFold），若预测结构与设计骨架的 **scTM-score ≥ 0.8**（或 RMSD < 2 Å）则视为高质量设计。这一步是核心过滤环节：传统方法中，通过率往往不足 1%；使用 RFdiffusion + ProteinMPNN 组合后，通过率可提升至 **10–50%**，大幅减少实验验证工作量。

### 3.4 阶段四：功能注释与适应性预测

通过 ESM3 的功能标记提示、DeepGO-SE 的 GO 术语预测，以及 ProteinGym 上预训练的零样本适应性预测模型，对候选设计进行功能筛选和突变效应预估，进一步缩减需要湿实验验证的候选集合。

---

## 模型对比表

| 模型 | 类别 | 主要功能 | 输入 | 输出 | 开源情况 | 关键性能指标 |
|------|------|---------|------|------|---------|------------|
| [AlphaFold3](https://www.nature.com/articles/s41586-024-07487-w) | 结构预测 | 蛋白质 / DNA / RNA / 小分子 / 离子联合结构预测 | 序列 + SMILES | 三维原子坐标 | 学术免费（权重） | PoseBusters 成功率 76%，比传统方法高 50% |
| [Chai-1](https://github.com/chaidiscovery/chai-lab) | 结构预测 | 多模态生物分子结构预测 + 实验约束提示 | 序列 / SMILES / 实验约束 | 三维坐标 + 置信度 | 完全开源 | PoseBusters 77%；蛋白质多聚体 DockQ 0.751（优于 AF-Multimer） |
| [Boltz-1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11601547/) | 结构预测 | 生物分子互作建模 | 序列 + SMILES | 三维结构 | 完全开源 | 性能与 AlphaFold3 相当 |
| [ESMFold](https://www.science.org/doi/10.1126/science.ade2574) | 结构预测 | 单序列快速结构预测（无需 MSA） | 单条氨基酸序列 | 三维坐标 + pLDDT | 完全开源 | 速度比 AlphaFold2 快 ~60 倍；适合大规模筛查 |
| [RFdiffusion](https://www.bakerlab.org/2023/07/11/diffusion-model-for-protein-design/) | 骨架生成 | 从头蛋白质骨架设计（binder / 酶 / 对称体） | 功能约束 / 靶蛋白结构 | 骨架坐标（.pdb） | 完全开源 | 皮摩尔级结合剂；实验成功率提升 10–100 倍 |
| [RFdiffusion2](https://www.ipd.uw.edu/2025/04/introducing-rfdiffusion2/) | 骨架生成（酶） | 酶活性位点脚手架设计 | 化学反应描述 / Theozyme | 带活性位点骨架 | 开源（学术） | AME 基准全 41/41；前最优方法仅 16/41 |
| [ProteinMPNN](https://www.science.org/doi/10.1126/science.add2187) | 序列设计 | 固定骨架序列设计（单链 / 多链 / 对称） | 骨架坐标（.pdb） | 氨基酸序列（FASTA） | 完全开源 | 序列回收率 ~50–55%；1–2 秒 / 条（GPU） |
| [LigandMPNN](https://www.nature.com/articles/s41592-025-02626-1) | 序列设计 | 含配体 / 核酸 / 金属的蛋白质序列设计 | 骨架 + 非蛋白原子 | 氨基酸序列 + 侧链构象 | 完全开源 | 小分子场景序列回收率 63.3%（ProteinMPNN 50.5%） |
| [ESM3](https://www.science.org/doi/10.1126/science.ads0018) | 多模态 PLM | 序列 / 结构 / 功能联合推理与生成 | 序列 / 结构 / 功能标记（任意组合） | 序列 / 结构 / 功能预测 | 1.4B 开源；98B 商用 | esmGFP：与最近自然荧光蛋白序列相似度仅 58%；pTM>0.8 |
| [ESM2](https://www.science.org/doi/10.1126/science.ade2574) | 蛋白质语言模型 | 序列嵌入（下游任务通用骨干） | 氨基酸序列 | 残基嵌入向量 | 完全开源（8M–15B） | 进化尺度预训练；广泛用于下游结构 / 功能任务 |
| [DeepGO-SE](https://www.nature.com/articles/s42256-024-00795-w) | 功能预测 | GO 本体功能注释（神经符号推理） | 氨基酸序列 | GO 功能标签 | 开源 | 蛋白质 - 蛋白质互作预测 AUROC 提升 0.12 |
| [ProteinGym](https://papers.nips.cc/paper_files/paper/2023/hash/cac723e5ff29f65e3fcbb0739ae91bee-Abstract-Datasets_and_Benchmarks.html) | 基准评估 | 蛋白质适应性预测基准 | 序列 + 突变 | 适应性得分 | 完全开源 | 2000+ DMS 数据集；零样本适应性预测黄金标准 |

---

## 实施建议

### 4.1 项目启动阶段：选型建议

**针对不同设计目标的推荐工具组合：**

| 设计场景 | 推荐骨架生成 | 推荐序列设计 | 推荐结构验证 | 备注 |
|---------|------------|------------|------------|------|
| 蛋白质结合剂（binder）设计 | RFdiffusion | ProteinMPNN | AlphaFold2 / Chai-1 | 成熟工作流，已有大量实验验证 |
| 含小分子酶 / 传感器设计 | RFdiffusion2 | LigandMPNN | AlphaFold3 | 明确配体时优先选用 |
| 新型酶活性位点设计 | RFdiffusion2 | LigandMPNN | AlphaFold3 | 仅需描述化学反应 |
| 大规模文库快速筛查 | ESM3 功能提示 | ESM3 / ProteinMPNN | ESMFold | 速度优先；pLDDT 作为初筛 |
| 多分子复合体 / 抗体设计 | — | ProteinMPNN | Chai-1 / AlphaFold3 | Chai-1 在抗体 - 抗原预测上表现突出 |
| 蛋白质适应性工程 | — | — | ESM2 嵌入 + ProteinGym 模型 | 突变效应零样本预测 |

### 4.2 计算基础设施建议

- **小规模探索**（< 100 设计）：Google Colab + Chai Discovery Lab Server + [AlphaFold Server](https://alphafold.ebi.ac.uk) 可满足需求，零本地 GPU 配置。
- **中规模设计活动**（100–10,000 设计）：推荐至少 4 × NVIDIA A100 80GB 节点，或使用云端 GPU（AWS / GCP / Azure）。
- **大规模工业级流水线**：建议在 HPC 集群上部署，结合 SLURM 作业调度与 Nextflow / Snakemake 工作流管理系统。

### 4.3 工作流集成建议

1. **使用 [OpenProtein.AI](https://news.mit.edu/2026/bringing-ai-driven-protein-design-tools-everywhere-0417) 等平台**：对于没有深度计算背景的生物学家，OpenProtein.AI 提供无代码界面、PoET-2 蛋白质语言模型及 API 接口，已被勃林格殷格翰等大型药企采用。
2. **建立"计算 → 实验"迭代循环**：以计算过滤后的候选库（通常 30–200 个序列）作为第一轮实验验证批次，用实验数据反馈更新模型或筛选策略。
3. **多模型集成验证**：结构验证步骤建议同时使用至少两种独立预测模型（如 AlphaFold3 + ESMFold），以降低单一模型幻觉导致的误选风险。
4. **版本控制和复现性**：使用 Docker 容器或 Conda 环境锁定模型版本；所有设计参数和随机种子需记录，确保计算可重现。

---

## 风险与局限性

### 5.1 模型幻觉与过度自信

AI 蛋白设计模型本质上是**生成式概率模型**，其输出在计算层面可能看似合理（高 pLDDT、高 scTM），但实际湿实验中可能无法折叠或不具备目标功能。模型置信度评分与真实实验成功率之间存在显著差距，应避免将高 pLDDT 直接等同于实验成功。

### 5.2 复杂靶点能力不足

正如行业观察者指出（[LinkedIn，2026](https://www.linkedin.com/posts/stefvangrieken_the-progress-in-de-novo-protein-design-is-activity-7419274074444455936-punz)），当前从头设计方法在结构数据稀缺的靶点上效果有限，包括：
- **离子通道**（跨膜拓扑复杂）
- **复杂 GPCR 类**（构象柔性大、表达困难）
- **多结构域大型蛋白**（长程相互作用难以建模）

### 5.3 训练数据偏差

所有现有模型均在公开蛋白质数据库（PDB、UniRef、UniProt）上训练，对进化上稀少或实验结构缺乏的蛋白质家族泛化能力有限。此外，可溶性单结构域蛋白训练数据远多于膜蛋白和大型复合体，导致模型在后者上表现较差。

### 5.4 开源与商业授权问题

- **AlphaFold3**：权重开放，但明确禁止商业使用；学术研究受少量限制。
- **Chai-1**：非商业免费，商业药物发现通过网络界面免费访问，但大规模商业部署需确认许可。
- **ESM3**（98B）：商业版本通过 EvolutionaryScale API 访问，开源版本为 1.4B 参数。
- **RFdiffusion / ProteinMPNN / LigandMPNN**：完全开源（MIT 许可），商业可用。

### 5.5 计算成本

大型模型（AlphaFold3、ESM3 98B）的单次推理成本较高，大规模工业流水线的计算成本不可忽视。ESMFold 或 Chai-1 单序列模式可作为初筛高效替代方案，在精度与速度之间取得平衡。

### 5.6 实验验证仍是决定性环节

据 [MIT News（2026）](https://news.mit.edu/2026/bringing-ai-driven-protein-design-tools-everywhere-0417)，尽管 AI 工具显著加速了候选库生成，实验验证（蛋白表达、纯化、功能测定、结构表征）仍是决定设计成败的最终环节，且通常是整个流程的时间和成本主要来源。

---

## 总结与展望

2026 年，AI 蛋白设计领域已从"概念验证"阶段进入"工程应用"阶段：

- **结构预测精度**已不再是核心瓶颈，重心转向生成式设计的质量、效率与可控性；
- **酶设计**（RFdiffusion2）和**配体结合蛋白设计**（LigandMPNN）取得突破性进展，正向临床应用转化；
- **多模态基础模型**（ESM3）开创了序列 - 结构 - 功能统一推理的新范式；
- **平台化工具**（OpenProtein.AI、Chai Discovery Lab 等）正在降低领域准入门槛，推动生物学家直接使用 AI 工具；
- 未来 2–3 年内，全原子从头设计能力（包括动态蛋白、变构调控蛋白）预计将成为下一个突破方向。

核心建议：**以 RFdiffusion + ProteinMPNN/LigandMPNN + AlphaFold3/Chai-1 作为标准起点工作流**，结合 ESM3 进行多模态功能引导，并始终维持与湿实验室的紧密迭代反馈循环。

---

## 参考文献

1. Abramson, J. et al. (2024). **Accurate structure prediction of biomolecular interactions with AlphaFold 3**. *Nature*, 630, 493–500. <https://www.nature.com/articles/s41586-024-07487-w>

2. Hayes, T. et al. (2025). **Simulating 500 million years of evolution with a language model**. *Science*, 371. <https://www.science.org/doi/10.1126/science.ads0018>

3. Watson, J.L. et al. (2023). **De novo design of protein structure and function with RFdiffusion**. *Nature*, 620, 1089–1100. <https://www.bakerlab.org/2023/07/11/diffusion-model-for-protein-design/>

4. Dauparas, J. et al. (2022). **Robust deep learning-based protein sequence design using ProteinMPNN**. *Science*, 378, 49–56. <https://www.science.org/doi/10.1126/science.add2187>

5. Dauparas, J. et al. (2025). **Atomic context-conditioned protein sequence design using LigandMPNN**. *Nature Methods*. <https://www.nature.com/articles/s41592-025-02626-1>

6. Institute for Protein Design (2025). **Introducing RFdiffusion2**. <https://www.ipd.uw.edu/2025/04/introducing-rfdiffusion2/>

7. Institute for Protein Design (2025). **Introducing LigandMPNN**. <https://www.ipd.uw.edu/2025/03/introducing-ligandmpnn/>

8. Chai Discovery Team (2024). **Chai-1: Decoding the molecular interactions of life**. *bioRxiv*. <https://github.com/chaidiscovery/chai-lab>

9. Wohlwend, J. et al. (2024). **Boltz-1: Democratizing Biomolecular Interaction Modeling**. *bioRxiv*. <https://pmc.ncbi.nlm.nih.gov/articles/PMC11601547/>

10. Lin, Z. et al. (2023). **Evolutionary-scale prediction of atomic-level protein structure with a language model (ESMFold)**. *Science*, 379, 1123–1130. <https://www.science.org/doi/10.1126/science.ade2574>

11. EvolutionaryScale (2024). **ESM3: Simulating 500 million years of evolution with a language model** (blog post). <https://www.evolutionaryscale.ai/blog/esm3-release>

12. Kulmanov, M. & Hoehndorf, R. (2024). **Protein function prediction as approximate semantic entailment (DeepGO-SE)**. *Nature Machine Intelligence*. <https://www.nature.com/articles/s42256-024-00795-w>

13. Notin, P. et al. (2023). **ProteinGym: Large-Scale Benchmarks for Protein Fitness Prediction and Design**. *NeurIPS 2023*. <https://papers.nips.cc/paper_files/paper/2023/hash/cac723e5ff29f65e3fcbb0739ae91bee-Abstract-Datasets_and_Benchmarks.html>

14. Yim, J. et al. (2023). **SE(3) diffusion model with application to protein backbone generation (FrameDiff)**. *arXiv*. <https://arxiv.org/abs/2302.02277>

15. Elliott, L.G. et al. (2025). **ABCFold: easier running and comparison of AlphaFold 3, Boltz-1, and Chai-1**. *Bioinformatics Advances*, 5(1), vbaf153. <https://academic.oup.com/bioinformaticsadvances/article/5/1/vbaf153/8176613>

16. MIT News (2026). **Bringing AI-driven protein-design tools to biologists everywhere (OpenProtein.AI)**. <https://news.mit.edu/2026/bringing-ai-driven-protein-design-tools-everywhere-0417>

17. Isomorphic Labs / Google DeepMind (2024). **AlphaFold 3 predicts the structure and interactions of all of life's molecules**. <https://www.isomorphiclabs.com/articles/alphafold-3-predicts-the-structure-and-interactions-of-all-of-lifes-molecules>

18. AlphaFold Protein Structure Database. <https://alphafold.ebi.ac.uk>

19. DataM Intelligence (2026). **AI Protein Design Market Forecast and Industry Trends 2033**. <https://www.datamintelligence.com/research-report/ai-protein-design-market>

20. Nature News (2024). **AI protein-prediction tool AlphaFold3 is now more open**. <https://www.nature.com/articles/d41586-024-03708-4>

---

*本报告基于公开来源信息编写，不包含任何私有或机密数据。所有引用模型均为公开发布的学术研究成果或开源项目。*
