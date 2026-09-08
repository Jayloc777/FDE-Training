from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CSS_NAME = "fde-curriculum.css"
JS_NAME = "fde-curriculum.js"
SCENARIO_SOURCE = "FDE行业场景库_V1.1.json"
CASE_PDF_HREF = "参考资料/Datawhale%20FDE案例100.pdf"

DOCS = [
    {
        "key": "roadmap",
        "source": "FDE人才培养体系总方案_V1.0.md",
        "output": "FDE人才培养体系总方案_V1.0.html",
        "eyebrow": "FDE · TALENT SYSTEM",
        "title": "川麒科技 FDE 人才培养体系总方案",
        "subtitle": "从入门、交付到带队与导师，形成可训练、可评价、可分流、可持续更新的人才路径。",
        "tone": "cyan",
        "stats": [("成长阶段", "L0 → L5"), ("能力维度", "6 项"), ("训练单元", "28 个")],
        "tagline": "系统总览",
    },
    {
        "key": "beginner",
        "source": "FDE入门班课程体系_V1.0.md",
        "output": "FDE入门班课程体系_V1.0.html",
        "eyebrow": "FDE · FOUNDATION",
        "title": "川麒科技 FDE 入门班课程体系",
        "subtitle": "从 AI 工具使用者到可复核的企业 AI 垂直功能 Demo 执行者，并能用 15 个练习场景和 24 个真实案例持续训练。",
        "tone": "lime",
        "stats": [("周期", "4 天 · 8 节"), ("课堂", "12 小时"), ("练习 + 案例", "15 + 24")],
        "tagline": "L1 Assisted Execution",
    },
    {
        "key": "advanced",
        "source": "FDE进阶班课程体系_V1.0.md",
        "output": "FDE进阶班课程体系_V1.0.html",
        "eyebrow": "FDE · FIELD CORE",
        "title": "川麒科技 FDE 进阶班课程体系",
        "subtitle": "在受控项目中完成问题定义、系统实现、失败治理、上线交接与资产复用。",
        "tone": "violet",
        "stats": [("核心周期", "8 周 · 16 节"), ("认证延展", "4 周 · P01-P04"), ("训练级别", "L2/L3 → L4")],
        "tagline": "L2/L3 Field Delivery",
    },
]

LOCAL_HTML_MAP = {item["source"]: item["output"] for item in DOCS}


def load_scenario_data() -> dict:
    return json.loads((ROOT / SCENARIO_SOURCE).read_text(encoding="utf-8"))


def scenario_card_html(scenario: dict) -> str:
    sources = scenario["sources"]
    first_source = sources[0]
    search_text = " ".join(
        [
            scenario["id"],
            scenario["industry"],
            scenario["process"],
            scenario["role"],
            scenario["difficulty"],
            scenario["pain_point"],
            " ".join(scenario["tags"]),
        ]
    )
    source_links = " ".join(
        f'<a href="{html.escape(source["url"], quote=True)}" target="_blank" rel="noreferrer noopener">{html.escape(source["publisher"])} ↗</a>'
        for source in sources
    )
    flow = " → ".join(html.escape(step) for step in scenario["business_flow"])
    inputs = "、".join(html.escape(item) for item in scenario["inputs"])
    outputs = "、".join(html.escape(item) for item in scenario["outputs"])
    tests = "；".join(html.escape(item) for item in scenario["test_prompts"])
    tasks = "".join(f"<li>{html.escape(task)}</li>" for task in scenario["practice_tasks"])
    tags = "".join(f'<span>{html.escape(tag)}</span>' for tag in scenario["tags"])
    return f'''<article class="scenario-card" data-scenario-card data-industry="{html.escape(scenario["industry"], quote=True)}" data-difficulty="{html.escape(scenario["difficulty"], quote=True)}" data-search="{html.escape(search_text, quote=True)}">
  <div class="scenario-card-head"><span class="scenario-id">{html.escape(scenario["id"])}</span><span class="scenario-level scenario-level-{html.escape(scenario["difficulty"], quote=True)}">{html.escape(scenario["difficulty"])}</span></div>
  <span class="micro-label">{html.escape(scenario["industry"])}</span>
  <h3>{html.escape(scenario["process"])}</h3>
  <p class="scenario-role">适用角色：{html.escape(scenario["role"])}</p>
  <div class="scenario-problem"><span>流程痛点</span><p>{html.escape(scenario["pain_point"])}</p></div>
  <div class="scenario-tags">{tags}</div>
  <details class="scenario-details">
    <summary>展开练习设计 <span>＋</span></summary>
    <div class="scenario-detail-body">
      <div class="scenario-detail-block"><b>业务流程</b><p>{flow}</p></div>
      <div class="scenario-detail-block"><b>FDE 切口</b><p>{html.escape(scenario["fde_cut"])}</p></div>
      <div class="scenario-detail-block"><b>L1 Demo</b><p>{html.escape(scenario["l1_demo"])}</p></div>
      <div class="scenario-detail-grid"><div><b>输入</b><p>{inputs}</p></div><div><b>输出</b><p>{outputs}</p></div></div>
      <div class="scenario-detail-block"><b>建议测试</b><p>{tests}</p></div>
      <div class="scenario-detail-block scenario-boundary"><b>练习边界</b><p>{html.escape(scenario["boundary"])}</p></div>
      <div class="scenario-detail-block"><b>学员作业</b><ul class="scenario-practice-list">{tasks}</ul></div>
      <p class="scenario-source-note">{html.escape(scenario["teaching_note"])}</p>
      <div class="scenario-sources"><b>参考来源</b><span>{source_links}</span></div>
    </div>
  </details>
  <div class="scenario-card-footer"><span>{len(sources)} 个来源 · 受控练习</span><button type="button" class="scenario-select" data-scenario-select data-scenario-id="{html.escape(scenario["id"], quote=True)}">选作练习 <span>→</span></button></div>
  <div class="scenario-hidden-data" hidden data-scenario-assignment="{html.escape(scenario["assignment"], quote=True)}" data-scenario-source-url="{html.escape(first_source["url"], quote=True)}" data-scenario-source-title="{html.escape(first_source["title"], quote=True)}"></div>
</article>'''


