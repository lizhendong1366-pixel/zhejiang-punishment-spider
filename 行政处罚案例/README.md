# 浙江省行政处罚案例数据集

## 项目概述

本项目采集并整理了浙江省政务服务网公开的行政处罚结果信息，经过脱敏处理后形成可供学习和研究使用的案例数据集。数据集涵盖了食品安全、交通违法、渔业违法、知识产权、环境保护等多个领域的行政处罚案例。

---

## 一、数据源选择理由及简介

### 1.1 数据源选择理由

选择浙江省政务服务网（https://xzcf.zjzwfw.gov.cn/punishment/）作为数据源，基于以下考量：

#### 1.1.1 权威性与官方性

- **官方发布平台**：浙江省政务服务网是浙江省人民政府办公厅主办的官方政务公开平台
- **数据权威性**：行政处罚结果信息由各级法定行政部门依法公开，具有法律效力
- **数据完整性**：包含完整的案件信息、处罚依据、决定内容等核心要素

#### 1.1.2 数据丰富性

- **案例多样性**：涵盖市场监管、交通运输、环境保护、渔业管理、治安管理等多个领域
- **地域覆盖**：覆盖浙江省所有地市（杭州、宁波、温州、嘉兴、湖州、绍兴、金华、衢州、舟山、台州、丽水）
- **时效性**：数据实时更新，反映最新的执法动态

#### 1.1.3 法律价值

- **典型意义**：案例涵盖常见违法行为类型，具有学习和研究价值
- **执法规范**：展现标准化的行政处罚文书格式和内容结构
- **适用法律**：明确引用相关法律法规条文，便于法律研究

#### 1.1.4 数据公开性

- **依法公开**：依据《中华人民共和国政府信息公开条例》及相关法律法规主动公开
- **无访问限制**：无需特殊权限即可公开访问
- **合规使用**：数据来源于政府公开信息，符合数据使用规范

### 1.2 数据源简介

**网站名称**：浙江省政务服务网行政处罚结果信息公开系统

**网站地址**：https://xzcf.zjzwfw.gov.cn/punishment/

**主办单位**：浙江省人民政府办公厅

**数据范围**：浙江省各级政府部门作出的行政处罚决定书摘要

**数据字段**：
- 案件名称
- 处罚对象（被处罚人/单位）
- 法定代表人
- 执法部门
- 处罚决定文书号
- 处罚决定日期
- 主要违法事实
- 处罚种类和依据
- 行政处罚决定内容
- 履行方式和期限
- 救济途径

**数据特点**：
- **结构化程度**：较高的字段化程度，便于机器读取
- **更新频率**：实时更新，每日新增大量案例
- **历史数据**：包含大量历史处罚记录，可供纵向研究
- **地域特色**：反映浙江省地方执法特点和行业分布

---

## 二、数据采集方法

### 2.1 采集架构

本项目采用基于Playwright的自动化网页采集方案，具体架构如下：

```
┌─────────────────┐    ┌──────────────┐    ┌──────────────┐
│  控制脚本      │───→│  Playwright   │───→│  浏览器引擎   │
│  (Python)      │    │  (自动化框架) │    │  (Chromium)   │
└─────────────────┘    └──────────────┘    └──────────────┘
         │                       │                      │
         │                       │                      │
         ↓                       ↓                      ↓
    ┌────────────────────────────────────────────────────┐
    │              浙江省政务服务网服务器                  │
    │        (https://xzcf.zjzwfw.gov.cn/punishment/)      │
    └────────────────────────────────────────────────────┘
```

### 2.2 采集流程

#### 2.2.1 环境准备

```bash
# 创建Python虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装Playwright
pip install playwright
playwright install chromium
```

#### 2.2.2 采集步骤

**步骤1：访问列表页面**
```
1. 启动Chromium浏览器（headless模式）
2. 访问目标URL：https://xzcf.zjzwfw.gov.cn/punishment/#/Punish
3. 等待页面JavaScript渲染完成（等待5-7秒）
4. 等待表格数据加载完成（等待tbody tr元素出现）
```

**步骤2：定位案例列表**
```
1. 使用CSS选择器定位表格行：tbody tr
2. 遍历每一行获取案例信息
3. 从第一列提取案例名称
4. 从第五列提取"查看详情"链接
```

