from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.popup import Popup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from variaveisambiente import chave


class EmailSenderApp(App):
    def build(self):
        # Configuração da janela principal
        Window.clearcolor = (0.9, 0.9, 0.9, 1)  # Cor de fundo
        self.title = "Enviar Email em Massa"

        # Layout principal
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Campo "De"
        layout.add_widget(Label(text="De:", size_hint_y=None, height=30))
        self.entry_from = TextInput(hint_text="Digite o email de origem", multiline=False)
        layout.add_widget(self.entry_from)

        # Campo "Para"
        layout.add_widget(Label(text="Para (separados por vírgula):", size_hint_y=None, height=30))
        self.entry_to = TextInput(hint_text="Digite os emails de destino", multiline=False)
        layout.add_widget(self.entry_to)

        # Campo "Assunto"
        layout.add_widget(Label(text="Assunto:", size_hint_y=None, height=30))
        self.entry_subject = TextInput(hint_text="Digite o assunto do email", multiline=False)
        layout.add_widget(self.entry_subject)

        # Campo "Corpo do Email (HTML)"
        layout.add_widget(Label(text="Corpo do Email (HTML):", size_hint_y=None, height=30))
        self.text_body = TextInput(hint_text="Digite o corpo do email em HTML", multiline=True)
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, 200))
        scroll_view.add_widget(self.text_body)
        layout.add_widget(scroll_view)

        # Botão "Enviar Email"
        self.btn_send = Button(text="Enviar Email", size_hint_y=None, height=50)
        self.btn_send.bind(on_press=self.enviar_email)
        layout.add_widget(self.btn_send)

        return layout

    def enviar_email(self, instance):
        # Coletar os dados da interface gráfica
        from_email = self.entry_from.text
        to_emails = self.entry_to.text.split(',')  # Assume que os emails são separados por vírgula
        subject = self.entry_subject.text
        html_content = self.text_body.text

        # Validar campos obrigatórios
        if not from_email or not to_emails or not subject or not html_content:
            self.mostrar_popup("Aviso", "Todos os campos são obrigatórios!")
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
                self.mostrar_popup("Sucesso", "Email enviado com sucesso!")
            else:
                self.mostrar_popup("Erro", f"Falha ao enviar email. Código de status: {resposta.status_code}")
        except Exception as e:
            self.mostrar_popup("Erro", f"Ocorreu um erro ao enviar o email: {str(e)}")

    def mostrar_popup(self, titulo, mensagem):
        # Exibir um popup com uma mensagem
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        popup_label = Label(text=mensagem, size_hint_y=None, height=50)
        popup_button = Button(text="Fechar", size_hint_y=None, height=50)
        popup = Popup(title=titulo, content=popup_layout, size_hint=(0.8, 0.4))

        popup_button.bind(on_press=popup.dismiss)
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)
        popup.open()


if __name__ == "__main__":
    EmailSenderApp().run()