def source_case_card_html(case: dict, qa_schema: dict) -> str:
    search_text = " ".join(
        [
            case["id"],
            case["case_title"],
            case["responsible_person"],
            case["responsible_affiliation"],
            case["industry"],
            case["focus"],
            " ".join(case["tags"]),
            " ".join(case["qa"].values()),
        ]
    )
    tags = "".join(f'<span>{html.escape(tag)}</span>' for tag in case["tags"])
    qa_blocks = "".join(
        f'<div class="case-qa"><b>{html.escape(question)}</b><div><span>{html.escape(qa_schema.get(question, ""))}</span><p>{html.escape(answer)}</p></div></div>'
        for question, answer in case["qa"].items()
    )
    translation = case["practice_translation"]
    inputs = "、".join(html.escape(item) for item in translation["suggested_inputs"])
    outputs = "、".join(html.escape(item) for item in translation["suggested_outputs"])
    pages = case["source_pdf_pages"]
    return f'''<article class="case-card" data-case-card data-industry="{html.escape(case["industry"], quote=True)}" data-search="{html.escape(search_text, quote=True)}">
  <div class="case-card-head"><span class="case-id">{html.escape(case["id"])}</span><span class="case-type">真实案例 · QA</span></div>
  <span class="micro-label">{html.escape(case["industry"])}</span>
  <h3>{html.escape(case["case_title"])}</h3>
  <p class="case-person">负责人：<strong>{html.escape(case["responsible_person"])}</strong><br><span>{html.escape(case["responsible_affiliation"])}</span></p>
  <div class="case-focus"><span>案例焦点</span><p>{html.escape(case["focus"])}</p></div>
  <div class="case-tags">{tags}</div>
  <details class="case-details">
    <summary>展开负责人 Q1–Q6 <span>＋</span></summary>
    <div class="case-detail-body">
      <div class="case-qa-list">{qa_blocks}</div>
      <div class="case-practice">
        <div class="case-practice-label">转化为 L1 练习 · {html.escape(translation["l1_focus"])}</div>
        <div class="case-detail-grid"><div><b>建议输入</b><p>{inputs}</p></div><div><b>建议输出</b><p>{outputs}</p></div></div>
        <p><b>练习任务</b><br>{html.escape(translation["assignment"])}</p>
        <p class="case-boundary"><b>练习边界</b><br>{html.escape(translation["boundary"])}</p>
      </div>
      <p class="case-source-note">原始PDF：标题页 {pages["title"]}，Q1–Q6 见第 {html.escape(pages["qa"])} 页；案例效果数字按原文状态保留，不能外推为通用ROI。</p>
      <div class="case-sources"><a href="{html.escape(CASE_PDF_HREF, quote=True)}" target="_blank" rel="noreferrer noopener">打开 Datawhale FDE案例100.pdf ↗</a></div>
    </div>
  </details>
  <div class="case-card-footer"><span>PDF p.{pages["title"]} · {html.escape(case["measurement_status"])}</span><span class="case-practice-flag">可转化为 L1 练习</span></div>
</article>'''