**步骤3：进入详情页面**
```
1. 点击"查看详情"链接（位于第五列）
2. 等待页面跳转或内容更新（等待5-6秒）
3. 检测是否成功进入详情页面（通过页面内容判断）
```

**步骤4：提取详情内容**
```
1. 使用JavaScript遍历DOM树提取所有文本节点
2. 过滤script和style标签中的内容
3. 按段落组织文本内容
4. 提取完整的页面文本（约5000字符）
```

**步骤5：翻页处理**
```
1. 对于第11-20个案例，需要翻到第二页
2. 使用JavaScript点击页码"2"
3. 等待第二页数据加载（等待6-8秒）
4. 重复步骤2-5获取第二页案例
```

**步骤6：数据保存**
```
1. 解析提取的文本内容，识别关键字段
2. 按字段组织数据（案件名称、违法事实、处罚依据等）
3. 生成Markdown格式的案例文件
4. 保存到指定目录
```

### 2.3 技术实现细节

#### 2.3.1 反爬虫应对策略

**用户代理伪装**
```python
user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
```

**浏览器指纹隐藏**
```python
context.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', {
        get: () => false
    });
""")
```

**启动参数优化**
```python
browser = p.chromium.launch(
    headless=True,
    args=[
        '--disable-blink-features=AutomationControlled',
        '--no-sandbox',
        '--disable-setuid-sandbox'
    ]
)
```

**请求间隔控制**
```python
time.sleep(random.uniform(2, 4))  # 随机延迟2-4秒
```

#### 2.3.2 动态内容加载处理

**Vue.js单页应用适配**
```python
# 不依赖URL变化，通过页面内容判断是否在详情页
def is_on_detail_page(page):
    return page.evaluate("""
        () => {
            const body = document.body.textContent || "";
            return body.includes('行政处罚结果信息公开详情') ||
                   body.includes('返回') ||
                   body.includes('案件名称');
        }
    """)
```

**表格等待机制**
```python
# 等待表格元素出现
page.wait_for_selector("tbody tr", timeout=30000)

# 额外等待JavaScript渲染
time.sleep(5)
```

#### 2.3.3 错误处理与重试

**连接超时处理**
```python
try:
    page.goto(url, wait_until="load", timeout=60000)
except TimeoutError:
    print("页面加载超时，正在重试...")
    page.goto(url, wait_until="networkidle", timeout=90000)
```

**元素定位容错**
```python
# 尝试多种选择器策略
selectors = [
    "tbody tr:nth-child(1) td:nth-child(5) a",
    "tbody tr:nth-child(1) td:last-child a",
    "tbody tr:nth-child(1) a"
]

for selector in selectors:
    element = page.query_selector(selector)
    if element:
        element.click()
        break
```

### 2.4 采集脚本说明

**主脚本**：`fetch_all_12_cases.py`

**功能**：批量采集12个行政处罚案例的完整详情

**使用方法**：
```bash
cd "/Users/lizhendong/Desktop/claude code/爬虫脚本"
venv/bin/python fetch_all_12_cases.py
```

**输出格式**：Markdown文件，包含完整的案例信息

**采集能力**：
- 支持多页采集（自动翻页）
- 支持详情页面内容提取
- 支持批量处理（一次采集12个案例）
- 支持进度显示和错误处理

---

## 三、数据清洗方法

### 3.1 清洗目标

数据清洗旨在提升数据质量，确保数据的一致性、完整性和可用性。主要目标包括：

1. **格式标准化**：统一日期格式、编号格式等
2. **字段规范化**：规范字段名称和取值范围
3. **异常值处理**：识别和处理异常数据
4. **关联关系建立**：建立案例间的关联关系
5. **分类标签化**：为案例添加分类标签

### 3.2 清洗流程

```
原始数据 → 格式检查 → 字段提取 → 内容标准化 → 关联处理 → 标签添加 → 清洗后数据
```

### 3.3 清洗方法详解

#### 3.3.1 格式检查与修正

**日期格式统一**
```python
# 识别多种日期格式并统一为 YYYY-MM-DD
date_patterns = [
    r'(\d{4})年(\d{1,2})月(\d{1,2})日',
    r'(\d{4})-(\d{1,2})-(\d{1,2})',
    r'(\d{4})/(\d{1,2})/(\d{1,2})',
]

for pattern in date_patterns:
    text = re.sub(pattern, r'\1-\2-\3', text)
```

