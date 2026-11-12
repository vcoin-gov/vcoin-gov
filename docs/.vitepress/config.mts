import { defineConfig } from 'vitepress'

export default defineConfig({
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
        ],
      },
      {
        text: '二 · 链上特征与情报研判组',
        collapsed: false,
        items: [
          { text: '组内概览', link: '/onchain/' },
          { text: '基础链上知识', link: '/onchain/basics' },
          { text: '异常地址特征', link: '/onchain/address-features' },
          { text: '链路可视化研究', link: '/onchain/visualization' },
          { text: '链上分析工具对比', link: '/onchain/tools' },
        ],
      },
      {
        text: '三 · 技术检测与原型开发组',
        collapsed: false,
        items: [
          { text: '组内概览', link: '/tech/' },
          { text: '开源项目调研', link: '/tech/oss-projects' },
          { text: '检测模型与原型', link: '/tech/detection-model' },
        ],
      },
      {
        text: '资源库',
        collapsed: true,
        items: [
          { text: '术语对照表', link: '/glossary/terms' },
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
      message: '内容由各研究小组共建 · 仅用于合规研究与治理技术交流',
      copyright: '虚拟币治理打击技术开源社区',
    },
  },
})
