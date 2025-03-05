import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from variaveisambiente import chave
import tkinter as tk
from tkinter import messagebox

# Função para enviar o email
def enviar_email():
    # Coletar os dados da interface gráfica
    from_email = entry_from.get()
    to_emails = entry_to.get().split(',')  # Assume que os emails são separados por vírgula
    subject = entry_subject.get()
    html_content = text_body.get("1.0", tk.END)

    # Criar o objeto Mail
    email = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content
    )

    # Enviar o email
    try:
        contaSendGrid = SendGridAPIClient(chave)
        resposta = contaSendGrid.send(email)
        if resposta.status_code == 202:
            messagebox.showinfo("Sucesso", "Email enviado com sucesso!")
        else:
            messagebox.showerror("Erro", f"Falha ao enviar email. Código de status: {resposta.status_code}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao enviar o email: {str(e)}")

# Criar a interface gráfica
root = tk.Tk()
root.title("Enviar Email em Massa")

# Campos de entrada
tk.Label(root, text="De:").grid(row=0, column=0, padx=10, pady=10)
entry_from = tk.Entry(root, width=50)
entry_from.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Para (separados por vírgula):").grid(row=1, column=0, padx=10, pady=10)
entry_to = tk.Entry(root, width=50)
entry_to.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Assunto:").grid(row=2, column=0, padx=10, pady=10)
entry_subject = tk.Entry(root, width=50)
entry_subject.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Corpo do Email (HTML):").grid(row=3, column=0, padx=10, pady=10)
text_body = tk.Text(root, width=50, height=10)
text_body.grid(row=3, column=1, padx=10, pady=10)

# Botão para enviar o email
btn_enviar = tk.Button(root, text="Enviar Email", command=enviar_email)
btn_enviar.grid(row=4, column=1, padx=10, pady=10)

# Iniciar a interface gráfica
root.mainloop()