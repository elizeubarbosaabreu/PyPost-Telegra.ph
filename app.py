import tkinter as tk
from tkinter import filedialog, messagebox, Menu, scrolledtext
from telegraph import Telegraph
import clipboard, webbrowser


# ---------------- Funções ----------------
def postar(user, title, content):
    telegraph = Telegraph()
    try:
        telegraph.create_account(short_name=user)
        response = telegraph.create_page(title, html_content=content)
        mensagem = response['url']
        clipboard.copy(mensagem)
        messagebox.showinfo(
            "Link gerado!",
            f"O link {mensagem} já está em sua área de transferência.\n"
            "Use CTRL+V para colar onde deseja compartilhar..."
        )
    except Exception as e:
        messagebox.showerror("Erro!", f"Mensagem não publicada...\n{e}")


def manual():
    messagebox.showinfo(
        "Manual",
        "PyPost Telegra.ph é uma versão gráfica para o site http://telegra.ph\n\n"
        "1. Preencha com um título\n"
        "2. Crie um nome de usuário (pode ser fictício)\n"
        "3. Escreva o conteúdo (texto simples ou HTML)\n"
        "4. Clique em [Publicar no Telegra.ph]\n\n"
        "O link é gerado e copiado para a área de transferência.\n"
        "Telegra.ph é anônimo, suporta links e embeds do YouTube, Vimeo, Twitter etc.\n\n"
        "Obrigado por usar o PyPost Telegra.ph!"
    )


def limpar():
    autor_var.set("")
    title_var.set("")
    content_text.delete("1.0", tk.END)


def publicar():
    user = autor_var.get()
    title = title_var.get()
    content = content_text.get("1.0", tk.END).strip()
    postar(user, title, content)


def abrir():
    try:
        with open(".temp.txt", "r") as f:
            content_text.delete("1.0", tk.END)
            content_text.insert(tk.END, f.read())
    except FileNotFoundError:
        messagebox.showwarning("Aviso", "Nenhum arquivo temporário encontrado.")


def salvar():
    content = content_text.get("1.0", tk.END)
    with open(".temp.txt", "w") as f:
        f.write(content)
    messagebox.showinfo("Arquivo salvo", "Seu texto foi salvo em '.temp.txt'.")


def copiar():
    content = content_text.get("1.0", tk.END)
    clipboard.copy(content)
    messagebox.showinfo("Copiado", "Texto copiado para a área de transferência.")


def colar():
    copiado = clipboard.paste()
    content_text.insert(tk.END, copiado)


def inserir(tag):
    templates = {
        "Negrito": "<b> Seu texto aqui </b>",
        "Itálico": "<i> Seu texto aqui </i>",
        "Parágrafo": "\n<p> Seu texto aqui </p>\n",
        "Imagem": '\n<p><img src="Link da sua imagem"></p>\n',
        "Link": ' <a href="link da internet">editar este texto</a>',
        "Lista": "\n<p><ol>\n\t<li>Editar esse texto</li>\n</ol></p>\n",
    }
    content_text.insert(tk.END, templates.get(tag, ""))


# ---------------- Interface ----------------
root = tk.Tk()
root.title("PyPost Telegra.ph")
root.geometry("640x480")

# Variáveis
title_var = tk.StringVar()
autor_var = tk.StringVar()

# Menu
menubar = Menu(root)

menu_arquivo = Menu(menubar, tearoff=0)
menu_arquivo.add_command(label="Abrir", command=abrir)
menu_arquivo.add_command(label="Salvar", command=salvar)
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Publicar", command=publicar)
menu_arquivo.add_command(label="Limpar", command=limpar)
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Sair", command=root.quit)
menubar.add_cascade(label="Arquivo", menu=menu_arquivo)

menu_editar = Menu(menubar, tearoff=0)
menu_editar.add_command(label="Copiar", command=copiar)
menu_editar.add_command(label="Colar", command=colar)
menubar.add_cascade(label="Editar", menu=menu_editar)

menu_formatar = Menu(menubar, tearoff=0)
menu_formatar.add_command(label="Negrito", command=lambda: inserir("Negrito"))
menu_formatar.add_command(label="Itálico", command=lambda: inserir("Itálico"))
menubar.add_cascade(label="Formatar", menu=menu_formatar)

menu_inserir = Menu(menubar, tearoff=0)
menu_inserir.add_command(label="Imagem", command=lambda: inserir("Imagem"))
menu_inserir.add_command(label="Link", command=lambda: inserir("Link"))
menu_inserir.add_command(label="Lista", command=lambda: inserir("Lista"))
menu_inserir.add_command(label="Parágrafo", command=lambda: inserir("Parágrafo"))
menubar.add_cascade(label="Inserir", menu=menu_inserir)

menu_ajuda = Menu(menubar, tearoff=0)
menu_ajuda.add_command(label="Manual", command=manual)
menu_ajuda.add_command(label="GitHub", command=lambda: webbrowser.open("https://github.com/elizeubarbosaabreu/PyPost-Telegra.ph.git"))
menu_ajuda.add_command(label="Linkedin", command=lambda: webbrowser.open("https://www.linkedin.com/in/elizeu-barbosa-abreu-69965b218/"))
menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

root.config(menu=menubar)

# Layout
tk.Label(root, text="Título da postagem:").pack(anchor="w")
tk.Entry(root, textvariable=title_var, width=80).pack(fill="x", padx=5, pady=5)

tk.Label(root, text="Autoria (seu nome):").pack(anchor="w")
tk.Entry(root, textvariable=autor_var, width=80).pack(fill="x", padx=5, pady=5)

tk.Label(root, text="Conteúdo (texto simples ou HTML):").pack(anchor="w")
content_text = scrolledtext.ScrolledText(root, width=80, height=15)
content_text.pack(fill="both", expand=True, padx=5, pady=5)

tk.Button(root, text="Publicar no Telegra.ph", font=("Arial", 14), command=publicar).pack(pady=10)

root.mainloop()
