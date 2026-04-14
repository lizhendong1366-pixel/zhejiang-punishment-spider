"""
交互式分页调试脚本
"""
from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        print("启动浏览器...")
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        print("访问页面...")
        page.goto("https://xzcf.zjzwfw.gov.cn/punishment/#/Punish")
        print("等待加载...")
        time.sleep(5)

        print("\n" + "="*60)
        print("观察浏览器窗口")
        print("="*60)

        # 获取分页HTML
        print("\n1. 分页区域HTML:")
        try:
            paging_html = page.evaluate("""
                () => {
                    const paging = document.querySelector('.paging-module');
                    if (paging) {
                        return paging.innerHTML;
                    }
                    return '未找到分页模块';
                }
            """)
            print(paging_html[:500])
        except:
            print("获取失败")

        # 获取分页文本
        print("\n2. 分页区域文本:")
        try:
            paging_text = page.evaluate("""
                () => {
                    const paging = document.querySelector('.paging-module');
                    if (paging) {
                        return paging.textContent;
                    }
                    return '';
                }
            """)
            print(paging_text)
        except:
            print("获取失败")

        # 获取所有li元素信息
        print("\n3. 所有分页li元素:")
        try:
            li_info = page.evaluate("""
                () => {
                    const lis = document.querySelectorAll('.paging-module li');
                    const info = [];
                    lis.forEach((li, i) => {
                        info.push({
                            index: i,
                            text: li.textContent.trim(),
                            className: li.className,
                            innerHTML: li.innerHTML
                        });
                    });
                    return info;
                }
            """)

            for info in li_info[:20]:
                print(f"  [{info['index']}] '{info['text']}' | class: {info['className']}")
        except:
            print("获取失败")

        # 等待用户观察
        print("\n" + "="*60)
        print("请在浏览器中观察页面")
        print("按回车键继续测试点击翻页...")
        print("="*60)

        input("按回车继续...")

        # 测试点击第2页
        print("\n尝试点击第2页...")
        try:
            result = page.evaluate("""
                () => {
                    const lis = document.querySelectorAll('.paging-module li');
                    for (let li of lis) {
                        if (li.textContent.trim() === '2') {
                            li.click();
                            return '已点击页码2';
                        }
                    }
                    return '未找到页码2';
                }
            """)
            print(f"  {result}")
            time.sleep(3)

            # 检查是否翻页成功
            print("\n检查翻页结果...")
            new_data = page.evaluate("""
                () => {
                    const rows = document.querySelectorAll('tbody tr');
                    if (rows.length > 0) {
                        const firstRow = rows[0];
                        const cols = firstRow.querySelectorAll('td');
                        if (cols.length >= 4) {
                            return cols[0].textContent.trim();
                        }
                    }
                    return '';
                }
            """)
            print(f"  新页第一条数据: {new_data[:50]}...")

        except Exception as e:
            print(f"  出错: {e}")

        print("\n" + "="*60)
        print("测试完成")
        print("浏览器将保持打开10秒供观察...")
        print("="*60)
        time.sleep(10)

        browser.close()

if __name__ == "__main__":
    main()
