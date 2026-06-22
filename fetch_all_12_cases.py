"""
批量抓取12个行政处罚案例的完整详情
"""
from playwright.sync_api import sync_playwright
import time
import os
import re

TARGET_URL = "https://xzcf.zjzwfw.gov.cn/punishment/#/Punish"
OUTPUT_DIR = "/Users/lizhendong/Desktop/claude code/爬虫脚本/行政处罚案例"

def get_page_text(page):
    """获取页面完整文本"""
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
        time.sleep(3)
        return page.evaluate("""
            () => {
                function getAllText(node) {
                    let text = "";
                    if (node.nodeType === Node.TEXT_NODE) {
                        let t = node.textContent.trim();
                        if (t) text += t + "\\n";
                    } else if (node.nodeType === Node.ELEMENT_NODE) {
                        if (node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE') {
                            for (let child of node.childNodes) {
                                text += getAllText(child);
                            }
                        }
                    }
                    return text;
                }
                return getAllText(document.body);
            }
        """)
    except:
        return ""

def is_on_detail_page(page):
    """检查是否在详情页面"""
    try:
        has_detail_title = page.evaluate("""
            () => {
                const body = document.body.textContent || "";
                return body.includes('行政处罚结果信息公开详情') ||
                       body.includes('返回') ||
                       body.includes('案件名称') ||
                       body.includes('处罚决定文书号');
            }
        """)
        return has_detail_title
    except:
        return False

def parse_and_save(case_num, case_name, content):
    """解析内容并保存为Markdown"""

    parsed = {
        "案件名称": case_name,
        "处罚决定文书号": "",
        "被处罚人": "",
        "法定代表人": "",
        "执法部门": "",
        "决定日期": "",
        "主要违法事实": "",
        "处罚种类和依据": "",
        "行政处罚决定": "",
        "履行方式": "",
        "救济途径": ""
    }

    if content and len(content) > 100:
        lines = content.split('\n')
        current_field = None
        current_content = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 识别字段
            if "案件名称" in line and len(line) < 30:
                if current_field and current_content:
                    parsed[current_field] = " ".join(current_content)
                current_field = "案件名称"
                current_content = []
            elif "处罚决定文书号" in line and len(line) < 30:
                if current_field and current_content:
                    parsed[current_field] = " ".join(current_content)
                current_field = "处罚决定文书号"
                current_content = []
            elif "被处罚" in line and len(line) < 30:
                if current_field and current_content:
                    parsed[current_field] = " ".join(current_content)
                current_field = "被处罚人"
                current_content = []
            elif "法定代表人" in line and len(line) < 30:
                if current_field and current_content:
                    parsed[current_field] = " ".join(current_content)
                current_field = "法定代表人"
                current_content = []
            elif "执法部门" in line and len(line) < 20:
                if current_field and current_content:
                    parsed[current_field] = " ".join(current_content)
                current_field = "执法部门"
                current_content = []
            elif "作出行政处罚的日期" in line or "处罚日期" in line:
                if current_field and current_content:
                    parsed[current_field] = " ".join(current_content)
                current_field = "决定日期"
                current_content = []
            elif "主要违法事实" in line and len(line) < 30:
                if current_field and current_content:
                    parsed[current_field] = " ".join(current_content)
                current_field = "主要违法事实"
                current_content = []
            elif "处罚种类" in line or "处罚依据" in line:
                if current_field and current_content:
                    parsed[current_field] = " ".join(current_content)
                current_field = "处罚种类和依据"
                current_content = []
            elif "行政处罚决定" in line and len(line) < 30:
                if current_field and current_content:
                    parsed[current_field] = " ".join(current_content)
                current_field = "行政处罚决定"
                current_content = []
            elif "履行方式" in line or "履行期限" in line:
                if current_field and current_content:
                    parsed[current_field] = " ".join(current_content)
                current_field = "履行方式"
                current_content = []
            elif "救济途径" in line:
                if current_field and current_content:
                    parsed[current_field] = " ".join(current_content)
                current_field = "救济途径"
                current_content = []
            else:
                if current_field:
                    current_content.append(line)

        if current_field and current_content:
            parsed[current_field] = " ".join(current_content)

    # 生成Markdown
    md = f"# {case_name}\n\n## 案件基本信息\n\n"
    if parsed["处罚决定文书号"]:
        md += f"**处罚决定文书号**：{parsed['处罚决定文书号']}\n\n"
    if parsed["被处罚人"]:
        md += f"**被处罚人**：{parsed['被处罚人']}\n\n"
    if parsed["法定代表人"]:
        md += f"**法定代表人**：{parsed['法定代表人']}\n\n"
    if parsed["执法部门"]:
        md += f"**执法部门**：{parsed['执法部门']}\n\n"
    if parsed["决定日期"]:
        md += f"**作出决定日期**：{parsed['决定日期']}\n\n"

    if parsed["主要违法事实"]:
        md += f"## 主要违法事实\n\n{parsed['主要违法事实']}\n\n"

    if parsed["处罚种类和依据"]:
        md += f"## 处罚种类和依据\n\n{parsed['处罚种类和依据']}\n\n"

    if parsed["行政处罚决定"]:
        md += f"## 行政处罚决定\n\n{parsed['行政处罚决定']}\n\n"

    if parsed["履行方式"]:
        md += f"## 履行方式和期限\n\n{parsed['履行方式']}\n\n"

    if parsed["救济途径"]:
        md += f"## 救济途径\n\n{parsed['救济途径']}\n\n"

    md += "---\n\n**数据来源**：浙江省政务服务网\n**抓取时间**：2026-06-21\n**案件序号**：第{case_num}号案例\n"

    # 保存文件
    safe_name = re.sub(r'[<>:"/\\|?*]', '', case_name).replace(' ', '_')
    filename = f"{case_num}_{safe_name}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md)

    return filename

