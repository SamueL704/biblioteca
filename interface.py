from tkinter import *
from tkinter import ttk
from app import *

root = Tk()
root.title("Controle de Emprestimos")

Label(root, text="Registros de emprestimos").grid(row=0, column=1, columnspan=2)
columns = ("nome", "email", "livro", "data do emprestimo", "status do emprestimo")
tree_emprestimos = ttk.Treeview(root, columns=columns, show = "headings")
for col in columns:
    tree_emprestimos.heading(col, text=col)
tree_emprestimos.grid(row=1, column=1, columnspan=1, sticky='nsew')

Button(root, text="Mostrar Dados").grid(row=2, column=1, columnspan=2)

root.mainloop()