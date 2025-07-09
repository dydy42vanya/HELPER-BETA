import tkinter as tk
import random

class MathGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Математическая Игра")
        self.root.geometry("400x400")

        self.score = 0
        self.current_question = ""
        self.correct_answer = 0

        # Виджеты
        self.label_score = tk.Label(root, text=f"Очки: {self.score}", font=("Arial", 14))
        self.label_score.pack(pady=10)

        self.label_question = tk.Label(root, text="", font=("Arial", 18))
        self.label_question.pack(pady=20)

        self.entry_answer = tk.Entry(root, font=("Arial", 14))
        self.entry_answer.pack(pady=10)

        self.button_submit = tk.Button(root, text="Проверить", command=self.check_answer, font=("Arial", 12))
        self.button_submit.pack(pady=10)

        self.label_result = tk.Label(root, text="", font=("Arial", 14))
        self.label_result.pack(pady=10)

        self.generate_question()

    def generate_question(self):
        a = random.randint(1, 50)
        b = random.randint(1, 50)
        operation = random.choice(["+", "-", "*"])

        if operation == "+":
            self.current_question = f"{a} + {b} = ?"
            self.correct_answer = a + b
        elif operation == "-":
            self.current_question = f"{a} - {b} = ?"
            self.correct_answer = a - b
        else:
            self.current_question = f"{a} × {b} = ?"
            self.correct_answer = a * b

        self.label_question.config(text=self.current_question)
        self.entry_answer.delete(0, tk.END)

    def check_answer(self):
        """Проверяет ответ пользователя."""
        try:
            user_answer = int(self.entry_answer.get())
            if user_answer == self.correct_answer:
                self.score += 1
                self.label_result.config(text="✅ Верно!", fg="green")
            else:
                self.label_result.config(text=f"❌ Неверно! Правильный ответ: {self.correct_answer}", fg="red")
        except ValueError:
            self.label_result.config(text="Введите число!", fg="red")

        self.label_score.config(text=f"Очки: {self.score}")
        self.root.after(1500, self.generate_question)

# Запуск игры
root = tk.Tk()
game = MathGame(root)
root.mainloop()