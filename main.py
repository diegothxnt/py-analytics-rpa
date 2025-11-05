"""
RPA para Análisis de Ventas y Envío de Reportes por WhatsApp
Autor: Eli Mora
Universidad Rafael Urdaneta
Proyecto III - Inteligencia Artificial
"""

import os
import sys
import logging
from twilio.rest import Client
from ventas_rpa import AnalizadorVentas
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Credenciales DIRECTAS 
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_WHATSAPP_NUMBER = ""

def generar_reporte_completo(analizador):
    """Genera el reporte completo para WhatsApp"""
    
    metricas = analizador.resultados['metricas']
    ventas_sede = analizador.resultados['ventas_por_sede']
    top_modelos = analizador.resultados['top_modelos']
    canales_ventas = analizador.resultados['canales_ventas']
    
    reporte = f"""📊 REPORTE COMPLETO - ANÁLISIS DE VENTAS 📊
Universidad Rafael Urdaneta
Proyecto III - Inteligencia Artificial

📈 MÉTRICAS PRINCIPALES:
• Clientes Únicos: {metricas['clientes_unicos']}
• Total de Ventas: {metricas['total_ventas']}
• Ventas Totales sin IGV: S/ {metricas['venta_total_sin_igv']:,.2f}
• Ventas Totales con IGV: S/ {metricas['venta_total_con_igv']:,.2f}
• IGV Total Recaudado: S/ {metricas['igv_total']:,.2f}

🏢 VENTAS POR SEDE:
{chr(10).join([f'• {sede}: S/ {venta:,.2f}' for sede, venta in ventas_sede.items()])}

🚗 TOP 5 MODELOS MÁS VENDIDOS:
{chr(10).join([f'• {modelo}: {cantidad} unidades' for modelo, cantidad in top_modelos.items()])}

📞 CANALES CON MÁS VENTAS:
{chr(10).join([f'• {canal}: S/ {venta:,.2f}' for canal, venta in canales_ventas.items()])}

🖼️ ENLACES A GRÁFICOS VISUALES:
• 📊 Ventas por Sede: https://ibb.co/wNJdPR7q
• 🚗 Top Modelos: https://ibb.co/PsqVkGfs
• 📞 Canales de Venta: https://ibb.co/0j2fCFFq
• 👥 Segmento Clientes: https://ibb.co/XfbGjGjc
• 📈 Dashboard Resumen: https://ibb.co/p6XDM8qg

 Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 Autor: Eli Mora

Instrucciones: Haz clic en los enlaces para ver los gráficos detallados."""
    
    return reporte

def enviar_whatsapp_directo(numero_destino, reporte):
    """Envía el reporte por WhatsApp usando Twilio directamente"""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        message = client.messages.create(
            body=reporte,
            from_='whatsapp:' + TWILIO_WHATSAPP_NUMBER,
            to='whatsapp:' + numero_destino
        )
        
        print(f" REPORTE ENVIADO EXITOSAMENTE!")
        print(f" SID: {message.sid}")
        print(" El mensaje llegará en 1-2 minutos...")
        return True
        
    except Exception as e:
        print(f" Error al enviar: {e}")
        return False

def main():
    print(" RPA PARA ANÁLISIS DE VENTAS")
    print("=" * 50)
    print("Universidad Rafael Urdaneta")
    print("Autor: Eli Mora")
    print("Proyecto III - Inteligencia Artificial")
    print("=" * 50)
    
    try:
        # 1. Inicializar analizador
        archivo_excel = "Ventas Fundamentos.xlsx"
        
        if not os.path.exists(archivo_excel):
            print(f" Error: El archivo '{archivo_excel}' no se encuentra")
            print(" Ejecuta primero: py crear_datos_prueba.py")
            return False
        
        print("📊 Inicializando analizador de ventas...")
        analizador = AnalizadorVentas(archivo_excel)
        
        # 2. Ejecutar análisis completo
        print("🔍 Ejecutando análisis completo...")
        if not analizador.ejecutar_analisis_completo():
            print(" El análisis no pudo completarse")
            return False
        
        # 3. Mostrar resultados en consola
        print("\n✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
        print("=" * 50)
        print(analizador.generar_reporte_texto())
        
        # 4. OFRECER ENVÍO POR WHATSAPP
        print("\n📱 ENVÍO POR WHATSAPP")
        print("=" * 50)
        
        enviar_whatsapp = input("¿Deseas enviar el reporte completo por WhatsApp? (s/n): ").lower().strip()
        
        if enviar_whatsapp in ['s', 'si', 'sí', 'yes']:
            numero_destino = input("Ingresa el número de destino (ej: +584127985110): ").strip()
            
            # Generar reporte completo
            reporte_completo = generar_reporte_completo(analizador)
            
            # Enviar directamente (SIN .env, SIN configuración complicada)
            print("📤 Enviando reporte por WhatsApp...")
            enviar_whatsapp_directo(numero_destino, reporte_completo)
        
        # 5. Mostrar archivos generados
        print("\n ARCHIVOS GENERADOS")
        print("=" * 50)
        if os.path.exists('graficos'):
            archivos = os.listdir('graficos')
            for archivo in archivos:
                print(f"• graficos/{archivo}")
        
        print("\n PROCESO COMPLETADO EXITOSAMENTE!")
        return True
        
    except Exception as e:
        print(f" Error durante la ejecución: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)