"""
测试翻页机制的脚本
"""
from playwright.sync_api import sync_playwright
import time

def test_pagination():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        print("正在访问页面...")
        page.goto("https://xzcf.zjzwfw.gov.cn/punishment/#/Punish", wait_until="networkidle", timeout=60000)

        print("等待页面渲染...")
        page.wait_for_timeout(5000)

        print("\n=== 第一页数据 ===")
        rows = page.query_selector_all("tbody tr")
        print(f"找到 {len(rows)} 行数据")

        for i, row in enumerate(rows[:3]):
            cols = row.query_selector_all("td")
            if len(cols) >= 5:
                print(f"第{i+1}行: {[col.inner_text().strip() for col in cols[:5]]}")

        print("\n=== 检查翻页元素 ===")

        # 检查各种可能的翻页选择器
        pagination_selectors = [
            ".el-pagination",
            ".pagination",
            ".pager",
            "[class*='pagination']",
            "[class*='pager']",
            "li.el-pager",
            "button.el-pagination__next",
            ".btn-next",
            "li.next",
            "a.next"
        ]

        for selector in pagination_selectors:
            try:
                elements = page.query_selector_all(selector)
                if elements:
                    print(f"找到元素: {selector} - 共 {len(elements)} 个")
                    # 打印第一个元素的文本和类名
                    first = elements[0]
                    print(f"  第一个元素: {first.inner_text()[:50]}")
                    print(f"  类名: {first.get_attribute('class')}")
            except Exception as e:
                print(f"选择器 {selector} 失败: {e}")

        print("\n=== 尝试查找下一页按钮 ===")

        # 尝试多种方式点击下一页
        next_attempts = [
            "li.el-pagination__next",
            "button.el-icon.el-pagination__next",
            "li.el-pager li.active + li",
            "button[aria-label='下一页']",
            ".el-pagination .btn-next",
            "li:last-child"
        ]

        for selector in next_attempts:
            try:
                next_btn = page.query_selector(selector)
                if next_btn:
                    print(f"找到下一页按钮: {selector}")
                    print(f"  文本: {next_btn.inner_text()}")
                    print(f"  可见: {next_btn.is_visible()}")
                    print(f"  启用: {next_btn.is_enabled()}")
            except:
                pass

        print("\n=== 打印页面上的所有分页相关文本 ===")
        try:
            pagination = page.query_selector(".el-pagination")
            if pagination:
                print("分页区域内容:")
                print(pagination.inner_text())
        except:
            pass

        print("\n=== 检查总页数 ===")
        # 查找页码信息
        page_info_selectors = [
            ".el-pagination__total",
            ".total",
            "[class*='total']",
            "span:has-text('条')",
            "span:has-text('共')"
        ]

        for selector in page_info_selectors:
            try:
                elements = page.query_selector_all(selector)
                for elem in elements:
                    text = elem.inner_text().strip()
                    if text and ('条' in text or '共' in text or 'total' in text.lower()):
                        print(f"找到分页信息: {text}")
            except:
                pass

        print("\n请查看浏览器页面，按回车键继续尝试点击下一页...")
        input()

        print("\n=== 尝试点击下一页 ===")
        try:
            # 尝试通过JavaScript点击
            page.evaluate("""
                // 查找并点击下一页按钮
                const nextBtn = document.querySelector('li.el-pagination__next');
                if (nextBtn && !nextBtn.classList.contains('disabled')) {
                    nextBtn.click();
                    return '点击成功';
                }
                return '未找到可点击的下一页按钮';
            """)
            print("已尝试通过JavaScript点击下一页")
            time.sleep(3)
        except Exception as e:
            print(f"点击失败: {e}")

        print("\n=== 检查是否翻页成功 ===")
        time.sleep(3)
        new_rows = page.query_selector_all("tbody tr")
        print(f"翻页后找到 {len(new_rows)} 行数据")

        if new_rows:
            for i, row in enumerate(new_rows[:3]):
                cols = row.query_selector_all("td")
                if len(cols) >= 5:
                    print(f"第{i+1}行: {[col.inner_text().strip() for col in cols[:5]]}")

        print("\n测试完成，浏览器将保持打开状态...")
        input("按回车键关闭浏览器...")
        browser.close()

if __name__ == "__main__":
    test_pagination()
