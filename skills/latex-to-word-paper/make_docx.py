# -*- coding: utf-8 -*-
'''
将论文 LaTeX 转换为 Word (.docx)，保持格式与 PDF 一致
'''

import os, sys
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUTPUT = r'c:\Users\liuwang\Desktop\新建文件夹 (2)\从AM广播看电子信息工程的传承与创新.docx'
IMG_DIR = r'c:\Users\liuwang\Desktop\新建文件夹 (2)\figures'
FIG1 = os.path.join(IMG_DIR, 'fig1_propagation.png')
FIG2 = os.path.join(IMG_DIR, 'fig2_architecture.png')


# ── 工具函数 ──

def set_run_font(run, cn_font='宋体', en_font='Times New Roman', size=Pt(12), bold=False):
    run.font.size = size
    run.font.bold = bold
    run.font.name = en_font
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), cn_font)
    rFonts.set(qn('w:ascii'), en_font)
    rFonts.set(qn('w:hAnsi'), en_font)


def add_cn_paragraph(doc, text, cn_font='宋体', en_font='Times New Roman',
                     size=Pt(12), bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                     first_line_indent=True, spacing=1.5, space_after=Pt(0)):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = spacing
    pf.space_after = space_after
    pf.space_before = Pt(0)
    pf.alignment = align
    if first_line_indent:
        pf.first_line_indent = Pt(24)
    run = p.add_run(text)
    set_run_font(run, cn_font, en_font, size, bold)
    return p


