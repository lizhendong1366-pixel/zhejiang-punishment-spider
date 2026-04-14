"""
行政处罚数据爬虫 - 稳定版本
处理反爬机制和动态加载
"""
import os
import csv
import time
import random
from playwright.sync_api import sync_playwright

# 配置项
TARGET_URL = "https://xzcf.zjzwfw.gov.cn/punishment/#/Punish"
SAVE_DIR = "/Users/lizhendong/Documents/claude code"
SAVE_PATH = os.path.join(SAVE_DIR, "zhejiang_punishment_data.csv")

def random_delay(min_sec=1, max_sec=3):
    """随机延迟，模拟人工操作"""
    delay = random.uniform(min_sec, max_sec)
    time.sleep(delay)

def run_spider(max_pages=10):
    """运行爬虫"""

    # 确保目录存在
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    with sync_playwright() as p:
        print("="*70)
        print("浙江省行政处罚数据爬虫 v2.0")
        print("="*70)
        print(f"目标网站: {TARGET_URL}")
        print(f"保存位置: {SAVE_PATH}")
        print(f"抓取页数: {max_pages} 页\n")

        # 启动浏览器，使用更真实的配置
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox'
            ]
        )

        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-CN'
        )

        # 添加初始化脚本，隐藏自动化特征
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false
            });
        """)

        page = context.new_page()

        try:
            # 访问页面
            print("正在访问页面...")
            page.goto(TARGET_URL, wait_until="load", timeout=60000)
            print("✓ 页面加载成功")

            # 等待JavaScript渲染
            print("等待数据渲染...")
            random_delay(3, 5)

            # 验证页面
            title = page.title()
            print(f"页面标题: {title}")

            # 准备CSV文件
            csv_file = open(SAVE_PATH, 'w', newline='', encoding='utf-8-sig')
            writer = csv.writer(csv_file)
            writer.writerow(["序号", "案件名称", "处罚对象", "决定书文号", "处罚决定日期", "详情"])

            # 抓取状态
            current_page = 1
            total_records = 0
            last_first_record = None
            same_page_count = 0

            print(f"\n{'='*70}")
            print("开始抓取数据")
            print(f"{'='*70}\n")

            while current_page <= max_pages:
                print(f"[第 {current_page}/{max_pages} 页] ", end="", flush=True)

                # 等待表格加载
                try:
                    page.wait_for_selector("tbody tr", timeout=15000)
                except:
                    print("✗ 表格加载超时")
                    break

                random_delay(1, 2)

                # 获取当前页数据
                rows = page.query_selector_all("tbody tr")

                if not rows:
                    print("✗ 未找到数据行")
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

                if not page_records:
                    print("✗ 本页无有效数据")
                    break

                # 检查是否重复（防止无限循环）
                if last_first_record and page_records[0] == last_first_record:
                    same_page_count += 1
                    print(f"✗ 检测到重复页 (第{same_page_count}次)")
                    if same_page_count >= 2:
                        print("✗ 连续重复，已到达最后一页")
                        break
                else:
                    same_page_count = 0

                # 写入数据
                page_start = total_records + 1
                for i, record in enumerate(page_records):
                    row_data = [page_start + i] + record
                    writer.writerow(row_data)
                    total_records += 1

                print(f"✓ {len(page_records)} 条 | 总计: {total_records} 条")

                # 显示最新一条
                if page_records:
                    latest = page_records[0][0][:50]
                    print(f"  最新: {latest}...")

                # 记录第一条用于检测重复
                last_first_record = page_records[0]

                # 如果是最后一页，退出
                if current_page >= max_pages:
                    print("\n✓ 已达到设定页数")
                    break

                # 尝试翻页
                print(f"  → 翻页中...", end="", flush=True)
                random_delay(1, 2)

                try:
                    # 使用JavaScript翻页，更稳定
                    page_number = current_page + 1
                    success = page.evaluate(f"""
                        (pageNum) => {{
                            // 查找分页模块中的所有数字链接
                            const pagingModule = document.querySelector('.paging-module');
                            if (!pagingModule) return false;

                            // 查找包含指定页码的li元素
                            const allLis = pagingModule.querySelectorAll('li');
                            for (let li of allLis) {{
                                const text = li.textContent.trim();
                                // 检查是否是数字且匹配目标页码
                                if (/^\\d+$/.test(text) && parseInt(text) === pageNum) {{
                                    // 滚动到元素可见
                                    li.scrollIntoView({{behavior: 'smooth', block: 'center'}});
                                    // 延迟后点击
                                    setTimeout(() => {{
                                        li.click();
                                    }}, 200);
                                    return true;
                                }}
                            }}

                            return false;
                        }}
                    """, page_number)

                    if success:
                        current_page += 1
                        print(" ✓")
                        random_delay(2, 4)  # 等待新页面加载
                    else:
                        print(" ✗")
                        print("\n✗ 无法翻到下一页，可能已到达最后一页")
                        break

                except Exception as e:
                    print(f" ✗")
                    print(f"\n✗ 翻页错误: {e}")
                    break

            # 完成
            csv_file.close()
            browser.close()

            print(f"\n{'='*70}")
            print("抓取完成！")
            print(f"  成功抓取: {current_page} 页")
            print(f"  总记录数: {total_records} 条")
            print(f"  保存位置: {SAVE_PATH}")
            print(f"{'='*70}\n")

        except KeyboardInterrupt:
            print("\n\n用户中断，正在清理...")
            csv_file.close()
            browser.close()
            print("✓ 已清理并退出")

        except Exception as e:
            print(f"\n✗ 发生错误: {e}")
            try:
                csv_file.close()
                browser.close()
            except:
                pass

if __name__ == "__main__":
    print("\n请选择抓取页数:")
    print("  [1] 3页 (测试)")
    print("  [2] 10页 (小规模)")
    print("  [3] 50页 (中等规模)")
    print("  [4] 100页 (大规模)")

    # 直接运行10页，不需要交互
    print("\n默认抓取 10 页...\n")
    run_spider(max_pages=10)
