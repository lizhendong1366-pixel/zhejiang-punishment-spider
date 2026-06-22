"""
行政处罚案例脱敏处理脚本 v3.0
添加YAML Front Matter元信息
"""
import os
import re
import glob
from datetime import datetime

# 配置
INPUT_DIR = "/Users/lizhendong/Desktop/claude code/爬虫脚本/行政处罚案例"
OUTPUT_DIR = "/Users/lizhendong/Desktop/claude code/爬虫脚本/行政处罚案例_脱敏版"


class SmartDesensitizer:
    """智能脱敏处理器"""

    def __init__(self):
        pass

    def desensitize_name(self, text):
        """脱敏姓名"""
        common_surnames = '王李张刘陈杨赵黄周吴徐孙胡朱高林何郭马罗梁宋郑谢韩唐冯于董萧程曹袁邓许傅沈曾彭吕苏卢蒋蔡贾丁魏薛叶阎余潘杜戴夏钟汪田任姜范方石姚谭廖邹熊金陆郝孔白崔康毛邱秦江史顾侯邵孟龙万段钱尹黎易常武乔贺赖龚文'

        text = re.sub(rf'([{common_surnames}])\*{{1,2}}', r'\1某某', text)
        text = re.sub(rf'([{common_surnames}])(某某)', r'\1某某', text)
        text = re.sub(rf'([{common_surnames}])([一-龥])', r'\1某某', text)
        text = re.sub(rf'([{common_surnames}])([一-龥]{{2}})', r'\1某某', text)

        return text

    def desensitize_id_card(self, text):
        """脱敏身份证号"""
        text = re.sub(r'(\d{6})\d{8}(\d{4})', r'\1********\2', text)
        text = re.sub(r'(\d{6})\d{6}(\d{3})', r'\1******\2', text)
        text = re.sub(r'(\d{6})\*{8,12}(\d{4})', r'\1********\2', text)

        return text

    def desensitize_phone(self, text):
        """脱敏电话号码"""
        text = re.sub(r'(1[3-9]\d)\d{4}(\d{4})', r'\1****\2', text)
        text = re.sub(r'(1[3-9]\d)\*{3,5}(\d{4})', r'\1****\2', text)
        text = re.sub(r'(\d{3,4}-)\d{4}(-\d{4})', r'\1****\2', text)

        return text

    def desensitize_address(self, text):
        """脱敏地址信息"""
        text = re.sub(r'(\d{1,4})[号栋楼座层]', r'**号', text)
        text = re.sub(r'[一二三四五六七八九十百千万]+[号栋楼座层]', r'**号', text)
        text = re.sub(r'[一-龥]{2,6}[村社区][号]{0,1}', r'**村', text)
        text = re.sub(r'[一-龥]{2,10}[街道路巷乡镇]', r'**路', text)

        return text

    def desensitize_doc_number(self, text):
        """脱敏处罚决定文书号"""
        text = re.sub(r'([一-龥A-Za-z]{2,8})处罚〔(\d{4})〕第(\d+)号', r'\1处罚〔\2〕第****号', text)
        text = re.sub(r'([一-龥A-Za-z]{2,8})〔(\d{4})〕第(\d+)号', r'\1〔\2〕第****号', text)
        text = re.sub(r'([一-龥A-Za-z]{2,8})\[(\d{4})\]第(\d+)号', r'\1〔\2〕第****号', text)
        text = re.sub(r'([一-龥A-Za-z]{2,8})【(\d{4})】第(\d+)号', r'\1〔\2〕第****号', text)
        text = re.sub(r'([一-龥A-Za-z]{2,8})〔(\d{4})〕(\d+)号', r'\1〔\2〕第****号', text)
        text = re.sub(r'([一-龥A-Za-z]{2,8})第(\d{4,8})号', r'\1第****号', text)

        return text

    def desensitize_company(self, text):
        """脱敏公司/商户名称"""
        text = re.sub(r'([一-龥]{2,10})（个体工商户）', r'某某（个体工商户）', text)
        text = re.sub(r'([一-龥]{2,10})个体工商户', r'某某个体工商户', text)
        text = re.sub(r'([一-龥]{2,15})(有限公司|股份有限公司)', r'某某\1', text)
        text = re.sub(r'([一-龥]{2,15})(有限责任公司|股份合作公司)', r'某某有限责任公司', text)
        text = re.sub(r'([一-龥]{2,15})(厂|店|商行|经营部|门市部|工作室|事务所|中心|服务部|超市|批发部)', r'某某\1', text)

        return text

    def desensitize_car_plate(self, text):
        """脱敏车牌号"""
        text = re.sub(r'([浙沪苏皖闽赣鲁豫鄂湘粤川渝陕甘宁云贵青新藏蒙京津晋辽吉黑])[A-Z]\s*([A-Z0-9]{5})', r'\1* *****', text)
        text = re.sub(r'([浙沪苏皖闽赣鲁豫鄂湘粤川渝陕甘宁云贵青新藏蒙京津晋辽吉黑])\*{2,5}[A-Z0-9]{2,5}', r'\1* *****', text)
        text = re.sub(r'([浙沪苏皖闽赣鲁豫鄂湘粤川渝陕甘宁云贵青新藏蒙京津晋辽吉黑])[A-Z]\*{3}([A-Z0-9]{2})', r'\1* **\2', text)

        return text

    def desensitize_bank_card(self, text):
        """脱敏银行卡号"""
        text = re.sub(r'(\d{4})\d{8,12}(\d{4})', r'\1********\2', text)
        text = re.sub(r'(\d{4})\*{8,12}(\d{4})', r'\1********\2', text)

        return text

    def desensitize_department(self, text):
        """脱敏具体部门/科室"""
        text = re.sub(r'([一-龥]{2,10}局)[一二三四五六七八九十]{2,10}[科处部队组所]', r'\1**科', text)
        text = re.sub(r'([一-龥]{2,10}局)[一-龥]{2,10}[所队]', r'\1**所', text)

        return text

    def apply_all_rules(self, text):
        """应用所有脱敏规则"""
        text = self.desensitize_car_plate(text)
        text = self.desensitize_bank_card(text)
        text = self.desensitize_phone(text)
        text = self.desensitize_id_card(text)
        text = self.desensitize_name(text)
        text = self.desensitize_address(text)
        text = self.desensitize_company(text)
        text = self.desensitize_doc_number(text)
        text = self.desensitize_department(text)

        return text

    def extract_case_info(self, content, filename):
        """从文件内容中提取案例信息"""
        info = {
            'title': '',
            'case_type': '',
            'department': '',
            'decision_date': '',
            'region': '',
            'tags': []
        }

        lines = content.split('\n')

        # 提取标题（第一行的#之后的内容）
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                info['title'] = line.replace('#', '').strip()
                break

        # 提取执法部门
        dept_match = re.search(r'执法部门[：:]\s*([^\n]+)', content)
        if dept_match:
            dept = dept_match.group(1).strip()
            info['department'] = dept
            # 提取地区
            if '浙江' in dept:
                info['region'] = '浙江省'
            elif dept.startswith(('杭州', '宁波', '温州', '嘉兴', '湖州', '绍兴', '金华', '衢州', '舟山', '台州', '丽水')):
                info['region'] = f'浙江省{dept[:2]}市'

        # 提取决定日期
        date_match = re.search(r'作出决定日期[：:]\s*(\d{4}-\d{2}-\d{2})', content)
        if date_match:
            info['decision_date'] = date_match.group(1)

        # 提取处罚日期
        if not info['decision_date']:
            date_match = re.search(r'作出行政处罚的日期[：:]\s*(\d{4}-\d{2}-\d{2})', content)
            if date_match:
                info['decision_date'] = date_match.group(1)

        # 确定案件类型和标签
        title_lower = info['title'].lower()
        if '食品' in title_lower or '食品安全' in title_lower:
            info['case_type'] = '食品安全'
            info['tags'].extend(['食品安全', '市场监管'])
        elif '醉驾' in title_lower or '醉酒驾驶' in title_lower:
            info['case_type'] = '交通违法'
            info['tags'].extend(['交通违法', '醉酒驾驶'])
        elif '禁渔' in title_lower or '捕捞' in title_lower:
            info['case_type'] = '渔业违法'
            info['tags'].extend(['渔业违法', '禁渔期'])
        elif '无照经营' in title_lower:
            info['case_type'] = '无照经营'
            info['tags'].extend(['无照经营', '市场监管'])
        elif '商标' in title_lower or '侵权' in title_lower:
            info['case_type'] = '知识产权'
            info['tags'].extend(['知识产权', '商标侵权'])
        elif '燃放' in title_lower or '烟花爆竹' in title_lower:
            info['case_type'] = '治安管理'
            info['tags'].extend(['治安管理', '烟花爆竹'])
        elif '身份证' in title_lower or '冒用' in title_lower:
            info['case_type'] = '身份证违法'
            info['tags'].extend(['身份证违法', '治安管理'])
        elif '公路' in title_lower or '污染' in title_lower:
            info['case_type'] = '交通运输'
            info['tags'].extend(['交通运输', '公路管理'])
        elif '垃圾分类' in title_lower or '生活垃圾' in title_lower:
            info['case_type'] = '环境保护'
            info['tags'].extend(['环境保护', '垃圾分类'])
        else:
            info['case_type'] = '其他'
            info['tags'].append('行政处罚')

        # 提取序号
        number_match = re.match(r'(\d+)', filename)
        if number_match:
            info['case_number'] = number_match.group(1)

        return info


