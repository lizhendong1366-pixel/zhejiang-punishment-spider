import os
import csv
import time
from playwright.sync_api import sync_playwright

# 配置项
TARGET_URL = "https://xzcf.zjzwfw.gov.cn/punishment/#/Punish"
SAVE_DIR = "/Users/lizhendong/Documents/claude code"
SAVE_PATH = os.path.join(SAVE_DIR, "zhejiang_punishment_data.csv")

def run_spider():
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

        # 访问页面并等待网络空闲
        try:
            page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)
            print("页面加载完成，等待 JavaScript 渲染...")
        except Exception as e:
            print(f"页面加载超时或出错: {e}")
            browser.close()
            return

        # 等待 JavaScript 渲染
        page.wait_for_timeout(5000)

        # 调试：打印页面标题
        print(f"页面标题: {page.title()}")

        # 检查页面是否真的加载了
        page_content = page.content()
        if "el-table" in page_content or "table" in page_content.lower():
            print("检测到表格元素存在")
        else:
            print("警告: 页面中未检测到表格元素")

        # 准备 CSV 文件
        csv_file = open(SAVE_PATH, 'w', newline='', encoding='utf-8-sig')
        writer = csv.writer(csv_file)
        # 写入表头
        writer.writerow(["决定书文号", "案件名称", "处罚对象", "处罚单位", "处罚决定日期"])

        # 抓取逻辑 (示例抓取前 3 页)
        max_pages = 3
        current_page = 1
        total_records = 0

        while current_page <= max_pages:
            print(f"\n正在处理第 {current_page} 页...")
            page.wait_for_timeout(3000)  # 等待数据渲染完成

            # 尝试多种选择器
            rows = page.query_selector_all(".el-table__row")
            if len(rows) == 0:
                print("未找到 .el-table__row，尝试其他选择器...")
                rows = page.query_selector_all("tbody tr")
            if len(rows) == 0:
                print("未找到 tbody tr，尝试...")
                rows = page.query_selector_all("tr")

            print(f"找到 {len(rows)} 行数据")

            page_row_count = 0
            for i, row in enumerate(rows):
                try:
                    cols = row.query_selector_all("td")
                    if len(cols) >= 5:
                        data = [col.inner_text().strip() for col in cols[:5]]
                        writer.writerow(data)
                        page_row_count += 1
                        total_records += 1
                        if i < 3:  # 打印前3条数据作为示例
                            print(f"  数据示例 {i+1}: {data[0]}")
                except Exception as e:
                    print(f"处理行 {i} 时出错: {e}")
                    continue

            print(f"第 {current_page} 页成功写入 {page_row_count} 行数据")

            # 翻页逻辑
            if current_page >= max_pages:
                print(f"已达到最大页数限制 ({max_pages} 页)")
                break

            try:
                # 尝试查找下一页按钮
                next_selectors = [
                    'button.btn-next',
                    '.btn-next',
                    'li.el-pagination__next',
                    '.pagination-next'
                ]

                next_clicked = False
                for selector in next_selectors:
                    try:
                        next_button = page.locator(selector).first
                        if next_button.is_visible() and next_button.is_enabled():
                            print(f"找到下一页按钮: {selector}")
                            next_button.click()
                            next_clicked = True
                            page.wait_for_timeout(3000)
                            break
                    except:
                        continue

                if not next_clicked:
                    print("未找到可用的下一页按钮")
                    break

                current_page += 1

            except Exception as e:
                print(f"翻页时出错: {e}")
                break

        csv_file.close()
        print(f"\n抓取完成！")
        print(f"总共抓取了 {total_records} 条记录")
        print(f"数据已保存至: {SAVE_PATH}")

        browser.close()

if __name__ == "__main__":
    run_spider()
