"""
DrawSign v2.0 - Automatic drawing bot for Edusign
Cross-platform: Windows & Linux
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import numpy as np
import cv2
import time
import tkinter as tk
from tkinter import filedialog, messagebox

class EdusignDrawBot:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("DrawSign v2.0")
        self.window.geometry("600x550")
        self.window.configure(bg="#f0f0f0")
        
        self.image_path = None
        self.driver = None
        
        self.create_ui()
    
    def create_ui(self):
        title = tk.Label(
            self.window,
            text="🎨 DrawSign v2.0",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#1976D2"
        )
        title.pack(pady=20)
        
        # Edusign URL
        frame_url = tk.LabelFrame(
            self.window,
            text="1. Edusign Link",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=20,
            pady=10
        )
        frame_url.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            frame_url,
            text="Paste your Edusign signature link:",
            bg="white",
            fg="#666",
            font=("Arial", 9)
        ).pack(pady=5)
        
        self.url_entry = tk.Entry(frame_url, width=50, font=("Arial", 10))
        self.url_entry.insert(0, "https://static.edusign.com/student/email-signature?courseId=...")
        self.url_entry.pack(pady=5)
        
        btn_open = tk.Button(
            frame_url,
            text="🌐 Open Edusign",
            command=self.open_edusign,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            relief="flat",
            padx=20,
            pady=10
        )
        btn_open.pack(pady=8)
        
        # Image
        frame_img = tk.LabelFrame(
            self.window,
            text="2. Select Image",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=20,
            pady=10
        )
        frame_img.pack(fill="x", padx=20, pady=10)
        
        btn_image = tk.Button(
            frame_img,
            text="📂 Choose Image",
            command=self.select_image,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            relief="flat",
            padx=20,
            pady=10
        )
        btn_image.pack(pady=5)
        
        self.label_image = tk.Label(
            frame_img,
            text="No image selected",
            bg="white",
            fg="#666"
        )
        self.label_image.pack(pady=5)
        
        # Options
        frame_opt = tk.LabelFrame(
            self.window,
            text="3. Drawing Options",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=20,
            pady=10
        )
        frame_opt.pack(fill="x", padx=20, pady=10)
        
        mode_frame = tk.Frame(frame_opt, bg="white")
        mode_frame.pack(fill="x", pady=5)
        
        tk.Label(mode_frame, text="Mode:", bg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        self.mode_var = tk.StringVar(value="contours")
        tk.Radiobutton(
            mode_frame,
            text="Contours only",
            variable=self.mode_var,
            value="contours",
            bg="white"
        ).pack(side="left", padx=10)
        tk.Radiobutton(
            mode_frame,
            text="Full image",
            variable=self.mode_var,
            value="full",
            bg="white"
        ).pack(side="left", padx=10)
        
        thickness_frame = tk.Frame(frame_opt, bg="white")
        thickness_frame.pack(fill="x", pady=5)
        
        tk.Label(thickness_frame, text="Thickness:", bg="white").pack(side="left", padx=5)
        self.thickness_var = tk.IntVar(value=1)
        tk.Scale(
            thickness_frame,
            from_=1,
            to=4,
            orient="horizontal",
            variable=self.thickness_var,
            bg="white",
            length=150
        ).pack(side="left", padx=5)
        
        size_frame = tk.Frame(frame_opt, bg="white")
        size_frame.pack(fill="x", pady=5)
        
        tk.Label(size_frame, text="Size (%):", bg="white").pack(side="left", padx=5)
        self.size_var = tk.IntVar(value=80)
        tk.Scale(
            size_frame,
            from_=30,
            to=100,
            orient="horizontal",
            variable=self.size_var,
            bg="white",
            length=200
        ).pack(side="left", padx=5)
        
        self.skip_white = tk.BooleanVar(value=True)
        tk.Checkbutton(
            frame_opt,
            text="Skip white pixels",
            variable=self.skip_white,
            bg="white"
        ).pack(pady=5)
        
        # Draw
        frame_draw = tk.LabelFrame(
            self.window,
            text="4. Start Drawing",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=20,
            pady=10
        )
        frame_draw.pack(fill="x", padx=20, pady=10)
        
        self.btn_draw = tk.Button(
            frame_draw,
            text="▶️ DRAW",
            command=self.start_drawing,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 14, "bold"),
            cursor="hand2",
            relief="flat",
            padx=30,
            pady=15,
            state="disabled"
        )
        self.btn_draw.pack(pady=10)
        
        self.status = tk.Label(
            frame_draw,
            text="",
            bg="white",
            fg="#666",
            font=("Arial", 10, "bold")
        )
        self.status.pack(pady=5)
    
    def open_edusign(self):
        url = self.url_entry.get()
        if not url or "courseId" not in url:
            messagebox.showerror("Error", "Please enter a valid Edusign URL")
            return
        
        try:
            self.status.config(text="⏳ Opening browser...", fg="#ff9800")
            self.driver = webdriver.Chrome()
            self.driver.get(url)
            self.status.config(text="✅ Edusign opened!", fg="#4CAF50")
            time.sleep(3)
            self.check_ready()
        except Exception as e:
            self.status.config(text=f"❌ Error", fg="#f44336")
            messagebox.showerror("Error", f"Failed to open browser:\n{e}")
    
    def select_image(self):
        path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if path:
            self.image_path = path
            filename = path.split("\\")[-1] if "\\" in path else path.split("/")[-1]
            self.label_image.config(text=f"✅ {filename}", fg="#4CAF50")
            self.check_ready()
    
    def check_ready(self):
        if self.driver and self.image_path:
            self.btn_draw.config(state="normal")
    
    def extract_contours(self, img, thickness=2):
        """Extract contours from image"""
        gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
        _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
        
        try:
            skeleton = cv2.ximgproc.thinning(binary)
        except:
            kernel = np.ones((2, 2), np.uint8)
            skeleton = cv2.erode(binary, kernel, iterations=1)
        
        if thickness > 1:
            kernel = np.ones((thickness, thickness), np.uint8)
            skeleton = cv2.dilate(skeleton, kernel, iterations=1)
        
        result = cv2.bitwise_not(skeleton)
        result_rgb = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
        
        return Image.fromarray(result_rgb)
    
    def resize_image_proportional(self, img, canvas_width, canvas_height, scale_percent):
        """Resize image proportionally"""
        img_width, img_height = img.size
        
        ratio_w = canvas_width / img_width
        ratio_h = canvas_height / img_height
        ratio = min(ratio_w, ratio_h) * (scale_percent / 100)
        
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
        canvas_img = Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255))
        
        offset_x = (canvas_width - new_width) // 2
        offset_y = (canvas_height - new_height) // 2
        canvas_img.paste(img_resized, (offset_x, offset_y))
        
        return canvas_img
    
    def start_drawing(self):
        if not self.driver or not self.image_path:
            return
        
        try:
            self.status.config(text="⏳ Finding canvas...", fg="#ff9800")
            
            canvas = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "canvas"))
            )
            
            canvas_width = self.driver.execute_script("return arguments[0].width;", canvas)
            canvas_height = self.driver.execute_script("return arguments[0].height;", canvas)
            
            self.status.config(text=f"✅ Canvas: {canvas_width}x{canvas_height}", fg="#4CAF50")
            
            img = Image.open(self.image_path)
            
            if self.mode_var.get() == "contours":
                self.status.config(text="🔍 Extracting contours...", fg="#2196F3")
                self.window.update()
                thickness = self.thickness_var.get()
                img = self.extract_contours(img, thickness)
            
            scale_percent = self.size_var.get()
            img_final = self.resize_image_proportional(img, canvas_width, canvas_height, scale_percent)
            
            self.status.config(text="🎨 Preparing...", fg="#2196F3")
            time.sleep(1)
            
            pixels = np.array(img_final.convert('RGB'))
            
            self.status.config(text="🖌️ Drawing...", fg="#2196F3")
            
            js_script = """
            const canvas = arguments[0];
            const ctx = canvas.getContext('2d');
            const pixels = arguments[1];
            const width = arguments[2];
            const height = arguments[3];
            const skipWhite = arguments[4];
            
            ctx.strokeStyle = '#000000';
            ctx.lineWidth = 1;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            
            let drawing = false;
            
            for (let y = 0; y < height; y++) {
                const xStart = (y % 2 === 0) ? 0 : width - 1;
                const xEnd = (y % 2 === 0) ? width : -1;
                const xStep = (y % 2 === 0) ? 1 : -1;
                
                for (let x = xStart; x !== xEnd; x += xStep) {
                    const idx = (y * width + x) * 3;
                    const r = pixels[idx];
                    const g = pixels[idx + 1];
                    const b = pixels[idx + 2];
                    
                    if (skipWhite && r > 240 && g > 240 && b > 240) {
                        if (drawing) {
                            ctx.stroke();
                            drawing = false;
                        }
                        continue;
                    }
                    
                    if (!drawing) {
                        ctx.beginPath();
                        ctx.moveTo(x, y);
                        drawing = true;
                    } else {
                        ctx.lineTo(x, y);
                    }
                }
            }
            
            if (drawing) {
                ctx.stroke();
            }
            
            return 'done';
            """
            
            pixels_list = pixels.flatten().tolist()
            
            result = self.driver.execute_script(
                js_script,
                canvas,
                pixels_list,
                canvas_width,
                canvas_height,
                self.skip_white.get()
            )
            
            self.status.config(text="✅ Done!", fg="#4CAF50")
            messagebox.showinfo("✅", "Drawing completed!")
            
        except Exception as e:
            self.status.config(text=f"❌ Error", fg="#f44336")
            messagebox.showerror("Error", f"{e}")
    
    def run(self):
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.mainloop()
    
    def on_close(self):
        if self.driver:
            self.driver.quit()
        self.window.destroy()


if __name__ == "__main__":
    print("🎨 DrawSign v2.0")
    print("Cross-platform drawing bot for Edusign")
    app = EdusignDrawBot()
    app.run()