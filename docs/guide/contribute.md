# 贡献指南

> 前提：有 GitHub 账号，会用 git 的基本操作（clone / branch / commit / push / PR）。不熟的话先花半小时过一遍 Pro Git 前三章，比在这里看十遍都值。

## 一、一次完整流程

```bash
# 1. 首次：克隆并装依赖
git clone https://github.com/vcoin-gov/vcoin-gov.git
cd vcoin-gov
npm install

# 2. 每次动手前：同步主分支（这一步不能省）
git checkout main
git pull origin main

# 3. 开分支，永远在分支上改
git checkout -b docs/onchain-address-features

# 4. 写内容，本地预览 http://localhost:5173
npm run dev

# 5. 提交（只 add 你改的那个文件）
git add docs/onchain/address-features.md
git commit -m "docs(onchain): 补充小额拆分特征的识别阈值"

# 6. 推送
git push -u origin docs/onchain-address-features
```

推送后 GitHub 会给出开 PR 的链接。PR 标题写 `[组别] 专题 - 动作`，描述写三行：改了什么 / 依据是什么 / 还有什么没做完。

::: tip 应急改错别字
只有改错别字、调格式这种一字之差的修正，才用网页点「在 GitHub 上编辑此页」。**实质内容一律走本地分支 + PR**，否则历史里一堆无意义的网页提交，回溯起来很痛苦。
:::

## 二、防冲突：四条铁律

冲突几乎都来自「多个人碰了同一块地方」。守好这四条，基本不会撞。

### 铁律 1 · 只改你负责的那一页

| 文件 / 目录 | 谁能改 |
| --- | --- |
| `docs/<组>/<你负责的那篇>.md` | 你，随便改 |
| 同组其他人负责的页面 | 别直接改，在 PR 里提建议，让对方改 |
| `docs/.vitepress/config.mts`（菜单、导航） | 组长 |
| `docs/.vitepress/theme/custom.css` | 组长 |
| `package.json` / `package-lock.json` | 组长 |
| `.github/`（工作流、Issue 模板） | 组长 |
| `README.md` / `LICENSE` | 组长 |
| `docs/guide/`（本页、分工、模板） | 组长 |

**要加新页面**：自己在目录下建 md 文件，PR 里说明「新增页面，需要加菜单」，由组长改 `config.mts`。不要自己动那个文件——9 个人都想加菜单，必冲突。

**不要顺手 `npm install` 后提交 `package-lock.json`**，除非组长要求升依赖。不同 npm 版本生成的 lock 文件不一样，提交上去全是无意义 diff。

### 铁律 2 · 一个 PR 只做一件事

改一篇文档、修一个错误、加一节内容——分开提。攒了八件事的大 PR 一旦冲突，解决起来是灾难。

### 铁律 3 · 提 PR 前先 rebase

```bash
git fetch origin
git rebase origin/main
```

有冲突现在解决，比在 PR 页面里解决容易得多。

### 铁律 4 · 主分支永远保持同步

每天开工前 `git pull origin main`。落后越多，冲突越大。

## 三、真撞了怎么办

| 情况 | 处理 |
| --- | --- |
| 同一段文字两边都改了 | 看谁的信息更全，合并成一段，别简单二选一 |
| 对方删了你保留的段落 | 先问为什么删，可能他掌握了新情况 |
| 表格同一行冲突 | 通常是你改的是旧版本，rebase 后以主分支为准，再重新加你的内容 |
| 看不明白冲突标记 | `<<<<<<<` 和 `>>>>>>>` 之间的两段是候选，`=======` 是分界。拿不准就群里问，别瞎删 |

```bash
# rebase 遇到冲突时的操作
# 1. 手动编辑文件，删掉冲突标记，留下正确内容
git add <冲突文件>
git rebase --continue

# 想放弃重来
git rebase --abort
```

## 四、写作规范

::: warning 六条硬性要求
1. **结论先行** —— 第一段就给结论，别铺垫背景
2. **表格优先** —— 能列表就别写长段落
3. **标来源** —— 法条给条号，案例给链接，链上数据给地址或哈希
4. **标可信度** —— 用【事实】【推断】【待验证】区分，别让人把推测当定论
5. **不写可操作手法** —— 讲识别特征，不写规避步骤
6. **不写真实身份信息** —— 涉案人员一律脱敏
:::

格式：

- `##` 是页面主标题，`###` 是小节，别跳级
- 地址、哈希、代码用反引号包起来：`` `0x1234...abcd` ``
- 加粗只用于关键结论，整段加粗等于没加粗
- 页面顶部那段 `doc-meta` 只改冒号后面的字，结构别动