def add_heading_cn(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        set_run_font(run, cn_font='黑体', en_font='Arial',
                     size=Pt(16 if level == 1 else 14), bold=True)
    pf = h.paragraph_format
    pf.space_before = Pt(12)
    pf.space_after = Pt(6)
    return h


def add_figure(doc, img_path, caption_text=None):
    if not os.path.exists(img_path):
        doc.add_paragraph('[图片未找到: ' + img_path + ']')
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(img_path, width=Cm(14))
    if caption_text:
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cap.add_run(caption_text)
        set_run_font(r, cn_font='宋体', size=Pt(10.5), bold=False)
    doc.add_paragraph()


def add_table_comparison(doc):
    headers = ['特性', 'AM广播', 'FM广播', '移动通信(4G/5G)', '互联网流媒体']
    rows = [
        ['工作频段', '530—1700 kHz', '88—108 MHz', '700 MHz—毫米波', '全IP网络'],
        ['典型覆盖半径', '100—-1000+ km', '30—50 km', '0.3—5 km（单站）', '取决于网络连通性'],
        ['系统复杂度', '低', '中', '高', '极高'],
        ['抗毁性', '高', '中', '低', '极低'],
        ['供电依赖性', '发电机即可', '需电网供电', '需电网+备份电源', '全链路不间断供电'],
        ['中间节点', '0（直发直收）', '0（直发直收）', '3+层', '5+层'],
        ['接收终端', '简易收音机', '专用收音机', '智能手机', '智能终端+网络接入'],
    ]
    table = doc.add_table(rows=1 + len(rows), cols=5)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        set_run_font(run, cn_font='黑体', size=Pt(9), bold=True)
    for r_idx, row_data in enumerate(rows):
        for c_idx, val in enumerate(row_data):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ''
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(val)
            set_run_font(run, cn_font='宋体', size=Pt(8.5))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap.add_run('表1  各通信方式技术特性对比')
    set_run_font(r, cn_font='宋体', size=Pt(10.5), bold=False)
    doc.add_paragraph()


# ── 正文内容 ──

doc = Document()

# 页面设置
section = doc.sections[0]
section.top_margin = Cm(2.5)
section.bottom_margin = Cm(2.5)
section.left_margin = Cm(3)
section.right_margin = Cm(3)

style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
style.paragraph_format.line_spacing = 1.5

# ── 标题 ──
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_p.paragraph_format.space_after = Pt(6)
TITLE = ('从“强制保留AM广播”看\n'
         '电子信息工程的传承与创新')
run = title_p.add_run(TITLE)
set_run_font(run, cn_font='黑体', en_font='Arial', size=Pt(22), bold=True)
doc.add_paragraph()

# ── 摘要 ──
abs_title = doc.add_paragraph()
abs_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = abs_title.add_run('摘　要')
set_run_font(r, cn_font='黑体', size=Pt(14), bold=True)

ABSTRACT = (
    '2024年，美国众议院通过《AM Radio for Every Vehicle Act of 2024》，'
    '中国工业和信息化部同步启动《车载无线广播接收系统》强制性国家标准制修订。'
    '两大汽车市场以立法与标准的形式，要求新车强制保留AM广播接收功能。'
    '在6G、低轨卫星互联网等前沿技术快速迭代的时代，这一政策选择看似违背技术演进'
    '“新替旧”的线性逻辑。本文从技术韧性、公共安全与产业标准三个维度，'
    '分析AM广播在现代通信体系中不可替代的备份价值。通过对比AM广播与FM广播、'
    '移动通信网络及互联网流媒体在传播特性、系统复杂度与抗毁性上的差异，论证在'
    '极端灾害与紧急状态下，低技术门槛、高物理鲁棒性的AM广播仍是最可靠的公共信息'
    '通道。进一步，本文探讨这一现象对电子信息工程学科的意义——传统技术'
    '与前沿创新并非简单的替代关系，而是互补共生。《高频电子线路》与《通信原理》'
    '所奠定的底层理论，恰恰是理解并应对这类复杂工程与社会问题的不可替代的知识根基。'
)
add_cn_paragraph(doc, ABSTRACT, size=Pt(12))

kw_p = doc.add_paragraph()
kw_p.paragraph_format.first_line_indent = Pt(24)
r1 = kw_p.add_run('关键词：')
set_run_font(r1, cn_font='黑体', size=Pt(12), bold=True)
r2 = kw_p.add_run('AM广播；技术韧性；公共安全；强制性标准；传承与创新')
set_run_font(r2, cn_font='宋体', size=Pt(12))
doc.add_page_break()

# ── 1 引言 ──
add_heading_cn(doc, '一、引言', level=1)

add_cn_paragraph(doc,
    '2024年9月18日，美国众议院通过《AM Radio for Every Vehicle Act of 2024》，'
    '要求所有在美国市场销售的新车必须保留AM广播接收功能。同一天，中国工业和信息化部'
    '科技司对《车载无线广播接收系统》强制性国家标准制修订计划予以公示，该标准于'
    '2025年4月正式下达立项。全球最大的两个汽车市场在同一个问题上做出了近乎同步的'
    '政策响应。')

add_cn_paragraph(doc,
    '这一现象与公众对技术演进的线性想象形成了张力。移动通信正从5G迈向6G，低轨卫星'
    '星座加速全球组网，中国载人登月计划稳步推进——在“未来已来”'
    '的叙事中，为何各国政府要回过头来，以法律和标准的形式，保障一项诞生于上世纪初期、'
    '已被许多家庭淘汰的无线电技术？')

add_cn_paragraph(doc,
    'AM广播的“强制保留”并非简单的怀旧或保守，而是一个关于技术备份、'
    '公共安全与工程理性的深层议题。本文将从技术韧性、公共安全、产业与标准三个维度'
    '展开分析，并在此基础上讨论这一事件对电子信息工程专业学习的启示——'
    '传统技术与前沿创新的关系，以及《高频电子线路》《通信原理》等基础课程的不可替代价值。')

# ── 2 政策背景 ──
add_heading_cn(doc, '二、政策背景：中美两国的共同选择', level=1)

add_cn_paragraph(doc,
    '2024年9月18日，美国众议院通过《AM Radio for Every Vehicle Act of 2024》。'
    '法案要求美国国家公路交通安全管理局（NHTSA）制定法规，确保所有在美国销售的新车'
    '——包括轿车、卡车和SUV——均配备AM广播接收功能。立法动议'
    '来自“9·11”事件后的应急通信反思：当移动电话网络因呼叫拥塞或'
    '基站损毁而瘫痪时，AM广播成为政府向公众传递紧急信息的可靠渠道。美国联邦紧急事务'
    '管理局（FEMA）长期将AM广播作为国家公共预警系统（IPAWS）的核心组成部分，要求'
    '所有AM台站配备备用电源和冗余发射设备。')

add_cn_paragraph(doc,
    '中国方面的动作同样迅速。2024年9月18日，工业和信息化部科技司对《车载无线广播'
    '接收系统》强制性国家标准制修订计划予以公示，面向社会公开征求意见。2025年4月30日，'
    '该国家标准计划正式下达，目前处于起草阶段。与美国的立法逻辑类似，中国在'
    '“十四五”规划中明确提出了“发挥广播覆盖网在应急信息发布中的'
    '主渠道作用”的方针。')

add_cn_paragraph(doc,
    '两国政策尽管法律形式不同——美国为国会立法，中国为国家标准'
    '——但其内在逻辑高度一致：在移动通信和互联网高度普及的今天，各国政府'
    '反而意识到，完全依赖高带宽、高复杂度的现代通信系统存在系统性风险。AM广播作为'
    '一种低技术门槛、高覆盖冗余的通信手段，正在被重新定义为“底线通信”'
    '基础设施。技术越发达，越需要为可能出现的最坏情况留下一条退路——这正是'
    '中美政策共振的深层逻辑。')

# ── 3 技术韧性 ──
add_heading_cn(doc, '三、技术韧性：AM广播的不可替代性', level=1)

add_cn_paragraph(doc,
    '要理解AM广播为何在今天仍被立法保护，需要回到其物理层特性。AM广播工作于530 kHz'
    '至1700 kHz的中频波段，这一频段赋予它两种独特的传播能力：地波传播和天波传播。'
    '地波沿地球表面传播，受地形起伏和建筑物的影响较小，可在复杂环境中稳定覆盖百公里'
    '半径。天波在夜间借助电离层反射，传播距离可达数百甚至上千公里。这意味着，一座'
    '中等功率的AM发射台在理想条件下即可覆盖一个省份的绝大部分区域。')

add_cn_paragraph(doc,
    '相比之下，FM广播工作于88 MHz至108 MHz的甚高频段，音质优于AM，但属于视距传播，'
    '受山体和高层建筑遮挡严重，单站覆盖半径通常仅有30至50公里。移动通信网络（4G/5G）'
    '依赖密集部署的基站群和光纤回传网络，单站覆盖在城市环境中仅数百米至数公里，且'
    '每个基站需要持续的电力供应和传输链路才能工作。互联网流媒体则更上层，完全依赖'
    '端到端的IP网络连通性，从内容分发网络到家庭路由器的任何一个环节中断，服务即告失效。')

add_cn_paragraph(doc,
    '从系统架构复杂度的视角观察，AM广播的优势更加突出。一套AM广播系统由音频源、'
    '调制器、射频功率放大器、发射天线和接收机构成。一台中波发射机加上一台柴油发电机，'
    '即可构成一个独立运行的信息发布节点。与之对照，移动通信系统涉及基站（gNB）、'
    '核心网（AMF/UPF）、传输网和供电冷却系统，每一层都是潜在的故障点。流媒体服务'
    '还需要内容分发网络、域名解析和光纤骨干网的全链路支撑。系统的复杂度与抗毁性之间，'
    '呈现出清晰的反比关系。')

add_cn_paragraph(doc,
    '技术“先进性”不等于技术“韧性”。5G可以提供每秒千兆比特的'
    '峰值速率，但在基站退服率超过90%的极端灾害场景中，其效能趋近于零。AM广播虽然'
    '信息速率低（单声道、窄带宽），但它的存在不受中间节点制约，接收端仅需简单的检波'
    '电路即可提取信息。这种“低速率、高可靠”的特性，使其在通信系统的韧性'
    '谱系中占据了一个不可替代的位置。')

# 图1
add_figure(doc, FIG1, '图1  AM广播地波与天波传播示意图')
# 表1
add_table_comparison(doc)

# ── 4 公共安全 ──
add_heading_cn(doc, '四、公共安全：极端情况下的“最后一道防线”', level=1)

add_cn_paragraph(doc,
    '现代社会的应急通信体系面临一个结构性矛盾：日常使用频率最高的通信手段，在危机'
    '时刻往往最先失效。移动通信网络在灾害中表现脆弱，原因在于其架构高度集中。2008年'
    '汶川特大地震中，灾区通信基站大面积损毁，光缆中断，震中地区的固定和移动通信完全'
    '瘫痪，救援部队与指挥中心失联长达数十小时。2011年日本东北地区太平洋地震引发海啸'
    '和核事故，灾区移动通信基站退服率一度超过90%，而AM广播电台在震后几分钟内即恢复'
    '播出，成为灾民获取官方信息和避难指引的主要渠道。')

add_cn_paragraph(doc,
    'AM广播在极端场景下的可靠性来自三个层面的物理优势。其一，不依赖电网。AM发射台'
    '通常配备柴油发电机和备用电源系统，接收端可以用电池供电或手摇发电的小型收音机，'
    '在电网完全瘫痪的情况下仍可工作。其二，不依赖中转网络。AM采用“一次发射、'
    '全域覆盖”的单向广播模式，不存在基站回传、核心网路由等中间环节，从根本上'
    '免疫了由基础设施级联失效导致的中断。其三，不会因用户数量增加而拥塞。移动通信'
    '网络中，大量用户同时呼叫或上网会导致基站过载、信道阻塞；而AM广播是“一对多'
    '”的广播模式，接收机数量增加不产生额外负载。')

add_cn_paragraph(doc,
    '三个场景可以清晰地呈现AM广播的战略备份价值。发生洪水或地震导致基站退服率超过'
    '90%时，AM广播仍可通过地波覆盖百公里半径的灾区。核心网或域名服务器遭受网络攻击'
    '导致流媒体瘫痪时，AM广播作为单向广播不存在握手协议和IP地址，从根本上免疫网络'
    '攻击。高空核爆产生的电磁脉冲可摧毁长导线和未屏蔽的半导体器件，但老式AM接收机'
    '（采用分立元件或真空管设计）具有更强的抗电磁脉冲能力。正是这些不可替代的应急'
    '属性，推动中美两国以立法和标准的形式将AM广播接收终端嵌入社会保有量最大、流动性'
    '最强的移动平台——汽车。')

# 图2
add_figure(doc, FIG2, '图2  AM广播系统与移动通信系统架构复杂度对比')

# ── 5 产业与标准 ──
add_heading_cn(doc, '五、产业与标准：国家力量保障技术底线', level=1)

add_cn_paragraph(doc,
    '在汽车智能化和电动化浪潮中，AM广播面临一个现实困境：部分车企开始以“空间'
    '优化”“电磁兼容复杂”为由，在新车型中悄然取消AM接收功能。特斯拉'
    '在2018年推出的Model 3中取消了AM广播，宣称电动机产生的电磁干扰严重劣化AM接收'
    '质量。这一做法逐步被其他电动汽车制造商效仿。消费者在购车过程中很少会专门检查AM'
    '功能是否存在，形成了事实上的“隐性减配”。')

add_cn_paragraph(doc,
    '强制性国家标准《车载无线广播接收系统》的制定，正是在这一背景下展开。从产业视角'
    '看，国标至少在三方面发挥作用。标准为AM接收性能设定了统一的技术门槛，所有在中国'
    '市场销售的乘用车必须通过相关测试，从制度上堵住了隐性减配的空间。同时，标准推动'
    '车企解决电磁兼容难题——为了满足AM接收灵敏度要求，电动汽车企业必须优化'
    '电机屏蔽设计、改进天线匹配网络、采用低噪声电源滤波器。这一过程反过来促进了国内'
    '电磁兼容技术水平的提升。标准还为国产射频芯片和天线模组创造了稳定的市场需求。'
    '恩智浦、Silicon Labs等传统车载收音芯片厂商逐步淡出AM市场时，国内射频前端企业'
    '如锐迪科、卓胜微等获得了进入车载前装市场的机会。')

add_cn_paragraph(doc,
    '强制性国家标准的意义不止于技术层面。它传递了一个清晰的信号：通信基础设施的'
    '“底线保障”不能完全交由市场机制决定。在经济效益与公共安全之间，政府'
    '需要发挥引导和兜底作用。AM广播的强制入车，是公共政策在技术演进过程中主动设置的'
    '一个“安全阀”——它不对技术创新的方向构成约束，但确保创新'
    '不会以牺牲基本安全保障为代价。')

# ── 6 传统与创新 ──
add_heading_cn(doc, '六、传统技术与前沿创新的辩证关系', level=1)

add_cn_paragraph(doc,
    '“强制保留AM广播”这一事件对电子信息工程专业提出了一个值得深思的问题：'
    '在技术快速迭代的行业环境中，传统技术的价值应当如何评估？')

add_cn_paragraph(doc,
    '一种常见的思维定势是将技术演进理解为线性替代——新技术的诞生意味着旧'
    '技术的消亡。移动通信从1G到5G的演进似乎印证了这一点；数字摄影取代胶片、智能手机'
    '取代功能手机，都强化了“新即先进、旧即淘汰”的直觉。然而，AM广播的'
    '案例提供了一个相反的证据：一项诞生于1906年的技术，在5G和低轨卫星互联网的时代，'
    '被全球最大的两个汽车市场以立法和标准的形式强制保留。这说明，技术的生命力不能'
    '仅用“新旧”或“速率”来衡量。')

add_cn_paragraph(doc,
    'AM广播的核心优势——极简系统架构带来的高可靠性——恰恰来自'
    '它的“陈旧”。在电子信息工程的底层逻辑中，系统的复杂度和可靠性之间'
    '存在根本性矛盾。增加一个节点就增加一个故障点，增加一层协议就增加一层失效风险。'
    '现代通信系统追求极致的信息速率和频谱效率，代价是系统复杂度的指数级上升。AM广播'
    '放弃了对速率和效率的追求，换来了在最恶劣条件下仍可工作的物理鲁棒性。这不是技术'
    '的落后，而是工程学中“取舍”（trade-off）原则的典型案例——'
    '不同的应用场景需要不同的技术特性，不存在一种在所有维度上都优于其他方案的'
    '“终极技术”。')

add_cn_paragraph(doc,
    '传统技术与前沿创新的关系，不是替代，而是互补。5G/6G的核心技术之一是毫米波通信，'
    '它同样建立在电磁波传播与调制解调的基本理论之上。无论通信技术如何演进，麦克斯韦'
    '方程组、傅里叶变换、香农信道容量公式这些底层工具始终是理解一切无线通信的基石。'
    'AM广播强制保留事件揭示的，正是电子信息工程学科中一个容易被忽视的规律：前沿创新'
    '的边界，往往由对传统技术原理的理解深度决定。')

# ── 7 课程重要性 ──
add_heading_cn(doc, '七、《高频电子线路》与《通信原理》的基石地位', level=1)

add_cn_paragraph(doc,
    '对于电子信息工程专业的学生而言，AM广播的强制保留事件提供了一面反思课程价值的镜子。')

add_cn_paragraph(doc,
    '《高频电子线路》是理解该事件的技术基础。这门课程讲授高频小信号谐振放大、非线性'
    '电路（调制与解调）、振荡器、混频器和锁相环等核心内容。一台AM广播发射机从音频'
    '信号的幅度调制到射频功率放大，一台超外差接收机从天线输入到本振混频、中频放大、'
    '包络检波——几乎涵盖了该课程的全部核心模块。理解AM广播为什么在低信噪比'
    '下仍可勉强分辨信息，需要掌握包络检波的门限效应；理解老式AM接收机为何能在电磁'
    '脉冲中幸存，需要了解分立元件与集成电路的抗扰度差异。这些知识无法通过学习高阶编程'
    '或应用层开发获得。')

add_cn_paragraph(doc,
    '《通信原理》则提供了理论层面的解释框架。AM调制在时域上表现为载波幅度随调制信号'
    '变化，频域上对应于载波频谱的搬移。这一过程是所有模拟通信的基础模型。香农公式从'
    '理论上限定了AM广播的信息传输容量，而AM在极端信道下的可达容量分析——'
    '尽管其带宽利用率低，但在莱斯衰落加强干扰的信道条件下并不一定劣于高阶QAM'
    '——需要扎实的信息论基础才能理解。从AM到FM到数字调制到正交频分复用，'
    '通信系统的实现技术在变，但信源编码、信道编码、调制解调的基本理论框架始终稳定。')

add_cn_paragraph(doc,
    '回到课程本身，这两门课在电子信息工程培养方案中常被贴上“硬核”'
    '“难学”的标签，部分学生倾向于将精力集中在更“前沿”的嵌入式'
    '开发或人工智能课程上。AM广播的案例说明，缺少对物理层核心原理的掌握，就无法真正'
    '理解通信系统的行为边界。当未来的工程师需要设计应急通信系统、评估基础设施安全性'
    '或制定技术标准时，高频电路和通信原理提供的不是公式和考题答案，而是从物理层思考'
    '问题的能力。')

# ── 8 结语 ──
add_heading_cn(doc, '八、结语', level=1)

add_cn_paragraph(doc,
    '“强制保留AM广播”不是技术保守主义的胜利，而是人类社会对复杂系统风险'
    '管理的理性选择。在一个高度互联但也极度脆弱的时代，保留一条低技术、高韧性的冗余'
    '通信通道，是工程伦理和公共安全意识的重要体现。')

add_cn_paragraph(doc,
    '对电子信息工程专业的学生而言，这一事件提供了双重启示：前沿创新需要传统技术作为'
    '“压舱石”；真正的工程能力既来自跟踪最新技术的能力，也来自对底层原理的'
    '深刻理解。学好《高频电子线路》与《通信原理》，不是为了一场考试，而是为未来可能'
    '遇到的任何通信系统——无论它多么“前沿”——准备好'
    '理解它、改进它、在极限条件下保障它的能力。')

# ── 参考文献 ──
doc.add_paragraph()
ref_title = doc.add_paragraph()
r = ref_title.add_run('参考文献')
set_run_font(r, cn_font='黑体', size=Pt(14), bold=True)

refs = [
    '[1] U.S. House of Representatives. H.R. 8449 — AM Radio for Every Vehicle Act of 2024.',
    '[2] 工业和信息化部科技司.《车载无线广播接收系统》强制性国家标准制修订计划项目公示, 2024-09-18.',
    '[3] 国家广播电视总局. 应急广播技术白皮书, 2022.',
    '[4] 国务院办公厅. 国家突发事件应急体系建设“十四五”规划, 2021.',
    '[5] Proakis, J.G., & Salehi, M. Digital Communications (5th ed.). McGraw-Hill, 2008.',
    '[6] 张肃文, 陆兆熊.《高频电子线路》(第五版). 高等教育出版社, 2018.',
    '[7] FEMA. Integrated Public Alert & Warning System (IPAWS) Modernization Report, 2023.',
]
for ref in refs:
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Pt(0)
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(ref)
    set_run_font(run, cn_font='宋体', size=Pt(10.5))

# ── 保存 ──
doc.save(OUTPUT)
print('Word文档已保存: ' + OUTPUT)