def main():
    print("="*70)
    print("批量抓取12个行政处罚案例的完整详情")
    print("="*70)

    # 确保输出目录存在
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )

        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            locale='zh-CN'
        )

        page = context.new_page()

        success_count = 0

        try:
            # 访问列表页
            print("访问列表页面...")
            page.goto(TARGET_URL, wait_until="load", timeout=60000)
            time.sleep(5)

            # 等待表格
            page.wait_for_selector("tbody tr", timeout=30000)
            time.sleep(2)

            # 抓取第一页的案例1-10
            for case_num in range(1, 11):
                print(f"\n处理案例{case_num}...")

                # 如果不是第一个案例，重新导航
                if case_num > 1:
                    page.goto(TARGET_URL, wait_until="load", timeout=30000)
                    time.sleep(4)
                    page.wait_for_selector("tbody tr", timeout=20000)
                    time.sleep(2)

                row = page.query_selector(f"tbody tr:nth-child({case_num})")
                if row:
                    cell_1 = row.query_selector("td:nth-child(1)")
                    cell_5 = row.query_selector("td:nth-child(5)")

                    name = cell_1.inner_text().strip() if cell_1 else ""
                    print(f"  案件名称: {name[:50]}...")

                    if cell_5:
                        link = cell_5.query_selector("a")
                        if link:
                            print(f"  ✓ 点击详情链接")
                            link.click()
                            time.sleep(6)

                            if is_on_detail_page(page):
                                print(f"  ✓ 进入详情页")
                                content = get_page_text(page)
                                print(f"  内容长度: {len(content)} 字符")

                                if len(content) > 500:
                                    filename = parse_and_save(case_num, name, content)
                                    print(f"  ✓ 已保存: {filename}")
                                    success_count += 1
                                else:
                                    print(f"  ✗ 内容过短")
                            else:
                                print(f"  ✗ 未进入详情页")

            # 翻到第二页抓取案例11-12
            print("\n翻到第二页...")
            page.goto(TARGET_URL, wait_until="load", timeout=30000)
            time.sleep(4)
            page.wait_for_selector("tbody tr", timeout=20000)
            time.sleep(2)

            page.evaluate("""
                () => {
                    const paging = document.querySelector('.paging-module');
                    if (paging) {
                        const items = paging.querySelectorAll('li, a, button, span');
                        for (let item of items) {
                            if (item.textContent.trim() === '2') {
                                item.click();
                                return true;
                            }
                        }
                    }
                    return false;
                }
            """)
            time.sleep(6)
            page.wait_for_selector("tbody tr", timeout=20000)
            time.sleep(2)

            # 抓取案例11-12
            for case_num in [11, 12]:
                print(f"\n处理案例{case_num}...")

                row_num = case_num - 10
                row = page.query_selector(f"tbody tr:nth-child({row_num})")
                if row:
                    cell_1 = row.query_selector("td:nth-child(1)")
                    cell_5 = row.query_selector("td:nth-child(5)")

                    name = cell_1.inner_text().strip() if cell_1 else ""
                    print(f"  案件名称: {name[:50]}...")

                    if cell_5:
                        link = cell_5.query_selector("a")
                        if link:
                            print(f"  ✓ 点击详情链接")
                            link.click()
                            time.sleep(6)

                            if is_on_detail_page(page):
                                print(f"  ✓ 进入详情页")
                                content = get_page_text(page)
                                print(f"  内容长度: {len(content)} 字符")

                                if len(content) > 500:
                                    filename = parse_and_save(case_num, name, content)
                                    print(f"  ✓ 已保存: {filename}")
                                    success_count += 1
                                else:
                                    print(f"  ✗ 内容过短")

                                # 返回列表页
                                page.goto(TARGET_URL, wait_until="load", timeout=30000)
                                time.sleep(4)
                                page.evaluate("""
                                    () => {
                                        const paging = document.querySelector('.paging-module');
                                        if (paging) {
                                            const items = paging.querySelectorAll('li, a, button, span');
                                            for (let item of items) {
                                                if (item.textContent.trim() === '2') {
                                                    item.click();
                                                    return true;
                                                }
                                            }
                                        }
                                        return false;
                                    }
                                """)
                                time.sleep(6)
                                page.wait_for_selector("tbody tr", timeout=20000)
                                time.sleep(2)
                            else:
                                print(f"  ✗ 未进入详情页")

            browser.close()
            print(f"\n{'='*70}")
            print(f"抓取完成！成功: {success_count}/12")
            print(f"{'='*70}\n")

        except Exception as e:
            print(f"\n错误: {e}")
            import traceback
            traceback.print_exc()
            try:
                browser.close()
            except:
                pass

if __name__ == "__main__":
    main()