## 五、我该写哪一页

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

## 六、提交与 PR 规范

分支名：

```
docs/<组>-<专题>
docs/onchain-address-features
docs/policy-cases
```

提交信息：

```
docs(policy): 补充帮信罪司法解释的明知认定情形
docs(onchain): 修正聚类术语的表述
docs(tech): 新增 TRON 数据拉取 demo 说明
fix(policy): 修正法释〔2024〕10 号的施行日期
```

一个提交只做一件事。把「补内容」「改错字」「调格式」混在一个 commit 里，review 的人没法看。

PR 标题：

```
[政策组] 国内法规 - 补充司法解释摘录
[链上组] 异常地址特征 - 新增周期性归集判据
```

## 七、主分支保护

`main` 已开启分支保护，规则如下：

| 规则 | 说明 |
| --- | --- |
| 禁止直接 push | 所有改动必须走 PR |
| 至少 1 人 approve | Review 通过才能合并 |
| CI 必须通过 | `build` 失败不允许合并 |
| 禁止 force push / 删除 | 历史不可改写 |
| 新提交后旧 approve 失效 | 改了代码要重新审 |

**为什么这么做**：不是为了卡流程，是为了三件事——冲突在合并前就被发现、每次改动都有记录可回溯、主分支永远处于可部署状态。

组长保留管理员豁免权，用于紧急修复。**但正常情况组长也走 PR**，豁免权只是保险丝，不是常规通道。

::: tip 只有 1 个协作者时怎么办
GitHub 不允许自己批准自己的 PR。在第二名协作者加入之前，组长开的 PR 会一直卡在 `Review required`。两个办法：

- 网页上：PR 页面底部会出现 **`Merge without waiting for requirements to be met`**（管理员专属按钮），点了直接合
- 命令行：`gh pr merge <编号> --squash --admin`

协作者到两人以上后，就别再用这个口子，正常互审。
:::

## 八、合并前自查

- [ ] `npm run dev` 本地预览正常，没乱版
- [ ] 只改了 `docs/` 下自己负责的文件（`git diff --stat` 确认）
- [ ] 结论都有来源，推测已标【推断】
- [ ] 图片已放到 `docs/public/assets/<页面名>/`，正文用 `/assets/...` 引用
- [ ] 没有未公开的案件材料、涉案人员真实信息
- [ ] 已经从主分支 rebase 过

## 九、出问题了

| 现象 | 怎么办 |
| --- | --- |
| `git push` 被拒绝 | 主分支保护生效，说明你直接推 main 了，改成推分支 |
| PR 显示 "This branch has conflicts" | 按第三节 rebase，或点 GitHub 的 `Resolve conflicts` 手改 |
| CI 红灯 | 点进 Actions 看日志，多数是 Markdown 语法错或死链 |
| 死链报错 `dead link found` | 链接指向的文件不存在，改成正确路径；不想当链接就用反引号包起来 |
| 图片不显示 | 路径要写 `/assets/...`，不是 `docs/public/assets/...` |
| `npm install` 报错 | 换源 `npm config set registry https://registry.npmmirror.com`；确认 Node ≥ 18 |
| PR 没人审 | 群里 @ 组长，附 PR 链接 |
| 合并了但网站没变 | 看 [Actions](https://github.com/vcoin-gov/vcoin-gov/actions) 有没有红灯，没有就等 1 分钟刷新 |

## 十、公开仓库须知

::: warning 仓库是公开的
每次提交、每条 Issue 和 PR 讨论永久可查。**草稿推上去就等于公开。**
:::

不要提交：

| 内容 | 原因 |
| --- | --- |
| 未公开的案件材料、内部通报 | 涉密风险，违反研究红线 |
| 涉案人员真实姓名、身份证、手机号 | 个人信息，公开即违规 |
| 截图里的聊天记录、账户余额、真实姓名 | 图最容易被忽略，提交前逐张看 |
| 单位内部联系人、工作群二维码 | 与内容无关，但会长期公开 |

邮箱匿名化可选，介意就配一次（只对之后的提交生效）：

```bash
git config user.email "你的GitHubID+你的用户名@users.noreply.github.com"
```

地址在 <https://github.com/settings/emails> 勾选 **Keep my email addresses private** 后可见。

## 十一、许可

本站内容采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans) 许可：可自由转载、改编，须署名、不得商用、改编后以相同方式共享。完整文本见仓库根目录 `LICENSE`。
