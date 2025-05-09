import keyboard
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime
import winsound

class ModernCounterApp:
    def __init__(self):
        self.counter = 0
        self.goal = None
        self.price_per_box = 0
        self.window = tk.Tk()
        self.window.title("Счётчик нажатий")
        self.window.geometry("500x800")
        self.window.configure(bg='#2F4F4F')  # Тёмный серо-зелёный
        
        # Основной контейнер
        self.main_frame = ttk.Frame(self.window, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Верхняя секция - Установка цели и цены
        self.top_frame = tk.Frame(self.main_frame, bg='#2F4F4F')  # Тёмный серо-зелёный
        self.top_frame.pack(fill=tk.X, pady=(0, 20))
        
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
            text="'e' - добавить | Backspace - убавить",
            font=('Helvetica', 14),
            fg='#ECF0F1',
            bg='#2F4F4F',  # Тёмный серо-зелёный
            wraplength=350
        )
        self.hint_label.pack(pady=20)
        
        # Запуск отслеживания клавиатуры
        self.keyboard_thread = threading.Thread(target=self.start_listening, daemon=True)
        self.keyboard_thread.start()
        
        # Эффект пульсации
        self.pulsating = False
    
    def set_goal(self):
        try:
            new_goal = int(self.goal_entry.get())
            if new_goal <= 0:
                messagebox.showerror("Ошибка", "Цель должна быть положительным числом!")
                return
            self.goal = new_goal
            self.update_remaining()
            self.goal_entry.delete(0, tk.END)
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
        self.counter += 1
        self.counter_label.config(text=str(self.counter))
        self.update_remaining()
        self.update_earnings()
    
    def decrement_counter(self):
        if self.counter > 0:
            self.counter -= 1
            self.counter_label.config(text=str(self.counter))
            self.update_remaining()
            self.update_earnings()
    
    def start_listening(self):
        keyboard.on_press_key('e', lambda _: self.window.after(0, self.increment_counter))
        keyboard.on_press_key('backspace', lambda _: self.window.after(0, self.decrement_counter))
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ModernCounterApp()
    app.run()
