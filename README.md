# 虚拟币治理打击技术开源社区

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans)
[![Docs](https://img.shields.io/badge/docs-vcoin--gov.github.io-0ea5e9.svg)](https://vcoin-gov.github.io/vcoin-gov/)

聚焦比特币、稳定币、各类土狗币、跑分、资金盘、跨境涉诈虚拟币链路，围绕**风险识别、链路特征、治理难点、技术研判、防控对策、宣传预警**开展协同研究的公开知识库。

> 内容仅用于合规研究与治理技术交流，不构成法律意见。

## 在线访问

站点地址：<https://vcoin-gov.github.io/vcoin-gov/>

## 这是什么

不是新闻聚合，是可复用的研判知识库。每条结论都要能回答：**依据是什么、怎么验证、什么场景下不成立**。

## 分三个组

| 组 | 内容 | 页面 |
| --- | --- | --- |
| 政策与法规研判组 | 国内法规定性、境外监管差异、公开通报案例、治理痛点 | [`docs/policy/`](docs/policy/) |
| 链上特征与情报研判组 | 基础链上知识、异常地址特征、链路可视化、工具对比 | [`docs/onchain/`](docs/onchain/) |
| 技术检测与原型开发组 | 开源项目调研、检测模型与原型 | [`docs/tech/`](docs/tech/) |

## 本地预览

```bash
npm install
npm run dev      # http://localhost:5173
```

构建：

```bash
npm run build    # 输出到 docs/.vitepress/dist
npm run preview  # 本地预览构建结果
```

## 怎么写内容

看 [`docs/guide/contribute.md`](docs/guide/contribute.md)。核心就一句：**只写 Markdown，提交 PR，自动上线。**

不想装环境也可以——在网页上点「在 GitHub 上编辑此页」直接改。

## 目录结构

```
.
├── docs/
│   ├── .vitepress/          # 站点配置与主题
│   ├── guide/               # 项目说明、分工、贡献指南、模板
│   ├── policy/              # 一、政策与法规研判
│   ├── onchain/             # 二、链上特征与情报研判
│   ├── tech/                # 三、技术检测与原型开发
│   ├── glossary/            # 术语与资源
│   └── public/              # 静态资源（图片放 assets/）
├── .github/workflows/       # 自动构建部署
└── package.json
```

## 技术栈

VitePress 1.x + GitHub Pages（Actions 自动构建）。选它的理由：Markdown 即内容，非技术人员只需写 md；自带全文搜索与深色主题；提交即发布。

## 协作方式

1. 在 [成员与分工](docs/guide/team.md) 找到自己的专题
2. 按 [调研文档模板](docs/guide/template.md) 写内容
3. 提 PR，组长 Review 后合并，约 1 分钟自动上线

## 更新日志

页面底部的「最后更新」由 git 提交时间自动生成，无需手工维护。

## 许可

本站全部文字、表格与图表采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans) 许可协议。

- **署名** —— 转载须注明来源与本许可链接，并说明是否修改
- **非商业性使用** —— 不得用于商业目的
- **相同方式共享** —— 改编后须以相同许可分发

法律文本以根目录 [LICENSE](LICENSE) 中的英文原文为准。

## 免责声明

本站内容仅用于合规研究与治理技术交流，不构成法律意见。涉及具体案件的研判结论须以办案单位正式认定为准。
