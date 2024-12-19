import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from paddleocr import PaddleOCR
import re

# 初始化 OCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

# 正则规则函数
def is_valid_license_plate(text):
    """
    判断是否为符合规则的车牌号（国际、中国车牌号或粤Z车牌号）
    """
    china_plate_pattern = r"^[\u4e00-\u9fff][A-Z]·[A-Z0-9]{5}$"
    international_plate_pattern = r"^[A-Z]{1,3}[0-9]{1,4}[A-Z0-9]{0,3}$"
    yue_z_plate_pattern = r"^粤Z·[A-Z0-9]{4}[港澳]$"
    newenergy_plate_pattern = r"^[\u4e00-\u9fff][A-Z]·[DF][A-Z0-9]{5}$"

    return (re.match(china_plate_pattern, text) or 
            re.match(international_plate_pattern, text) or
            re.match(yue_z_plate_pattern, text) or
            re.match(newenergy_plate_pattern, text))

# 车牌识别函数
def recognize_license_plate(image_path):
    result = ocr.ocr(image_path, det=True, rec=True)
    valid_candidates = []

    for line in result[0]:
        text, confidence = line[1]
        if is_valid_license_plate(text) and confidence > 0.9:
            valid_candidates.append((text, confidence))

    valid_candidates.sort(key=lambda x: x[1], reverse=True)
    return valid_candidates

# 界面更新函数
def update_image_and_results(image_path):
    # 更新图片显示
    try:
        img = Image.open(image_path)
    except Exception as e:
        result_label.configure(text=f"图片加载失败：{e}")
        return

    img.thumbnail((500, 300))  # 限制图片大小
    photo = ImageTk.PhotoImage(img)
    img_label.configure(image=photo)
    img_label.image = photo

    # 识别车牌
    results = recognize_license_plate(image_path)
    results_text = "识别结果：\n" + "\n".join([f"车牌: {text}, 置信度: {confidence:.2f}" for text, confidence in results])
    if not results:
        results_text = "未识别到符合条件的车牌号"
    result_label.configure(text=results_text)

# 选择文件函数
def select_file():
    filetypes = [("图片文件", "*.jpg *.jpeg *.png *.bmp"), ("所有文件", "*.*")]
    file_path = filedialog.askopenfilename(title="选择图片文件", filetypes=filetypes)
    if file_path:
        update_image_and_results(file_path)

# 退出系统函数
def exit_system():
    root.destroy()

# 创建主窗口
root = tk.Tk()
root.title("车牌识别系统")
root.geometry("800x600")
root.configure(bg="#2c3e50")

# 样式
style = ttk.Style()
style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Arial", 12))
style.configure("TButton", background="#3498db", foreground="white", font=("Arial", 12))
style.map("TButton", background=[("active", "#2980b9")])

# 界面布局
title_label = ttk.Label(root, text="车牌识别系统", style="TLabel", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

img_label = ttk.Label(root, text="请选择图片文件", style="TLabel", anchor="center")
img_label.pack(pady=10, padx=10)

btn_frame = tk.Frame(root, bg="#2c3e50")
btn_frame.pack(pady=20)

# 配置按钮的文本颜色
style.configure("TextColor.TButton", foreground="#2c3e50")

# 创建“选择图片”按钮
select_button = ttk.Button(btn_frame, text="选择图片", command=select_file, style="TextColor.TButton")
select_button.pack(side="left", padx=20)

# 创建“退出系统”按钮
exit_button = ttk.Button(btn_frame, text="退出系统", command=exit_system, style="TextColor.TButton")
exit_button.pack(side="right", padx=20)

result_label = ttk.Label(root, text="结果将在这里显示", style="TLabel", wraplength=600, anchor="w", justify="left")
result_label.pack(pady=20)

# 启动主循环
root.mainloop()
