# 清线画风

视觉依据：[宝玉项目的清线画风定义](https://github.com/JimLiu/baoyu-skills/blob/main/skills/baoyu-comic/references/art-styles/ligne-claire.md)。以下为面向本工作流的转述与执行补充。

## 画面特征

使用稳定、均匀的黑色轮廓线描绘人物和物体，边缘清楚。随画布缩放线宽，不把源参考中的像素值当作任何尺寸都通用的常数。人物为自然比例、略漫画化的成人，五官简洁但辨识度高，表情和肢体语言清楚。

用有边界的平涂色块上色；需要阴影时使用简洁阴影块。避免渐变塑形、厚涂、水彩晕染、铅笔/交叉排线和电影镜头光效。背景可有可信的空间、建筑和生活道具，但气泡后的区域应安静，不能以堆满细节证明完成度。

每场景保持少量主色、明确光照逻辑，角色服装色跨页固定。页面可由较冷的困惑期转向较暖的理解期，但不以炫光表达所有转折。源参考的蓝红黄为可用配色示例，不强制每页都出现三原色。

清线规范管画法，不强制“只能中性、不能动作”。可以有明确的动作、反应、幽默和情绪，动作以清楚姿态和分格表达，保持轮廓与色块语言。

## 气泡与字体

- 对话通常用白底黑边椭圆气泡，内文黑色，尾巴明确指向说话者。
- 旁白使用短矩形框；思考泡泡只在必要时使用。AI界面发言可以用有屏幕来源的方角气泡，保持与人声区分。
- 不机械套用“手写字体”：选择清楚的中文漫画字或黑体，大字号、足够行距。中文可读性优先于模拟潦草手写。
- 正文建议从画布宽度的约4.5%—5.5%试排，缩小至手机宽检查；标题不应每页占据1/4画面。

## 可复用提示词骨架

```text
Use case: illustration-story. One finished Chinese comic page, portrait 3:4.
Art direction: ligne claire, consistent clean black contours, flat solid colors,
simple flat shadow shapes, recognizable slightly cartooned figures with natural
proportions, carefully staged believable environments, clear panel gutters.
No crosshatching, no painterly rendering, no watercolor washes, no volumetric
light, no lens flare, no photorealistic skin shading, no dense microtext.
Character references: specify identity, clothing, and continuity roles.
Scene or panels: specify setting, actions, expressions, camera, and reading order.
Speech bubbles: exact simplified Chinese text, speaker, location, tail target.
Leave clear room for large readable Chinese; protect faces and acting gestures.
```

具体页必须把场景与台词补全后才能调用。此骨架不是完整成图提示词，也不要求在画面上渲染英文指令。