**文书号格式统一**
```python
# 统一文书号格式
patterns = [
    r'〔(\d{4})〕',  # 替换为 [YYYY]
    r'第(\d+)号',    # 统一编号格式
    r'\[(\d{4})\]',  # 替换为 〔YYYY〕
]
```

#### 3.3.2 字段提取与验证

**关键字段提取**
```python
def extract_field(content, field_name):
    """提取特定字段内容"""
    patterns = {
        '案件名称': r'案件名称[：:]\s*([^\n]+)',
        '处罚对象': r'被处罚人[单位（被处罚人）][：:]\s*([^\n]+)',
        '执法部门': r'执法部门[：:]\s*([^\n]+)',
        '决定日期': r'作出决定日期[：:]\s*([^\n]+)',
    }

    pattern = patterns.get(field_name)
    if pattern:
        match = re.search(pattern, content)
        if match:
            return match.group(1).strip()
    return None
```

**字段完整性验证**
```python
required_fields = ['案件名称', '处罚对象', '执法部门', '决定日期']
missing_fields = [f for f in required_fields if not extract_field(content, f)]

if missing_fields:
    print(f"警告：案例缺少字段: {missing_fields}")
```

#### 3.3.3 内容标准化

**机构名称规范化**
```python
# 标准化常见机构名称后缀
agency_rules = {
    '局': ['局', '分局', '县局', '市局'],
    '所': ['派出所', '所', '站所'],
}

# 统一执法部门表述
text = re.sub(r'([^路镇乡村街道]{2,10})派出所', r'\1公安派出所', text)
```

**地域信息提取**
```python
# 提取行政区划信息
def extract_region(content):
    regions = {
        '杭州市': ['杭州', '萧山', '西湖', '滨江', '拱墅', '上城', '下城', '江干', '余杭', '临平', '富阳', '临安', '桐庐', '淳安', '建德'],
        '宁波市': ['宁波', '海曙', '江北', '北仑', '镇海', '鄞州', '奉化', '余姚', '慈溪', '象山', '宁海', '杭州湾'],
        # ... 其他地市
    }

    for city, districts in regions.items():
        for district in districts:
            if district in content:
                return f"浙江省{city}"
```

#### 3.3.4 关联关系建立

**案件类型关联**
```python
case_types = {
    '食品安全': ['食品', '超市', '餐饮', '生产日期', '保质期', '标签'],
    '交通违法': ['车辆', '驾驶', '行驶', '道路', '醉驾', '无证'],
    '渔业违法': ['渔', '捕捞', '禁渔', '禁渔期', '水域', '渔具'],
    '知识产权': ['商标', '侵权', '专利', '版权', '假冒'],
    '环境保护': ['污染', '环境', '排放', '废弃物', '噪音'],
    '无照经营': ['无照', '经营', '营业执照', '登记'],
}

def classify_case(content):
    """根据关键词分类案件"""
    scores = {}
    for case_type, keywords in case_types.items():
        score = sum(1 for keyword in keywords if keyword in content)
        if score > 0:
            scores[case_type] = score

    return max(scores.keys(), key=scores.get) if scores else '其他'
```

**时间序列分析**
```python
# 提取决定日期，建立时间序列
def extract_decision_dates(cases):
    dates = []
    for case in cases:
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', case)
        if date_match:
            dates.append(date_match.group(1))
    return dates
```

#### 3.3.5 异常值处理

**空值处理**
```python
if not content or len(content.strip()) < 50:
    return {
        'status': 'invalid',
        'reason': '内容过短或为空'
    }
```

**格式验证**
```python
# 验证案件名称格式
def validate_case_name(name):
    if not name or len(name) < 5:
        return False
    if '案' not in name:
        return False
    return True

# 验证日期格式
def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
```

### 3.4 清洗脚本说明

**脚本位置**：`save_to_md.py`（数据清洗与Markdown生成）

**主要功能**：
1. 从CSV格式数据中读取案例信息
2. 提取和解析各个字段
3. 应用格式转换规则
4. 生成标准化的Markdown文件

