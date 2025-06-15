'''
word, pdf, excel to png
'''

from docx2pdf import convert
import os
import subprocess
from pdf2image import convert_from_path


def word_to_png(word_path, output_folder):
    # 先将Word转为PDF
    pdf_path = os.path.join(output_folder, "temp.pdf")
    convert(word_path, pdf_path)
    
    # 再将PDF转为PNG
    images = convert_from_path(pdf_path)
    
    # 保存PNG图片
    for i, image in enumerate(images):
        image.save(os.path.join(output_folder, f"page_{i+1}.png"), "PNG")
    
    # 删除临时PDF文件
    os.remove(pdf_path)


def pdf_to_png(pdf_path, output_folder):
    images = convert_from_path(pdf_path)
    
    for i, image in enumerate(images):
        image.save(os.path.join(output_folder, f"page_{i+1}.png"), "PNG")


def excel_to_png(input_path, output_folder):
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 临时PDF文件路径
    pdf_path = os.path.join(output_folder, "temp.pdf")
    
    # 使用LibreOffice将Excel转为PDF
    try:
        subprocess.run([
            "/Applications/LibreOffice.app/Contents/MacOS/soffice",  # MacOS上的完整路径
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_folder, 
            input_path
        ], check=True)
        
        # 获取转换后的PDF文件名（LibreOffice会自动命名）
        converted_pdf = os.path.join(
            output_folder,
            os.path.splitext(os.path.basename(input_path))[0] + ".pdf"
        )
        
        # 重命名为temp.pdf
        if os.path.exists(converted_pdf):
            os.rename(converted_pdf, pdf_path)
        
        # 将PDF转为PNG
        images = convert_from_path(pdf_path)
        
        # 保存PNG图片
        for i, image in enumerate(images):
            image.save(os.path.join(output_folder, f"excel_sheet_{i+1}.png"), "PNG")
        
    finally:
        # 确保删除临时PDF文件
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

# excel2png
excel_to_png("/Users/orange/code/FormGPT/TestDemo/form3.xlsx", "/Users/orange/code/FormGPT/Output")  # Excel
# pdf2png
#pdf_to_png("/Users/orange/code/FormGPT/TestDemo/form1.pdf", "/Users/orange/code/FormGPT/Output")
# word2png
# word_to_png("/Users/orange/code/FormGPT/TestDemo/form1.docx", "/Users/orange/code/FormGPT/Output")



