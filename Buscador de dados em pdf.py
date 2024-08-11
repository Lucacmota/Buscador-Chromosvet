import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import fitz  # PyMuPDF
import os
import threading

def buscar_numero_em_pdf(numero, diretorio, progresso_var):
    resultados = []

    for pasta_raiz, _, arquivos in os.walk(diretorio):
        for nome_arquivo in arquivos:
            if nome_arquivo.endswith(".pdf"):
                caminho_arquivo = os.path.join(pasta_raiz, nome_arquivo)

                documento = fitz.open(caminho_arquivo)

                for numero_pagina in range(len(documento)):
                    pagina = documento.load_page(numero_pagina)
                    texto_pagina = pagina.get_text()
                    if numero in texto_pagina:
                        resultados.append((nome_arquivo, pasta_raiz))
                        break

                    progresso_var.set(numero_pagina / len(documento) * 100)
                    root.update_idletasks()

                documento.close()

    return resultados

def buscar_numero():
    numero = entrada_numero.get()
    diretorio = entrada_diretorio.get()

    if not numero:
        messagebox.showwarning("Aviso", "Por favor, insira um número para buscar.")
        return
    if not os.path.isdir(diretorio):
        messagebox.showwarning("Aviso", "Por favor, selecione um diretório válido.")
        return

    progress_window = tk.Toplevel(root)
    progress_window.title("Aguarde...")
    progress_window.geometry("300x100")
    progress_window.resizable(False, False)

    label_aguarde = tk.Label(progress_window, text="Buscando arquivo, por favor aguarde...")
    label_aguarde.pack(pady=10)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=100)
    progress_bar.pack(padx=20, pady=5, fill='x')

    def realizar_busca():
        resultados = buscar_numero_em_pdf(numero, diretorio, progress_var)
        progress_window.destroy()
        mostrar_resultados(resultados)

    thread = threading.Thread(target=realizar_busca)
    thread.start()

def mostrar_resultados(resultados):
    if resultados:
        mensagem = "O número foi encontrado nos seguintes arquivos:\n"
        for arquivo, pasta in resultados:
            mensagem += f"{arquivo} - Pasta: {pasta}\n"
        messagebox.showinfo("Resultados", mensagem)
    else:
        messagebox.showinfo("Resultados", "O número não foi encontrado em nenhum arquivo PDF no diretório.")

def selecionar_diretorio():
    diretorio = filedialog.askdirectory()
    if diretorio:
        entrada_diretorio.delete(0, tk.END)
        entrada_diretorio.insert(0, diretorio)

root = tk.Tk()
root.title("Buscar em PDF")

style = ttk.Style()
style.theme_use('default')

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.columnconfigure(1, weight=1)

label_numero = ttk.Label(frame, text="Número:")
label_numero.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

entrada_numero = ttk.Entry(frame, width=30)
entrada_numero.grid(row=0, column=1, padx=5, pady=5)

label_diretorio = ttk.Label(frame, text="Diretório:")
label_diretorio.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

entrada_diretorio = ttk.Entry(frame, width=30)
entrada_diretorio.grid(row=1, column=1, padx=5, pady=5)

botao_buscar = ttk.Button(frame, text="Buscar Número", command=buscar_numero)
botao_buscar.grid(row=2, column=0, sticky=tk.W, pady=10, padx=(5, 0))

botao_selecionar = ttk.Button(frame, text="Selecionar Diretório", command=selecionar_diretorio)
botao_selecionar.grid(row=2, column=1, sticky=tk.E, pady=10, padx=(0, 5))

root.geometry("310x120")
root.resizable(False, False)

root.mainloop()
