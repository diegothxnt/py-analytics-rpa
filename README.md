# Py-analytics-rpa
Descripción del Proyecto
Sistema RPA (Robotic Process Automation) desarrollado en Python para el análisis automatizado de datos de ventas vehiculares, generación de reportes estadísticos y envío de resultados por WhatsApp.

🎯 Objetivos
Automatizar el proceso de análisis de datos de ventas

Generar reportes financieros y estadísticos automatizados

Visualizar datos mediante gráficos profesionales

Enviar reportes completos por WhatsApp

🏗️ Arquitectura del Sistema
RPA_Ventas/
│
├── 📊 main.py                 # Script principal de ejecución
├── 🔧 ventas_rpa.py          # Clase principal de análisis
├── 📱 whatsapp_sender.py     # Módulo de envío por WhatsApp
├── 📁 graficos/              # Carpeta de gráficos generados
├── 📄 Ventas Fundamentos.xlsx # Datos fuente (3 hojas)
├── 📋 requirements.txt       # Dependencias del proyecto
└── 🔐 .env                   # Configuración de Twilio (opcional)
🚀 Características Principales
📈 Análisis Automatizado
Carga inteligente de 3 hojas Excel: VENTAS, VEHICULOS, NUEVOS REGISTROS

Procesamiento de 10,000+ registros

Combinación automática de datos relacionados

Validación de integridad de datos

📊 Métricas Calculadas
✅ Precio de ventas sin IGV por sede

✅ Top 5 modelos más vendidos

✅ Canales con más ventas

✅ Segmento de clientes por ventas

✅ Conteo de clientes únicos

✅ Total de ventas (con y sin IGV)

✅ IGV total recaudado

🎨 Visualizaciones Generadas
📊 Gráfico de barras: Ventas por sede

🚗 Gráfico horizontal: Top modelos

📞 Gráfico de barras: Canales de venta

👥 Gráfico circular: Segmento clientes

📈 Dashboard resumen completo

📱 Integración WhatsApp
✅ Envío directo de reportes

✅ Configuración simplificada

✅ Mensajes formateados profesionalmente



🛠️ Instalación y Configuración
*Prerrequisitos
Python 3.8+
Cuenta en Twilio (para WhatsApp)
*Pasos
Instalar dependencias requirements.txt
ejecutar con py main.py



Autor:
Diego Rojas
Universidad Rafael Urdaneta
Proyecto III - Inteligencia Artificial
2025