def scenario_library_html(data: dict) -> str:
    scenarios = data["scenarios"]
    casebook = data["source_casebook"]
    cases = casebook["cases"]
    industries: list[str] = []
    difficulties: list[str] = []
    for scenario in scenarios:
        if scenario["industry"] not in industries:
            industries.append(scenario["industry"])
        if scenario["difficulty"] not in difficulties:
            difficulties.append(scenario["difficulty"])
    industry_options = "".join(
        f'<option value="{html.escape(industry, quote=True)}">{html.escape(industry)}</option>'
        for industry in industries
    )
    difficulty_options = "".join(
        f'<option value="{html.escape(difficulty, quote=True)}">{html.escape(difficulty)}</option>'
        for difficulty in difficulties
    )
    cards = "\n".join(scenario_card_html(scenario) for scenario in scenarios)
    case_industries: list[str] = []
    for case in cases:
        if case["industry"] not in case_industries:
            case_industries.append(case["industry"])
    case_industry_options = "".join(
        f'<option value="{html.escape(industry, quote=True)}">{html.escape(industry)}</option>'
        for industry in case_industries
    )
    case_cards = "\n".join(source_case_card_html(case, casebook["qa_schema"]) for case in cases)
    return f'''<section id="scenario-library" class="portal-section scenario-library-section" data-scenario-library>
      <div class="section-heading"><div><span class="micro-label">PRACTICE + FIELD CASE LIBRARY</span><h2>15 个练习切口 + 24 个真实案例</h2></div><p>练习卡用于直接选题与交付；真实案例卡保留负责人 Q1–Q6，帮助学员理解问题发现、方案取舍、落地挑战和可转化的练习切口。</p></div>
      <div class="scenario-summary"><div><strong>{len(scenarios)}</strong><span>可直接练习</span></div><div><strong>{len(cases)}</strong><span>Datawhale案例</span></div><div><strong>{len(scenarios) + len(cases)}</strong><span>场景与案例</span></div><div><strong>T01–T12</strong><span>统一测试框架</span></div></div>
      <div class="scenario-toolbar" aria-label="场景库筛选">
        <label class="scenario-search"><span>⌕</span><input type="search" data-scenario-search placeholder="搜索行业、岗位、流程或标签" aria-label="搜索行业场景"></label>
        <label class="scenario-filter"><span>行业</span><select data-scenario-industry aria-label="按行业筛选"><option value="">全部行业</option>{industry_options}</select></label>
        <label class="scenario-filter"><span>难度</span><select data-scenario-difficulty aria-label="按难度筛选"><option value="">全部难度</option>{difficulty_options}</select></label>
        <button type="button" class="text-button scenario-reset" data-scenario-reset>重置筛选</button>
      </div>
      <div class="scenario-count" data-scenario-count>显示 {len(scenarios)} / {len(scenarios)} 个场景</div>
      <div class="scenario-layout">
        <div><div class="scenario-grid" data-scenario-grid>{cards}</div><p class="scenario-empty" data-scenario-empty hidden>没有符合当前筛选条件的场景，请调整关键词、行业或难度。</p></div>
        <aside class="scenario-workbench" aria-live="polite">
          <span class="micro-label">MY PRACTICE BRIEF</span>
          <div class="scenario-selection-empty" data-scenario-selection-empty><div class="selection-orbit">＋</div><h3>选择一张场景卡</h3><p>点击“选作练习”，把它变成你的 Demo 题目。然后按入门班的九项证据包推进。</p></div>
          <div class="scenario-selection" data-scenario-selection hidden><span class="scenario-selected-meta" data-scenario-selected-meta></span><h3 data-scenario-selected-title></h3><p class="scenario-selected-assignment" data-scenario-selected-assignment></p><div class="selected-checklist"><b>建议先完成</b><ol data-scenario-selected-tasks></ol></div><a class="panel-link" data-scenario-selected-source target="_blank" rel="noreferrer noopener">打开首要参考来源 <span>↗</span></a><p class="scenario-workbench-note">完成后回到入门班课程文档，按机会卡 → Brief → IO 契约 → 材料 → T01-T12 → 失败/修订 → Runbook → 演示推进。</p></div>
        </aside>
      </div>
      <div class="casebook-section">
        <div class="casebook-heading"><div><span class="micro-label">DATAWHALE CASEBOOK · 24 CASES</span><h3>真实案例与负责人问答</h3></div><p>案例事实与QA来自 <a href="{html.escape(CASE_PDF_HREF, quote=True)}" target="_blank" rel="noreferrer noopener">Datawhale FDE案例100.pdf</a>；下方的L1转化仅用于训练设计。</p></div>
        <div class="casebook-toolbar" aria-label="真实案例筛选">
          <label class="scenario-search"><span>⌕</span><input type="search" data-case-search placeholder="搜索案例、负责人、行业或关键词" aria-label="搜索真实案例"></label>
          <label class="scenario-filter"><span>行业</span><select data-case-industry aria-label="按案例行业筛选"><option value="">全部行业</option>{case_industry_options}</select></label>
          <button type="button" class="text-button scenario-reset" data-case-reset>重置案例筛选</button>
        </div>
        <div class="casebook-count" data-case-count>显示 {len(cases)} / {len(cases)} 个案例</div>
        <div class="casebook-grid" data-case-grid>{case_cards}</div>
        <p class="casebook-empty" data-case-empty hidden>没有符合当前筛选条件的真实案例，请调整关键词或行业。</p>
      </div>
      <p class="scenario-library-note">资料源：<a href="{html.escape(SCENARIO_SOURCE, quote=True)}">下载完整场景库 JSON</a>；真实案例原文：<a href="{html.escape(CASE_PDF_HREF, quote=True)}">Datawhale FDE案例100.pdf</a>。行业流程、FDE切口、作业与L1边界属于课程设计推断，不能替代行业合规、法律或生产审批。</p>
    </section>'''


