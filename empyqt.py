import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox
)
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from variaveisambiente import chave


class EmailSenderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurações da janela principal
        self.setWindowTitle("Enviar Email em Massa")
        self.setGeometry(100, 100, 600, 400)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Campo "De"
        self.label_from = QLabel("De:")
        self.entry_from = QLineEdit()
        self.entry_from.setPlaceholderText("Digite o email de origem")
        main_layout.addWidget(self.label_from)
        main_layout.addWidget(self.entry_from)

        # Campo "Para"
        self.label_to = QLabel("Para (separados por vírgula):")
        self.entry_to = QLineEdit()
        self.entry_to.setPlaceholderText("Digite os emails de destino")
        main_layout.addWidget(self.label_to)
        main_layout.addWidget(self.entry_to)

        # Campo "Assunto"
        self.label_subject = QLabel("Assunto:")
        self.entry_subject = QLineEdit()
        self.entry_subject.setPlaceholderText("Digite o assunto do email")
        main_layout.addWidget(self.label_subject)
        main_layout.addWidget(self.entry_subject)

        # Campo "Corpo do Email (HTML)"
        self.label_body = QLabel("Corpo do Email (HTML):")
        self.text_body = QTextEdit()
        self.text_body.setPlaceholderText("Digite o corpo do email em HTML")
        main_layout.addWidget(self.label_body)
        main_layout.addWidget(self.text_body)

        # Botão "Enviar Email"
        self.btn_send = QPushButton("Enviar Email")
        self.btn_send.clicked.connect(self.enviar_email)
        main_layout.addWidget(self.btn_send)

    def enviar_email(self):
        # Coletar os dados da interface gráfica
        from_email = self.entry_from.text()
        to_emails = self.entry_to.text().split(',')  # Assume que os emails são separados por vírgula
        subject = self.entry_subject.text()
        html_content = self.text_body.toPlainText()

        # Validar campos obrigatórios
        if not from_email or not to_emails or not subject or not html_content:
            QMessageBox.warning(self, "Aviso", "Todos os campos são obrigatórios!")
            return

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
                QMessageBox.information(self, "Sucesso", "Email enviado com sucesso!")
            else:
                QMessageBox.critical(self, "Erro", f"Falha ao enviar email. Código de status: {resposta.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao enviar o email: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailSenderApp()
    window.show()
    sys.exit(app.exec())