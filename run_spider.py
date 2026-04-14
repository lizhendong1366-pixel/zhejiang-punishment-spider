"""
行政处罚数据爬虫 - 直接运行版本
抓取前10页数据进行测试
"""
import os
import csv
import time
from playwright.sync_api import sync_playwright

# 配置项
TARGET_URL = "https://xzcf.zjzwfw.gov.cn/punishment/#/Punish"
SAVE_DIR = "/Users/lizhendong/Documents/claude code"
SAVE_PATH = os.path.join(SAVE_DIR, "zhejiang_punishment_data.csv")

def run_spider(max_pages=10):
    """运行爬虫"""

    # 确保目录存在
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    with sync_playwright() as p:
        print("="*60)
        print("浙江省行政处罚数据爬虫")
        print("="*60)
        print(f"\n目标网站: {TARGET_URL}")
        print(f"保存位置: {SAVE_PATH}")
        print(f"抓取页数: {max_pages} 页")
        print(f"\n开始抓取...\n")

        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        # 访问页面
        try:
            page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
            print("✓ 页面加载成功")
        except Exception as e:
            print(f"✗ 页面加载失败: {e}")
            browser.close()
            return

        page.wait_for_timeout(5000)

        # 准备CSV文件
        csv_file = open(SAVE_PATH, 'w', newline='', encoding='utf-8-sig')
        writer = csv.writer(csv_file)
        writer.writerow(["案件名称", "处罚对象", "决定书文号", "处罚决定日期", "详情"])

        # 抓取状态
        current_page = 1
        total_records = 0
        last_first_record = None

        while current_page <= max_pages:
            print(f"[第 {current_page}/{max_pages} 页] ", end="")

            page.wait_for_timeout(2000)

            # 获取数据
            rows = page.query_selector_all("tbody tr")

            if not rows:
                print("✗ 未找到数据")
                break

            page_records = []
            for row in rows:
                try:
                    cols = row.query_selector_all("td")
                    if len(cols) >= 5:
                        data = [col.inner_text().strip() for col in cols[:5]]
                        page_records.append(data)
                except:
                    continue

            # 检查重复
            if page_records and last_first_record:
                if page_records[0] == last_first_record:
                    print("✓ 检测到重复，已到最后一页")
                    break

            # 写入数据
            for record in page_records:
                writer.writerow(record)
                total_records += 1

            if page_records:
                last_first_record = page_records[0]

            print(f"✓ {len(page_records)} 条 | 累计: {total_records} 条")

            # 显示第一条数据
            if page_records:
                case_name = page_records[0][0][:40]
                print(f"  最新: {case_name}...")

            # 尝试翻页
            if current_page < max_pages:
                try:
                    success = page.evaluate(f"""
                        () => {{
                            const activeLi = document.querySelector('.paging-module li.active');
                            if (!activeLi) return false;

                            const current = parseInt(activeLi.textContent.trim());
                            const allLis = document.querySelectorAll('.paging-module li');

                            for (let li of allLis) {{
                                const pageNum = parseInt(li.textContent.trim());
                                if (pageNum === current + 1) {{
                                    li.click();
                                    return true;
                                }}
                            }}
                            return false;
                        }}
                    """)

                    if success:
                        current_page += 1
                        page.wait_for_timeout(3000)
                    else:
                        print("\n✓ 无法继续翻页")
                        break
                except Exception as e:
                    print(f"\n✗ 翻页错误: {e}")
                    break
            else:
                break

        csv_file.close()
        browser.close()

        print(f"\n{'='*60}")
        print("✓ 抓取完成！")
        print(f"  总页数: {current_page} 页")
        print(f"  总记录: {total_records} 条")
        print(f"  文件: {SAVE_PATH}")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    run_spider(max_pages=10)