def href_for(raw: str) -> str:
    """Keep public links usable without leaking a local workspace path."""
    value = raw.strip()
    value = value.replace("\\", "/")
    if value in LOCAL_HTML_MAP:
        return LOCAL_HTML_MAP[value]
    if value.lower().startswith("file:///") or re.match(r"^[A-Za-z]:/", value) or value.startswith(("/Users/", "/home/")):
        basename = Path(value).name
        if basename in LOCAL_HTML_MAP:
            return LOCAL_HTML_MAP[basename]
        return ""
    return value


def inline_markdown(value: str) -> str:
    tokens: dict[str, str] = {}

    def stash(content: str) -> str:
        key = f"@@FDE{len(tokens)}@@"
        tokens[key] = content
        return key

    link_pattern = re.compile(
        r"\[([^\]]+)\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+[\"']([^\"']+)[\"'])?\s*\)"
    )

    def link_replacement(match: re.Match[str]) -> str:
        label = html.escape(match.group(1), quote=False)
        target = href_for(match.group(2) or match.group(3) or "")
        if not target:
            return stash(f'<span class="offline-reference" title="工作区材料未随仓库分发">{label}</span>')
        title = match.group(4)
        attrs = f' href="{html.escape(target, quote=True)}"'
        if title:
            attrs += f' title="{html.escape(title, quote=True)}"'
        if target.startswith(("http://", "https://")):
            attrs += ' target="_blank" rel="noreferrer noopener"'
        return stash(f'<a{attrs}>{label}</a>')

    value = link_pattern.sub(link_replacement, value)

    def code_replacement(match: re.Match[str]) -> str:
        return stash(f'<code>{html.escape(match.group(1), quote=False)}</code>')

    value = re.sub(r"`([^`]+)`", code_replacement, value)
    value = html.escape(value, quote=False)
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"__(.+?)__", r"<strong>\1</strong>", value)
    value = re.sub(r"~~(.+?)~~", r"<del>\1</del>", value)
    value = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", value)
    value = re.sub(r"(?<![\w])_([^_\n]+)_(?![\w])", r"<em>\1</em>", value)

    for key, content in tokens.items():
        value = value.replace(key, content)
    return value


def plain_heading(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"[*_`~]", "", value)
    return value.strip()


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def split_table_row(line: str) -> list[str]:
    value = line.strip()
    if value.startswith("|"):
        value = value[1:]
    if value.endswith("|"):
        value = value[:-1]
    return [cell.strip() for cell in value.split("|")]


def render_table(lines: list[str]) -> str:
    rows = [split_table_row(line) for line in lines]
    header = rows[0]
    body = rows[2:]
    head_html = "".join(f"<th scope=\"col\">{inline_markdown(cell)}</th>" for cell in header)
    body_html = []
    for row in body:
        cells = row + [""] * max(0, len(header) - len(row))
        body_html.append("<tr>" + "".join(f"<td>{inline_markdown(cell)}</td>" for cell in cells[: len(header)]) + "</tr>")
    return (
        '<div class="table-wrap"><table class="data-table">'
        f"<thead><tr>{head_html}</tr></thead>"
        f"<tbody>{''.join(body_html)}</tbody>"
        "</table></div>"
    )