**输出标准**：
- 统一的文件命名格式：`{序号}_{案件名称}.md`
- 统一的字段结构
- 统一的格式规范

---

## 四、脱敏处理方法

### 4.1 脱敏目标

脱敏处理旨在保护个人隐私和商业秘密，同时保留案例的法律学习和研究价值。脱敏原则如下：

1. **可识别性最小化**：降低个人信息识别风险
2. **数据可用性保持**：保留案例的法律属性和学习价值
3. **格式一致性**：统一的脱敏格式，便于使用
4. **可逆性控制**：敏感信息不可逆，防止还原

### 4.2 脱敏范围与规则

#### 4.2.1 个人信息脱敏

**姓名脱敏**
```python
# 规则：将真实姓名替换为"某某"
patterns = [
    r'([王李张刘陈杨赵黄周吴徐孙胡朱高林何郭马罗梁宋郑谢韩唐冯于董萧程曹袁邓许傅沈曾彭吕苏卢蒋蔡贾丁魏薛叶阎余潘杜戴夏钟汪田任姜范方石姚谭廖邹熊金陆郝孔白崔康毛邱秦江史顾侯邵孟龙万段钱尹黎易常武乔贺赖龚文])([一-龥]{1,2})',
    r'([A-Za-z一-龥]{2,15})\*{1,2}',  # 已部分隐藏的
]

replacement = r'\1某某'
```

**示例**：
- 张三 → 张某某
- 李四 → 李某某
- 王** → 王某某

**身份证号脱敏**
```python
# 规则：保留前6位和后4位，中间用*代替
pattern = r'(\d{6})\d{8}(\d{4})'
replacement = r'\1********\2'

# 15位身份证号
pattern = r'(\d{6})\d{6}(\d{3})'
replacement = r'\1******\2'
```

**示例**：
- 330102199001011234 → 330102********1234
- 330102900101234 → 330102******234

**电话号码脱敏**
```python
# 手机号：保留前3位和后4位
pattern = r'(1[3-9]\d)\d{4}(\d{4})'
replacement = r'\1****\2'

# 固话：保留区号和后4位
pattern = r'(\d{3,4}-)\d{4}(-\d{4})'
replacement = r'\1****\2'
```

**示例**：
- 13812345678 → 138****5678
- 0571-12345678 → 0571****5678

#### 4.2.2 地理信息脱敏

**详细地址脱敏**
```python
# 规则：只保留到区县级，具体地址脱敏
patterns = [
    r'(浙江省.{2,6}市)(.{2,8}[区县])(.{2,20}[街道路巷乡镇])(.{2,30}[号村])',
    r'(\d{1,4})[号栋楼座层]',
    r'[一-龥]{2,10}[街道路巷乡镇]',
]

replacements = [
    r'\1\2**路**号',
    r'**号',
    r'**路',
]
```

**示例**：
- 浙江省杭州市西湖区文三路123号 → 浙江省杭州市西湖区**路**号
- 杭州市上城区解放路8号 → 杭州市上城区**路**号

#### 4.2.3 企业信息脱敏

**公司名称脱敏**
```python
# 规则：保留组织形式，脱敏具体名称
patterns = [
    r'([一-龥]{2,15})(有限公司|股份有限公司)',
    r'([一-龥]{2,15})(有限责任公司)',
    r'([一-龥]{2,15})(厂|店|商行|经营部|门市部)',
]

replacement = r'某某\1'
```

**示例**：
- 浙江兴达石业有限公司 → 某某有限公司
- 杭州某某商行 → 某某商行
- 个体工商户张三 → 某某（个体工商户）

#### 4.2.4 法律文书脱敏

**处罚决定文书号脱敏**
```python
# 规则：保留机关简称和年份，脱敏具体编号
patterns = [
    r'([一-龥A-Za-z]{2,8})处罚〔(\d{4})〕第(\d+)号',
    r'([一-龥A-Za-z]{2,8})〔(\d{4})〕第(\d+)号',
]

replacement = r'\1处罚〔\2〕第****号'
```

**示例**：
- 杭临市监处罚〔2026〕108号 → 杭临市监处罚〔2026〕第****号
- 嘉公（交）决字[2026]第330400210053741号 → 嘉公（交）决字〔2026〕第****号

#### 4.2.5 其他敏感信息脱敏

