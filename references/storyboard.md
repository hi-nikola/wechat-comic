# 分镜与交付

## 项目文件

```text
项目目录/
  storyboard.json
  完整分镜.md
  prompts/01.md ...
  references/角色与风格参考
  pages/01.png ...
  改编与来源.md
  检查记录.md
  全篇预览.html
```

目录按实际需要创建。独立排字时另存 `lettering/` 的文本框、气泡和字体数据；直接生图的文字已嵌入PNG，不能声称可直接编辑。

## 最小结构

`references/example-page.json` 是可读的一页示例。正式项目至少记录：

- 全篇：title、aspect_ratio、style、page_mode、expected_page_count、characters、pages。
- 每页：id、title、purpose、page_mode、image、panels、bubbles，以及少量可选captions。
- 每格：panel_id、画面区域/布局说明、场景、景别、动作、表情和角色列表。
- 每气泡：id、panel_id、speaker、order、text、kind、placement、tail_target。
- 角色身份、气泡顺序和事实来源应可追踪。场景重构与虚构AI对话在项目说明注明。

单场景页也有一个panel_id用于绑定气泡。位置可先用语义（左上、人物头顶），需要独立排字时转换成归一化坐标或像素坐标，记录坐标系。

## 成图提示词

每个prompts文件包含：画风与角色参考的用途、输出比例、单场景或分格构图、各格动作、完整可见文字及气泡次序、尾巴目标、避让区域。更新内容先更新分镜和提示词，再修改图像，保持记录与成品一致。

## 预览脚本

```text
python scripts/build_preview.py 项目目录/storyboard.json --output 项目目录/全篇预览.html
```

`python`指当前环境可用的Python解释器；环境有指定运行时时优先用该运行时。脚本仅用标准库，不安装依赖、不调用网络、不生成图像。

脚本默认要求每页存在PNG、比例精确3:4，页数与expected_page_count一致，编号不重复。`image`为相对storyboard.json的路径；也兼容旧项目的数字id及默认 `pages/01.png` 命名。HTML图片相对HTML位置引用，分享时连同图片一起打包。

已有预览文件不覆盖，需要加 `--overwrite` 或换一个文件名。检查失败时退出，不写入新预览。页面中转录的是剧本台词，不代表OCR识别结果，不能据此声称图中文字正确。

## 检查记录

区分机器检查（页数、文件、尺寸）和人工/视觉检查（人物、对白、尾巴、风格、剧情）。列出实际查看过的页、修订页和仍存在的问题。交付时只承诺已经完成的检查。
