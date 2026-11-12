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
git clone https://github.com/vcoin-gov/vcoin-gov.git
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

构建失败会在这里看到红灯：<https://github.com/vcoin-gov/vcoin-gov/actions>

## 九、常见问题

**Q：我的群昵称和 GitHub 账号不一样，怎么对上人？**
去 [成员与分工](./team) 把自己的 GitHub 账号填进对应行，之后 Review 就按这行认人。

**Q：能不能直接 push 到 main？**
建议不。走 PR 有两个好处：有人帮你挑错，且每次改动留下记录。紧急修错别字可以直接改，但别养成习惯。

**Q：内容涉及具体案件细节能不能写？**
只写已公开的部分。未公开的笔录、内部通报、涉案人员真实身份信息一律不写。案例统一用「某地某案」的脱敏写法 + 公开通报链接。

---

## 十、公开仓库须知

::: warning 先看这一条
**本仓库是公开的。** 你提交的每一次 commit、每一条 Issue 和 PR 讨论，都会永久记录在 git 历史里，任何人（包括搜索引擎）都能查到。写之前先想一下：这段东西被陌生人看到，有没有问题。
:::

### 1. 邮箱匿名化（可选）

如果你不介意邮箱公开，这节可以跳过——组长本人的邮箱就一直在公开仓库里。

介意的话，git 默认用你的真实邮箱，它会直接进公开历史：

```bash
# 只看本仓库，不影响你其他项目
git config user.email "你的GitHubID+你的用户名@users.noreply.github.com"
```

**怎么拿到这个地址**：

1. 打开 <https://github.com/settings/emails>
2. 勾选 **Keep my email addresses private**
3. 页面上会显示形如 `12345678+yourname@users.noreply.github.com` 的地址
4. 把它填进上面的命令

验证：

```bash
git config user.email          # 应显示 noreply 地址
git log -1 --format='%ae'      # 上一次提交实际用的邮箱
```

::: tip 已经提交过怎么办
改配置只对之后的提交生效，之前那些记录会一直留在历史里。想清掉只能 force push 重写，一般没必要——除非里面有你不想公开的真实信息。
:::

### 2. 这些内容不要提交

| 不要提交 | 原因 |
| --- | --- |
| 未公开的案件材料、内部通报 | 涉密风险，且违反研究红线 |
| 涉案人员真实姓名、身份证、手机号 | 个人信息，公开即违规 |
| 截图里的聊天记录、账户余额、真实姓名 | 图比文字更容易被忽略，提交前逐张看 |
| 单位内部联系人、工作群二维码 | 与内容无关，但会长期公开 |
| 自己的完整履历、所在单位 | 公开仓库会被搜索引擎收录 |

### 3. 草稿也是公开的

没有"先私有后公开"这个中间态——你推到仓库的东西当场就可见。

如果内容还没到能给人看的程度，两种做法：

- 本地写完再推（`npm run dev` 预览，满意了一次性提交）
- 或者干脆先推，但页面顶部状态标「进行中」，让读者知道这不是定稿

### 4. Issue 和 PR 讨论同样公开

不要在 Issue 里贴涉密截图或内部资料。需要私下沟通的，走群聊，不要走仓库。

### 5. 公开不代表没人管

公开仓库的另一个好处：GitHub 会自动开启密钥扫描，万一误提交了 token 或密钥会告警。看到告警立刻删除并重新生成密钥，**光删文件不够，历史里还在**。
