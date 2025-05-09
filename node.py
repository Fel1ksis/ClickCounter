import keyboard
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime, timedelta
import winsound
import json
import os

class ModernCounterApp:
    def __init__(self):
        self.counter = 0
        self.goal = None
        self.price_per_box = 0
        self.count_key = 'e'  # Кнопка по умолчанию
        self.start_time = None
        self.last_click_time = None
        self.average_time_per_click = None
        
        # Загрузка сохраненных данных
        self.load_settings()
        
        self.window = tk.Tk()
        self.window.title("Счётчик нажатий")
        self.window.geometry("500x800")
        self.window.configure(bg='#2F4F4F')  # Тёмный серо-зелёный
        
        # Добавляем обработчик сворачивания окна
        self.window.bind('<Unmap>', self.on_window_minimize)
        
        # Основной контейнер
        self.main_frame = ttk.Frame(self.window, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Прогресс-бар слева
        self.progress_frame = tk.Frame(self.main_frame, bg='#2F4F4F')
        self.progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            orient='vertical',
            length=200,
            mode='determinate'
        )
        self.progress_bar.pack(side=tk.LEFT, padx=10)
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="0%",
            font=('Helvetica', 12),
            fg='#ECF0F1',
            bg='#2F4F4F'
        )
        self.progress_label.pack(side=tk.LEFT, padx=5)
        
        # Время выполнения
        self.time_label = tk.Label(
            self.progress_frame,
            text="",
            font=('Helvetica', 12),
            fg='#ECF0F1',
            bg='#2F4F4F'
        )
        self.time_label.pack(side=tk.LEFT, padx=5)
        
        # Верхняя секция - Установка цели и цены
        self.top_frame = tk.Frame(self.main_frame, bg='#2F4F4F')
        self.top_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Установка кнопки подсчета
        self.key_frame = tk.Frame(self.top_frame, bg='#2F4F4F')
        self.key_frame.pack(fill=tk.X, pady=10)
        
        self.key_label = tk.Label(
            self.key_frame,
            text="Кнопка подсчета:",
            font=('Helvetica', 14),
            fg='#ECF0F1',
            bg='#2F4F4F',
            width=15,
            anchor='e'
        )
        self.key_label.pack(side=tk.LEFT, padx=5)
        
        self.key_button = tk.Button(
            self.key_frame,
            text=f"Нажмите для смены (сейчас: {self.count_key})",
            command=self.start_key_capture,
            bg='#3498DB',
            fg='white',
            font=('Helvetica', 12),
            relief=tk.FLAT,
            width=30
        )
        self.key_button.pack(side=tk.LEFT, padx=5)
        
        # Установка цели
        self.goal_frame = tk.Frame(self.top_frame, bg='#2F4F4F')  # Тёмный серо-зелёный
        self.goal_frame.pack(fill=tk.X, pady=10)
        
        self.goal_label = tk.Label(
            self.goal_frame,
            text="Цель:",
            font=('Helvetica', 14),
            fg='#ECF0F1',
            bg='#2F4F4F',  # Тёмный серо-зелёный
            width=15,
            anchor='e'
        )
        self.goal_label.pack(side=tk.LEFT, padx=5)
        
        self.goal_entry = tk.Entry(
            self.goal_frame,
            font=('Helvetica', 14),
            bg='#34495E',
            fg='#ECF0F1',
            insertbackground='#ECF0F1',
            width=15
        )
        self.goal_entry.pack(side=tk.LEFT, padx=5)
        
        self.set_goal_button = tk.Button(
            self.goal_frame,
            text="Установить",
            command=self.set_goal,
            bg='#3498DB',
            fg='white',
            font=('Helvetica', 12),
            relief=tk.FLAT,
            width=15
        )
        self.set_goal_button.pack(side=tk.LEFT, padx=5)
        
        # Установка цены за коробку
        self.price_frame = tk.Frame(self.top_frame, bg='#2F4F4F')  # Тёмный серо-зелёный
        self.price_frame.pack(fill=tk.X, pady=10)
        
        self.price_label = tk.Label(
            self.price_frame,
            text="Цена за коробку:",
            font=('Helvetica', 14),
            fg='#ECF0F1',
            bg='#2F4F4F',  # Тёмный серо-зелёный
            width=15,
            anchor='e'
        )
        self.price_label.pack(side=tk.LEFT, padx=5)
        
        self.price_entry = tk.Entry(
            self.price_frame,
            font=('Helvetica', 14),
            bg='#34495E',
            fg='#ECF0F1',
            insertbackground='#ECF0F1',
            width=15
        )
        self.price_entry.pack(side=tk.LEFT, padx=5)
        
        self.set_price_button = tk.Button(
            self.price_frame,
            text="Установить",
            command=self.set_price,
            bg='#3498DB',
            fg='white',
            font=('Helvetica', 12),
            relief=tk.FLAT,
            width=15
        )
        self.set_price_button.pack(side=tk.LEFT, padx=5)
        
        # Создаем рамки одинакового размера для всех счетчиков
        counter_height = 120
        
        # Отображение оставшихся единиц (красные цифры)
        self.remaining_frame = tk.Frame(self.main_frame, bg='#D3D3D3')  # Светло-серый
        self.remaining_frame.pack(fill=tk.X, pady=20)
        self.remaining_frame.configure(height=counter_height)
        self.remaining_frame.pack_propagate(False)
        
        self.remaining_label = tk.Label(
            self.remaining_frame,
            text="0",
            font=('Helvetica', 48, 'bold'),
            fg='#e74c3c',
            bg='#D3D3D3'  # Светло-серый
        )
        self.remaining_label.pack(expand=True)
        
        # Основной счётчик (по центру)
        self.counter_frame = tk.Frame(self.main_frame, bg='#D3D3D3')  # Светло-серый
        self.counter_frame.pack(fill=tk.X, pady=20)
        self.counter_frame.configure(height=counter_height)
        self.counter_frame.pack_propagate(False)
        
        self.counter_label = tk.Label(
            self.counter_frame,
            text="0",
            font=('Helvetica', 48, 'bold'),
            fg='#3498DB',
            bg='#D3D3D3'  # Светло-серый
        )
        self.counter_label.pack(expand=True)
        
        # Отображение заработка (зеленые цифры)
        self.earnings_frame = tk.Frame(self.main_frame, bg='#D3D3D3')  # Светло-серый
        self.earnings_frame.pack(fill=tk.X, pady=20)
        self.earnings_frame.configure(height=counter_height)
        self.earnings_frame.pack_propagate(False)
        
        self.earnings_label = tk.Label(
            self.earnings_frame,
            text="0",  # Убрали символ рубля
            font=('Helvetica', 48, 'bold'),
            fg='#2ecc71',
            bg='#D3D3D3'  # Светло-серый
        )
        self.earnings_label.pack(expand=True)
        
        # Подсказка
        self.hint_label = tk.Label(
            self.main_frame,
            text=f"'{self.count_key}' - добавить | Backspace - убавить",
            font=('Helvetica', 14),
            fg='#ECF0F1',
            bg='#2F4F4F',  # Тёмный серо-зелёный
            wraplength=350
        )
        self.hint_label.pack(pady=20)
        
        # Кнопка сброса в самом низу
        self.reset_button = tk.Label(
            self.main_frame,
            text="СБРОСИТЬ ВСЁ",
            command=self.reset_all,
            fg='#ECF0F1',
            font=('Helvetica', 14),
            bg='#2F4F4F',
            cursor='hand2'
        )
        self.reset_button.pack(pady=(0, 20), side=tk.BOTTOM)
        self.reset_button.bind('<Button-1>', lambda e: self.reset_all())
        
        # Запуск отслеживания клавиатуры
        self.keyboard_thread = threading.Thread(target=self.start_listening, daemon=True)
        self.keyboard_thread.start()
        
        # Эффект пульсации
        self.pulsating = False
        
        # Обновляем отображение счетчика и других значений после загрузки
        self.counter_label.config(text=str(self.counter))
        if self.goal is not None:
            self.goal_entry.insert(0, str(self.goal))
            self.update_remaining()
        if self.price_per_box > 0:
            self.price_entry.insert(0, str(self.price_per_box))
            self.update_earnings()
    
    def load_settings(self):
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    settings = json.load(f)
                    saved_counter = settings.get('counter', 0)
                    saved_goal = settings.get('goal', None)
                    saved_price = settings.get('price_per_box', 0)
                    
                    # Если есть сохраненные значения и они не нулевые
                    if saved_counter > 0 or (saved_goal is not None and saved_goal > 0) or saved_price > 0:
                        if messagebox.askyesno("Восстановление", 
                            f"Найдены сохраненные значения:\n"
                            f"Счетчик: {saved_counter}\n"
                            f"Цель: {saved_goal if saved_goal is not None else 'Не установлена'}\n"
                            f"Цена за коробку: {saved_price}\n\n"
                            f"Восстановить эти значения?"):
                            self.count_key = settings.get('count_key', 'e')
                            self.counter = saved_counter
                            self.goal = saved_goal
                            self.price_per_box = saved_price
                            return
                    
                    # Если пользователь отказался или значения нулевые
                    self.count_key = settings.get('count_key', 'e')
                    self.counter = 0
                    self.goal = None
                    self.price_per_box = 0
        except:
            self.count_key = 'e'
            self.counter = 0
            self.goal = None
            self.price_per_box = 0
    
    def save_settings(self):
        settings = {
            'count_key': self.count_key,
            'counter': self.counter,
            'goal': self.goal,
            'price_per_box': self.price_per_box
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
    
    def on_window_minimize(self, event):
        # Сохраняем данные при сворачивании окна
        self.save_settings()
    
    def set_goal(self):
        try:
            new_goal = int(self.goal_entry.get())
            if new_goal <= 0:
                messagebox.showerror("Ошибка", "Цель должна быть положительным числом!")
                return
            self.goal = new_goal
            self.update_remaining()
            self.goal_entry.delete(0, tk.END)
            self.save_settings()  # Сохраняем после изменения цели
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите целое число!")
    
    def set_price(self):
        try:
            new_price = float(self.price_entry.get())
            if new_price <= 0:
                messagebox.showerror("Ошибка", "Цена должна быть положительным числом!")
                return
            self.price_per_box = new_price
            self.update_earnings()
            self.price_entry.delete(0, tk.END)
            self.save_settings()  # Сохраняем после изменения цены
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите число!")
    
    def update_remaining(self):
        if self.goal is not None:
            remaining = max(0, self.goal - self.counter)
            self.remaining_label.config(text=str(remaining))
            if remaining == 0:
                try:
                    winsound.PlaySound("goal.wav", winsound.SND_FILENAME)
                except:
                    winsound.MessageBeep()
                messagebox.showinfo("Поздравляем!", "Вы достигли своей цели!")
    
    def update_earnings(self):
        earnings = int(self.counter * self.price_per_box)
        self.earnings_label.config(text=str(earnings))  # Убрали символ рубля
    
    def increment_counter(self):
        current_time = datetime.now()
        if self.start_time is None:
            self.start_time = current_time
            self.last_click_time = current_time
        else:
            if self.last_click_time:
                time_diff = (current_time - self.last_click_time).total_seconds()
                if self.average_time_per_click is None:
                    self.average_time_per_click = time_diff
                else:
                    self.average_time_per_click = (self.average_time_per_click + time_diff) / 2
            self.last_click_time = current_time
            
        self.counter += 1
        self.counter_label.config(text=str(self.counter))
        self.update_remaining()
        self.update_earnings()
        self.update_progress()
        self.update_time_estimate()
        self.save_settings()
        
        # Эффект пульсации
        self.pulsate_counter()
        
        # Звуковой эффект
        winsound.Beep(1000, 50)

    def update_progress(self):
        if self.goal and self.goal > 0:
            progress = (self.counter / self.goal) * 100
            self.progress_bar['value'] = progress
            self.progress_label.config(text=f"{int(progress)}%")

    def update_time_estimate(self):
        if self.goal and self.average_time_per_click:
            remaining_clicks = self.goal - self.counter
            if remaining_clicks > 0:
                estimated_seconds = remaining_clicks * self.average_time_per_click
                estimated_time = timedelta(seconds=int(estimated_seconds))
                hours = estimated_time.seconds // 3600
                minutes = (estimated_time.seconds % 3600) // 60
                seconds = estimated_time.seconds % 60
                time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                self.time_label.config(text=f"Осталось: {time_str}")
            else:
                self.time_label.config(text="Задача выполнена!")

    def decrement_counter(self):
        if self.counter > 0:
            self.counter -= 1
            self.counter_label.config(text=str(self.counter))
            self.update_remaining()
            self.update_earnings()
            self.save_settings()  # Сохраняем после изменения счетчика
    
    def start_key_capture(self):
        self.key_button.config(text="Нажмите любую клавишу...")
        self.window.bind('<Key>', self.capture_key)
    
    def capture_key(self, event):
        if event.keysym.lower() != 'backspace':  # Не позволяем использовать backspace
            self.count_key = event.keysym.lower()
            self.key_button.config(text=f"Нажмите для смены (сейчас: {self.count_key})")
            self.window.unbind('<Key>')
            self.save_settings()
            
            # Перезапускаем прослушивание клавиатуры с новой клавишей
            keyboard.unhook_all()
            self.start_listening()
            
            # Обновляем подсказку
            self.update_hint()
            
            messagebox.showinfo("Успех", f"Кнопка подсчета изменена на '{self.count_key}'")
    
    def start_listening(self):
        keyboard.on_press_key(self.count_key, lambda _: self.window.after(0, self.increment_counter))
        keyboard.on_press_key('backspace', lambda _: self.window.after(0, self.decrement_counter))
    
    def update_hint(self):
        self.hint_label.config(
            text=f"'{self.count_key}' - добавить | Backspace - убавить"
        )
    
    def reset_all(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите сбросить все значения?"):
            self.counter = 0
            self.goal = None
            self.price_per_box = 0
            self.start_time = None
            self.last_click_time = None
            self.average_time_per_click = None
            self.counter_label.config(text="0")
            self.goal_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.remaining_label.config(text="0")
            self.earnings_label.config(text="0")
            self.progress_bar['value'] = 0
            self.progress_label.config(text="0%")
            self.time_label.config(text="")
            self.save_settings()
            
            messagebox.showinfo("Успех", "Все значения сброшены!")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ModernCounterApp()
    app.run()
