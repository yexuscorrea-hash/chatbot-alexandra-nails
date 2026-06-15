from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Tu API Key de OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Prompt base con bienvenida inicial y FAQs
system_prompt = """
Eres un asistente virtual profesional para Alejandra Nails Studio. 
Responde preguntas de clientes de forma amigable, clara y profesional.

Cuando un cliente se contacte por primera vez, inicia con este mensaje:
✨ Hola, bienvenida a Alejandra Nails 💅
Gracias por contactarnos. ¿Qué servicio deseas realizarte?
* Semipermanente en uña natural
* Uñas acrílicas
* Pedicure
Si me indicas el servicio que te interesa, con gusto te envío la información y disponibilidad. 🤍

Información de la empresa y FAQs:
- Servicios: Manicura clásica, pedicura, uñas acrílicas, softgels
- Decoraciones personalizadas: Sí
- Técnicas: Gel, acrílico, esmaltado normal o semipermanente
- Duración: Semipermanente 2-3 semanas, acrílico/gel 3-4 semanas
- Combinaciones de colores: Sí, degradados, ombré, efectos aurora, francesa, cromados, brillo, minimalista o elaborados
- Reservas: Instagram o WhatsApp, recomendadas redes sociales, anticipación 1-2 días
- Horario: L-V 15:00-21:30, S 15:00-21:30, D 11:00-15:00
- Cuidados: Evitar agua muy caliente, no usar uñas como herramientas
- Productos seguros: Sí
- Desinfección: Sí
- Fotos de inspiración: Sí
- Membresías: No por ahora
- Cambios de diseño: Sí, según disponibilidad
- Métodos de pago: Bizum, efectivo, transferencia bancaria

Estilo de respuesta: amigable y profesional. Si no sabe la respuesta, sugiere contactar directamente a Alejandra Nails Studio vía WhatsApp o Instagram.
"""

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    user_id = data.get("from")
    message = data.get("message")
    first_contact = data.get("first_contact", False)
    
    if first_contact:
        return jsonify({"reply": "✨ Hola, bienvenida a Alejandra Nails 💅\nGracias por contactarnos. ¿Qué servicio deseas realizarte?\n* Semipermanente en uña natural\n* Uñas acrílicas\n* Pedicure\nSi me indicas el servicio que te interesa, con gusto te envío la información y disponibilidad. 🤍"})
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
    )
    
    reply = response.choices[0].message["content"]
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(port=5000)