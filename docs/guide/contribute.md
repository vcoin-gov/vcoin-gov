# 贡献指南

> 你只需要会打字。不用装软件，不用懂代码，不用学 git。

## 先搞清楚三件事（1 分钟）

**这个站是怎么来的。** 它就是一堆 Markdown 文本文件，存在 GitHub 上，每次有人改动就自动重新排版成网页。你改文字 = 网站跟着变。

**三个词，够用了：**

| 词 | 人话 |
| --- | --- |
| 仓库 | 云端的一个文件夹，装着这个站的全部源文件 |
| Markdown | 一种极简排版法。`#` 开头是标题，`-` 开头是列表，`**加粗**` 是加粗。跟微信打字差不多 |
| PR（Pull Request） | 「我改好了，请合并」的请求。有人点同意，你的内容才会上线 |

**你不需要理解 git。** 下面的方式一全程在网页上点，一次命令都不用敲。

---

## 方式一：在网页上改（推荐，零安装）

### 第一次操作，对着做

**第 1 步**　打开 <https://vcoin-gov.github.io/vcoin-gov/>，用左侧菜单找到你负责的那一页。

**第 2 步**　拉到页面最底部，点那行「**在 GitHub 上编辑此页**」。

**第 3 步**　如果没登录，GitHub 会让你登录或注册。没账号就注册一个，免费，两分钟。

**第 4 步**　登录后可能出现一个页面让你 Fork。**看到就点绿色的 `Fork` 按钮。** 这只是把仓库复制一份到你名下，原站不受任何影响。

**第 5 步**　现在进入编辑界面。上半部分是文本，点 `Preview` 标签能看排版效果。

**第 6 步**　直接改文字。想确认效果就切到 `Preview` 看。

**第 7 步**　改完点右上角绿色的 **`Commit changes...`**。

**第 8 步**　弹出的小窗口里：

- 第一行填一句话，比如「补充帮信罪司法解释」
- 下面选 **`Create a new branch for this commit and start a pull request`**
- 点绿色 **`Propose changes`**

**第 9 步**　新页面再点一次绿色 **`Create pull request`**。

**第 10 步**　标题改成 `[组别] 专题 - 动作`，比如 `[政策组] 国内法规 - 补充司法解释`，再点 **`Create pull request`**。

**完事。** 组长合并后约 1 分钟，网站上就能看到你的内容。

::: tip 记不住就记这一句
**点「在 GitHub 上编辑此页」→ 改字 → Commit changes → 一路点绿色按钮。**
:::

### 以后再改就快了

已经 Fork 过、账号也登录着，第 3、4 步直接跳过，从改字开始，两三分钟结束。

### 想改别人写的内容

一样的流程，不需要先问谁。提了 PR 之后，原作者和组长都能看到你改了什么。

---

## 方式二：不写文档，只交素材

手上有法规原文、通报链接、案例、数据集，但不想自己排版——用这个。

1. 打开 <https://github.com/vcoin-gov/vcoin-gov/issues/new?template=content.md>
2. 按模板填：属于哪个专题、材料是什么、建议放哪页
3. 提交，等对应成员整理上站

**不用 Fork，不用改文件。** 适合临时甩个链接过来。

---

## 方式三：本地写（想边写边看效果）

适合一次要写很多、或者需要频繁预览排版的情况。

```bash
# 1. 克隆到本地
git clone https://github.com/vcoin-gov/vcoin-gov.git
cd vcoin-gov

# 2. 装依赖（已配国内镜像源，可直接装）
npm install

# 3. 启动预览，浏览器打开 http://localhost:5173
npm run dev
```

改文件保存即自动刷新，看完按 `Ctrl + C` 停止。

::: warning 这一步需要装 Node.js
没装过去 <https://nodejs.org/> 下 LTS 版，一路下一步即可。**装不上或报错就退回方式一**，网页改完全一样。
:::

---

## 我该写哪一页