def render_markdown(text: str, skip_first_h1: bool = False) -> tuple[str, list[dict[str, str]]]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    output: list[str] = []
    toc: list[dict[str, str]] = []
    i = 0
    first_h1_skipped = False

    def special_start(line: str) -> bool:
        stripped = line.strip()
        return bool(
            re.match(r"^#{1,6}\s+", stripped)
            or stripped.startswith(("~~~", "```", ">", "|"))
            or re.match(r"^(?:[-*+]\s+|\d+[.)]\s+)", stripped)
            or re.fullmatch(r"\s*([-*_])(?:\s*\1){2,}\s*", stripped)
        )

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        if not stripped:
            i += 1
            continue

        fence = re.match(r"^\s*(```|~~~)\s*([^ ]*)?\s*$", raw)
        if fence:
            marker = fence.group(1)
            language = (fence.group(2) or "").strip()
            i += 1
            block: list[str] = []
            while i < len(lines) and not re.match(rf"^\s*{re.escape(marker)}\s*$", lines[i]):
                block.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            class_attr = f' class="language-{html.escape(language, quote=True)}"' if language else ""
            output.append(f"<pre><code{class_attr}>{html.escape(chr(10).join(block), quote=False)}</code></pre>")
            continue

        heading = re.match(r"^\s*(#{1,6})\s+(.+?)\s*$", raw)
        if heading:
            level = len(heading.group(1))
            content = heading.group(2)
            if skip_first_h1 and level == 1 and not first_h1_skipped:
                first_h1_skipped = True
                i += 1
                continue
            section_id = f"section-{len(toc) + 1:02d}"
            title = plain_heading(content)
            toc.append({"level": str(level), "id": section_id, "title": title})
            output.append(
                f'<h{level} id="{section_id}" data-heading="true">{inline_markdown(content)}</h{level}>'
            )
            i += 1
            continue

        if re.fullmatch(r"\s*([-*_])(?:\s*\1){2,}\s*", raw):
            output.append('<hr class="section-rule">')
            i += 1
            continue

        if stripped.startswith(">"):
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(re.sub(r"^\s*>\s?", "", lines[i].strip()))
                i += 1
            output.append(f'<blockquote><p>{"<br>".join(inline_markdown(line) for line in quote_lines)}</p></blockquote>')
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            table_lines = [lines[i], lines[i + 1]]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            output.append(render_table(table_lines))
            continue

        list_match = re.match(r"^\s*(?:([-*+])|(\d+)[.)])\s+(.+?)\s*$", raw)
        if list_match:
            ordered = bool(list_match.group(2))
            items: list[str] = []
            start = int(list_match.group(2)) if ordered else 1
            while i < len(lines):
                current = lines[i]
                match = re.match(r"^\s*(?:([-*+])|(\d+)[.)])\s+(.+?)\s*$", current)
                if match and bool(match.group(2)) == ordered:
                    items.append(match.group(3))
                    i += 1
                    continue
                if items and current.strip() and (current.startswith("  ") or current.startswith("\t")):
                    items[-1] += " " + current.strip()
                    i += 1
                    continue
                break
            tag = "ol" if ordered else "ul"
            attr = f' start="{start}"' if ordered and start != 1 else ""
            output.append(f'<{tag}{attr} class="content-list">' + "".join(f"<li>{inline_markdown(item)}</li>" for item in items) + f"</{tag}>")
            continue

        paragraph_lines = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not special_start(lines[i]):
            paragraph_lines.append(lines[i].strip())
            i += 1
        output.append(f'<p>{"<br>".join(inline_markdown(line) for line in paragraph_lines)}</p>')

    return "\n".join(output), toc


def stats_html(stats: list[tuple[str, str]]) -> str:
    return "".join(
        f'<div class="hero-stat"><span>{html.escape(label)}</span><strong>{html.escape(value)}</strong></div>'
        for label, value in stats
    )


def page_nav(active: str) -> str:
    links = [
        ("portal", "体系门户", "FDE人才培养体系门户.html"),
        ("roadmap", "体系总览", "FDE人才培养体系总方案_V1.0.html"),
        ("beginner", "入门班", "FDE入门班课程体系_V1.0.html"),
        ("advanced", "进阶班", "FDE进阶班课程体系_V1.0.html"),
        ("scenario", "场景库", "FDE人才培养体系门户.html#scenario-library"),
    ]
    return "".join(
        f'<a class="nav-link {"is-active" if key == active else ""}" href="{target}">{label}</a>'
        for key, label, target in links
    )


