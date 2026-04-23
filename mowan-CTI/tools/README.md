# 工具目录

本目录包含 B 模式（聊天记录导入）所需的采集和解析工具。

## 工具清单

| 工具 | 用途 |
|------|------|
| `feishu_auto_collector.py` | 飞书自动采集（群聊+私聊消息、文档） |
| `feishu_parser.py` | 解析飞书消息 JSON 导出 |
| `feishu_browser.py` | 通过浏览器登录态读取飞书文档 |
| `feishu_mcp_client.py` | 通过飞书 App Token 调用官方 API |
| `dingtalk_auto_collector.py` | 钉钉自动采集（文档+消息） |
| `email_parser.py` | 解析邮件 .eml/.mbox 文件 |

## 来源

这些工具来自 [colleague-skill](https://github.com/titanwings/colleague-skill/tree/dot-skill) 项目（MIT 许可证），已复制到本目录以确保 Skill 独立可用。

## 使用方式

SKILL.md 中通过相对路径调用：

```bash
python3 tools/feishu_auto_collector.py --setup
python3 tools/feishu_auto_collector.py --name "{name}" --output-dir /tmp/cti_knowledge/{slug} --msg-limit 500
python3 tools/feishu_parser.py --file {path} --target "{name}" --output /tmp/cti_feishu_out.txt
python3 tools/dingtalk_auto_collector.py --name "{name}" --output-dir /tmp/cti_knowledge/{slug} --msg-limit 500
python3 tools/email_parser.py --file {path} --target "{name}" --output /tmp/cti_email_out.txt
```

## 不依赖工具的降级方案

如果采集工具运行失败（缺少依赖、权限不足等），B 模式仍可通过以下方式工作：
- 用户直接粘贴聊天文本
- 用户上传 PDF / 图片 / TXT 文件（使用 Read 工具直接读取）
