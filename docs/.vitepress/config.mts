import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid(defineConfig({
  lang: 'zh-CN',
  title: '虚拟币治理打击技术开源社区',
  description: '聚焦虚拟货币涉诈涉赌链路的风险识别、链上特征、治理难点、技术研判与防控对策',
  base: '/vcoin-gov/',

  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/vcoin-gov/logo.svg' }],
    ['meta', { name: 'theme-color', content: '#0ea5e9' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: '虚拟币治理打击技术开源社区' }],
    ['meta', { property: 'og:description', content: '风险识别 · 链上特征 · 治理难点 · 技术研判 · 防控对策 · 宣传预警' }],
  ],

  lastUpdated: true,
  cleanUrls: false,
  metaChunk: true,

  markdown: {
    image: { lazyLoading: true },
    lineNumbers: false,
    config(md) {
      // 外链自动新窗口打开
      const defaultRender = md.renderer.rules.link_open ||
        ((tokens, idx, options, _env, self) => self.renderToken(tokens, idx, options))
      md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
        const href = tokens[idx].attrGet('href') || ''
        if (/^https?:\/\//.test(href)) {
          tokens[idx].attrSet('target', '_blank')
          tokens[idx].attrSet('rel', 'noopener noreferrer')
        }
        return defaultRender(tokens, idx, options, env, self)
      }
    },
  },

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: '虚拟币治理 · 技术社区',

    nav: [
      { text: '导览', items: [
        { text: '总目标与定位', link: '/guide/intro' },
        { text: '成员与分工', link: '/guide/team' },
        { text: '贡献指南', link: '/guide/contribute' },
        { text: '文档模板', link: '/guide/template' },
      ]},
      { text: '政策法规', link: '/policy/', activeMatch: '/policy/' },
      { text: '链上研判', link: '/onchain/', activeMatch: '/onchain/' },
      { text: '技术原型', link: '/tech/', activeMatch: '/tech/' },
      { text: '资源库', link: '/glossary/resources', activeMatch: '/glossary/' },
    ],

    sidebar: [
      {
        text: '项目导览',
        items: [
          { text: '总目标与定位', link: '/guide/intro' },
          { text: '成员与分工', link: '/guide/team' },
          { text: '贡献指南', link: '/guide/contribute' },
          { text: '调研文档模板', link: '/guide/template' },
        ],
      },
      {
        text: '一 · 政策与法规研判组',
        collapsed: false,
        items: [
          { text: '组内概览', link: '/policy/' },
          { text: '国内法规与司法解释', link: '/policy/domestic-regulation' },
          { text: '境外监管与跨境差异', link: '/policy/overseas-regulation' },
          { text: '公开通报案例库', link: '/policy/cases' },
          { text: '治理痛点提炼', link: '/policy/pain-points' },
          { text: '治理难点与防控对策', link: '/policy/governance' },
          { text: '宣传预警', link: '/policy/awareness' },
        ],
      },
      {
        text: '二 · 链上特征与情报研判组',
        collapsed: false,
        items: [
          { text: '组内概览', link: '/onchain/' },
          { text: '基础链上知识', link: '/onchain/basics' },
          {
            text: '异常地址特征',
            collapsed: false,
            items: [
              { text: '总览 · 组合与评分', link: '/onchain/address-features' },
              { text: '特征一 · 大额快转', link: '/onchain/features/rapid-pass' },
              { text: '特征二 · 小额拆分', link: '/onchain/features/smurfing' },
              { text: '特征三 · 多地址集散', link: '/onchain/features/scatter-gather' },
              { text: '特征四 · 标签地址交互', link: '/onchain/features/risk-neighbor' },
              { text: '特征五 · 高频跨链', link: '/onchain/features/chain-hopping' },
              { text: '公开数据集清单', link: '/onchain/datasets' },
              { text: '公开案例地址与链路', link: '/onchain/case-addresses' },
              { text: '重点场景链路画像', link: '/onchain/scenarios' },
            ],
          },
          { text: '链路可视化研究', link: '/onchain/visualization' },
          { text: '链上分析工具对比', link: '/onchain/tools' },
          { text: '工具选型一页纸', link: '/onchain/tools-brief' },
          { text: '实测与自建附录', link: '/onchain/tools-appendix' },
          { text: '标签横评取数单', link: '/onchain/tools-testlog' },
        ],
      },
      {
        text: '三 · 技术检测与原型开发组',
        collapsed: false,
        items: [
          { text: '组内概览', link: '/tech/' },
          { text: '开源项目调研', link: '/tech/oss-projects' },
          { text: '开源项目全量扫描', link: '/tech/oss-projects-scan' },
          { text: 'Blockscout 专题', link: '/tech/blockscout' },
          { text: '技术研判方法', link: '/tech/forensic-methods' },
          { text: '检测模型与原型', link: '/tech/detection-model' },
        ],
      },
      {
        text: '资源库',
        collapsed: true,
        items: [
          { text: '术语对照表', link: '/glossary/terms' },
          { text: '涉诈行话速查', link: '/glossary/slang' },
          { text: '数据与文献资源', link: '/glossary/resources' },
        ],
      },
    ],

    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索文档', buttonAriaLabel: '搜索文档' },
          modal: {
            noResultsText: '没有找到结果',
            resetButtonTitle: '清空',
            footer: {
              selectText: '选择',
              navigateText: '切换',
              closeText: '关闭',
            },
          },
        },
      },
    },

    outline: { level: [2, 3], label: '本页导航' },

    lastUpdated: {
      text: '最后更新',
      formatOptions: { dateStyle: 'short', timeStyle: 'short' },
    },

    docFooter: { prev: '上一篇', next: '下一篇' },
    darkModeSwitchLabel: '主题',
    lightModeSwitchTitle: '切换到浅色模式',
    darkModeSwitchTitle: '切换到深色模式',
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '菜单',
    externalLinkIcon: true,

    editLink: {
      pattern: 'https://github.com/vcoin-gov/vcoin-gov/edit/main/docs/:path',
      text: '在 GitHub 上编辑此页',
    },

    footer: {
      message: '内容采用 <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans" target="_blank" rel="noopener">CC BY-NC-SA 4.0</a> 许可 · 仅用于合规研究与治理技术交流',
      copyright: '虚拟币治理打击技术开源社区',
    },
  },

  mermaid: {
    // 浅色模式的 mermaid 主题；深色模式下插件按 body 的 dark 类自动切换
    theme: 'neutral',
  },
  mermaidPlugin: {
    // 语言标签，页面里用 ```mermaid 即触发渲染
    class: 'mermaid',
  },
}))
