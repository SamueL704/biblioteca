from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import requests

def fecth_data():
    try:   
        requisicao = requests.get("http://127.0.0.1:5000/emprestimos")
        requisicao_dic = requisicao.json()

        for row in tree_emprestimos.get_children():
            tree_emprestimos.delete(row)
        for emprestimo in requisicao_dic:
            values = (
                emprestimo["nome"],
                emprestimo["email"],
                emprestimo["livro"],
                emprestimo["data_emprestimo"],
                emprestimo["status_emprestimo"]
            )
            tree_emprestimos.insert("", "end", values=values)
    
        messagebox.showinfo("Sucesso", "Dados carregados com sucesso!")
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "Não foi possível conectar ao servidor.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro de API", f"Houve um erro ao buscar os dados: {e}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

root = Tk()
root.title("Controle de Emprestimos")

Label(root, text="Registros de emprestimos").grid(row=0, column=1, columnspan=2)
columns = ("nome", "email", "livro", "data do emprestimo", "status do emprestimo")
tree_emprestimos = ttk.Treeview(root, columns=columns, show = "headings")
for col in columns:
    tree_emprestimos.heading(col, text=col)
tree_emprestimos.grid(row=1, column=1, columnspan=1, sticky='nsew')

Button(root, text="Mostrar Dados", command=fecth_data).grid(row=2, column=1, columnspan=2)

root.mainloop()