---
name: claude-vision
description: Describe or analyze an image with an external vision model when the current model cannot see images. Use when a local image path or image URL must be understood, OCR'd, or described and the read_image tool is unavailable or fails.
---

# 识图能力（外部 vision 脚本）

本机没有原生识图能力时，用外部的 OpenAI 兼容 vision 接口把图片转成文字描述。

## 何时使用

- 需要理解本地图片文件或图片 URL 的内容（描述、OCR、识别物体/界面/图表）。
- 优先尝试内置的 `read_image` 工具；只有在它不可用、或当前模型看不到图片时，才走本脚本。

## 用法

脚本位置（固定，勿复制）：

- `E:\skill\skills\claude-vision-skill\vision.js`
- 配置读取自同目录的 `.env`（已存在，含 `DASHSCOPE_API_KEY`、`VISION_MODEL`）。

```
node "E:\skill\skills\claude-vision-skill\vision.js" "<本地图片路径>" "<问题>"
node "E:\skill\skills\claude-vision-skill\vision.js" --url "<图片链接>" "<问题>"
```

省略问题时默认「请详细描述这张图片的内容」。脚本把结果直接打印到 stdout。

## 注意

- 依赖 `dotenv`（已在该目录 `node_modules` 中安装），必须在脚本所在目录之外运行也没问题，因为 `.env` 按脚本目录解析。
- 支持的图片格式：jpg / jpeg / png / gif / webp / bmp。
- 想换服务：改 `.env` 里的 `DASHSCOPE_API_KEY`、`VISION_MODEL`，必要时加 `DASHSCOPE_BASE_URL`。
- 失败时脚本以非 0 退出并打印 `识图失败: <原因>`；把原始错误一并回报给用户，不要编造图片内容。
