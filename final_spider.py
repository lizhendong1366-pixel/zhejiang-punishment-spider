"""
行政处罚数据爬虫 - 多页版本
支持自动翻页，可靠稳定
"""
import os
import csv
import time
from playwright.sync_api import sync_playwright

TARGET_URL = "https://xzcf.zjzwfw.gov.cn/punishment/#/Punish"
SAVE_PATH = "/Users/lizhendong/Documents/claude code/zhejiang_punishment_data.csv"

def scrape_page(page, page_num, writer, start_index):
    """抓取单页数据"""
    print(f"[第 {page_num} 页] ", end="", flush=True)

    # 等待表格
    time.sleep(3)

    # 获取数据行
    rows = page.query_selector_all("tbody tr")

    if not rows:
        print("✗ 未找到数据")
        return 0, None

    page_records = []
    for row in rows:
        cols = row.query_selector_all("td")
        if len(cols) >= 4:
            data = [col.inner_text().strip() for col in cols[:4]]
            page_records.append(data)

    if not page_records:
        print("✗ 无有效数据")
        return 0, None

    # 写入CSV
    for i, record in enumerate(page_records):
        writer.writerow([start_index + i + 1] + record)

    print(f"✓ {len(page_records)} 条")
    if page_records:
        print(f"  首条: {page_records[0][0][:40]}...")

    return len(page_records), page_records[0]

def click_next_page(page):
    """点击下一页"""
    try:
        # 使用JavaScript查找并点击下一页
        success = page.evaluate("""
            () => {
                // 查找所有数字页码
                const pagingModule = document.querySelector('.paging-module');
                if (!pagingModule) return false;

                // 找到当前激活的页码
                const current = pagingModule.querySelector('li.active');
                if (!current) return false;

                // 点击下一个页码
                const next = current.nextElementSibling;
                if (next && next.tagName === 'LI') {
                    const text = next.textContent.trim();
                    // 只点击数字页码，不点击"下一页"按钮或省略号
                    if (/^\d+$/.test(text)) {
                        next.scrollIntoView();
                        next.click();
                        return true;
                    }
                }

                return false;
            }
        """)

        return success
    except:
        return False

def main(max_pages=10):
    """主函数"""

    # 确保目录存在
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

    print("="*70)
    print("浙江省行政处罚数据爬虫")
    print("="*70)
    print(f"目标: {TARGET_URL}")
    print(f"保存: {SAVE_PATH}")
    print(f"页数: {max_pages} 页\n")

    with sync_playwright() as p:
        print("启动浏览器...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={'width': 1280, 'height': 800})

        print("访问页面...")
        page.goto(TARGET_URL, timeout=60000)
        print("等待加载...")
        time.sleep(8)

        # 准备CSV
        csv_file = open(SAVE_PATH, 'w', newline='', encoding='utf-8-sig')
        writer = csv.writer(csv_file)
        writer.writerow(["序号", "案件名称", "处罚对象", "决定书文号", "处罚决定日期"])

        total_records = 0
        last_first_record = None
        duplicate_count = 0

        print("\n开始抓取...\n")

        for page_num in range(1, max_pages + 1):
            count, first_record = scrape_page(page, page_num, writer, total_records)
            total_records += count

            # 检查重复
            if first_record:
                if last_first_record and first_record == last_first_record:
                    duplicate_count += 1
                    print(f"  ⚠ 检测到重复页 (第{duplicate_count}次)")
                    if duplicate_count >= 2:
                        print("\n✓ 已到达最后一页")
                        break
                else:
                    duplicate_count = 0
                last_first_record = first_record

            # 如果是最后一页，结束
            if page_num >= max_pages:
                break

            # 尝试翻页
            print("  → 翻页...", end=" ", flush=True)
            if click_next_page(page):
                print("✓")
                time.sleep(4)  # 等待新页面加载
            else:
                print("✗ 无法翻页")
                break

        # 完成
        csv_file.close()
        browser.close()

        print(f"\n{'='*70}")
        print("✓ 抓取完成！")
        print(f"  总记录: {total_records} 条")
        print(f"  保存位置: {SAVE_PATH}")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    # 抓取10页
    print("开始抓取 10 页数据...\n")
    main(max_pages=10)
