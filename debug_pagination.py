"""
分页调试脚本 - 详细分析网站翻页机制
"""
from playwright.sync_api import sync_playwright
import json

def debug_pagination():
    with sync_playwright() as p:
        print("启动浏览器进行分页调试...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        print("访问页面...")
        page.goto("https://xzcf.zjzwfw.gov.cn/punishment/#/Punish", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(5000)

        print("\n" + "="*60)
        print("分析分页结构")
        print("="*60)

        # 1. 查找分页容器
        print("\n1. 查找分页容器...")
        pagination = page.query_selector(".paging-module")
        if pagination:
            print("   ✓ 找到 .paging-module")
            html = pagination.inner_html()
            print(f"   HTML长度: {len(html)} 字符")
        else:
            print("   ✗ 未找到 .paging-module")

        # 2. 获取所有分页链接
        print("\n2. 获取所有分页元素...")
        all_items = page.query_selector_all(".paging-module li")
        print(f"   找到 {len(all_items)} 个 li 元素")

        for i, item in enumerate(all_items[:15]):  # 只显示前15个
            try:
                text = item.inner_text().strip()
                class_attr = item.get_attribute("class") or ""
                print(f"   [{i}] 文本: '{text}' | 类名: '{class_attr}'")
            except:
                pass

        # 3. 查找当前激活的页码
        print("\n3. 查找当前激活页码...")
        active = page.query_selector(".paging-module li.active")
        if active:
            active_text = active.inner_text().strip()
            print(f"   当前页码: {active_text}")
        else:
            print("   未找到激活页码")

        # 4. 尝试通过JavaScript获取更详细的信息
        print("\n4. JavaScript分析...")
        js_result = page.evaluate("""
            () => {
                const result = {
                    pagination_found: false,
                    current_page: null,
                    total_pages: null,
                    page_items: [],
                    next_button: null,
                    prev_button: null
                };

                const pagingModule = document.querySelector('.paging-module');
                if (!pagingModule) return result;

                result.pagination_found = true;

                // 获取所有li元素
                const lis = pagingModule.querySelectorAll('li');
                lis.forEach((li, index) => {
                    const text = li.textContent.trim();
                    const className = li.className;
                    const onclick = li.getAttribute('onclick');
                    const data = { index, text, className, onclick };

                    // 检查是否有onclick属性
                    if (onclick) {
                        result.page_items.push(data);
                    }
                });

                // 查找当前页
                const active = pagingModule.querySelector('li.active');
                if (active) {
                    result.current_page = parseInt(active.textContent.trim());
                }

                // 查找上一页/下一页按钮
                const prevBtn = pagingModule.querySelector('li:first-child');
                const nextBtn = pagingModule.querySelector('li:last-child');

                if (prevBtn) result.prev_button = prevBtn.textContent.trim();
                if (nextBtn) result.next_button = nextBtn.textContent.trim();

                // 尝试从页面文本中提取总页数
                const pageText = pagingModule.textContent;
                const match = pageText.match(/(\\d+)\\s*条/);
                if (match) {
                    result.total_records = match[1];
                }

                return result;
            }
        """)

        print("\nJavaScript分析结果:")
        print(json.dumps(js_result, indent=2, ensure_ascii=False))

        # 5. 获取第一页数据作为基准
        print("\n5. 获取第一页数据...")
        rows = page.query_selector_all("tbody tr")
        print(f"   第1页数据: {len(rows)} 条")
        if rows:
            first_row = rows[0]
            cols = first_row.query_selector_all("td")
            if len(cols) >= 5:
                first_data = [col.inner_text().strip() for col in cols[:5]]
                print(f"   第一条: {first_data[0][:40]}...")

        # 6. 尝试点击第2页
        print("\n6. 尝试点击第2页...")
        try:
            # 方法1: 直接点击页码"2"
            page2_clicked = page.evaluate("""
                () => {
                    const lis = document.querySelectorAll('.paging-module li');
                    for (let li of lis) {
                        if (li.textContent.trim() === '2') {
                            li.click();
                            return true;
                        }
                    }
                    return false;
                }
            """)

            if page2_clicked:
                print("   ✓ 成功点击第2页")
                page.wait_for_timeout(3000)

                # 验证是否真的翻页了
                new_rows = page.query_selector_all("tbody tr")
                print(f"   第2页数据: {len(new_rows)} 条")

                if new_rows:
                    new_first = new_rows[0]
                    new_cols = new_first.query_selector_all("td")
                    if len(new_cols) >= 5:
                        new_data = [col.inner_text().strip() for col in new_cols[:5]]
                        print(f"   第一条: {new_data[0][:40]}...")

                        # 比较是否不同
                        if first_data and new_data and new_data[0] != first_data[0]:
                            print("   ✓ 确认翻页成功！数据已更新")
                        else:
                            print("   ✗ 数据未更新，翻页可能失败")
            else:
                print("   ✗ 无法找到第2页按钮")

        except Exception as e:
            print(f"   ✗ 点击第2页出错: {e}")

        # 7. 查找可能的事件处理器
        print("\n7. 检查页面是否使用Vue/React...")
        framework_info = page.evaluate("""
            () => {
                return {
                    hasVue: !!window.Vue,
                    hasReact: !!window.React,
                    hasElementUI: !!window.ELEMENT,
                    document_ready: document.readyState
                };
            }
        """)
        print(f"   框架信息: {framework_info}")

        print("\n" + "="*60)
        print("调试完成，浏览器将保持打开30秒供查看...")
        print("="*60)
        page.wait_for_timeout(30000)

        browser.close()

if __name__ == "__main__":
    debug_pagination()
