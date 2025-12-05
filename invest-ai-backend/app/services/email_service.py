import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_email(to_email: str, subject: str, content: str):
        if not settings.EMAIL_SENDER or not settings.EMAIL_PASSWORD:
            logger.warning("Email credentials not set. Skipping email.")
            return

        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_SENDER
        msg['To'] = to_email
        msg['Subject'] = subject

        # Check if content is HTML (rudimentary check) or just send as text/html
        # User said "pode ser texto simples ou HTML básico". 
        # Since the AI returns Markdown/Text, we might want to convert to HTML or just send as plain text.
        # But MIMEText(content, 'html') implies we expect HTML.
        # For now, let's treat it as HTML if it contains tags, otherwise plain. 
        # Actually, let's just use 'html' and wrap in <pre> if it's markdown, or use 'plain' if we want.
        # But the prompt output is Markdown. Sending Markdown as HTML usually requires conversion.
        # For simplicity (Step 2 instructions: "Use MIMEText para enviar o corpo do email"), I will use 'plain' for now 
        # OR wrapping in a simple HTML template if I have time. 
        # User instructions: "Use MIMEText para enviar o corpo do email (pode ser texto simples ou HTML básico por enquanto)."
        
        # Let's send as HTML but formatting newlines if it's plain text structure.
        # A simple approach is converting \n to <br> if we send as HTML.
        
        # However, to support Markdown properly, I should use `markdown` lib like `src/notifier.py` did.
        # "Adapte a classe Notifier..."
        # src/notifier.py imports markdown.
        # I should probably import markdown here too.
        import markdown
        
        html_content = markdown.markdown(content)
        
        # Add a simple wrapper
        html_body = f"""
        <html>
        <body>
            <h2>Sua Análise de Portfólio</h2>
            {html_content}
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))

        try:
            # Gmail SMTP default (can be extracted to settings)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            logger.info(f"Email sent successfully to: {to_email}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise e
