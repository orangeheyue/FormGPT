import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from paddleocr import PaddleOCR
import paddle 

class FormFiller:
    def __init__(self):
        # 初始化OCR，使用兼容的参数配置
        self.ocr = PaddleOCR(
            use_textline_orientation=True,  # 替换已废弃的use_angle_cls
            lang="ch"
        )
        
        # self.ocr = PaddleOCR(
        #     use_doc_orientation_classify=False,
        #     use_doc_unwarping=False,
        #     use_textline_orientation=False)

        # 设置字体（MacOS示例）
        try:
            self.font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 18)
        except:
            self.font = ImageFont.load_default()
    

    def recognize_text_and_tables(self, image_path):
        """识别文字内容和表格结构"""
        result = self.ocr.predict([image_path]) # 可支持多张
        print("len(result):", len(result)) 
        # 解析OCR结果
        text_data = []
        table_boxes = []
        
        for res in result:
            res.print()
            res.save_to_img("/home/orange/orangeai/FormGPT/Output/output_img")
            res.save_to_json("/home/orange/orangeai/FormGPT/Output/output_json")


        if result and len(result) > 0:
            for line in result:
                if line and len(line) >= 2:
                    # 提取文本和位置信息
                    text_info = {
                        'text': line[1][0],
                        'box': line[0],
                        'position': (int(np.mean([p[0] for p in line[0]])), 
                                     int(np.mean([p[1] for p in line[0]])))
                    }
                    text_data.append(text_info)
                    
                    # 简单判断是否为表格单元格（可根据实际情况调整）
                    if len(line[0]) == 4:  # 矩形框
                        table_boxes.append(line[0])
        
        return text_data, table_boxes
    
    def fill_form(self, template_path, data_dict, output_path):
        """自动填写表单并保存"""
        # 读取图像
        img = Image.open(template_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        
        # 识别文字和表格结构
        text_data, table_boxes = self.recognize_text_and_tables(template_path)
        
        print("识别到的文字内容:", [t['text'] for t in text_data])
        
        # 建立单元格映射关系（简化版）
        cell_mapping = {}
        for i, box in enumerate(table_boxes):
            center_x = sum([p[0] for p in box]) / 4
            center_y = sum([p[1] for p in box]) / 4
            cell_mapping[(center_x, center_y)] = box
        
        # 填充数据
        for field, value in data_dict.items():
            # 查找匹配的字段位置
            for text in text_data:
                if field in text['text']:
                    # 找到最近的单元格
                    min_dist = float('inf')
                    target_box = None
                    for (cx, cy), box in cell_mapping.items():
                        dist = (text['position'][0] - cx)**2 + (text['position'][1] - cy)**2
                        if dist < min_dist:
                            min_dist = dist
                            target_box = box
                    
                    # 在单元格内填写内容
                    if target_box:
                        # 计算文本框的中心位置
                        x_center = sum([p[0] for p in target_box]) / 4
                        y_center = sum([p[1] for p in target_box]) / 4
                        
                        # 获取文本宽度以居中显示
                        text_width = draw.textlength(str(value), font=self.font)
                        text_x = x_center - text_width / 2
                        text_y = y_center - 10  # 稍微向上偏移
                        
                        draw.text((text_x, text_y), str(value), fill="black", font=self.font)
        
        # 保存结果
        img.save(output_path)
        print(f"已保存填写后的表单到: {output_path}")

if __name__ == "__main__":
    # 初始化表单填写器
    filler = FormFiller()
    
    # 表单模板路径
    template_path = "/home/orange/orangeai/FormGPT/Output/page_1.png"
    
    # 要填写的数据（键为识别到的字段名或部分内容）
    form_data = {
        "姓名": "张三",
        "性别": "男",
        "年龄": "28",
        "联系电话": "13800138000",
        "地址": "北京市海淀区"
    }
    
    # 输出路径
    output_path = "/Users/orange/orangeai/FormGPT/Output/filled_form.png"
    
    # 填写并保存表单
    filler.fill_form(template_path, form_data, output_path)
