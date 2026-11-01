# TCCN正式修订文件（2026-11-01）

稿件编号：TCCN-TP-26-1155

题目：Hierarchical Load Balancing and Cooperative Beam Hopping for Multi-Satellite Direct-to-Cell LEO Networks

## 正式PDF

| 文件 | 内容 |
| --- | --- |
| Revised_Manuscript_Clean.pdf | 16页，最新英文论文修改稿，采用IEEE双栏格式。 |
| Revised_Manuscript_Marked_Reviewers.pdf | 17页，蓝色修订标注，页边标有对应审稿意见编号，覆盖全部19条意见。 |
| Response_to_Reviewers_EN.pdf | 21页，三位审稿人的英文回复合并为一个文件，保留原始意见并逐条回复。 |

回复中的页码以Clean版为准。标注版包含相同的论文内容和相同的章节、公式、图表编号；颜色标记会影响局部排版和分页。

## 回复中加入的材料

- 34处当前论文原文或公式摘录，采用蓝色排版。
- Table R1-1：热点反转实验结果，放在意见1.1下。
- 正文Fig. 9：ISA参数敏感性结果，放在意见1.2下。
- Fig. R1-4：真实天线和信道模型下的物理诊断，放在意见1.4下。
- 正文Fig. 2：当前MAPPO框架，放在意见2.4下。
- 正文Fig. 8：含Without coverage priors的消融结果，放在意见2.7下。
- 正文Fig. 7：含置信区间的性能对比，放在意见3.6下。

相关图表在其他意见中采用交叉指引，避免重复放置。动作延迟实验按已确认的汇总结果以文字报告。

## 可编辑文件

- Revised_Manuscript_Clean.tex：正式修改稿源文件，与当前工作论文源文件一致。
- Revised_Manuscript_Marked.tex：修订标注源文件。
- Response_to_Reviewers_EN.tex：合并回复的正式排版源文件。
- Response_to_Reviewers_EN.md：回复的可阅读文本。
- Fig files/、response_assets/：编译所需图件。
- IEEEtran.cls：论文文档类。
- Original_Manuscript.tex：生成修订标记时使用的原始稿件，仅供比对。
- Reviewer_Tag_Map.json：审稿意见编号与标注位置。
- Verification_Report.json、SHA256SUMS.txt：交付文件核验记录及校验值。

## 重新编译

在本目录运行：

```powershell
.\build.ps1
```

需要TeX Live中的pdflatex和xelatex、Times New Roman字体、Poppler的pdftotext，以及安装了pypdf和reportlab的Python。脚本优先使用当前电脑的Codex内置Python，也可通过`-Python`指定解释器。正式TeX文件与图件均使用相对路径。

重新编译结果写入build/；脚本随后更新根目录的三个正式PDF。重新编译后如需校验完整包，应重新生成校验值。

## 本版核对范围

已核对正文与回复中的共视度、共视重叠先验、全连接局部图、混合动作概率、奖励时间尺度、周期关联、RT TTL、图表编号、公式编号和参考文献编号。用户指定的三篇Cui等人的论文已纳入正文和参考文献。

已完成三份PDF的逐页可视检查、编译日志检查、正文内容一致性检查及全部19条审稿意见覆盖检查。
