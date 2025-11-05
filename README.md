# Py-analytics-rpa
Sistema RPA (Robotic Process Automation) desarrollado en Python para el análisis automatizado de datos de ventas vehiculares, generación de reportes estadísticos y envío de resultados completos por WhatsApp con imágenes integradas.

🎯 Objetivos
✅ Automatizar el proceso de análisis de datos de ventas

✅ Generar reportes financieros y estadísticos automatizados

✅ Visualizar datos mediante gráficos profesionales

✅ Enviar reportes completos por WhatsApp con texto e imágenes

🏗️ Arquitectura del Sistema
text
RPA_Ventas/
│
├── 📊 main.py                 # Script principal de ejecución
├── 🔧 ventas_rpa.py          # Clase principal de análisis
├── 📱 whatsapp_sender.py     # Módulo de envío por WhatsApp
├── 🖼️ img_uploader.py        # Upload automático de imágenes
├── 📁 graficos/              # Carpeta de gráficos generados
├── 📄 Ventas Fundamentos.xlsx # Datos fuente (3 hojas)
├── 📋 requirements.txt       # Dependencias del proyecto
└── 🔐 .env                   # Configuración de Twilio (opcional)
🚀 Características Principales
📈 Análisis Automatizado
Carga inteligente de 3 hojas Excel: VENTAS, VEHICULOS, NUEVOS REGISTROS

Procesamiento de 10,000+ registros sin problemas de rendimiento

Combinación automática de datos relacionados entre hojas

Validación de integridad de datos con reportes detallados

📊 Métricas Calculadas
Métrica	Descripción
✅ Precio de ventas sin IGV por sede	Distribución geográfica de ventas netas
✅ Top 5 modelos más vendidos	Popularidad de vehículos por unidades
✅ Canales con más ventas	Efectividad de canales de marketing
✅ Segmento de clientes por ventas	Comportamiento por tipo de cliente
✅ Conteo de clientes únicos	Base de clientes activos
✅ Total de ventas (con y sin IGV)	Volumen de negocio total
✅ IGV total recaudado	Impacto impositivo
🎨 Visualizaciones Generadas
📊 Gráfico de barras: Ventas por sede

🚗 Gráfico horizontal: Top modelos más vendidos

📞 Gráfico de barras: Canales de venta

👥 Gráfico circular: Segmento clientes

📈 Dashboard resumen: Vista general completa

📱 Integración WhatsApp Avanzada
✅ Envío directo de reportes con formato profesional

✅ Imágenes integradas en el mismo hilo de conversación

✅ Configuración simplificada sin complicaciones

✅ Subida automática a servidores cloud (ImgBB)

✅ Mensajes secuenciales con descripciones detalladas

🛠️ Instalación y Configuración
Prerrequisitos
Python 3.8+

Cuenta en Twilio (para funcionalidad WhatsApp)

API Key de ImgBB (gratuita, para envío de imágenes)
