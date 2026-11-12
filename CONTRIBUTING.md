# 贡献指南

完整说明见站点上的 [贡献指南](docs/guide/contribute.md)，这里只放最短路径。

## 三种参与方式

**只改文字**（不装任何环境）
打开页面 → 点右下角「在 GitHub 上编辑此页」→ 改完提交 → 选「Create a new branch and start a pull request」。

**本地写**（想边写边看）
```bash
git clone <repo-url>
cd vcoin-gov
npm install
npm run dev
```

**提素材但不写文档**
用仓库的 Issue 模板提交，注明属于哪个专题，由对应成员整理落页。

## 提交规范

分支名：`docs/<组>-<专题>`，例如 `docs/onchain-address-features`

提交信息：`docs(范围): 做了什么`
```
docs(policy): 补充帮信罪司法解释的明知认定情形
docs(onchain): 修正聚类术语的表述
```

PR 标题：`[组别] 专题 - 动作`
```
[政策组] 国内法规 - 补充司法解释摘录
[链上组] 异常地址特征 - 新增周期性归集判据
```

## 合并前自查

- [ ] 本地 `npm run dev` 渲染正常
- [ ] 结论有来源，推断已标注【推断】【待验证】
- [ ] 页面顶部状态标签与实际进度一致
- [ ] 图片在 `docs/public/assets/` 下且能显示
- [ ] 未上传未公开的案件材料与个人信息

## 内容红线

1. 只用公开信息
2. 结论标来源
3. 不写可操作的规避手法
4. 涉案人员真实身份信息一律脱敏

详见 [docs/guide/intro.md](docs/guide/intro.md) 的「研究边界」。
