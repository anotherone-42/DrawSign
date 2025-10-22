"""
DrawBot pour Edusign - Dessine directement sur le canvas HTML5
Installation: pip install selenium pillow numpy webdriver-manager
Usage: python drawbot_simple.py
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import numpy as np
import time
import tkinter as tk
from tkinter import filedialog, messagebox

class EdusignDrawBot:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("DrawBot pour Edusign")
        self.window.geometry("600x550")
        self.window.configure(bg="#f0f0f0")
        
        self.image_path = None
        self.driver = None
        
        self.create_ui()
    
    def create_ui(self):
        title = tk.Label(
            self.window,
            text="🎨 DrawBot pour Edusign",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#1976D2"
        )
        title.pack(pady=20)
        
        # URL Edusign
        frame_url = tk.LabelFrame(
            self.window,
            text="1. URL Edusign",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=20,
            pady=10
        )
        frame_url.pack(fill="x", padx=20, pady=10)
        
        self.url_entry = tk.Entry(frame_url, width=50, font=("Arial", 10))
        self.url_entry.insert(0, "https://static.edusign.com/student/email-signature?courseId=...")
        self.url_entry.pack(pady=5)
        
        btn_open = tk.Button(
            frame_url,
            text="🌐 Ouvrir Edusign",
            command=self.open_edusign,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            relief="flat",
            padx=20,
            pady=10
        )
        btn_open.pack(pady=5)
        
        # Image
        frame_img = tk.LabelFrame(
            self.window,
            text="2. Image à dessiner",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=20,
            pady=10
        )
        frame_img.pack(fill="x", padx=20, pady=10)
        
        btn_image = tk.Button(
            frame_img,
            text="📂 Sélectionner une image",
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
            text="Aucune image",
            bg="white",
            fg="#666"
        )
        self.label_image.pack(pady=5)
        
        # Options
        frame_opt = tk.LabelFrame(
            self.window,
            text="3. Options",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=20,
            pady=10
        )
        frame_opt.pack(fill="x", padx=20, pady=10)
        
        speed_frame = tk.Frame(frame_opt, bg="white")
        speed_frame.pack(fill="x", pady=5)
        
        tk.Label(speed_frame, text="Vitesse:", bg="white").pack(side="left", padx=5)
        self.speed_var = tk.IntVar(value=5)
        tk.Scale(
            speed_frame,
            from_=1,
            to=10,
            orient="horizontal",
            variable=self.speed_var,
            bg="white",
            length=200
        ).pack(side="left", padx=5)
        
        # Nouvelle option: taille de l'image
        size_frame = tk.Frame(frame_opt, bg="white")
        size_frame.pack(fill="x", pady=5)
        
        tk.Label(size_frame, text="Taille (% du canvas):", bg="white").pack(side="left", padx=5)
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
            text="Ignorer pixels blancs",
            variable=self.skip_white,
            bg="white"
        ).pack(pady=5)
        
        # Dessin
        frame_draw = tk.LabelFrame(
            self.window,
            text="4. Dessiner",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=20,
            pady=10
        )
        frame_draw.pack(fill="x", padx=20, pady=10)
        
        self.btn_draw = tk.Button(
            frame_draw,
            text="▶️ DESSINER SUR EDUSIGN",
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
            font=("Arial", 11, "bold")
        )
        self.status.pack(pady=5)
    
    def open_edusign(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Erreur", "Entrez l'URL Edusign")
            return
        
        try:
            self.status.config(text="⏳ Ouverture du navigateur...", fg="#ff9800")
            self.driver = webdriver.Chrome()
            self.driver.get(url)
            self.status.config(text="✅ Edusign ouvert ! Attendez le chargement...", fg="#4CAF50")
            time.sleep(3)
            self.check_ready()
        except Exception as e:
            self.status.config(text=f"❌ Erreur: {e}", fg="#f44336")
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le navigateur.\n\nInstallez ChromeDriver:\npip install webdriver-manager\n\nErreur: {e}")
    
    def select_image(self):
        path = filedialog.askopenfilename(
            title="Choisir une image",
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
    
    def resize_image_proportional(self, img, canvas_width, canvas_height, scale_percent):
        """
        Redimensionne l'image proportionnellement pour tenir dans le canvas
        sans déformation, puis applique le facteur d'échelle
        """
        # Dimensions originales
        img_width, img_height = img.size
        
        # Calculer le ratio pour tenir dans le canvas
        ratio_w = canvas_width / img_width
        ratio_h = canvas_height / img_height
        ratio = min(ratio_w, ratio_h)
        
        # Appliquer le facteur d'échelle utilisateur
        ratio *= (scale_percent / 100)
        
        # Nouvelles dimensions
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        
        # Redimensionner avec LANCZOS (meilleure qualité)
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Créer une image blanche de la taille du canvas
        canvas_img = Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255))
        
        # Centrer l'image redimensionnée
        offset_x = (canvas_width - new_width) // 2
        offset_y = (canvas_height - new_height) // 2
        canvas_img.paste(img_resized, (offset_x, offset_y))
        
        return canvas_img, offset_x, offset_y, new_width, new_height
    
    def start_drawing(self):
        if not self.driver or not self.image_path:
            return
        
        try:
            self.status.config(text="⏳ Recherche du canvas...", fg="#ff9800")
            
            # Trouver le canvas
            canvas = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "canvas"))
            )
            
            # Obtenir les dimensions du canvas
            canvas_width = self.driver.execute_script("return arguments[0].width;", canvas)
            canvas_height = self.driver.execute_script("return arguments[0].height;", canvas)
            
            self.status.config(text=f"✅ Canvas: {canvas_width}x{canvas_height}", fg="#4CAF50")
            
            # Charger l'image et la redimensionner proportionnellement
            img = Image.open(self.image_path)
            scale_percent = self.size_var.get()
            
            img_final, offset_x, offset_y, img_w, img_h = self.resize_image_proportional(
                img, canvas_width, canvas_height, scale_percent
            )
            
            self.status.config(text=f"🎨 Image: {img_w}x{img_h} (centrée)", fg="#2196F3")
            time.sleep(1)
            
            pixels = np.array(img_final.convert('RGB'))
            
            self.status.config(text="🖌️ Dessin en cours...", fg="#2196F3")
            
            # Script de dessin JavaScript optimisé
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
                // Zigzag pour optimiser le tracé
                const xStart = (y % 2 === 0) ? 0 : width - 1;
                const xEnd = (y % 2 === 0) ? width : -1;
                const xStep = (y % 2 === 0) ? 1 : -1;
                
                for (let x = xStart; x !== xEnd; x += xStep) {
                    const idx = (y * width + x) * 3;
                    const r = pixels[idx];
                    const g = pixels[idx + 1];
                    const b = pixels[idx + 2];
                    
                    // Ignorer les pixels blancs
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
            
            # Convertir pixels en liste pour JavaScript
            pixels_list = pixels.flatten().tolist()
            
            # Exécuter le script
            result = self.driver.execute_script(
                js_script,
                canvas,
                pixels_list,
                canvas_width,
                canvas_height,
                self.skip_white.get()
            )
            
            self.status.config(text="✅ Dessin terminé !", fg="#4CAF50")
            messagebox.showinfo("✅ Succès", "Le dessin est terminé sur Edusign !")
            
        except Exception as e:
            self.status.config(text=f"❌ Erreur: {e}", fg="#f44336")
            messagebox.showerror("Erreur", f"Erreur lors du dessin:\n{e}")
    
    def run(self):
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.mainloop()
    
    def on_close(self):
        if self.driver:
            self.driver.quit()
        self.window.destroy()


if __name__ == "__main__":
    print("🎨 DrawBot pour Edusign")
    print("Installation: pip install selenium pillow numpy webdriver-manager")
    app = EdusignDrawBot()
    app.run()