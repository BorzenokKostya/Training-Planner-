import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

# Основное окно
root = tk.Tk()
root.title("Training Planner")
root.geometry("600x500")  # Размер, чтобы всё поместилось

# Глобальный список тренировок
trainings = []

# --- Функции ---
def add_training():
    date = date_entry.get()
    tr_type = type_var.get()
    duration_str = duration_entry.get()
    # Валидация ввода
    try:
        duration = int(duration_str)
        # Проверка формата даты
        datetime.strptime(date, "%d.%m.%Y")
        if duration <= 0:
            raise ValueError("Длительность должна быть положительным числом.")
    except ValueError as e:
        messagebox.showerror("Ошибка", f"Некорректный ввод: {e}")
        return
    
    training = {"date": date, "type": tr_type, "duration": duration}
    trainings.append(training)
    table.insert("", "end", values=(date, tr_type, duration))
    # Очистка полей
    date_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)

def filter_trainings():
    f_type = filter_type_var.get()
    f_date = filter_date_entry.get()
    # Удаляем все строки
    for row in table.get_children():
        table.delete(row)
    # Добавляем подходящие по фильтру
    for tr in trainings:
        if (not f_type or tr["type"] == f_type) and (not f_date or tr["date"] == f_date):
            table.insert("", "end", values=(tr["date"], tr["type"], tr["duration"]))

def save_to_json():
    path = filedialog.asksaveasfilename(defaultextension=".json",
                                         filetypes=[("JSON Files", "*.json")])
    if path:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(trainings, f, ensure_ascii=False, indent=2)

def load_from_json():
    path = filedialog.askopenfilename(filetypes=[('JSON Files', '*.json')])
    if path:
        with open(path, "r", encoding="utf-8") as f:
            global trainings
            trainings = json.load(f)
        # Очистить таблицу
        for row in table.get_children():
            table.delete(row)
        # Добавить все из файла
        for tr in trainings:
            table.insert("", "end", values=(tr["date"], tr["type"], tr["duration"]))

# --- Создание интерфейса ---

# Поля для ввода
tk.Label(root, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
type_var = tk.StringVar()
type_combo = ttk.Combobox(root, textvariable=type_var)
type_combo["values"] = ["Бег", "Плавание", "Велосипед", "Силовая", "Другое"]
type_combo.current(0)
type_combo.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Длительность (минут):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
duration_entry = tk.Entry(root)
duration_entry.grid(row=2, column=1, padx=5, pady=5)

# Кнопка добавить
tk.Button(root, text="Добавить тренировку", command=add_training).grid(row=3, column=0, columnspan=2, pady=10)

# Таблица с тренировками
columns = ("date", "type", "duration")
table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col.capitalize())
    table.column(col, width=150)
table.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

# Фильтр
tk.Label(root, text="Фильтр по типу:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
filter_type_var = tk.StringVar()
filter_type_combo = ttk.Combobox(root, textvariable=filter_type_var, 
                                 values=["", "Бег", "Плавание", "Велосипед", "Силовая", "Другое"])
filter_type_combo.current(0)
filter_type_combo.grid(row=6, column=1, padx=5, pady=5)

tk.Label(root, text="Фильтр по дате (ДД.ММ.ГГГГ):").grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
filter_date_entry = tk.Entry(root)
filter_date_entry.grid(row=7, column=1, padx=5, pady=5)

tk.Button(root, text="Применить фильтр", command=filter_trainings).grid(row=8, column=0, padx=5, pady=10)
tk.Button(root, text="Сбросить фильтр", command=lambda: [filter_type_combo.set(""), filter_date_entry.delete(0, tk.END), filter_trainings()]).grid(row=8, column=1, padx=5, pady=10)

# Сохранение/загрузка JSON
tk.Button(root, text="Сохранить в JSON", command=save_to_json).grid(row=9, column=0, padx=5, pady=10)
tk.Button(root, text="Загрузить из JSON", command=load_from_json).grid(row=9, column=1, padx=5, pady=10)

# Запуск главного цикла
root.mainloop()