| 你负责的内容 | 文件路径 | 网址 |
| --- | --- | --- |
| 国内法规、司法解释、指导案例 | `docs/policy/domestic-regulation.md` | [/policy/domestic-regulation](/policy/domestic-regulation) |
| 境外监管、MiCA、美国框架 | `docs/policy/overseas-regulation.md` | [/policy/overseas-regulation](/policy/overseas-regulation) |
| 公开通报案例库 | `docs/policy/cases.md` | [/policy/cases](/policy/cases) |
| 治理痛点 | `docs/policy/pain-points.md` | [/policy/pain-points](/policy/pain-points) |
| 链上基础知识 | `docs/onchain/basics.md` | [/onchain/basics](/onchain/basics) |
| 异常地址特征 | `docs/onchain/address-features.md` | [/onchain/address-features](/onchain/address-features) |
| 链路可视化 | `docs/onchain/visualization.md` | [/onchain/visualization](/onchain/visualization) |
| 链上分析工具 | `docs/onchain/tools.md` | [/onchain/tools](/onchain/tools) |
| 开源项目调研 | `docs/tech/oss-projects.md` | [/tech/oss-projects](/tech/oss-projects) |
| 检测模型与原型 | `docs/tech/detection-model.md` | [/tech/detection-model](/tech/detection-model) |
| 术语 | `docs/glossary/terms.md` | [/glossary/terms](/glossary/terms) |
| 数据源、文献、链接 | `docs/glossary/resources.md` | [/glossary/resources](/glossary/resources) |

**内容太多一页装不下**：在同目录新建文件（如 `docs/onchain/mixer-cases.md`），原页面顶部加一句跳转文字 `详见 [xxx](./mixer-cases)`，然后告诉组长加菜单链接（改 `config.mts` 里的 `sidebar`，不熟就别自己动）。

---

## 页面开头有段固定格式，别动

每个 md 文件最上面都有这一段，**位置和格式固定**，只需要改冒号后面的字：

```markdown
---
title: 页面标题
---

<div class="doc-meta">
  <span class="owner">负责人：@你的昵称</span>
  <span class="doing">状态：进行中</span>
</div>
```

状态三个选一个，只改英文部分：

| 写法 | 显示 |
| --- | --- |
| `<span class="todo">` | 待启动（橙色） |
| `<span class="doing">` | 进行中（蓝色） |
| `<span class="done">` | 已发布（绿色） |

::: tip 只加内容，别删结构
页面里已有的小标题是「这里该写什么」的清单。你写完某一节，把这节的提示文字换成实际内容，**标题保留**。
:::

---

## 写作规范

::: warning 六条硬性要求
1. **结论先行** —— 第一段就给结论，别铺垫背景
2. **表格优先** —— 能列表就别写长段落
3. **标来源** —— 法条给条号，案例给链接，链上数据给地址或哈希
4. **标可信度** —— 用【事实】【推断】【待验证】区分，别让人把推测当定论
5. **不写可操作手法** —— 讲识别特征，不写规避步骤
6. **不写真实身份信息** —— 涉案人员一律脱敏
:::

格式上的小事：

- `##` 是页面主标题，`###` 是小节，别跳级
- 地址、哈希、代码用反引号包起来：`` `0x1234...abcd` ``
- 强调用 `**加粗**`，别整段加粗，加粗多了等于没加粗
- 分隔线 `---` 用来切大块，别滥用

---

## 提交信息怎么写（只走方式三才需要）

```bash
git checkout -b docs/onchain-address-features   # 建分支，命名：docs/<组>-<专题>
git add .
git commit -m "docs(onchain): 补充小额拆分特征的识别阈值"
git push origin docs/onchain-address-features
```

格式就三种，照抄结构改内容：

```
docs(policy): 补充帮信罪司法解释的明知认定情形
docs(onchain): 修正聚类术语的表述
docs(tech): 新增 TRON 数据拉取 demo 说明
```

PR 标题：

```
[政策组] 国内法规 - 补充司法解释摘录
[链上组] 异常地址特征 - 新增周期性归集判据
```

PR 描述写三行就够：**改了什么 / 依据是什么 / 还有哪些没做完**。

---

## 合并前扫一眼

- [ ] 在 `Preview`（或本地预览）里看过效果，没乱版
- [ ] 结论都有来源，推测已标【推断】
- [ ] 页面顶部的状态标签和实际进度对得上
- [ ] 图片能正常显示
- [ ] 没有贴未公开的案件材料、涉案人员真实信息

---

## 出问题了看这里

