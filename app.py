import sys
import os
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class FormFillerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user_info = {}  # 存储用户信息
        self.current_file = None  # 当前处理的文件
        self.init_ui()
        self.load_stylesheet()
        
    def init_ui(self):
        # 主窗口设置
        self.setWindowTitle("AI表单自动填写助手")
        self.setGeometry(100, 100, 1400, 900)
        self.setWindowIcon(QIcon(self.create_icon("A")))
        
        # 创建主部件和布局
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 左侧导航栏
        self.init_navigation()
        
        # 右侧内容区
        self.init_content_area()
        
        # 状态栏
        self.init_status_bar()
        
        # 初始化功能模块
        self.init_modules()
        
        # 加载示例数据
        self.load_sample_data()
    
    def load_stylesheet(self):
        # 加载炫酷的样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QWidget {
                color: #ecf0f1;
                font-family: 'Segoe UI';
            }
            QFrame#navFrame {
                background-color: #1a1a2e;
                border-radius: 15px;
                border: 1px solid #3498db;
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #1a5276;
            }
            QListWidget {
                background-color: rgba(44, 62, 80, 180);
                color: #ecf0f1;
                border: 1px solid #3498db;
                border-radius: 8px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #34495e;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QProgressBar {
                border: 2px solid #3498db;
                border-radius: 5px;
                text-align: center;
                background: #1a1a2e;
            }
            QProgressBar::chunk {
                background-color: #2ecc71;
                width: 10px;
            }
            QTabWidget::pane {
                border: 1px solid #3498db;
                border-radius: 8px;
                background: rgba(26, 26, 46, 200);
            }
            QTabBar::tab {
                background: #2980b9;
                color: white;
                padding: 8px 20px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                border-bottom-color: #3498db;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: rgba(44, 62, 80, 180);
                color: #ecf0f1;
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
            }
            QGroupBox {
                border: 2px solid #3498db;
                border-radius: 10px;
                margin-top: 20px;
                font-size: 16px;
                font-weight: bold;
                color: #3498db;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
            }
            #contentFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                            stop:0 #0f2027, stop:1 #2c5364);
                border-radius: 15px;
            }
            #dropZone {
                border: 3px dashed #3498db;
                border-radius: 15px;
                background-color: rgba(26, 26, 46, 150);
            }
        """)
    
    def create_icon(self, text):
        """创建圆形图标"""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制渐变背景
        gradient = QRadialGradient(32, 32, 32, 32, 32)
        gradient.setColorAt(0, QColor("#3498db"))
        gradient.setColorAt(1, QColor("#1a5276"))
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 64, 64)
        
        # 绘制文字
        font = QFont("Arial", 24, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor("#ecf0f1"))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, text)
        painter.end()
        
        return pixmap
    
    def init_navigation(self):
        """初始化炫酷导航栏"""
        self.nav_frame = QFrame()
        self.nav_frame.setFixedWidth(250)
        self.nav_frame.setObjectName("navFrame")
        
        nav_layout = QVBoxLayout(self.nav_frame)
        nav_layout.setContentsMargins(20, 20, 20, 20)
        nav_layout.setSpacing(15)
        
        # 应用标题和logo
        title_layout = QHBoxLayout()
        app_icon = QLabel()
        app_icon.setPixmap(self.create_icon("AI").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        title_layout.addWidget(app_icon)
        
        title_text = QLabel("AI表单助手")
        title_text.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")
        title_layout.addWidget(title_text)
        title_layout.setAlignment(Qt.AlignCenter)
        nav_layout.addLayout(title_layout)
        
        # 添加分隔线
        nav_layout.addWidget(QLabel())
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #3498db;")
        nav_layout.addWidget(separator)
        
        # 功能导航按钮
        self.nav_buttons = []
        
        buttons = [
            ("系统信息收集", "icons/system.png", self.show_system_info),
            ("多模态数据处理", "icons/multimodal.png", self.show_multimodal),
            ("文件信息提取", "icons/extract.png", self.show_extraction),
            ("用户信息管理", "icons/user.png", self.show_user_profile),
            ("表单自动填充", "icons/fill.png", self.show_form_filling),
            ("设置", "icons/settings.png", self.show_settings)
        ]
        
        for text, icon, callback in buttons:
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon))
            btn.setMinimumHeight(50)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(callback)
            nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)
        
        # 添加伸展空间
        nav_layout.addStretch()
        
        # 添加状态指示器
        status_layout = QHBoxLayout()
        status_icon = QLabel()
        status_icon.setPixmap(QPixmap("icons/online.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        status_layout.addWidget(status_icon)
        
        status_label = QLabel("离线模式")
        status_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
        status_layout.addWidget(status_label)
        nav_layout.addLayout(status_layout)
        
        self.main_layout.addWidget(self.nav_frame)
    
    def init_content_area(self):
        """初始化内容区域"""
        self.content_frame = QFrame()
        self.content_frame.setObjectName("contentFrame")
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(20)
        
        # 内容标题
        self.content_title = QLabel("欢迎使用AI表单自动填写助手")
        self.content_title.setStyleSheet("font-size: 28px; font-weight: bold; color: #3498db;")
        self.content_title.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(self.content_title)
        
        # 内容堆叠窗口
        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget)
        
        # 初始化所有页面
        self.init_welcome_page()
        self.init_system_info_page()
        self.init_multimodal_page()
        self.init_extraction_page()
        self.init_user_profile_page()
        self.init_form_filling_page()
        self.init_settings_page()
        
        self.main_layout.addWidget(self.content_frame, 1)
    
    def init_welcome_page(self):
        """初始化欢迎页面"""
        self.welcome_page = QWidget()
        layout = QVBoxLayout(self.welcome_page)
        layout.setAlignment(Qt.AlignCenter)
        
        # 欢迎标题
        title = QLabel("AI表单自动填写助手")
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #3498db;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 副标题
        subtitle = QLabel("基于大语言模型的多模态表单自动填写解决方案")
        subtitle.setStyleSheet("font-size: 24px; color: #ecf0f1;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # 添加分隔符
        layout.addSpacing(40)
        
        # 功能描述
        features = [
            ("自动收集系统信息", "从操作系统中提取用户设置、设备状态等信息"),
            ("多模态数据处理", "处理文本、图像、音频等多种格式的数据"),
            ("文件信息提取", "从PDF、DOC、XLS等文件中提取关键信息"),
            ("智能表单填充", "根据用户信息自动填充DOC和XLS表单")
        ]
        
        for i, (title, desc) in enumerate(features):
            feature_layout = QHBoxLayout()
            
            icon_label = QLabel()
            icon_label.setPixmap(QPixmap(f"icons/feature_{i+1}.png").scaled(64, 64))
            feature_layout.addWidget(icon_label)
            
            text_layout = QVBoxLayout()
            title_label = QLabel(title)
            title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3498db;")
            text_layout.addWidget(title_label)
            
            desc_label = QLabel(desc)
            desc_label.setStyleSheet("font-size: 16px; color: #bdc3c7;")
            text_layout.addWidget(desc_label)
            
            feature_layout.addLayout(text_layout)
            layout.addLayout(feature_layout)
            layout.addSpacing(20)
        
        # 开始按钮
        start_btn = QPushButton("开始使用")
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                font-size: 20px;
                padding: 15px 30px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        start_btn.setCursor(Qt.PointingHandCursor)
        start_btn.clicked.connect(lambda: self.nav_buttons[0].click())
        layout.addWidget(start_btn, alignment=Qt.AlignCenter)
        
        self.stacked_widget.addWidget(self.welcome_page)
    
    def init_system_info_page(self):
        """系统信息收集页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 标题
        title = QLabel("系统信息收集")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")
        layout.addWidget(title)
        
        # 描述
        desc = QLabel("自动从操作系统中收集当前用户相关信息，包括个人设置、设备状态和最近活动等")
        desc.setStyleSheet("font-size: 16px; color: #bdc3c7;")
        layout.addWidget(desc)
        
        # 添加分隔符
        layout.addSpacing(20)
        
        # 收集按钮
        collect_btn = QPushButton("收集系统信息")
        collect_btn.setIcon(QIcon("icons/collect.png"))
        collect_btn.setStyleSheet("font-size: 16px; padding: 12px;")
        collect_btn.setCursor(Qt.PointingHandCursor)
        collect_btn.clicked.connect(self.collect_system_info) # button组件 链接 对应事件函数
        layout.addWidget(collect_btn, alignment=Qt.AlignLeft)
        
        # 添加分隔符
        layout.addSpacing(20)
        
        # 信息展示区域
        group_box = QGroupBox("收集到的系统信息")
        group_layout = QVBoxLayout(group_box)
        
        self.system_info_table = QTableWidget()
        self.system_info_table.setColumnCount(2)
        self.system_info_table.setHorizontalHeaderLabels(["信息类型", "详细信息"])
        self.system_info_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.system_info_table.verticalHeader().setVisible(False)
        self.system_info_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.system_info_table.setStyleSheet("""
            QTableWidget {
                background-color: rgba(26, 26, 46, 180);
                gridline-color: #3498db;
            }
            QHeaderView::section {
                background-color: #2980b9;
                color: white;
                padding: 5px;
                font-weight: bold;
            }
        """)
        
        group_layout.addWidget(self.system_info_table)
        layout.addWidget(group_box)
        
        self.stacked_widget.addWidget(page)
    
    def init_multimodal_page(self):
        """多模态数据处理页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 标题
        title = QLabel("多模态数据处理")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")
        layout.addWidget(title)
        
        # 描述
        desc = QLabel("使用多模态大模型技术处理文本、图像、音频等多种格式的数据")
        desc.setStyleSheet("font-size: 16px; color: #bdc3c7;")
        layout.addWidget(desc)
        
        # 添加分隔符
        layout.addSpacing(20)
        
        # 选项卡
        tab_widget = QTabWidget()
        
        # 文本处理标签页
        text_tab = QWidget()
        text_layout = QVBoxLayout(text_tab)
        
        text_input = QTextEdit()
        text_input.setPlaceholderText("在此输入文本内容...")
        text_input.setMinimumHeight(150)
        text_layout.addWidget(text_input)
        
        text_btn = QPushButton("分析文本")
        text_btn.setIcon(QIcon("icons/text.png"))
        text_btn.setCursor(Qt.PointingHandCursor)
        text_btn.clicked.connect(lambda: self.process_text(text_input.toPlainText()))
        text_layout.addWidget(text_btn)
        
        tab_widget.addTab(text_tab, "文本处理")
        
        # 图像处理标签页
        image_tab = QWidget()
        image_layout = QVBoxLayout(image_tab)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(200)
        self.image_label.setStyleSheet("background-color: rgba(44, 62, 80, 180); border-radius: 10px;")
        self.image_label.setText("拖放图像文件到此处或点击下方按钮选择")
        image_layout.addWidget(self.image_label)
        
        image_btn_layout = QHBoxLayout()
        select_btn = QPushButton("选择图像")
        select_btn.setIcon(QIcon("icons/image.png"))
        select_btn.setCursor(Qt.PointingHandCursor)
        select_btn.clicked.connect(self.select_image)
        image_btn_layout.addWidget(select_btn)
        
        analyze_btn = QPushButton("分析图像")
        analyze_btn.setIcon(QIcon("icons/analyze.png"))
        analyze_btn.setCursor(Qt.PointingHandCursor)
        analyze_btn.clicked.connect(self.process_image)
        image_btn_layout.addWidget(analyze_btn)
        
        image_layout.addLayout(image_btn_layout)
        
        tab_widget.addTab(image_tab, "图像处理")
        
        # 音频处理标签页
        audio_tab = QWidget()
        audio_layout = QVBoxLayout(audio_tab)
        
        self.audio_label = QLabel("未选择音频文件")
        self.audio_label.setStyleSheet("font-size: 16px;")
        audio_layout.addWidget(self.audio_label)
        
        audio_btn_layout = QHBoxLayout()
        select_audio_btn = QPushButton("选择音频")
        select_audio_btn.setIcon(QIcon("icons/audio.png"))
        select_audio_btn.setCursor(Qt.PointingHandCursor)
        select_audio_btn.clicked.connect(self.select_audio)
        audio_btn_layout.addWidget(select_audio_btn)
        
        analyze_audio_btn = QPushButton("分析音频")
        analyze_audio_btn.setIcon(QIcon("icons/analyze.png"))
        analyze_audio_btn.setCursor(Qt.PointingHandCursor)
        analyze_audio_btn.clicked.connect(self.process_audio)
        audio_btn_layout.addWidget(analyze_audio_btn)
        
        audio_layout.addLayout(audio_btn_layout)
        
        tab_widget.addTab(audio_tab, "音频处理")
        
        layout.addWidget(tab_widget)
        
        # 结果展示
        result_group = QGroupBox("分析结果")
        result_layout = QVBoxLayout(result_group)
        
        self.multimodal_result = QTextEdit()
        self.multimodal_result.setReadOnly(True)
        self.multimodal_result.setMinimumHeight(150)
        result_layout.addWidget(self.multimodal_result)
        
        layout.addWidget(result_group)
        
        self.stacked_widget.addWidget(page)
    
    def init_extraction_page(self):
        """文件信息提取页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 标题
        title = QLabel("文件信息提取")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")
        layout.addWidget(title)
        
        # 描述
        desc = QLabel("从PDF、DOC、XLS等格式文件中提取关键信息")
        desc.setStyleSheet("font-size: 16px; color: #bdc3c7;")
        layout.addWidget(desc)
        
        # 添加分隔符
        layout.addSpacing(20)
        
        # 文件拖放区域
        drop_frame = QFrame()
        drop_frame.setObjectName("dropZone")
        drop_frame.setMinimumHeight(200)
        drop_layout = QVBoxLayout(drop_frame)
        drop_layout.setAlignment(Qt.AlignCenter)
        
        drop_icon = QLabel()
        drop_icon.setPixmap(QPixmap("icons/file.png").scaled(80, 80))
        drop_icon.setAlignment(Qt.AlignCenter)
        drop_layout.addWidget(drop_icon)
        
        drop_text = QLabel("拖放文件到此处\n或点击下方按钮选择文件")
        drop_text.setStyleSheet("font-size: 18px; color: #3498db; text-align: center;")
        drop_text.setAlignment(Qt.AlignCenter)
        drop_layout.addWidget(drop_text)
        
        file_types = QLabel("支持格式: PDF, DOC, DOCX, XLS, XLSX")
        file_types.setStyleSheet("font-size: 14px; color: #bdc3c7; text-align: center;")
        drop_layout.addWidget(file_types)
        
        layout.addWidget(drop_frame)
        
        # 文件选择按钮
        btn_layout = QHBoxLayout()
        select_btn = QPushButton("选择文件")
        select_btn.setIcon(QIcon("icons/folder.png"))
        select_btn.setCursor(Qt.PointingHandCursor)
        select_btn.clicked.connect(self.select_file)
        btn_layout.addWidget(select_btn)
        
        extract_btn = QPushButton("提取信息")
        extract_btn.setIcon(QIcon("icons/extract.png"))
        extract_btn.setCursor(Qt.PointingHandCursor)
        extract_btn.clicked.connect(self.extract_file_info)
        btn_layout.addWidget(extract_btn)
        
        layout.addLayout(btn_layout)
        
        # 结果展示
        result_group = QGroupBox("提取结果")
        result_layout = QVBoxLayout(result_group)
        
        self.extraction_result = QTextEdit()
        self.extraction_result.setReadOnly(True)
        self.extraction_result.setMinimumHeight(200)
        result_layout.addWidget(self.extraction_result)
        
        layout.addWidget(result_group)
        
        self.stacked_widget.addWidget(page)
    
    def init_user_profile_page(self):
        """用户信息管理页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 标题
        title = QLabel("用户信息管理")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")
        layout.addWidget(title)
        
        # 描述
        desc = QLabel("构建和管理用户信息体系")
        desc.setStyleSheet("font-size: 16px; color: #bdc3c7;")
        layout.addWidget(desc)
        
        # 添加分隔符
        layout.addSpacing(20)
        
        # 用户信息表格
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(2)
        self.user_table.setHorizontalHeaderLabels(["信息类型", "值"])
        self.user_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.user_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.user_table.setStyleSheet("""
            QTableWidget {
                background-color: rgba(26, 26, 46, 180);
                gridline-color: #3498db;
            }
            QHeaderView::section {
                background-color: #2980b9;
                color: white;
                padding: 5px;
                font-weight: bold;
            }
        """)
        
        # 填充表格
        self.populate_user_table()
        
        layout.addWidget(self.user_table)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("保存信息")
        save_btn.setIcon(QIcon("icons/save.png"))
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(self.save_user_info)
        btn_layout.addWidget(save_btn)
        
        load_btn = QPushButton("加载信息")
        load_btn.setIcon(QIcon("icons/load.png"))
        load_btn.setCursor(Qt.PointingHandCursor)
        load_btn.clicked.connect(self.load_user_info)
        btn_layout.addWidget(load_btn)
        
        layout.addLayout(btn_layout)
        
        self.stacked_widget.addWidget(page)
    
    def init_form_filling_page(self):
        """表单自动填充页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 标题
        title = QLabel("表单自动填充")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")
        layout.addWidget(title)
        
        # 描述
        desc = QLabel("根据用户信息自动填充DOC和XLS表单")
        desc.setStyleSheet("font-size: 16px; color: #bdc3c7;")
        layout.addWidget(desc)
        
        # 添加分隔符
        layout.addSpacing(20)
        
        # 模板选择区域
        template_group = QGroupBox("选择模板文件")
        template_layout = QVBoxLayout(template_group)
        
        self.template_path = QLineEdit()
        self.template_path.setReadOnly(True)
        self.template_path.setPlaceholderText("未选择模板文件")
        template_layout.addWidget(self.template_path)
        
        btn_layout = QHBoxLayout()
        select_template_btn = QPushButton("选择模板")
        select_template_btn.setIcon(QIcon("icons/template.png"))
        select_template_btn.setCursor(Qt.PointingHandCursor)
        select_template_btn.clicked.connect(self.select_template)
        btn_layout.addWidget(select_template_btn)
        
        fill_btn = QPushButton("填充表单")
        fill_btn.setIcon(QIcon("icons/fill.png"))
        fill_btn.setCursor(Qt.PointingHandCursor)
        fill_btn.clicked.connect(self.auto_fill_forms)
        btn_layout.addWidget(fill_btn)
        
        template_layout.addLayout(btn_layout)
        layout.addWidget(template_group)
        
        # 预览区域
        preview_group = QGroupBox("填充预览")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMinimumHeight(300)
        preview_layout.addWidget(self.preview_text)
        
        layout.addWidget(preview_group)
        
        # 导出按钮
        export_btn = QPushButton("导出填充后的表单")
        export_btn.setIcon(QIcon("icons/export.png"))
        export_btn.setStyleSheet("font-size: 16px; padding: 12px;")
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.clicked.connect(self.export_filled_form)
        layout.addWidget(export_btn, alignment=Qt.AlignRight)
        
        self.stacked_widget.addWidget(page)
    
    def init_settings_page(self):
        """设置页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 标题
        title = QLabel("设置")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")
        layout.addWidget(title)
        
        # 添加分隔符
        layout.addSpacing(20)
        
        # 模型设置
        model_group = QGroupBox("模型设置")
        model_layout = QVBoxLayout(model_group)
        
        model_layout.addWidget(QLabel("本地模型路径:"))
        self.model_path = QLineEdit()
        self.model_path.setText("models/local_model")
        model_layout.addWidget(self.model_path)
        
        model_layout.addWidget(QLabel("模型类型:"))
        model_type = QComboBox()
        model_type.addItems(["多模态模型", "文本模型", "图像模型", "音频模型"])
        model_layout.addWidget(model_type)
        
        layout.addWidget(model_group)
        
        # 资源管理
        resource_group = QGroupBox("资源管理")
        resource_layout = QVBoxLayout(resource_group)
        
        resource_layout.addWidget(QLabel("CPU使用限制:"))
        cpu_slider = QSlider(Qt.Horizontal)
        cpu_slider.setRange(0, 100)
        cpu_slider.setValue(80)
        resource_layout.addWidget(cpu_slider)
        
        resource_layout.addWidget(QLabel("内存使用限制:"))
        mem_slider = QSlider(Qt.Horizontal)
        mem_slider.setRange(0, 100)
        mem_slider.setValue(70)
        resource_layout.addWidget(mem_slider)
        
        layout.addWidget(resource_group)
        
        # 隐私设置
        privacy_group = QGroupBox("隐私设置")
        privacy_layout = QVBoxLayout(privacy_group)
        
        encrypt_check = QCheckBox("加密存储用户信息")
        encrypt_check.setChecked(True)
        privacy_layout.addWidget(encrypt_check)
        
        auto_clear_check = QCheckBox("处理完成后自动清除临时文件")
        auto_clear_check.setChecked(True)
        privacy_layout.addWidget(auto_clear_check)
        
        layout.addWidget(privacy_group)
        
        # 保存按钮
        save_btn = QPushButton("保存设置")
        save_btn.setIcon(QIcon("icons/save.png"))
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn, alignment=Qt.AlignRight)
        
        self.stacked_widget.addWidget(page)
    
    def init_status_bar(self):
        """初始化状态栏"""
        self.status_bar = self.statusBar()
        
        # 添加状态标签
        self.status_label = QLabel("就绪")
        self.status_bar.addWidget(self.status_label)
        
        # 添加进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setMinimumHeight(20)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # 添加资源监视器
        self.cpu_label = QLabel("CPU: 0%")
        self.status_bar.addPermanentWidget(self.cpu_label)
        
        self.mem_label = QLabel("内存: 0MB")
        self.status_bar.addPermanentWidget(self.mem_label)
    
    def init_modules(self):
        """初始化功能模块"""
        # 这里可以初始化算法模块
        pass
    
    def load_sample_data(self):
        """加载示例数据"""
        self.user_info = {
            "姓名": "张三",
            "性别": "男",
            "年龄": "32",
            "身份证号": "110101199001011234",
            "职业": "软件工程师",
            "联系方式": "13800138000",
            "邮箱": "zhangsan@example.com",
            "兴趣爱好": "编程, 阅读, 旅行",
            "个性习惯": "早睡早起, 喜欢户外活动"
        }
    
    def populate_user_table(self):
        """填充用户信息表格"""
        self.user_table.setRowCount(len(self.user_info))
        
        for i, (key, value) in enumerate(self.user_info.items()):
            key_item = QTableWidgetItem(key)
            value_item = QTableWidgetItem(str(value))
            
            self.user_table.setItem(i, 0, key_item)
            self.user_table.setItem(i, 1, value_item)
    
    # =============== 页面导航方法 ===============
    
    def show_system_info(self):
        self.stacked_widget.setCurrentIndex(1)
        self.content_title.setText("系统信息收集")
    
    def show_multimodal(self):
        self.stacked_widget.setCurrentIndex(2)
        self.content_title.setText("多模态数据处理")
    
    def show_extraction(self):
        self.stacked_widget.setCurrentIndex(3)
        self.content_title.setText("文件信息提取")
    
    def show_user_profile(self):
        self.stacked_widget.setCurrentIndex(4)
        self.content_title.setText("用户信息管理")
        self.populate_user_table()
    
    def show_form_filling(self):
        self.stacked_widget.setCurrentIndex(5)
        self.content_title.setText("表单自动填充")
    
    def show_settings(self):
        self.stacked_widget.setCurrentIndex(6)
        self.content_title.setText("设置")
    
    # =============== 功能方法 ===============
    
    def collect_system_info(self):
        """收集系统信息"""
        self.status_label.setText("正在收集系统信息...")
        self.progress_bar.setVisible(True)
        
        # 模拟收集过程
        for i in range(1, 101):
            self.progress_bar.setValue(i)
            QApplication.processEvents()
            QThread.msleep(20)
        
        # 显示收集到的信息
        system_info = [
            ("用户名", "orangeai"),
            ("操作系统", "Windows 11 Pro"),
            ("系统版本", "22H2"),
            ("CPU", "Intel Core i7-12700H (16核)"),
            ("内存", "32GB DDR5"),
            ("磁盘空间", "512GB SSD (剩余 128GB)"),
            ("最近活动", "文档编辑, 网页浏览"),
            ("系统语言", "中文(简体)"),
            ("时区", "GMT+8"),
            ("安全状态", "受保护")
        ]
        
        self.system_info_table.setRowCount(len(system_info))
        for i, (key, value) in enumerate(system_info):
            self.system_info_table.setItem(i, 0, QTableWidgetItem(key))
            self.system_info_table.setItem(i, 1, QTableWidgetItem(value))
        
        self.status_label.setText("系统信息收集完成")
        self.progress_bar.setVisible(False)
    
    def process_text(self, text):
        """处理文本数据"""
        if not text:
            QMessageBox.warning(self, "输入错误", "请输入要分析的文本内容")
            return
        
        self.status_label.setText("正在分析文本...")
        self.progress_bar.setVisible(True)
        
        # 模拟分析过程
        for i in range(1, 101):
            self.progress_bar.setValue(i)
            QApplication.processEvents()
            QThread.msleep(10)
        
        # 显示分析结果
        result = f"文本分析结果:\n\n"
        result += f"文本长度: {len(text)} 字符\n"
        result += f"关键词: 人工智能, 表单, 自动化, 系统\n"
        result += f"情感分析: 积极 (置信度: 85%)\n"
        result += f"主题: 技术文档\n"
        result += f"摘要: 本文档讨论了基于人工智能的表单自动填写技术..."
        
        self.multimodal_result.setText(result)
        self.status_label.setText("文本分析完成")
        self.progress_bar.setVisible(False)
    
    def select_image(self):
        """选择图像文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图像文件", "", 
            "图像文件 (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.image_label.setPixmap(pixmap.scaled(
                    self.image_label.width(), 
                    self.image_label.height(),
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                ))
    
    def process_image(self):
        """处理图像数据"""
        if not self.image_label.pixmap():
            QMessageBox.warning(self, "错误", "请先选择图像文件")
            return
        
        self.status_label.setText("正在分析图像...")
        self.progress_bar.setVisible(True)
        
        # 模拟分析过程
        for i in range(1, 101):
            self.progress_bar.setValue(i)
            QApplication.processEvents()
            QThread.msleep(15)
        
        # 显示分析结果
        result = f"图像分析结果:\n\n"
        result += f"图像尺寸: 1920x1080 像素\n"
        result += f"主要颜色: 蓝色, 灰色, 白色\n"
        result += f"检测到的对象: 电脑, 显示器, 键盘, 书本\n"
        result += f"场景: 办公环境\n"
        result += f"文本识别: 'AI表单自动填写助手', '基于大语言模型'"
        
        self.multimodal_result.setText(result)
        self.status_label.setText("图像分析完成")
        self.progress_bar.setVisible(False)
    
    def select_audio(self):
        """选择音频文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择音频文件", "", 
            "音频文件 (*.mp3 *.wav *.ogg)"
        )
        
        if file_path:
            self.audio_label.setText(f"已选择: {os.path.basename(file_path)}")
    
    def process_audio(self):
        """处理音频数据"""
        if "已选择" not in self.audio_label.text():
            QMessageBox.warning(self, "错误", "请先选择音频文件")
            return
        
        self.status_label.setText("正在分析音频...")
        self.progress_bar.setVisible(True)
        
        # 模拟分析过程
        for i in range(1, 101):
            self.progress_bar.setValue(i)
            QApplication.processEvents()
            QThread.msleep(20)
        
        # 显示分析结果
        result = f"音频分析结果:\n\n"
        result += f"音频时长: 2分35秒\n"
        result += f"说话人: 男性 (置信度: 92%)\n"
        result += f"情绪状态: 中性\n"
        result += f"关键词: 人工智能, 自动化, 表单, 系统\n"
        result += f"转录文本: '欢迎使用AI表单自动填写助手. 本软件基于大语言模型...'"
        
        self.multimodal_result.setText(result)
        self.status_label.setText("音频分析完成")
        self.progress_bar.setVisible(False)
    
    def select_file(self):
        """选择要提取信息的文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "", 
            "所有文件 (*.pdf *.doc *.docx *.xls *.xlsx);;"
            "PDF文件 (*.pdf);;"
            "Word文件 (*.doc *.docx);;"
            "Excel文件 (*.xls *.xlsx)"
        )
        
        if file_path:
            self.current_file = file_path
            self.extraction_result.setText(f"已选择文件: {os.path.basename(file_path)}\n\n点击'提取信息'按钮开始提取")
    
    def extract_file_info(self):
        """从文件中提取信息"""
        if not self.current_file:
            QMessageBox.warning(self, "错误", "请先选择文件")
            return
        
        self.status_label.setText(f"正在从文件中提取信息...")
        self.progress_bar.setVisible(True)
        
        # 模拟提取过程
        for i in range(1, 101):
            self.progress_bar.setValue(i)
            QApplication.processEvents()
            QThread.msleep(20)
        
        # 显示提取结果
        file_name = os.path.basename(self.current_file)
        if file_name.endswith(".pdf"):
            result = f"PDF文件提取结果:\n\n"
            result += f"文档标题: 个人简历\n"
            result += f"作者: 张三\n"
            result += f"创建日期: 2023-10-15\n"
            result += f"页数: 3\n"
            result += f"提取内容:\n"
            result += f"姓名: 张三\n性别: 男\n年龄: 32\n"
            result += f"联系电话: 13800138000\n邮箱: zhangsan@example.com\n"
            result += f"教育背景: 计算机科学与技术 硕士\n工作经历: 高级软件工程师 (5年)"
        elif file_name.endswith((".doc", ".docx")):
            result = f"Word文档提取结果:\n\n"
            result += f"文档标题: 用户信息表\n"
            result += f"作者: 人力资源部\n"
            result += f"创建日期: 2023-11-20\n"
            result += f"字数: 856\n"
            result += f"提取内容:\n"
            result += f"姓名: 张三\n身份证号: 110101199001011234\n"
            result += f"地址: 北京市海淀区中关村大街1号\n"
            result += f"紧急联系人: 李四 (13800138001)\n"
            result += f"兴趣爱好: 编程, 阅读, 旅行"
        else:  # Excel文件
            result = f"Excel文件提取结果:\n\n"
            result += f"工作表数: 3\n"
            result += f"创建者: 财务部\n"
            result += f"最后修改: 2023-12-05\n"
            result += f"提取内容:\n"
            result += f"姓名: 张三\n部门: 技术研发部\n"
            result += f"员工编号: TECH2023001\n薪资: 25000\n"
            result += f"入职日期: 2019-03-15\n绩效评级: A"
        
        self.extraction_result.setText(result)
        self.status_label.setText("文件信息提取完成")
        self.progress_bar.setVisible(False)
        
        # 更新用户信息
        self.update_user_info_from_extraction(result)
    
    def update_user_info_from_extraction(self, result):
        """从提取结果更新用户信息"""
        # 这里可以添加更复杂的解析逻辑
        if "姓名: 张三" in result:
            self.user_info["姓名"] = "张三"
        if "性别: 男" in result:
            self.user_info["性别"] = "男"
        if "年龄: 32" in result:
            self.user_info["年龄"] = "32"
        if "身份证号: 110101199001011234" in result:
            self.user_info["身份证号"] = "110101199001011234"
        
        self.populate_user_table()
    
    def save_user_info(self):
        """保存用户信息"""
        self.status_label.setText("正在保存用户信息...")
        
        # 模拟保存过程
        QThread.msleep(500)
        
        self.status_label.setText("用户信息已保存到本地数据库")
        QMessageBox.information(self, "保存成功", "用户信息已成功保存")
    
    def load_user_info(self):
        """加载用户信息"""
        self.status_label.setText("正在加载用户信息...")
        
        # 模拟加载过程
        QThread.msleep(500)
        
        self.status_label.setText("用户信息加载完成")
        self.populate_user_table()
        QMessageBox.information(self, "加载成功", "用户信息已成功加载")
    
    def select_template(self):
        """选择表单模板"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择模板文件", "", 
            "模板文件 (*.doc *.docx *.xls *.xlsx);;"
            "Word模板 (*.doc *.docx);;"
            "Excel模板 (*.xls *.xlsx)"
        )
        
        if file_path:
            self.template_path.setText(file_path)
            self.current_file = file_path
    
    def auto_fill_forms(self):
        """自动填充表单"""
        if not self.template_path.text():
            QMessageBox.warning(self, "错误", "请先选择模板文件")
            return
        
        self.status_label.setText("正在填充表单...")
        self.progress_bar.setVisible(True)
        
        # 模拟填充过程
        for i in range(1, 101):
            self.progress_bar.setValue(i)
            QApplication.processEvents()
            QThread.msleep(20)
        
        # 显示填充预览
        template_name = os.path.basename(self.template_path.text())
        if template_name.endswith((".doc", ".docx")):
            preview = f"Word表单填充预览:\n\n"
            preview += f"文档标题: 个人信息表\n\n"
            preview += f"姓名: {self.user_info['姓名']}\n"
            preview += f"性别: {self.user_info['性别']}\n"
            preview += f"年龄: {self.user_info['年龄']}\n"
            preview += f"身份证号: {self.user_info['身份证号']}\n"
            preview += f"联系方式: {self.user_info.get('联系方式', '13800138000')}\n"
            preview += f"邮箱: {self.user_info.get('邮箱', 'zhangsan@example.com')}\n"
            preview += f"兴趣爱好: {self.user_info.get('兴趣爱好', '编程, 阅读, 旅行')}"
        else:  # Excel文件
            preview = f"Excel表单填充预览:\n\n"
            preview += f"工作表: 个人信息\n\n"
            preview += "字段\t\t值\n"
            preview += "----------------------------\n"
            preview += f"姓名\t\t{self.user_info['姓名']}\n"
            preview += f"性别\t\t{self.user_info['性别']}\n"
            preview += f"年龄\t\t{self.user_info['年龄']}\n"
            preview += f"身份证号\t{self.user_info['身份证号']}\n"
            preview += f"职业\t\t{self.user_info.get('职业', '软件工程师')}\n"
            preview += f"联系方式\t{self.user_info.get('联系方式', '13800138000')}"
        
        self.preview_text.setText(preview)
        self.status_label.setText("表单填充完成")
        self.progress_bar.setVisible(False)
    
    def export_filled_form(self):
        """导出填充后的表单"""
        if not self.preview_text.toPlainText():
            QMessageBox.warning(self, "错误", "没有可导出的表单内容")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存表单", "", 
            "Word文档 (*.docx);;Excel文档 (*.xlsx)"
        )
        
        if file_path:
            self.status_label.setText(f"正在导出表单到 {os.path.basename(file_path)}...")
            self.progress_bar.setVisible(True)
            
            # 模拟导出过程
            for i in range(1, 101):
                self.progress_bar.setValue(i)
                QApplication.processEvents()
                QThread.msleep(15)
            
            self.status_label.setText(f"表单已成功导出到 {file_path}")
            self.progress_bar.setVisible(False)
            QMessageBox.information(self, "导出成功", f"表单已成功导出到:\n{file_path}")
    
    def save_settings(self):
        """保存设置"""
        self.status_label.setText("设置已保存")
        QMessageBox.information(self, "设置保存", "您的设置已成功保存")

if __name__ == "__main__":

    from PyQt5.QtGui import QFont

    app = QApplication(sys.argv)
    # 设置支持中文的字体
    font = QFont("Microsoft YaHei", 10)  # Windows
    # font = QFont("WenQuanYi Micro Hei", 10)  # Linux
    app.setFont(font)
    # app = QApplication(sys.argv)
    
    # 设置应用程序样式和字体
    app.setStyle("Fusion")
    
    # 加载字体
    font_id = QFontDatabase.addApplicationFont("fonts/SegoeUI.ttf")
    if font_id != -1:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            app.setFont(QFont(font_families[0], 10))
    
    window = FormFillerApp()
    window.show()
    sys.exit(app.exec_())