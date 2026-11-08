"""Check numbered comic PNGs and build an offline reading page. No image edits."""
import argparse
import html
import json
import os
from pathlib import Path
import struct


def png_size(path):
    with path.open("rb") as handle:
        head = handle.read(24)
    if len(head) != 24 or head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise ValueError(f"Not a PNG with IHDR: {path}")
    return struct.unpack(">II", head[16:24])


def build(plan_path, output, overwrite=False):
    plan_path, output = Path(plan_path).resolve(), Path(output).resolve()
    if output.exists() and not overwrite:
        raise ValueError(f"Output exists, use a new name or --overwrite: {output}")
    plan = json.loads(plan_path.read_text(encoding="utf-8-sig"))
    pages = plan.get("pages", [])
    if not pages:
        raise ValueError("No pages in storyboard")
    expected = plan.get("expected_page_count", len(pages))
    if expected != len(pages):
        raise ValueError(f"Expected {expected} pages, found {len(pages)}")
    if plan.get("aspect_ratio", plan.get("ratio", "3:4")) != "3:4":
        raise ValueError("This preview checker expects 3:4 pages")
    ids, rows = set(), []
    for index, page in enumerate(pages, 1):
        ident = str(page.get("id", index))
        if ident in ids:
            raise ValueError(f"Duplicate page id: {ident}")
        ids.add(ident)
        fallback = f"pages/{int(ident):02}.png" if ident.isdigit() else f"pages/{ident}.png"
        path = (plan_path.parent / page.get("image", fallback)).resolve()
        if not path.is_file():
            raise ValueError(f"Missing page {ident}: {path}")
        width, height = png_size(path)
        if width <= 0 or height <= 0 or width * 4 != height * 3:
            raise ValueError(f"Page {ident} is {width}x{height}, expected exact 3:4")
        relative = Path(os.path.relpath(path, output.parent)).as_posix()
        lines = [b["text"] for b in sorted(page.get("bubbles", []), key=lambda b: b.get("order", 0))]
        lines += [c["text"] for c in page.get("captions", [])]
        if not lines:
            lines = page.get("text", [])
        rows.append((index, page.get("title", ""), relative, width, height, lines))
    esc = html.escape
    title = esc(plan.get("title", "公众号漫画"))
    nav, content = [], []
    for index, page_title, relative, width, height, lines in rows:
        nav.append(f'<a href="#p{index}">{index:02}</a>')
        text = "".join(f"<p>{esc(str(line))}</p>" for line in lines)
        content.append(
            f'<section id="p{index}"><div class="label">{index:02} / {len(rows):02}　{esc(page_title)}</div>'
            f'<img src="{esc(relative, quote=True)}" width="{width}" height="{height}" '
            f'alt="{esc(page_title, quote=True)}" loading="lazy">'
            f'<details><summary>剧本文字转录</summary>{text}</details></section>'
        )
    document = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<style>*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:70px}}
body{{margin:0;background:#efeee9;color:#202524;font-family:"Microsoft YaHei",sans-serif}}
header,main,footer{{max-width:840px;margin:auto}}header,footer{{padding:24px 16px}}
h1{{font-size:28px;margin:0 0 10px}}header p{{line-height:1.7;margin:0}}
nav{{position:sticky;top:0;background:#fffef9f5;padding:12px;display:flex;gap:8px;overflow:auto;z-index:2}}
nav a{{color:inherit;text-decoration:none;border:1px solid #bbb;padding:6px 10px;border-radius:4px}}
section{{margin:20px 0 35px}}.label{{padding:8px 12px;font-size:13px}}img{{width:100%;height:auto;display:block}}
details{{padding:12px 16px;background:#fffef9;line-height:1.7}}summary{{cursor:pointer}}footer{{font-size:13px}}
@media(min-width:860px){{main{{padding:0 16px}}}}@media print{{header,nav,details,footer,.label{{display:none}}
body{{background:white}}section{{margin:0;break-after:page}}}}</style></head><body>
<header><h1>{title}</h1><p>{len(rows)}页 · 3:4竖幅 · 点击页码或向下阅读</p></header>
<nav>{''.join(nav)}</nav><main>{''.join(content)}</main>
<footer>文字转录来自剧本，不能替代图片内文字检查。离线分享时连同图片文件一起保存。</footer></body></html>'''
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    return {"pages": len(rows), "all_exact_3_4": True, "output": str(output)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("storyboard", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.storyboard, args.output, args.overwrite), ensure_ascii=False))
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1, f"Preview check failed: {error}\n")


if __name__ == "__main__":
    main()
