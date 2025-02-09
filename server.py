from flask import Flask, request, jsonify
import time
import base64
import hmac
import hashlib

app = Flask(__name__)

# Configuración
SECRET_KEY = b"ClaveSecretaSuperSegura"
EXPIRATION_TIME = 10 * 60  # 10 minutos

# Función para generar un código
def generar_codigo():
    timestamp = int(time.time() / EXPIRATION_TIME)  # Redondear tiempo
    data = f"{timestamp}:999999".encode()  # Número aleatorio fijo (no se usa en validación)

    # Generar el código HMAC-SHA256
    hash_hmac = hmac.new(SECRET_KEY, data, hashlib.sha256).digest()
    codigo = base64.b64encode(hash_hmac).decode()[:20]

    return codigo

# Ruta para obtener un código nuevo
@app.route('/generar', methods=['GET'])
def obtener_codigo():
    codigo = generar_codigo()
    return jsonify({"codigo": codigo})

# Ruta para validar un código recibido
@app.route('/validar', methods=['POST'])
def validar_codigo():
    datos = request.json
    codigo_recibido = datos.get("codigo")
    user_id = datos.get("usuario")

    if not codigo_recibido or not user_id:
        return jsonify({"error": "Faltan parámetros"}), 400

    timestamp_actual = int(time.time() / EXPIRATION_TIME)

    for i in range(0,1):  # Permitir margen de 1 intervalo antes y después
        timestamp_verificar = timestamp_actual + i
        data = f"{timestamp_verificar}:999999".encode()

        hash_hmac = hmac.new(SECRET_KEY, data, hashlib.sha256).digest()
        codigo_esperado = base64.b64encode(hash_hmac).decode()[:20]

        if codigo_recibido == codigo_esperado:
            return jsonify({"valid": True, "message": f"✅ Código válido. Usuario {user_id}."})

    return jsonify({"valid": False, "message": "❌ Código inválido o expirado."}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)