def generate_yaml_frontmatter(case_info):
    """生成YAML Front Matter"""
    current_date = datetime.now().strftime('%Y-%m-%d')

    yaml_content = f"""---
title: "{case_info['title']}"
date: {current_date}
type: 脱敏案例
category: 行政处罚
tags: {case_info['tags']}
source: 浙江省政务服务网行政处罚结果信息公开系统
department: {case_info.get('department', '未知')}
decision_date: {case_info.get('decision_date', '未知')}
region: {case_info.get('region', '浙江省')}
case_type: {case_info['case_type']}
case_number: {case_info.get('case_number', 'N/A')}
description: 来源于浙江省政务服务网的{case_info['case_type']}案例，经脱敏处理后用于学习和研究。
slug: "{case_info['title'].replace('/', '-')}"

---

"""
    return yaml_content


def process_markdown_file(input_file, output_file, desensitizer):
    """处理单个Markdown文件"""

    try:
        # 读取文件
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 提取案例信息
        filename = os.path.basename(input_file)
        case_info = desensitizer.extract_case_info(content, filename)

        # 应用脱敏规则
        content = desensitizer.apply_all_rules(content)

        # 生成YAML Front Matter
        yaml_frontmatter = generate_yaml_frontmatter(case_info)

        # 添加脱敏说明
        desensitization_notice = f"""

---

**【重要提示】**
本文档已进行脱敏处理，仅用于学习和研究目的。

**脱敏范围**：
- 个人姓名（替换为"某某"）
- 身份证号（保留前后几位，中间隐藏）
- 电话号码（保留前后几位，中间隐藏）
- 详细地址（具体门牌号、街道名称隐藏）
- 公司名称（保留组织形式，具体名称隐藏）
- 车牌号（部分隐藏）
- 处罚决定文书号（保留年份和机关，编号隐藏）
- 具体部门科室信息

**处理时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**版权声明**：本文内容来源于政府公开信息，仅供学习研究使用，不得用于商业用途或非法目的。
"""

        # 组合最终内容
        final_content = yaml_frontmatter + content + desensitization_notice

        # 保存文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)

        return True, None

    except Exception as e:
        return False, str(e)


