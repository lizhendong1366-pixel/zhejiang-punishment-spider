"""
行政处罚数据爬虫 - 简单可靠版本
"""
import os
import csv
import time
from playwright.sync_api import sync_playwright

TARGET_URL = "https://xzcf.zjzwfw.gov.cn/punishment/#/Punish"
SAVE_PATH = "/Users/lizhendong/Documents/claude code/zhejiang_punishment_data.csv"

def main():
    # 确保目录存在
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

    with sync_playwright() as p:
        print("启动浏览器...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={'width': 1280, 'height': 800})

        print(f"访问: {TARGET_URL}")
        page.goto(TARGET_URL, timeout=60000)
        print("等待页面加载...")
        time.sleep(8)  # 给足够时间加载

        # 准备CSV
        csv_file = open(SAVE_PATH, 'w', newline='', encoding='utf-8-sig')
        writer = csv.writer(csv_file)
        writer.writerow(["序号", "案件名称", "处罚对象", "决定书文号", "处罚决定日期"])

        total = 0

        # 只抓取第一页作为测试
        print("抓取数据...")
        rows = page.query_selector_all("tbody tr")
        print(f"找到 {len(rows)} 行")

        for i, row in enumerate(rows):
            cols = row.query_selector_all("td")
            if len(cols) >= 4:
                data = [col.inner_text().strip() for col in cols[:4]]
                writer.writerow([total+1] + data)
                total += 1
                print(f"  {total}. {data[0][:40]}...")

        csv_file.close()
        browser.close()

        print(f"\n✓ 完成！抓取了 {total} 条记录")
        print(f"✓ 保存到: {SAVE_PATH}")

if __name__ == "__main__":
    main()