| 现象 | 原因 | 怎么办 |
| --- | --- | --- |
| 点「在 GitHub 上编辑此页」让我登录 | 没登录 GitHub | 注册或登录，免费 |
| 出现 `Fork` 字样 | 你还不是仓库成员 | 点 Fork 就行，不影响原站 |
| 改完不知道点哪 | 还没提交 | 找右上角绿色 `Commit changes...` |
| 提交完发现改错了 | 只是错字，不是灾难 | 重新点编辑再改一遍提第二个 PR，或直接告诉组长 |
| PR 挂了好几天没人理 | 组长没看到 | 群里 @ 他，附上 PR 链接 |
| 图片显示不出来 | 路径写错 | 见下方说明 |
| 本地 `npm install` 报错 | 网络或 Node 版本 | 换源 `npm config set registry https://registry.npmmirror.com`；搞不定就用方式一 |
| 合并了但网站没变 | 构建失败或缓存 | 看 [Actions](https://github.com/vcoin-gov/vcoin-gov/actions) 有没有红灯，没有就等 1 分钟刷新 |

**图片怎么放：**

1. 图片传到 `docs/public/assets/<页面名>/` 目录（网页上也能传：进到该目录点 `Add file` → `Upload files`）
2. 正文里这样引用：`![说明文字](/assets/<页面名>/fig-01.png)`

注意路径写 `/assets/...`，**不要**写成 `docs/public/assets/...`，也不要在结尾加 `.html`。

---

## 合并之后发生什么

1. 组长点合并 → 触发自动构建
2. 约 1 分钟全网可见，手机刷新就能看到
3. 页面底部的「最后更新」自动变成这次提交的时间，不用手动改

构建失败会在这里显示红灯：<https://github.com/vcoin-gov/vcoin-gov/actions>

---

## 公开仓库须知

::: warning 这个仓库是公开的
你提交的每一次修改、每一条 Issue 和 PR 讨论，都会永久记录，任何人都能查到。**草稿推上去就等于公开，没有「先私有后公开」这个中间态。**
:::

### 这些内容绝对不要提交

| 不要提交 | 原因 |
| --- | --- |
| 未公开的案件材料、内部通报 | 涉密风险，违反研究红线 |
| 涉案人员真实姓名、身份证、手机号 | 个人信息，公开即违规 |
| 截图里的聊天记录、账户余额、真实姓名 | 图最容易被忽略，提交前逐张看 |
| 单位内部联系人、工作群二维码 | 与内容无关，但会长期公开 |
| 自己的完整履历、所在单位 | 会被搜索引擎收录 |

### 邮箱匿名化（可选）

不介意邮箱公开就跳过——组长的邮箱一直挂在公开仓库里，没什么问题。

介意的话，本地提交前配一次：

```bash
git config user.email "你的GitHubID+你的用户名@users.noreply.github.com"
```

这个地址在 <https://github.com/settings/emails> 勾选 **Keep my email addresses private** 后能看到。**只对之后的提交生效。**

### 一个额外的好处

公开仓库会自动开启密钥扫描。万一误把 token、密钥提交上去，GitHub 会告警。看到告警要立刻删掉并重新生成——**光删文件不够，历史里还在**。

---

## 常见问题

**Q：我的群昵称和 GitHub 账号不一样，怎么对上人？**
去 [成员与分工](./team) 把自己那行的「_待填_」改成 GitHub 用户名，之后 Review 就按这个认人。

**Q：能不能跳过 PR 直接改？**
不建议。PR 有两个好处：有人帮你挑错，每次改动留下记录。紧急改错别字可以直接改，别养成习惯。

**Q：一页内容太多写不下怎么办？**
拆页。新建文件，原页面顶部加「详见 xxx」链接，菜单交给组长加。

**Q：能不能贴大段法条原文？**
可以，但必须配「这条解决什么问题、适用边界在哪」。**只贴原文不解读等于没写。**

**Q：写完发现别人已经写了一样的内容？**
PR 里能直接看到冲突。两边合并成一段，别各写一份。提交前先扫一眼对方写了什么。

---

## 本项目的许可

站点内容采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans) 许可：可以自由转载、改编，但须署名、不得商用、改编后须以相同方式共享。完整法律文本见仓库根目录 `LICENSE`。
