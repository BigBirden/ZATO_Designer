import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import colorchooser, filedialog, messagebox

# TODO:
# 1. Настроить масштабирование изображений при изменении размеров окна
# 2. Добавить кнопку справки с информацией о: Начальных параметрах, Авторе программы
# 3. Добавить "ползунки" (настройки) порогам контраста

class ZATODesigner:
    def __init__(self, root):
        self.root = root
        
        # Создание окна
        self.root.title("ZATO Designer")
        self.root.geometry("1700x700")
        self.root.minsize(1100, 700)
        
        self.original = None
        self.result = None
        self.main_color = np.array([50, 150, 80])
        
        self.build_ui()
        
        # Начальные параметры
        #self.graylevels = 4
        #self.main_color = np.array([50, 150, 80])
        #self.noise_strength = 5
        #self.contrast_min = 60
        #self.contrast_max = 200
        #self.brightness = 0
        #self.contrast = 0
    
    # Создание интерфейса в окне
    def build_ui(self):
        # Кнопки сверху
        top = tk.Frame(self.root, padx=10, pady=10)
        top.pack(fill="x")
        
        tk.Button(top, text="Открыть фото", command=self.open_image,
            width=16).pack(side="left", padx=4)
        tk.Button(top, text="Обработать", command=self.generate_image,
            width=16).pack(side="left", padx=4)
        tk.Button(top, text="Сохранить фото", command=self.save_image,
            width=16).pack(side="left", padx=4)
        
        # Кнопка смены цвета
        color_frame = tk.Frame(top)
        color_frame.pack(fill="x", pady=5)
        
        tk.Label(
            color_frame,
            text="Цвет:"
        ).pack(side="left")

        self.color_button = tk.Button(
            color_frame,
            command=self.choose_color,
            bg=self.rgb_to_hex(self.main_color),
            width=10,
            height=1
        )
        self.color_button.pack(side="left", padx=(5, 0))
        
        # Каркас основной области
        main = tk.Frame(self.root)
        main.pack(fill="both", expand=True, padx=10, pady=5)

        # Левая область: картинки
        images_frame = tk.Frame(main)
        images_frame.pack(side="left", fill="both", expand=True)

        # Загружаем в области фото
        self.original_label = tk.Label(
            images_frame, text="Оригинал", bd=1, 
            relief="solid", bg="#eeeeee"
        )
        self.original_label.pack(
            side="left", fill="both", expand=True, 
            padx=5, pady=5
        )
        
        self.result_label = tk.Label(
            images_frame, text="Результат", bd=1, 
            relief="solid", bg="#eeeeee"
        )
        self.result_label.pack(
            side="left", fill="both", expand=True, 
            padx=5, pady=5
        )

        # Правая область: элементы управления
        control_frame = tk.Frame(main, width=300, padx=15)
        control_frame.pack(side="right", fill="y")
        control_frame.pack_propagate(False)
        
        # Заголовок
        tk.Label(
            control_frame, text="Параметры обработки",
            font=("Arial", 14, "bold")
        ).pack(pady=(5, 15))
        
        # Ползунки
        self.brightness = self.add_slider(
            control_frame, "Яркость", -100, 100, 0, 1
        )
        self.contrast = self.add_slider(
            control_frame, "Контраст", -100, 100, 0, 1
        )
        self.graylevels = self.add_slider(
            control_frame, "Уровни серого", 2, 16, 4, 1
        )
        self.noise_strength = self.add_slider(
            control_frame, "Шум", 0, 50, 5, 1
        )
    
    # Вспомогательная функция добавления слайдеров для настроек
    def add_slider(self, parent, name, min_value, max_value,
                   default, resolution):
        frame = tk.Frame(parent)
        frame.pack(fill="x", pady=5)
        
        label = tk.Label(frame, text=name, anchor="c")
        label.pack(fill="x")
        
        var = tk.IntVar(value=default)
        scale = tk.Scale(
            frame,
            from_ = min_value,
            to = max_value,
            resolution = resolution, 
            orient = "horizontal",
            variable = var,
            showvalue = True
        )
        scale.pack(fill="x")
        
        return var
    
    # Функция выбора картинки
    def open_image(self):
        path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.webp *.bmp"),
                ("Все файлы", "*.*")
            ]
        )
        
        if not path:
            return
        
        try:
            self.original = Image.open(path).convert("RGB")
            self.show_image(self.original, self.original_label)
            
            self.result = Image.open(path).convert("RGB")
            self.show_image(self.result, self.result_label)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть изображение:\n{e}")
    
    # Функция сохранения картинки
    def save_image(self):
        if self.result is None:
            messagebox.showwarning(
                "Нет результата",
                "Сначала обработайте фотографию."
            )
            return
        
        path = filedialog.asksaveasfilename(
            title="Сохранить результат",
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg")
            ]
        )
        
        if not path:
            return
        
        try:
            self.result.save(path)
            messagebox.showinfo("Готово", "Изображение сохранено.")
        except Exception as e:
            messagebox.showerror(
                "Ошибка сохранения",
                f"Не удалось сохранить изображение:\n{e}"
            )
    
    # Функция выбора цвета
    def choose_color(self):
        color = colorchooser.askcolor(
            initialcolor=self.rgb_to_hex(self.main_color),
            title="Выберите основной цвет"
        )
        
        if color[0] is None:
            return
        
        self.main_color = np.array(tuple(int(x) for x in color[0]))
        self.color_button.config(
            bg = self.rgb_to_hex(self.main_color)
        )
    
    @staticmethod
    def rgb_to_hex(rgb):
        return "#{:02x}{:02x}{:02x}".format(*rgb)
    
    def process_image(self, 
        image, 
        main_color, 
        brightness, 
        contrast, 
        graylevels, 
        noise_strength, 
        contrast_min, 
        contrast_max
    ):
        
        # Создание массива размерности (n x m x k), где 
        # n, m - высота и ширина картинки (не наоборот)
        # k - кортеж с тремя числами цветов R, G, B
        array = np.array(image)
        
        # Переводим изображение в Ч/Б
        gray = np.mean(array, axis=2)
        
        # Генерируем шум на изображении
        noise = np.random.normal( 0, noise_strength, gray.shape )
        noisy_gray = gray + noise
        noisy_gray = np.clip(noisy_gray, 0, 255)

        # Добавляем яркость к картинке
        adjusted_gray = noisy_gray + brightness
        adjusted_gray = np.clip(adjusted_gray, 0, 255)

        # Добавляем контраст к картинке
        contrast_factor = 1 + contrast / 100
        adjusted_gray = (adjusted_gray - 128) * contrast_factor + 128
        adjusted_gray = np.clip(adjusted_gray, 0, 255)

        # Нормализуем картинку таким образом, чтобы с помощью границ контраста прийти к примерному результату
        normalized_gray = ( (adjusted_gray - contrast_min) / (contrast_max - contrast_min) )
        normalized_gray = np.clip(normalized_gray, 0, 1)

        # Распределяем цвета по уровням серого (т.е. в массиве мы дальше храним индексы уровня от 0 до graylevels)
        level = np.floor( normalized_gray * graylevels ).astype(np.uint8)
        level = np.clip(level, 0, graylevels - 1)
        level = graylevels - 1 - level

        # Создаем палитру цветов от белого к основному цвету к черному
        # Делим пополам уровни серости и первую половину относим к градиенту "белый -> основной цвет", а вторую к "основной цвет -> черный"
        palette = np.zeros( (graylevels, 3), dtype=np.uint8 )
        for i in range(graylevels):
            value = i / (graylevels - 1)
            
            if value < 0.5:
                t = value * 2
                color = 255 * (1 - t) + main_color * t
            else:
                t = (value - 0.5) * 2
                color = main_color * (1 - t)
            palette[i] = color

        # Накладываем получившуюся палитру на оттенки серого
        colored = palette[level]
        colored_image = Image.fromarray(colored)
        
        return colored_image
       
    # Функция масштабирования (Не используется)
    def resize_image(self, image, width, height):
        resized = image.copy()
        resized.thumbnail((width, height))
        
        return ImageTk.PhotoImage(resized)

    # Функция отрисовки изображения
    def show_image(self, image, label):
        preview = image.copy()
        preview.thumbnail((560, 650))
        
        photo = ImageTk.PhotoImage(preview)
        label.config(image=photo, text="")
        label.image = photo
        
    # Применение изменений в ползунках
    def generate_image(self):
        if self.original is None:
            messagebox.showwarning(
                "Нет изображения",
                "Сначала откройте изображение."
            )
            return
            
        try:
            self.result = self.process_image(
                self.original,
                main_color=self.main_color,
                brightness=self.brightness.get(),
                contrast=self.contrast.get(),
                graylevels=self.graylevels.get(),
                noise_strength=self.noise_strength.get(),
                contrast_min=60,
                contrast_max=200
            )
            
            self.show_image(self.result, self.result_label)
        except Exception as e:
            messagebox.showerror(
                "Ошибка обработки",
                f"Не удалось обработать изображение:\n{e}"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = ZATODesigner(root)
    root.mainloop()


