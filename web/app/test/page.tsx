'use client'

import { Markdown } from '@/app/components/base/markdown'

export default function Page() {
  const content = '我的首页是 https://www.baidu.com。你好吗'

  return <Markdown content={content} />
}