def shell(item: dict, content_html: str, toc: list[dict[str, str]], source_text: str) -> str:
    source_path = item["source"]
    source_bytes = len(source_text.encode("utf-8"))
    toc_fallback = "".join(
        f'<a class="toc-link toc-level-{entry["level"]}" href="#{entry["id"]}">{html.escape(entry["title"])}</a>'
        for entry in toc
        if int(entry["level"]) >= 2
    )
    return f'''<!doctype html>
<html lang="zh-CN" data-page="{item["key"]}" data-source="{html.escape(source_path, quote=True)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(item["subtitle"], quote=True)}">
  <title>{html.escape(item["title"])} · FDE 人才培养体系</title>
  <link rel="stylesheet" href="{CSS_NAME}">
</head>
<body class="document-page tone-{item["tone"]}">
  <div class="ambient ambient-one"></div>
  <div class="ambient ambient-two"></div>
  <header class="topbar">
    <a class="brand" href="FDE人才培养体系门户.html" aria-label="返回 FDE 人才培养体系门户">
      <span class="brand-mark">F</span><span><b>FDE</b><small>FIELD ENABLED</small></span>
    </a>
    <nav class="main-nav" aria-label="文档导航">{page_nav(item["key"])}</nav>
    <div class="top-actions">
      <button class="icon-button" type="button" data-action="theme" aria-label="切换主题" title="切换主题">◐</button>
      <button class="icon-button mobile-only" type="button" data-action="sidebar" aria-label="打开目录">☰</button>
    </div>
  </header>

  <div class="reading-progress" data-reading-progress></div>
  <div class="document-layout">
    <aside class="sidebar" data-sidebar>
      <div class="sidebar-head">
        <span class="micro-label">DOCUMENT MAP</span>
        <button class="sidebar-close mobile-only" type="button" data-action="sidebar">×</button>
      </div>
      <div class="source-card">
        <span class="source-dot"></span>
        <div><span>内容源</span><strong>{html.escape(source_path)}</strong></div>
      </div>
      <nav class="doc-toc" aria-label="本页目录" data-toc>
        {toc_fallback}
      </nav>
      <div class="sidebar-footer">
        <span class="micro-label">SOURCE INTEGRITY</span>
        <p>本页由 Markdown 原文逐段转换，保留标题、表格、链接、代码块与原始数据。</p>
        <span class="source-size">{source_bytes:,} bytes UTF-8</span>
      </div>
    </aside>

    <main class="main-content">
      <section class="doc-hero" data-search-scope>
        <div class="hero-orbit" aria-hidden="true"><span></span><i></i><b></b></div>
        <div class="eyebrow"><span class="pulse"></span>{html.escape(item["eyebrow"])}</div>
        <div class="hero-grid">
          <div class="hero-copy">
            <p class="overline">{html.escape(item["tagline"])}</p>
            <h1>{html.escape(item["title"])}</h1>
            <p class="hero-subtitle">{html.escape(item["subtitle"])}</p>
            <div class="hero-actions">
              <button class="primary-button" type="button" data-action="print">打印 / 导出 PDF <span>↗</span></button>
              <label class="search-box"><span>⌕</span><input type="search" placeholder="搜索本页内容" data-search aria-label="搜索本页内容"></label>
            </div>
          </div>
          <div class="hero-stats" aria-label="文档指标">{stats_html(item["stats"])}</div>
        </div>
      </section>

      <div class="mobile-toc-bar mobile-only"><span>本页目录</span><button type="button" data-action="sidebar">查看章节 <span>→</span></button></div>
      <article id="article" class="markdown-body" data-article data-search-scope>{content_html}</article>
      <footer class="document-footer">
        <div><span class="brand-mark small">F</span><span>FDE 人才培养体系 · 内容源完整保留</span></div>
        <a href="FDE人才培养体系门户.html">返回体系门户 ↑</a>
      </footer>
    </main>
  </div>
  <div class="search-status" data-search-status aria-live="polite"></div>
  <script src="{JS_NAME}" defer></script>
</body>
</html>'''


