import os
from twilio.rest import Client
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)

class WhatsAppSender:
    def __init__(self):
        # Cargar .env explícitamente
        from dotenv import load_dotenv
        load_dotenv()
        
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
        
        if not all([self.account_sid, self.auth_token, self.twilio_whatsapp_number]):
            logger.warning("Credenciales de Twilio no encontradas. El envío por WhatsApp no funcionará.")
            self.client = None
        else:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                logger.info("Cliente de Twilio inicializado correctamente")
            except Exception as e:
                logger.error(f"Error al inicializar Twilio: {str(e)}")
                self.client = None
    
    def enviar_mensaje(self, destino, mensaje):
        """
        Envía un mensaje de texto por WhatsApp
        
        Args:
            destino (str): Número de destino en formato WhatsApp (ej: whatsapp:+1234567890)
            mensaje (str): Mensaje a enviar
            
        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        if not self.client:
            logger.error("Cliente de Twilio no disponible")
            return False
        
        try:
            message = self.client.messages.create(
                body=mensaje,
                from_=self.twilio_whatsapp_number,
                to=f'whatsapp:{destino}'
            )
            logger.info(f"Mensaje enviado exitosamente. SID: {message.sid}")
            return True
        except Exception as e:
            logger.error(f"Error al enviar mensaje: {str(e)}")
            return False
    
    def enviar_imagen(self, destino, url_imagen, mensaje=""):
        """
        Envía una imagen por WhatsApp
        
        Args:
            destino (str): Número de destino
            url_imagen (str): URL de la imagen a enviar
            mensaje (str): Mensaje acompañante
            
        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        if not self.client:
            logger.error("Cliente de Twilio no disponible")
            return False
        
        try:
            message = self.client.messages.create(
                body=mensaje,
                from_=self.twilio_whatsapp_number,
                media_url=[url_imagen],
                to=f'whatsapp:{destino}'
            )
            logger.info(f"Imagen enviada exitosamente. SID: {message.sid}")
            return True
        except Exception as e:
            logger.error(f"Error al enviar imagen: {str(e)}")
            return False
    
    def enviar_reporte_completo(self, destino, analizador, servidor_web=None):
        """
        Envía un reporte completo por WhatsApp
        
        Args:
            destino (str): Número de destino
            analizador (AnalizadorVentas): Instancia del analizador con resultados
            servidor_web (str): URL base para acceder a las imágenes (opcional)
            
        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        if not self.client:
            logger.error("Cliente de Twilio no disponible")
            return False
        
        try:
            # Enviar reporte de texto
            reporte_texto = analizador.generar_reporte_texto()
            if not self.enviar_mensaje(destino, reporte_texto):
                return False
            
            # Si hay servidor web configurado, enviar imágenes
            if servidor_web:
                imagenes = [
                    'graficos/ventas_por_sede.png',
                    'graficos/top_modelos.png',
                    'graficos/canales_ventas.png',
                    'graficos/segmento_clientes.png',
                    'graficos/dashboard_resumen.png'
                ]
                
                mensajes_imagenes = [
                    "📊 Ventas por Sede",
                    "🚗 Top 5 Modelos Más Vendidos",
                    "📞 Canales de Venta",
                    "👥 Segmento de Clientes",
                    "📈 Dashboard Resumen"
                ]
                
                for i, imagen in enumerate(imagenes):
                    if os.path.exists(imagen):
                        url_imagen = f"{servidor_web}/{imagen}"
                        self.enviar_imagen(destino, url_imagen, mensajes_imagenes[i])
            
            logger.info("Reporte completo enviado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error al enviar reporte completo: {str(e)}")
            return False

# Función de utilidad para configurar Twilio
def configurar_twilio():
    """
    Guía al usuario para configurar Twilio
    """
    print("🔧 Configuración de Twilio para WhatsApp")
    print("=" * 50)
    
    if not os.path.exists('.env'):
        print("Creando archivo .env...")
        
        account_sid = input("Ingresa tu TWILIO_ACCOUNT_SID: ")
        auth_token = input("Ingresa tu TWILIO_AUTH_TOKEN: ")
        whatsapp_number = input("Ingresa tu TWILIO_WHATSAPP_NUMBER (ej: +1234242): ")
        
        with open('.env', 'w') as f:
            f.write(f"TWILIO_ACCOUNT_SID={account_sid}\n")
            f.write(f"TWILIO_AUTH_TOKEN={auth_token}\n")
            f.write(f"TWILIO_WHATSAPP_NUMBER={whatsapp_number}\n")
        
        print("✅ Archivo .env creado exitosamente")
    else:
        print("✅ Archivo .env ya existe")