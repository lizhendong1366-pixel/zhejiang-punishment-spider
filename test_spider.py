"""
行政处罚数据爬虫测试版本 - 抓取前3页
"""
import os
import csv
import time
from playwright.sync_api import sync_playwright

# 配置项
TARGET_URL = "https://xzcf.zjzwfw.gov.cn/punishment/#/Punish"
SAVE_DIR = "/Users/lizhendong/Documents/claude code"
SAVE_PATH = os.path.join(SAVE_DIR, "zhejiang_punishment_test.csv")

def run_spider(max_pages=3):
    """
    运行爬虫
    max_pages: 最大抓取页数
    """
    # 1. 确保目录存在
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        print(f"创建目录: {SAVE_DIR}")

    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        print(f"正在访问: {TARGET_URL}")

        # 访问页面，增加重试机制
        max_retries = 3
        for attempt in range(max_retries):
            try:
                page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
                print("页面加载成功")
                break
            except Exception as e:
                print(f"尝试 {attempt + 1}/{max_retries} 失败: {e}")
                if attempt < max_retries - 1:
                    print("5秒后重试...")
                    time.sleep(5)
                else:
                    raise

        print("等待页面渲染...")
        page.wait_for_timeout(5000)

        # 准备 CSV 文件
        csv_file = open(SAVE_PATH, 'w', newline='', encoding='utf-8-sig')
        writer = csv.writer(csv_file)
        # 写入表头
        writer.writerow(["案件名称", "处罚对象", "决定书文号", "处罚决定日期", "详情"])

        current_page = 1
        total_records = 0
        last_first_data = None

        print("\n开始抓取数据...")

        while current_page <= max_pages:
            print(f"\n正在处理第 {current_page} 页...")
            page.wait_for_timeout(2000)

            # 获取当前页数据
            rows = page.query_selector_all("tbody tr")
            print(f"找到 {len(rows)} 行数据")

            page_row_count = 0
            page_data = []

            for i, row in enumerate(rows):
                try:
                    cols = row.query_selector_all("td")
                    if len(cols) >= 5:
                        data = [col.inner_text().strip() for col in cols[:5]]
                        page_data.append(data)

                        # 检查重复
                        if i == 0 and last_first_data and data == last_first_data:
                            print("检测到数据重复，已到达最后一页")
                            csv_file.close()
                            browser.close()
                            return

                        writer.writerow(data)
                        page_row_count += 1
                        total_records += 1

                        # 显示前3条数据
                        if i < 3:
                            print(f"  {i+1}. {data[0][:30]}... | {data[2]}")

                except Exception as e:
                    print(f"处理行时出错: {e}")
                    continue

            # 记录第一条数据用于检测重复
            if page_data:
                last_first_data = page_data[0]

            print(f"第 {current_page} 页完成: {page_row_count} 行 | 总计: {total_records} 条")

            # 如果是最后一页，不再翻页
            if current_page >= max_pages:
                break

            # 尝试翻页
            try:
                # 使用JavaScript点击下一个页码
                success = page.evaluate("""
                    () => {
                        const current = document.querySelector('li.active');
                        if (current && current.nextElementSibling) {
                            const next = current.nextElementSibling;
                            if (next.tagName === 'LI' && !next.classList.contains('disabled')) {
                                const pageNum = next.textContent.trim();
                                if (pageNum && pageNum !== '•••') {
                                    next.click();
                                    return true;
                                }
                            }
                        }
                        return false;
                    }
                """)

                if success:
                    print(f"成功翻到第 {current_page + 1} 页")
                    current_page += 1
                    page.wait_for_timeout(3000)
                else:
                    print("无法翻到下一页，可能已到达最后一页")
                    break

            except Exception as e:
                print(f"翻页时出错: {e}")
                break

        csv_file.close()
        browser.close()

        print(f"\n" + "="*60)
        print(f"抓取完成！")
        print(f"总共抓取: {current_page} 页，{total_records} 条记录")
        print(f"保存位置: {SAVE_PATH}")
        print(f"="*60)

if __name__ == "__main__":
    print("开始运行爬虫...")
    run_spider(max_pages=3)