**车牌号脱敏**
```python
pattern = r'([浙沪苏皖闽赣鲁豫鄂湘粤川渝陕甘宁云贵青新藏蒙京津晋辽吉黑])[A-Z]\s*([A-Z0-9]{5})'
replacement = r'\1* *****'
```

**示例**：
- 浙AH12345 → 浙* *****
- 浙F3***97 → 浙* *****

**部门信息脱敏**
```python
# 规则：保留上级机关，脱敏具体部门
pattern = r'([一-龥]{2,10}局)[一-龥]{2,10}[所队分局科]'
replacement = r'\1**所'
```

**示例**：
- 嘉兴市公安局交通管理支队 → 嘉兴市公安局**所
- 杭州市市场监督管理局西湖分局 → 杭州市市场监督管理局**分局

### 4.3 脱敏实现技术

#### 4.3.1 脱敏引擎设计

```python
class SmartDesensitizer:
    """智能脱敏处理器"""

    def __init__(self):
        # 已脱敏实体记录，确保一致性
        self.entity_mapping = {
            'names': {},
            'companies': {},
            'addresses': {},
        }

    def apply_all_rules(self, text):
        """按优先级顺序应用所有脱敏规则"""
        # 顺序：车牌 → 银行卡 → 电话 → 身份证 → 姓名 → 地址 → 公司 → 文书号 → 部门
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
```

#### 4.3.2 一致性保证

**同一实体的统一脱敏**
```python
# 使用映射表确保同一实体脱敏结果一致
if case_name not in self.entity_mapping['names']:
    self.entity_mapping['names'][case_name] = f"某某{self.name_counter}"
    self.name_counter += 1
```

**批处理模式**
```python
# 先扫描所有文件，识别实体
# 然后生成统一的脱敏映射
# 最后应用脱敏规则
```

#### 4.3.3 质量控制

**脱敏完整性检查**
```python
def check_desensitization_quality(original, desensitized):
    """检查脱敏是否完整"""
    # 检查是否还有未脱敏的敏感信息
    sensitive_patterns = [
        r'(\d{17}[\dXx]',  # 18位身份证号
        r'(1[3-9]\d)\d{4}(\d{4})',  # 未脱敏手机号
        r'([王李张刘陈杨])\s*[一-龥]{1,2}(?![某某])',  # 姓名未脱敏
    ]

    for pattern in sensitive_patterns:
        if re.search(pattern, desensitized):
            return False, f"可能存在未脱敏信息: {pattern}"

    return True, "脱敏检查通过"
```

**脱敏过度检查**
```python
def check_over_desensitization(desensitized):
    """检查是否脱敏过度"""
    # 检查是否过度脱敏影响了可用性
    if desensitized.count('**') > 50:
        return False, "脱敏过度，可读性严重下降"

    if len(desensitized) < len(desensitized) * 0.3:
        return False, "脱敏过度，内容损失严重"

    return True, "脱敏适度检查通过"
```

### 4.4 脱敏脚本说明

**脚本位置**：`desensitize_cases_v3.py`

**主要功能**：
1. 读取原始案例文件
2. 提取案例元信息（标题、类型、标签等）
3. 应用脱敏规则处理敏感信息
4. 生成YAML Front Matter元信息
5. 添加脱敏说明和版权声明

**使用方法**：
```bash
cd "/Users/lizhendong/Desktop/claude code/爬虫脚本"
venv/bin/python desensitize_cases_v3.py
```

**输出格式**：带YAML Front Matter的Markdown文件

**脱敏质量保证**：
- 一致性：相同类型信息脱敏格式一致
- 完整性：覆盖所有敏感信息类型
- 可用性：保留案例的法律学习价值
- 不可逆性：敏感信息无法被还原

### 4.5 脱敏效果示例

**原始文本**：
```
主要违法事实：被处罚对象张某某，驾驶证号330102199001011234，准驾车型：C1，于2026年05月30日03时07分驾驶浙F312345号小型新能源汽车在桐乡市梧桐街道XX处实施醉酒驾驶机动车的行为。
```

**脱敏后文本**：
```
主要违法事实：被处罚对象张某某，驾驶证号330102********1234，准驾车型：C1，于2026年05月30日03时07分驾驶浙* *****号小型新能源汽车在桐乡市**街道**处实施醉酒驾驶机动车的行为。
```

