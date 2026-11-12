# 贡献指南

本页是全集：从拿到仓库到内容上线，照着做就行。**不需要懂前端**，只写 Markdown。

## 一、最快路径：不装任何环境

如果只是改一篇已有页面的内容：

1. 打开要改的页面，点右下角「在 GitHub 上编辑此页」
2. 在 GitHub 网页编辑器里直接改 Markdown
3. 页面底部填一句改动说明 → 选 **Create a new branch and start a pull request**
4. 提 PR，等组长合并

这样改完自动上线，本地什么都不用装。

## 二、本地预览（想边写边看效果）

```bash
# 1. 克隆
git clone https://github.com/Fiagainster/vcoin-gov.git
cd vcoin-gov

# 2. 装依赖（已配 npmmirror 源，国内可直接装）
npm install

# 3. 起本地预览，浏览器打开 http://localhost:5173
npm run dev
```

改文件保存即热更新，看完 `Ctrl+C` 停掉。

## 三、文件放哪

| 你负责的内容 | 文件路径 |
| --- | --- |
| 国内法规、司法解释、指导案例 | `docs/policy/domestic-regulation.md` |
| 境外监管、MiCA、美国框架 | `docs/policy/overseas-regulation.md` |
| 公开通报案例库 | `docs/policy/cases.md` |
| 治理痛点 | `docs/policy/pain-points.md` |
| 链上基础知识 | `docs/onchain/basics.md` |
| 异常地址特征 | `docs/onchain/address-features.md` |
| 链路可视化 | `docs/onchain/visualization.md` |
| 链上分析工具 | `docs/onchain/tools.md` |
| 开源项目调研 | `docs/tech/oss-projects.md` |
| 检测模型与原型 | `docs/tech/detection-model.md` |
| 术语 | `docs/glossary/terms.md` |
| 数据源、文献、链接 | `docs/glossary/resources.md` |

一个专题内容太多，就在同目录下拆新文件（如 `docs/onchain/mixer-cases.md`），然后到 `docs/.vitepress/config.mts` 的 `sidebar` 里加一行链接。

## 四、新建页面的头部

每个 md 文件开头必须有这段（`---` 之间）：

```markdown
---
title: 页面标题
---

<div class="doc-meta">
  <span class="owner">负责人：@你的昵称</span>
  <span class="doing">状态：进行中</span>
</div>
```

状态三选一：`todo`（待启动）、`doing`（进行中）、`done`（已发布）。

**已有页面不要动 frontmatter 以外的公共结构**，只往正文里加内容。

## 五、写作规范

::: warning 硬性要求
- **结论先行**：第一段就给出结论，别铺垫。
- **表格优先**：能列表格就别写长段落。
- **标来源**：法条给条号，案例给通报链接，链上数据给地址/交易哈希。
- **标可信度**：用【事实】【推断】【待验证】区分，别让读者把推测当定论。
- **不写可操作手法**：讲识别特征，不写规避步骤。
:::

格式细节：

- 二级标题 `##` 是页面主骨架，三级 `###` 用于具体条目
- 代码、地址、哈希一律用反引号包裹，如 `0x1234...abcd`
- 图放 `docs/public/assets/<页面名>/`，正文用相对路径引用：

```markdown
![资金树示例](/assets/visualization/fund-tree-01.png)
```

## 六、提交与 PR

```bash
# 建分支，命名：docs/<组>-<专题>
git checkout -b docs/onchain-address-features

# 改完提交，message 格式：docs(范围): 做了什么
git add .
git commit -m "docs(onchain): 补充小额拆分特征的识别阈值"
git push origin docs/onchain-address-features
```

然后在 GitHub 上开 PR，标题格式：

```
[链上组] 异常地址特征 - 补充小额拆分识别规则
```

PR 描述里写三行就够：**改了什么 / 依据是什么 / 还有哪些没做**。

## 七、合并前自查

- [ ] 本地 `npm run dev` 能看到效果，没有渲染错乱
- [ ] 所有结论都有来源，推断已标注
- [ ] 页面顶部状态标签和实际进度一致
- [ ] 图片已放进 `docs/public/assets/` 并确认能显示
- [ ] 没有把案件原始敏感材料（未公开笔录、内部通报、个人信息）传上来

## 八、合入后发生什么

合并到 `main` 后自动触发 GitHub Actions 构建，约 1 分钟站点更新。页面底部的「最后更新」随 git 提交时间自动变化。

构建失败会在这里看到红灯：<https://github.com/Fiagainster/vcoin-gov/actions>

## 九、常见问题

**Q：我的群昵称和 GitHub 账号不一样，怎么对上人？**
去 [成员与分工](./team) 把自己的 GitHub 账号填进对应行，之后 Review 就按这行认人。

**Q：能不能直接 push 到 main？**
建议不。走 PR 有两个好处：有人帮你挑错，且每次改动留下记录。紧急修错别字可以直接改，但别养成习惯。

**Q：内容涉及具体案件细节能不能写？**
只写已公开的部分。未公开的笔录、内部通报、涉案人员真实身份信息一律不写。案例统一用「某地某案」的脱敏写法 + 公开通报链接。