def portal_html() -> str:
    scenario_section = scenario_library_html(load_scenario_data())
    template = '''<!doctype html>
<html lang="zh-CN" data-page="portal" data-portal="true">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="川麒科技 FDE 人才培养体系门户">
  <title>FDE 人才培养体系 · 川麒科技</title>
  <link rel="stylesheet" href="fde-curriculum.css">
</head>
<body class="portal-page tone-cyan">
  <div class="ambient ambient-one"></div><div class="ambient ambient-two"></div>
  <header class="topbar">
    <a class="brand" href="FDE人才培养体系门户.html" aria-label="FDE 人才培养体系门户">
      <span class="brand-mark">F</span><span><b>FDE</b><small>FIELD ENABLED</small></span>
    </a>
    <nav class="main-nav" aria-label="文档导航">
      <a class="nav-link is-active" href="FDE人才培养体系门户.html">体系门户</a>
      <a class="nav-link" href="FDE人才培养体系总方案_V1.0.html">总方案</a>
      <a class="nav-link" href="FDE入门班课程体系_V1.0.html">入门班</a>
      <a class="nav-link" href="FDE进阶班课程体系_V1.0.html">进阶班</a>
      <a class="nav-link" href="#scenario-library">场景库</a>
    </nav>
    <div class="top-actions"><button class="icon-button" type="button" data-action="theme" aria-label="切换主题" title="切换主题">◐</button></div>
  </header>
  <div class="reading-progress" data-reading-progress></div>

  <main class="portal-main">
    <section class="portal-hero">
      <div class="hero-orbit hero-orbit-large" aria-hidden="true"><span></span><i></i><b></b></div>
      <div class="eyebrow"><span class="pulse"></span>CHUANQI TECHNOLOGY · FDE ACADEMY</div>
      <div class="portal-hero-grid">
        <div>
          <p class="overline">人才培养操作系统 / 2026</p>
          <h1>把 AI 能力，<br><em>部署到真实工作里。</em></h1>
          <p class="hero-subtitle">一套从 L0 准备、L1 入门、L2/L3 交付，到 L4 认证与 L5 带队的完整 FDE 成长路径。</p>
          <div class="hero-actions"><a class="primary-button" href="FDE人才培养体系总方案_V1.0.html">进入总方案 <span>→</span></a><a class="text-button" href="#scenario-library">浏览行业场景库 <span>↓</span></a></div>
        </div>
        <div class="hero-visual" aria-label="FDE 能力环">
          <div class="capability-ring ring-back"></div><div class="capability-ring ring-mid"></div><div class="capability-ring ring-front"></div>
          <div class="ring-core"><span>FDE</span><small>FIELD<br>DELIVERY</small></div>
          <span class="ring-label label-top">业务理解</span><span class="ring-label label-right">系统实现</span><span class="ring-label label-bottom">现场交付</span><span class="ring-label label-left">资产复用</span>
        </div>
      </div>
    </section>

    <section class="metric-strip" aria-label="体系概览指标">
      <div class="metric"><strong>3</strong><span>核心文档</span><small>总方案 / 入门 / 进阶</small></div>
      <div class="metric"><strong>28</strong><span>训练单元</span><small>8 节课 + 16 节课 + 4 个认证实训</small></div>
      <div class="metric"><strong>6</strong><span>能力维度</span><small>从问题定义到组织推动</small></div>
      <div class="metric"><strong>1,251</strong><span>信号资料</span><small>分层采样、Source Ledger、季度更新</small></div>
    </section>

    <section id="curriculum" class="portal-section">
      <div class="section-heading"><div><span class="micro-label">LEARNING ARCHITECTURE</span><h2>一条完整的人才路径</h2></div><p>每个阶段都绑定目标能力、实训项目、可验证产出与下一阶段门槛。</p></div>
      <div class="path-line" aria-label="L0 到 L5 成长路径">
        <article class="path-card path-muted"><span class="path-index">01</span><div class="path-level">L0</div><h3>准备</h3><p>工具、文件、AI 基础与安全边界。</p><span class="path-output">学习契约 · 安全练习</span></article>
        <div class="path-connector"></div>
        <article class="path-card path-lime"><span class="path-index">02</span><div class="path-level">L1</div><h3>入门班</h3><p>在脚手架中交付一个可复核 Demo。</p><span class="path-output">MVP-DEMO-01</span></article>
        <div class="path-connector"></div>
        <article class="path-card path-violet"><span class="path-index">03</span><div class="path-level">L2 / L3</div><h3>进阶班</h3><p>从需求、系统到失败治理的项目交付。</p><span class="path-output">PRJ-A / B / C</span></article>
        <div class="path-connector"></div>
        <article class="path-card path-cyan"><span class="path-index">04</span><div class="path-level">L3 / L4</div><h3>项目认证</h3><p>现场实战、MVD、ROI 与资产复用认证。</p><span class="path-output">P01 — P04</span></article>
        <div class="path-connector"></div>
        <article class="path-card path-gold"><span class="path-index">05</span><div class="path-level">L5</div><h3>带队 / 导师</h3><p>管理 FDE pod，沉淀组织与产品能力。</p><span class="path-output">可复制交付系统</span></article>
      </div>
    </section>

    <section class="portal-section two-column">
      <div class="visual-panel capability-panel">
        <div class="panel-heading"><span class="micro-label">CAPABILITY MODEL</span><h2>六项核心能力</h2><span class="panel-chip">0 — 4 级评价</span></div>
        <div class="capability-list">
          <div class="capability-row"><span>问题定义</span><div class="bar"><i style="--value:92%"></i></div><b>4</b></div>
          <div class="capability-row"><span>业务理解</span><div class="bar"><i style="--value:86%"></i></div><b>4</b></div>
          <div class="capability-row"><span>系统实现</span><div class="bar"><i style="--value:78%"></i></div><b>3</b></div>
          <div class="capability-row"><span>可靠性与评估</span><div class="bar"><i style="--value:75%"></i></div><b>3</b></div>
          <div class="capability-row"><span>现场交付</span><div class="bar"><i style="--value:68%"></i></div><b>3</b></div>
          <div class="capability-row"><span>组织推动</span><div class="bar"><i style="--value:60%"></i></div><b>2</b></div>
        </div>
        <p class="panel-note">图示为培养体系的能力结构示意；真实认证以课程文档中的 Gate、证据包与评分标准为准。</p>
      </div>
      <div class="visual-panel signal-panel">
        <div class="panel-heading"><span class="micro-label">SIGNAL LIBRARY</span><h2>1,251 份资料如何进入课程</h2></div>
        <div class="signal-flow"><div class="signal-node"><b>01</b><span>分层</span><small>核心方法 / 实战案例 / 变化信号 / 证据材料</small></div><div class="flow-arrow">→</div><div class="signal-node"><b>02</b><span>筛选</span><small>来源、可信度、课程映射、使用边界</small></div><div class="flow-arrow">→</div><div class="signal-node"><b>03</b><span>更新</span><small>Source Ledger 与季度复核机制</small></div></div>
        <blockquote class="signal-quote">完整课程不等于逐条把资料库当教材；课程用稳定方法搭骨架，用分层信号补案例与变化。</blockquote>
        <a class="panel-link" href="FDE人才培养体系总方案_V1.0.html#section-26">查看信号库治理机制 <span>↗</span></a>
      </div>
    </section>

    __SCENARIO_LIBRARY__

    <section class="portal-section" id="documents">
      <div class="section-heading"><div><span class="micro-label">COURSE DOCUMENTS</span><h2>三份可直接执行的文档</h2></div><p>点击进入完整版本。所有正文均由原始 Markdown 逐段转换，适合阅读、检索、打印与分享。</p></div>
      <div class="document-cards">
        <a class="document-card card-cyan" href="FDE人才培养体系总方案_V1.0.html"><div class="card-top"><span class="doc-number">01</span><span class="card-arrow">↗</span></div><span class="micro-label">SYSTEM MAP</span><h3>人才培养体系总方案</h3><p>全路径、能力模型、分流门槛、项目梯度、信号库治理与运营指标。</p><div class="card-meta"><span>L0 → L5</span><span>392 行源文档</span></div></a>
        <a class="document-card card-lime" href="FDE入门班课程体系_V1.0.html"><div class="card-top"><span class="doc-number">02</span><span class="card-arrow">↗</span></div><span class="micro-label">FOUNDATION</span><h3>FDE 入门班课程体系</h3><p>4 天 8 节课，每节 90 分钟，完成一个安全、可测试、可复核的垂直功能 Demo。</p><div class="card-meta"><span>L1 Assisted</span><span>V1.3 · 15练习 + 24案例</span></div></a>
        <a class="document-card card-violet" href="FDE进阶班课程体系_V1.0.html"><div class="card-top"><span class="doc-number">03</span><span class="card-arrow">↗</span></div><span class="micro-label">FIELD CORE</span><h3>FDE 进阶班课程体系</h3><p>8 周核心训练 + 4 周认证延展，覆盖 16 节课与 P01-P04 现场实训。</p><div class="card-meta"><span>L2/L3 → L4</span><span>606 行源文档</span></div></a>
      </div>
    </section>

    <section class="portal-section delivery-band">
      <div><span class="micro-label">DELIVERY PRINCIPLE</span><h2>学完不是“会说”，而是“能交付”。</h2><p>从每次训练的输入、过程、失败记录，到证据包、Runbook 和回顾，所有晋级都以可复核产出为依据。</p></div>
      <div class="principle-stack"><span>定义问题</span><span>受控实现</span><span>测试失败</span><span>保留证据</span><span>完成交接</span></div>
    </section>
  </main>
  <footer class="portal-footer"><span><span class="brand-mark small">F</span> 川麒科技 FDE Academy</span><span>离线可读 · 可打印 · 内容源完整保留</span></footer>
  <script src="fde-curriculum.js" defer></script>
</body>
</html>'''
    return template.replace("__SCENARIO_LIBRARY__", scenario_section)


def build() -> None:
    for item in DOCS:
        source_path = ROOT / item["source"]
        source_text = source_path.read_text(encoding="utf-8")
        rendered, toc = render_markdown(source_text, skip_first_h1=True)
        output = shell(item, rendered, toc, source_text)
        (ROOT / item["output"]).write_text(output, encoding="utf-8", newline="\n")
        print(f"built {item['output']} | headings={len(toc)} | source_bytes={len(source_text.encode('utf-8'))}")
    portal_path = ROOT / "FDE人才培养体系门户.html"
    portal_path.write_text(portal_html(), encoding="utf-8", newline="\n")
    print(f"built {portal_path.name}")


if __name__ == "__main__":
    build()