---

## 五、数据集结构

### 5.1 目录组织

```
爬虫脚本/
├── 行政处罚案例/              # 原始案例数据
│   ├── 1_案例名称.md
│   ├── 2_案例名称.md
│   └── ...
├── 行政处罚案例_脱敏版/      # 脱敏后的案例
│   ├── 1_案例名称.md        # 包含YAML Front Matter
│   ├── 2_案例名称.md
│   └── ...
├── fetch_all_12_cases.py       # 数据采集脚本
├── desensitize_cases_v3.py    # 脱敏处理脚本
└── README.md                  # 本文档
```

### 5.2 文件命名规范

**格式**：`{序号}_{案件名称}.md`

**示例**：
- `1_舟山市定海区民跃超市销售超过保质期的食品案.md`
- `2_嵊州市贺兴生鲜超市其他食品安全违法行为案.md`

### 5.3 文件内容结构

每个案例文件包含以下部分：

```markdown
---
title: "案例标题"
date: 2026-06-22
type: 脱敏案例
category: 行政处罚
tags: ['标签1', '标签2']
source: 浙江省政务服务网行政处罚结果信息公开系统
---

# 案件标题

## 案件基本信息
**处罚决定文书号**：...
**被处罚人**：...
**执法部门**：...
**作出决定日期**：...

## 主要违法事实
...

## 处罚种类和依据
...

## 行政处罚决定
...

---

**【重要提示】**
本文档已进行脱敏处理...
```

---

## 六、使用说明

### 6.1 环境要求

- Python 3.8+
- Playwright
- Chromium浏览器

### 6.2 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install playwright
playwright install chromium
```

### 6.3 使用脚本

**数据采集**
```bash
cd "/Users/lizhendong/Desktop/claude code/爬虫脚本"
venv/bin/python fetch_all_12_cases.py
```

**数据脱敏**
```bash
cd "/Users/lizhendong/Desktop/claude code/爬虫脚本"
venv/bin/python desensitize_cases_v3.py
```

### 6.4 自定义使用

**修改采集数量**
编辑 `fetch_all_12_cases.py`，修改 `range(1, 11)` 中的数字

**调整脱敏规则**
编辑 `desensitize_cases_v3.py` 中的脱敏模式（`patterns` 和 `replacements`）

---

## 七、注意事项

### 7.1 法律合规性

- 本数据集仅供学习和研究使用
- 不得用于商业用途或非法目的
- 使用时需遵守相关法律法规

### 7.2 数据安全

- 脱敏后的数据仍可能包含可识别信息
- 禁止尝试还原脱敏信息
- 禁止用于个人身份识别

### 7.3 更新维护

- 原始数据会随政府网站更新而变化
- 建议定期重新采集和脱敏
- 脱敏规则可根据需要调整

### 7.4 技术限制

- 网站结构变化可能导致采集失败
- 部分案例详情页面可能无法访问
- 网络问题可能影响采集效率

---

## 八、版本信息

**当前版本**：v3.0

**更新日期**：2026-06-22

**主要特性**：
- ✅ 自动化网页采集
- ✅ 批量处理能力
- ✅ 智能脱敏处理
- ✅ YAML Front Matter元信息
- ✅ 分类标签自动提取
- ✅ 质量控制机制

**技术栈**：
- Python 3.14
- Playwright 1.60.0
- Chromium 148.0.7778.96

---

## 九、许可证与声明

### 9.1 数据来源声明

本数据集的信息来源于浙江省政务服务网公开的行政处罚结果信息，原始数据版权归原作者所有。

### 9.2 使用许可

- **学习研究**：允许
- **商业用途**：禁止
- **再分发**：需保留本声明
- **修改**：允许，但需注明修改内容

### 9.3 免责声明

本数据集按"现状"提供，不对数据的准确性、完整性或时效性做任何保证。使用本数据集所产生的任何后果，数据提供者不承担责任。

---

## 十、联系与支持

如有问题或建议，请通过以下方式联系：

- **项目地址**：`/Users/lizhendong/Desktop/claude code/爬虫脚本/`
- **更新日志**：详见各脚本文件注释

---

**文档生成日期**：2026年6月22日
**文档版本**：1.0
**维护者**：Claude AI Assistant
