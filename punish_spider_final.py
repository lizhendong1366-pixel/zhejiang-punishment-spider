"""
行政处罚数据爬虫 - 最终优化版
支持智能翻页和大规模数据抓取
"""
import os
import csv
import time
from playwright.sync_api import sync_playwright

# 配置项
TARGET_URL = "https://xzcf.zjzwfw.gov.cn/punishment/#/Punish"
SAVE_DIR = "/Users/lizhendong/Documents/claude code"
SAVE_PATH = os.path.join(SAVE_DIR, "zhejiang_punishment_data.csv")

def run_spider(max_pages=10, delay=2):
    """
    运行爬虫

    参数:
    - max_pages: 最大抓取页数（默认10页）
    - delay: 每页之间的延迟秒数（默认2秒）
    """
    # 1. 确保目录存在
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        print(f"✓ 创建目录: {SAVE_DIR}")

    with sync_playwright() as p:
        print("启动浏览器...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = context.new_page()

        # 访问页面
        print(f"→ 访问: {TARGET_URL}")
        try:
            page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
        except Exception as e:
            print(f"✗ 页面加载失败: {e}")
            browser.close()
            return

        # 等待JavaScript渲染
        print("→ 等待页面渲染...")
        page.wait_for_timeout(5000)

        # 验证页面加载成功
        page_title = page.title()
        print(f"→ 页面标题: {page_title}")

        # 准备 CSV 文件
        csv_file = open(SAVE_PATH, 'w', newline='', encoding='utf-8-sig')
        writer = csv.writer(csv_file)
        writer.writerow(["案件名称", "处罚对象", "决定书文号", "处罚决定日期", "详情"])

        # 抓取状态
        current_page = 1
        total_records = 0
        consecutive_empty_pages = 0
        last_first_record = None

        print(f"\n{'='*60}")
        print("开始抓取数据...")
        print(f"目标: {max_pages} 页 | 延迟: {delay}秒")
        print(f"{'='*60}\n")

        while current_page <= max_pages:
            print(f"[第 {current_page} 页] 正在抓取...")
            page.wait_for_timeout(delay * 1000)

            # 获取表格数据
            rows = page.query_selector_all("tbody tr")

            if not rows:
                print(f"  ✗ 未找到数据行")
                consecutive_empty_pages += 1
                if consecutive_empty_pages >= 3:
                    print("\n✗ 连续3页无数据，停止抓取")
                    break
                # 尝试翻页继续
                current_page += 1
                continue

            consecutive_empty_pages = 0  # 重置计数器

            page_records = []
            for i, row in enumerate(rows):
                try:
                    cols = row.query_selector_all("td")
                    if len(cols) >= 5:
                        data = [col.inner_text().strip() for col in cols[:5]]
                        page_records.append(data)
                except Exception as e:
                    print(f"  ✗ 处理第 {i+1} 行时出错: {e}")
                    continue

            # 检查是否到达最后一页（重复数据检测）
            if page_records and last_first_record:
                if page_records[0] == last_first_record:
                    print(f"  ✓ 检测到重复数据，已到达最后一页")
                    break

            # 写入数据
            for i, record in enumerate(page_records):
                writer.writerow(record)
                total_records += 1
                # 显示前3条
                if i < 3:
                    case_name = record[0][:30] + "..." if len(record[0]) > 30 else record[0]
                    print(f"  {i+1}. {case_name} | {record[2]}")

            # 记录当前页第一条数据
            if page_records:
                last_first_record = page_records[0]

            print(f"  ✓ 本页: {len(page_records)} 条 | 累计: {total_records} 条")

            # 检查是否到达最后一页
            if current_page >= max_pages:
                print(f"\n✓ 已达到设定页数限制 ({max_pages} 页)")
                break

            # 尝试翻页
            print(f"  → 翻到第 {current_page + 1} 页...")
            try:
                # 方法1: 点击页码
                next_clicked = page.evaluate(f"""
                    () => {{
                        // 查找当前激活的页码
                        const activeLi = document.querySelector('.paging-module li.active');
                        if (!activeLi) return false;

                        // 获取当前页码
                        const currentPage = parseInt(activeLi.textContent.trim());

                        // 查找下一页的链接
                        const allLis = document.querySelectorAll('.paging-module li');
                        for (let li of allLis) {{
                            const pageNum = parseInt(li.textContent.trim());
                            if (pageNum === currentPage + 1) {{
                                li.click();
                                return true;
                            }}
                        }}

                        // 如果找不到具体页码，尝试点击当前页的下一个兄弟元素
                        const nextLi = activeLi.nextElementSibling;
                        if (nextLi && nextLi.tagName === 'LI') {{
                            const text = nextLi.textContent.trim();
                            if (text && text !== '•••') {{
                                nextLi.click();
                                return true;
                            }}
                        }}

                        return false;
                    }}
                """)

                if next_clicked:
                    current_page += 1
                    page.wait_for_timeout(3000)
                else:
                    print(f"\n  ✗ 无法翻页，可能已到达最后一页")
                    break

            except Exception as e:
                print(f"  ✗ 翻页出错: {e}")
                break

        # 关闭文件和浏览器
        csv_file.close()
        browser.close()

        # 输出总结
        print(f"\n{'='*60}")
        print("✓ 抓取完成！")
        print(f"  总页数: {current_page} 页")
        print(f"  总记录: {total_records} 条")
        print(f"  保存位置: {SAVE_PATH}")
        print(f"{'='*60}\n")

def main():
    print("=" * 60)
    print("  浙江省行政处罚数据爬虫")
    print("=" * 60)
    print("\n请选择抓取模式:")
    print("  1. 测试模式 (3页)")
    print("  2. 小规模抓取 (10页)")
    print("  3. 中等规模抓取 (50页)")
    print("  4. 大规模抓取 (100页)")
    print("  5. 自定义页数")

    try:
        choice = input("\n请输入选择 (1-5): ").strip()

        page_config = {
            "1": 3,
            "2": 10,
            "3": 50,
            "4": 100
        }

        if choice in page_config:
            max_pages = page_config[choice]
            print(f"\n开始抓取 {max_pages} 页数据...\n")
            run_spider(max_pages=max_pages)

        elif choice == "5":
            max_pages = input("请输入要抓取的页数: ").strip()
            try:
                max_pages = int(max_pages)
                if max_pages > 0:
                    print(f"\n开始抓取 {max_pages} 页数据...\n")
                    run_spider(max_pages=max_pages)
                else:
                    print("✗ 页数必须大于0")
            except ValueError:
                print("✗ 无效的页数")
        else:
            print("✗ 无效的选择，使用默认设置 (10页)")
            run_spider(max_pages=10)

    except KeyboardInterrupt:
        print("\n\n✗ 用户中断，程序退出")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")

if __name__ == "__main__":
    main()