def main():
    """主函数"""
    print("="*70)
    print("行政处罚案例脱敏处理脚本 v3.0")
    print("添加YAML Front Matter元信息")
    print("="*70)

    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"\n输入目录: {INPUT_DIR}")
    print(f"输出目录: {OUTPUT_DIR}")
    print("\n功能：脱敏处理 + YAML Front Matter\n")
    print("开始处理...\n")

    # 创建脱敏处理器
    desensitizer = SmartDesensitizer()

    # 获取所有Markdown文件
    pattern = os.path.join(INPUT_DIR, "*.md")
    md_files = glob.glob(pattern)

    # 排除临时文件
    md_files = [f for f in md_files if "临时" not in os.path.basename(f)]

    # 按文件名排序
    md_files.sort()

    success_count = 0
    fail_count = 0

    for input_file in md_files:
        filename = os.path.basename(input_file)
        output_file = os.path.join(OUTPUT_DIR, filename)

        print(f"处理: {filename}...", end=" ")

        success, error = process_markdown_file(input_file, output_file, desensitizer)

        if success:
            print("✓")
            success_count += 1
        else:
            print(f"✗ ({error})")
            fail_count += 1

    print(f"\n{'='*70}")
    print(f"处理完成！")
    print(f"  成功: {success_count} 个")
    print(f"  失败: {fail_count} 个")
    print(f"  保存位置: {OUTPUT_DIR}")
    print(f"{'='*70}\n")

    # 显示YAML Front Matter示例
    if success_count > 0:
        print("YAML Front Matter示例（已添加到每个文件开头）:")
        print("---")
        print("title: \"案例标题\"")
        print("date: 2026-06-22")
        print("type: 脱敏案例")
        print("category: 行政处罚")
        print("tags: ['食品安全', '市场监管']")
        print("source: 浙江省政务服务网行政处罚结果信息公开系统")
        print("department: 执法部门名称")
        print("decision_date: 2026-06-20")
        print("region: 浙江省")
        print("case_type: 食品安全")
        print("---")
        print()

        # 显示脱敏后的文件列表
        print("脱敏后的文件:")
        output_files = glob.glob(os.path.join(OUTPUT_DIR, "*.md"))
        output_files.sort()

        for i, file in enumerate(output_files[:12], 1):
            filename = os.path.basename(file)
            print(f"  {i:2d}. {filename}")


if __name__ == "__main__":
    main()
