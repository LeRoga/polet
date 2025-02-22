import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3


class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQLite Database App")

        # Создаем соединение с БД (или создаем новую, если ее нет)
        self.conn = sqlite3.connect('polet.db')
        self.cursor = self.conn.cursor()

        # Назначаем интерфейс
        self.create_widgets()

    def create_widgets(self):
        # Выбор таблицы
        self.table_label = tk.Label(self.root, text="Выберите таблицу:")
        self.table_label.pack()

        self.table_select = tk.StringVar(self.root)
        self.table_menu = tk.OptionMenu(self.root, self.table_select, *self.get_tables())
        self.table_menu.pack()

        self.show_button = tk.Button(self.root, text="Показать данные", command=self.show_data)
        self.show_button.pack()

        self.output_text = tk.Text(self.root, height=10, width=50)
        self.output_text.pack()

        self.insert_button = tk.Button(self.root, text="Вставить данные", command=self.insert_data)
        self.insert_button.pack()

        self.update_button = tk.Button(self.root, text="Обновить данные", command=self.update_data)
        self.update_button.pack()

        self.delete_button = tk.Button(self.root, text="Удалить данные", command=self.delete_data)
        self.delete_button.pack()

        # Поле для ввода пользовательского SQL-запроса
        self.query_label = tk.Label(self.root, text="Введите ваш SQL-запрос:")
        self.query_label.pack()

        self.query_text = tk.Text(self.root, height=4, width=50)
        self.query_text.pack()

        self.execute_button = tk.Button(self.root, text="Выполнить запрос", command=self.execute_query)
        self.execute_button.pack()

    def get_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in self.cursor.fetchall()] or ["Нет таблиц"]

    def show_data(self):
        table = self.table_select.get()
        if not table:
            messagebox.showwarning("Предупреждение", "Выберите таблицу для отображения данных.")
            return
        self.cursor.execute(f"SELECT * FROM {table};")
        rows = self.cursor.fetchall()
        
        self.output_text.delete(1.0, tk.END)  # Очистить текстовое поле
        for row in rows:
            self.output_text.insert(tk.END, f"{row}\n")

    def insert_data(self):
        table = self.table_select.get()
        if not table:
            messagebox.showwarning("Предупреждение", "Выберите таблицу для вставки данных.")
            return

        row_data = simpledialog.askstring("Вставить данные", "Введите данные через запятую:")
        if row_data:
            values = tuple(row_data.split(","))
            placeholders = ", ".join(["?"] * len(values))
            try:
                self.cursor.execute(f"INSERT INTO {table} VALUES ({placeholders})", values)
                self.conn.commit()
                messagebox.showinfo("Успех", "Данные успешно вставлены!")
                self.show_data()  # Обновить отображение данных
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка при вставке данных: {e}")

    def update_data(self):
        table = self.table_select.get()
        if not table:
            messagebox.showwarning("Предупреждение", "Выберите таблицу для обновления данных.")
            return

        row_id = simpledialog.askinteger("Обновить данные", "Введите ID строки для обновления:")
        if row_id is None:
            return

        new_data = simpledialog.askstring("Обновить данные", "Введите новые данные через запятую:")
        if new_data:
            values = tuple(new_data.split(","))
            set_clause = ", ".join([f"col{i + 1} = ?" for i in range(len(values))])  # Предполагая, что ваши столбцы называются col1, col2, ...
            try:
                self.cursor.execute(f"UPDATE {table} SET {set_clause} WHERE id = ?", values + (row_id,))
                self.conn.commit()
                messagebox.showinfo("Успех", "Данные успешно обновлены!")
                self.show_data()  # Обновить отображение данных
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка при обновлении данных: {e}")

    def delete_data(self):
        table = self.table_select.get()
        if not table:
            messagebox.showwarning("Предупреждение", "Выберите таблицу для удаления данных.")
            return

        row_id = simpledialog.askinteger("Удалить данные", "Введите ID строки для удаления:")
        if row_id is not None:
            try:
                self.cursor.execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))
                self.conn.commit()
                messagebox.showinfo("Успех", "Данные успешно удалены!")
                self.show_data()  # Обновить отображение данных
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении данных: {e}")

    def execute_query(self):
        query = self.query_text.get("1.0", tk.END).strip()
        if not query:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите SQL-запрос.")
            return
        
        try:
            self.cursor.execute(query)
            if query.lower().startswith("select"):
                rows = self.cursor.fetchall()
                self.output_text.delete(1.0, tk.END)  # Очистить текстовое поле
                for row in rows:
                    self.output_text.insert(tk.END, f"{row}\n")
                self.conn.commit()
            else:
                self.conn.commit()
                messagebox.showinfo("Успех", "Запрос выполнен успешно!")
                self.show_data()  # Обновить отображение данных
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {e}")

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
