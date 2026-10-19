from flask import Flask, request
from email.message import EmailMessage
import smtplib
import html

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def inicio():
    resultado = ""

    if request.method == "POST":
        destinatario = request.form.get("destinatario", "").strip()
        asunto = request.form.get("asunto", "").strip()
        mensaje = request.form.get("mensaje", "").strip()

        try:
            if not destinatario or not asunto or not mensaje:
                raise ValueError("Completa todos los campos.")

            correo = EmailMessage()
            correo["Subject"] = asunto
            correo["From"] = "prueba@ejemplo.test"
            correo["To"] = destinatario
            correo.set_content(mensaje)

            with smtplib.SMTP("mailpit", 1025, timeout=10) as servidor:
                servidor.send_message(correo)

            resultado = (
                "<p style='color:green'>"
                "¡Correo enviado correctamente a Mailpit!</p>"
                "<p>Destinatario: " + html.escape(destinatario) + "</p>"
            )

        except Exception as error:
            resultado = (
                "<p style='color:red'>No se pudo enviar el correo: "
                + html.escape(str(error)) + "</p>"
            )

    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Prueba de correo - Mailpit</title>
      <style>
        body {font-family:Arial;max-width:600px;margin:40px auto;padding:20px;background:#f2f4f8}
        main {background:white;padding:25px;border-radius:12px}
        input,textarea,button {box-sizing:border-box;width:100%;padding:12px;margin:8px 0 16px}
        button {background:#2563eb;color:white;border:0;border-radius:6px;cursor:pointer}
      </style>
    </head>
    <body>
      <main>
        <h1>Prueba de envío de correo</h1>
        <p>Envía un mensaje de prueba a la bandeja de Mailpit.</p>
        """ + resultado + """
        <form method="POST">
          <label>Correo destinatario:</label>
          <input type="email" name="destinatario" placeholder="alumno@ejemplo.com" required>
          <label>Asunto:</label>
          <input name="asunto" value="Correo de prueba" required>
          <label>Mensaje:</label>
          <textarea name="mensaje" rows="5" required>Este es un correo de prueba enviado desde una aplicación web a Mailpit.</textarea>
          <button type="submit">Enviar correo de prueba</button>
        </form>
        <p>Los mensajes recibidos se pueden consultar en la bandeja de Mailpit.</p>
        <p><a href="https://mailpit.alantrinidad.com">Abrir Mailpit</a></p>
      </main>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
