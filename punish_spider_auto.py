"""
行政处罚数据自动爬虫 - 自动化翻页版本
自动抓取所有页面数据
"""
import os
import csv
import time
from playwright.sync_api import sync_playwright

# 配置项
TARGET_URL = "https://xzcf.zjzwfw.gov.cn/punishment/#/Punish"
SAVE_DIR = "/Users/lizhendong/Documents/claude code"
SAVE_PATH = os.path.join(SAVE_DIR, "zhejiang_punishment_data_full.csv")

def run_spider(max_pages=None):
    """
    运行爬虫
    max_pages: 最大抓取页数，None表示抓取所有页面
    """
    # 1. 确保目录存在
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        print(f"创建目录: {SAVE_DIR}")

    with sync_playwright() as p:
        # 启动浏览器 (headless=True 可以提高速度)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        print(f"正在访问: {TARGET_URL}")
        page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)
        print("等待页面渲染...")
        page.wait_for_timeout(5000)

        # 准备 CSV 文件
        csv_file = open(SAVE_PATH, 'w', newline='', encoding='utf-8-sig')
        writer = csv.writer(csv_file)
        # 写入表头
        writer.writerow(["案件名称", "处罚对象", "决定书文号", "处罚决定日期", "详情"])

        current_page = 1
        total_records = 0
        no_new_data_count = 0  # 检测是否没有新数据
        last_data = None  # 记录上一页的第一条数据

        print("\n开始抓取数据...")

        while True:
            print(f"\n正在处理第 {current_page} 页...")
            page.wait_for_timeout(2000)  # 等待数据渲染

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

                        # 检查是否与上一页的第一条数据重复（防止无限循环）
                        if i == 0 and last_data and data == last_data:
                            print("检测到数据重复，可能已到达最后一页")
                            no_new_data_count += 1
                            break

                        writer.writerow(data)
                        page_row_count += 1
                        total_records += 1
                except Exception as e:
                    print(f"处理行时出错: {e}")
                    continue

            # 记录当前页第一条数据
            if page_data:
                last_data = page_data[0]

            print(f"第 {current_page} 页成功写入 {page_row_count} 行数据")
            print(f"总计已抓取 {total_records} 条记录")

            # 检查是否达到最大页数
            if max_pages and current_page >= max_pages:
                print(f"\n已达到最大页数限制 ({max_pages} 页)")
                break

            # 检查是否连续多次没有新数据
            if no_new_data_count >= 2:
                print("\n检测到已到达最后一页，停止抓取")
                break

            # 尝试翻页
            try:
                # 方法1: 点击当前页码的下一个页码
                # 查找当前激活的页码，然后点击下一个
                current_active = page.query_selector("li.active")
                if current_active:
                    print(f"当前页码: {current_active.inner_text().strip()}")
                    # 尝试点击下一个兄弟元素
                    next_page = page.evaluate("""
                        () => {
                            const current = document.querySelector('li.active');
                            if (current && current.nextElementSibling) {
                                const next = current.nextElementSibling;
                                if (next.tagName === 'LI' && next.textContent.trim() !== '•••') {
                                    next.click();
                                    return true;
                                }
                            }
                            return false;
                        }
                    """)

                    if next_page:
                        print("成功点击下一页")
                        current_page += 1
                        page.wait_for_timeout(3000)
                        continue

                # 方法2: 如果方法1失败，尝试直接点击数字页码
                page.evaluate(f"""
                    () => {{
                        const pageLinks = document.querySelectorAll('.paging-module li');
                        const targetPage = {current_page + 1};
                        for (let link of pageLinks) {{
                            const pageNum = parseInt(link.textContent.trim());
                            if (pageNum === targetPage) {{
                                link.click();
                                return true;
                            }}
                        }}
                        return false;
                    }}
                """)

                print("尝试通过页码翻页")
                current_page += 1
                page.wait_for_timeout(3000)

                # 验证是否真的翻页了
                new_rows = page.query_selector_all("tbody tr")
                if len(new_rows) == 0:
                    print("翻页后未找到数据，可能已到达最后一页")
                    break

            except Exception as e:
                print(f"翻页时出错: {e}")
                print("尝试其他翻页方法...")

                # 最后的尝试：直接构造URL（如果网站支持）
                try:
                    new_url = f"{TARGET_URL}?page={current_page + 1}"
                    page.goto(new_url, wait_until="networkidle", timeout=30000)
                    page.wait_for_timeout(3000)
                    current_page += 1
                except:
                    print("所有翻页方法都失败，停止抓取")
                    break

        csv_file.close()
        print(f"\n" + "="*50)
        print(f"抓取完成！")
        print(f"总共抓取了 {current_page} 页，{total_records} 条记录")
        print(f"数据已保存至: {SAVE_PATH}")
        print(f"="*50)

        browser.close()

if __name__ == "__main__":
    # 可以设置最大页数，比如 5 页，或者设置为 None 抓取所有页面
    print("选择抓取模式：")
    print("1. 抓取前 5 页（测试）")
    print("2. 抓取前 50 页")
    print("3. 抓取所有页面（可能需要很长时间）")

    choice = input("请输入选择 (1/2/3): ").strip()

    if choice == "1":
        run_spider(max_pages=5)
    elif choice == "2":
        run_spider(max_pages=50)
    elif choice == "3":
        confirm = input("确定要抓取所有页面吗？这可能需要很长时间。输入 'yes' 确认: ")
        if confirm.lower() == 'yes':
            run_spider(max_pages=None)
        else:
            print("已取消")
    else:
        print("无效选择，默认抓取前 5 页")
        run_spider(max_pages=5)
