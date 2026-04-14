"""
行政处罚数据爬虫 - 自动化版本
使用截图记录状态，自动分析翻页机制
"""
import os
import csv
import time
from playwright.sync_api import sync_playwright

TARGET_URL = "https://xzcf.zjzwfw.gov.cn/punishment/#/Punish"
SAVE_PATH = "/Users/lizhendong/Documents/claude code/zhejiang_punishment_data.csv"
SCREENSHOT_DIR = "/Users/lizhendong/Documents/claude code/screenshots"

def main():
    """主函数"""

    # 创建目录
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    print("="*70)
    print("浙江省行政处罚数据爬虫 - 自动化版本")
    print("="*70)
    print(f"目标: {TARGET_URL}")
    print(f"保存: {SAVE_PATH}")
    print(f"截图: {SCREENSHOT_DIR}\n")

    with sync_playwright() as p:
        print("启动浏览器...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        print("访问页面...")
        page.goto(TARGET_URL, timeout=60000)
        time.sleep(5)

        # 截图初始状态
        page.screenshot(path=f"{SCREENSHOT_DIR}/01_initial.png")
        print("✓ 页面加载完成")

        # 获取分页信息
        print("\n分析分页结构...")
        paging_info = page.evaluate("""
            () => {
                const result = {
                    found: false,
                    items: [],
                    current: null
                };

                const paging = document.querySelector('.paging-module');
                if (!paging) return result;

                result.found = true;

                const lis = paging.querySelectorAll('li');
                lis.forEach((li, i) => {
                    const text = li.textContent.trim();
                    const className = li.className;
                    const isCurrent = className.includes('active');

                    if (isCurrent) {
                        result.current = parseInt(text);
                    }

                    result.items.push({
                        index: i,
                        text: text,
                        className: className,
                        isCurrent: isCurrent
                    });
                });

                return result;
            }
        """)

        print(f"  分页模块: {'✓ 找到' if paging_info['found'] else '✗ 未找到'}")
        print(f"  当前页码: {paging_info.get('current')}")
        print(f"  页码数量: {len(paging_info.get('items', []))}")

        # 显示前15个页码项
        for item in paging_info.get('items', [])[:15]:
            marker = "→" if item['isCurrent'] else " "
            print(f"    {marker} [{item['index']}] '{item['text']}' ({item['className']})")

        # 准备CSV
        csv_file = open(SAVE_PATH, 'w', newline='', encoding='utf-8-sig')
        writer = csv.writer(csv_file)
        writer.writerow(["序号", "案件名称", "处罚对象", "决定书文号", "处罚决定日期"])

        print("\n开始抓取...\n")

        total_records = 0
        current_page_num = 1
        max_pages = 10
        last_first_record = None

        while current_page_num <= max_pages:
            print(f"[第 {current_page_num} 页] ", end="", flush=True)
            time.sleep(2)

            # 获取表格数据
            rows = page.query_selector_all("tbody tr")
            if not rows:
                print("✗ 无数据")
                break

            page_records = []
            for row in rows:
                cols = row.query_selector_all("td")
                if len(cols) >= 4:
                    data = [col.inner_text().strip() for col in cols[:4]]
                    page_records.append(data)

            if not page_records:
                print("✗ 无有效数据")
                break

            # 检查重复
            if last_first_record and page_records[0] == last_first_record:
                print("✗ 重复数据，已到最后一页")
                break

            # 写入数据
            for i, record in enumerate(page_records):
                writer.writerow([total_records + i + 1] + record)
            total_records += len(page_records)

            print(f"✓ {len(page_records)} 条 | 总计: {total_records} 条")
            print(f"  首条: {page_records[0][0][:40]}...")

            # 记录第一条
            last_first_record = page_records[0]

            # 截图当前页
            page.screenshot(path=f"{SCREENSHOT_DIR}/page_{current_page_num}.png")

            # 如果是最后一页
            if current_page_num >= max_pages:
                break

            # 尝试翻页
            print(f"  → 点击第 {current_page_num + 1} 页...", end=" ", flush=True)

            # 使用JavaScript点击下一页数字
            clicked = page.evaluate(f"""
                (targetPage) => {{
                    const paging = document.querySelector('.paging-module');
                    if (!paging) return false;

                    const lis = paging.querySelectorAll('li');
                    for (let li of lis) {{
                        const text = li.textContent.trim();
                        if (/^\\d+$/.test(text) && parseInt(text) === targetPage) {{
                            li.scrollIntoView({{block: 'center'}});
                            setTimeout(() => {{
                                li.click();
                            }}, 100);
                            return true;
                        }}
                    }}
                    return false;
                }}
            """, current_page_num + 1)

            if clicked:
                print("✓")
                current_page_num += 1
                time.sleep(4)  # 等待页面加载
                page.screenshot(path=f"{SCREENSHOT_DIR}/after_page_{current_page_num-1}.png")
            else:
                print("✗ 无法翻页")
                break

        # 完成
        csv_file.close()
        browser.close()

        print(f"\n{'='*70}")
        print("✓ 抓取完成！")
        print(f"  总页数: {current_page_num} 页")
        print(f"  总记录: {total_records} 条")
        print(f"  数据文件: {SAVE_PATH}")
        print(f"  截图目录: {SCREENSHOT_DIR}")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
