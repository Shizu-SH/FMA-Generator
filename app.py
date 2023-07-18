from flask import Flask, render_template, request, jsonify
import random
from faker import Faker
import smtplib

app = Flask(__name__)
fake = Faker()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        serie = request.form['bin']
        num_resultados = int(request.form['num_resultados'])

        resultados = []
        for _ in range(num_resultados):
            numeros_faltantes = 16 - len(serie)
            numeros_aleatorios = ''.join(str(random.randint(0, 9)) for _ in range(numeros_faltantes))

            mes_caducidad = request.form['mes_caducidad']
            anio_caducidad = request.form['anio_caducidad']
            if not mes_caducidad or not anio_caducidad:
                mes_caducidad = str(random.randint(1, 12)).zfill(2)
                anio_caducidad = str(random.randint(23, 30)).zfill(2)

            digitos_seguridad = request.form['digitos_seguridad']
            if not digitos_seguridad:
                digitos_seguridad = str(random.randint(0, 999)).zfill(3)

            resultado = serie + numeros_aleatorios + '|' + mes_caducidad + '|' + anio_caducidad + '|' + digitos_seguridad

            resultados.append(resultado)

        return render_template('result.html', resultados=resultados)

    return render_template('index.html')

@app.route('/tempmail')
def tempmail():
    return render_template('tempmail.html')

@app.route('/fakegenerator')
def fakegenerator():
    return render_template('fakegenerator.html')

@app.route('/generate', methods=['POST'])
def generate_email():
    email = f'user{random.randint(1000, 9999)}@example.com'  # Generar un correo temporal aleatorio
    return jsonify({'email': email})

@app.route('/sms', methods=['POST'])
def receive_sms():
    sms = request.form['sms']  # Obtener el SMS recibido desde el formulario
    # Aquí puedes agregar la lógica para guardar el SMS en una base de datos o hacer cualquier otro procesamiento necesario
    return jsonify({'success': True})

@app.route('/fake', methods=['GET'])
def generate_fake_data():
    country = request.args.get('country')  # Obtener el país desde la consulta en la URL
    fake_data = generate_fake_data_for_country(country)  # Generar los datos falsos para el país
    return render_template('fake.html', country=country, fake_data=fake_data)

@app.route('/creditcard', methods=['GET'])
def generate_fake_credit_card():
    credit_card = fake.credit_card_number()  # Generar un número de tarjeta de crédito falso
    return jsonify({'credit_card': credit_card})

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/enviar_correo', methods=['POST'])
def enviar_correo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        mensaje = request.form['mensaje']

        # Configura el servidor SMTP y las credenciales
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = 'facundoagostini.m@gmail.com'  # Cambia esto por tu dirección de correo
        sender_password = 'Facu20081014'  # Cambia esto por tu contraseña de correo

        # Crea el mensaje de correo
        subject = 'Nuevo mensaje de contacto'
        body = f"Nombre: {nombre}\nApellido: {apellido}\nCorreo electrónico: {correo}\nMensaje:\n{mensaje}"
        message = f'Subject: {subject}\n\n{body}'

        try:
            # Inicia la conexión SMTP y envía el correo
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, sender_email, message)

            # Devuelve una respuesta exitosa
            return '¡Gracias por contactarnos! Tu mensaje ha sido enviado.'
        except Exception as e:
            # Devuelve un mensaje de error en caso de que falle el envío del correo
            return f'Ha ocurrido un error al enviar el mensaje. Por favor, inténtalo nuevamente. Error: {str(e)}'


def generate_fake_data_for_country(country):
    # Agrega la lógica para generar los datos falsos según el país seleccionado
    if country == 'us':
        fake_data = {
            'name': fake.name(),
            'address': fake.address(),
            'phone': fake.phone_number(),
            'email': fake.email(),
            'birthdate': fake.date_of_birth().strftime('%Y-%m-%d'),
            'ssn': fake.ssn(),
            'credit_card': fake.credit_card_number()
        }
    elif country == 'uk':
        fake_data = {
            'name': fake.name(),
            'address': fake.address(),
            'phone': fake.phone_number(),
            'email': fake.email(),
            'birthdate': fake.date_of_birth().strftime('%Y-%m-%d'),
            'national_insurance': fake.numerify('AA 00 00 00 A'),
            'credit_card': fake.credit_card_number()
        }
    elif country == 'ar':
        fake_data = {
            'name': fake.name(),
            'address': fake.address(),
            'phone': fake.phone_number(),
            'email': fake.email(),
            'birthdate': fake.date_of_birth().strftime('%Y-%m-%d'),
            'national_insurance': fake.numerify('AA 00 00 00 A'),
            'credit_card': fake.credit_card_number()
        }
    elif country == 'au':
        fake_data = {
            'name': fake.name(),
            'address': fake.address(),
            'phone': fake.phone_number(),
            'email': fake.email(),
            'birthdate': fake.date_of_birth().strftime('%Y-%m-%d'),
            'national_insurance': fake.numerify('AA 00 00 00 A'),
            'credit_card': fake.credit_card_number()
        }
    else:
        fake_data = {}  # Define los datos falsos para otros países aquí

    return fake_data

if __name__ == '__main__':
    app.run(debug=True)
