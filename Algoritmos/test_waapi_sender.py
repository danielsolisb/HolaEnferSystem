#WnEV5GbjbO65S2N5JE6LFabpgMqYgdL85JduOaWj634ddb45
import requests
import json # Para mostrar errores de API en formato JSON si ocurren

# NO necesitas cambiar nada aquí directamente, el script te pedirá los datos.

def send_waapi_message(instance_id, api_token, phone_number_recipient, message_text):
    """
    Envía un mensaje utilizando la API de WaAPI.

    Args:
        instance_id (str): Tu ID de instancia de WaAPI.
        api_token (str): Tu token de API de WaAPI.
        phone_number_recipient (str): Número de teléfono del destinatario 
                                     (ej. para Ecuador: "593991234567").
                                     La función se encargará de añadir "@c.us".
        message_text (str): El mensaje que deseas enviar.

    Returns:
        tuple: (bool, str) donde el bool indica éxito y str es un mensaje de respuesta.
    """
    
    # URL del endpoint para enviar mensajes de WaAPI (confirmada por tu blog)
    waapi_send_url = f"https://waapi.app/api/v1/instances/{instance_id}/client/action/send-message"
    
    # El `chatId` en el payload usualmente requiere el formato numero@c.us
    chat_id = f"{phone_number_recipient}@c.us"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_token}"  # Autenticación tipo Bearer
    }
    
    payload = {
        "chatId": chat_id,
        "message": message_text
    }

    print(f"--- Preparando para enviar a WaAPI ---")
    print(f"URL: {waapi_send_url}")
    print(f"Headers: {{'accept': 'application/json', 'content-type': 'application/json', 'authorization': 'Bearer [REDACTED]'}}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print(f"------------------------------------")

    try:
        # Hacemos la solicitud POST a la API de WaAPI
        response = requests.post(waapi_send_url, json=payload, headers=headers, timeout=30) # Timeout de 30 segundos

        # Revisamos si la solicitud fue exitosa (código de estado HTTP 2xx)
        if 200 <= response.status_code < 300:
            try:
                # Intentamos decodificar la respuesta JSON de WaAPI
                response_data = response.json()
                # Podrías buscar un ID de mensaje aquí si WaAPI lo devuelve:
                # message_api_id = response_data.get('id') 
                # return True, f"Mensaje enviado exitosamente a {phone_number_recipient}. Respuesta de WaAPI: {response_data}"
                return True, f"Solicitud de mensaje enviada a {phone_number_recipient} (HTTP {response.status_code}). Respuesta de WaAPI: {response.text}"
            except json.JSONDecodeError:
                # Si la respuesta no es JSON pero el código es 2xx, igual podría ser un éxito parcial
                return True, f"Solicitud de mensaje enviada a {phone_number_recipient} (HTTP {response.status_code}). Respuesta (no JSON): {response.text}"
        else:
            # Si hay un error HTTP (4xx, 5xx)
            error_message = f"Error al enviar mensaje. Código de estado HTTP: {response.status_code}. Respuesta: {response.text}"
            try:
                # Intentar obtener más detalles del error si la respuesta es JSON
                error_details = response.json()
                error_message += f" Detalles JSON: {error_details}"
            except json.JSONDecodeError:
                pass # Ya tenemos el texto del error
            return False, error_message

    except requests.exceptions.Timeout:
        return False, "Error: La solicitud a WaAPI excedió el tiempo de espera (timeout)."
    except requests.exceptions.RequestException as e:
        # Errores de red, DNS, etc.
        return False, f"Error de conexión o en la solicitud a WaAPI: {e}"
    except Exception as e:
        # Cualquier otro error inesperado
        return False, f"Ocurrió un error inesperado durante el envío: {e}"

def main_terminal_menu():
    """
    Función principal para el menú interactivo en la terminal.
    """
    print("=" * 40)
    print("   Probador de Envío de Mensajes WaAPI   ")
    print("=" * 40)

    # Solicitar credenciales una vez
    instance_id = input("Ingresa tu WAAPI Instance ID: ").strip()
    api_token = input("Ingresa tu WAAPI API Token: ").strip()

    if not instance_id or not api_token:
        print("\nERROR: El Instance ID y el API Token son obligatorios para continuar.")
        print("Por favor, ejecute el script de nuevo y proporcione los datos.")
        return

    print("\n--- Credenciales Recibidas ---")
    # Por seguridad, no mostramos el token completo, solo una parte del ID
    print(f"ID de Instancia: ...{instance_id[-5:] if len(instance_id) > 5 else instance_id}")
    print(f"Token de API: [CONFIGURADO Y GUARDADO]")
    print("-" * 30)
    print("IMPORTANTE:")
    print(" - Asegúrate de que tu instancia de WaAPI esté activa y conectada.")
    print(" - El número de teléfono del destinatario debe ser válido y tener WhatsApp.")
    print(" - Ingresa el número en formato internacional sin el '+' ni espacios.")
    print("   Ejemplo para Ecuador: 593991234567")
    print("   Ejemplo para México: 521XXXXXXXXXX (incluyendo el '1' después del código de país si es celular)")
    print("   Ejemplo para EE.UU.: 1XXXXXXXXXX")
    print("-" * 30)

    while True:
        print("\nOpciones del Menú:")
        print("  1. Enviar un mensaje de prueba")
        print("  2. Actualizar credenciales de WaAPI")
        print("  3. Salir")
        
        choice = input("Selecciona una opción (1-3): ").strip()

        if choice == '1':
            phone_to = input("Número de teléfono del destinatario: ").strip()
            message_to_send = input("Mensaje a enviar: ")

            if not phone_to or not message_to_send:
                print("\nERROR: El número de teléfono y el mensaje no pueden estar vacíos.")
                continue
            
            print(f"\nIntentando enviar mensaje a '{phone_to}'...")
            success, response_message = send_waapi_message(instance_id, api_token, phone_to, message_to_send)
            
            if success:
                print("\n✅ MENSAJE PROCESADO POR WAAPI:")
                print(response_message)
            else:
                print("\n❌ ERROR EN EL ENVÍO:")
                print(response_message)
            print("-" * 20)

        elif choice == '2':
            print("\n--- Actualizar Credenciales ---")
            instance_id_new = input(f"Nuevo WAAPI Instance ID (actual: ...{instance_id[-5:] if len(instance_id) > 5 else instance_id}): ").strip()
            api_token_new = input(f"Nuevo WAAPI API Token (actual: [CONFIGURADO]): ").strip()
            if instance_id_new:
                instance_id = instance_id_new
            if api_token_new:
                api_token = api_token_new
            print("Credenciales actualizadas.")
            print(f"ID de Instancia: ...{instance_id[-5:] if len(instance_id) > 5 else instance_id}")
            print(f"Token de API: [CONFIGURADO Y GUARDADO]")
            print("-" * 30)

        elif choice == '3':
            print("\nSaliendo del probador de WaAPI. ¡Hasta pronto!")
            break
        else:
            print("\nOpción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    # Verificar si la biblioteca 'requests' está instalada
    try:
        import requests
    except ImportError:
        print("Error: La biblioteca 'requests' es necesaria para ejecutar este script.")
        print("Por favor, instálala ejecutando en tu terminal:")
        print("pip install requests")
        # Si estás usando un entorno virtual, asegúrate de que esté activado.
        exit() # Salir si 'requests' no está disponible
        
    main_terminal_menu()