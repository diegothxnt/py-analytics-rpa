import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnalizadorVentas:
    def __init__(self, archivo_excel):
        self.archivo_excel = archivo_excel
        self.df = None
        self.resultados = {}
    
    def cargar_datos_multiple_hojas(self):
        """
        Carga y combina datos de las 3 hojas del Excel del profesor
        """
        try:
            logger.info(f"Cargando datos desde {self.archivo_excel}")
            
            # Leer las 3 hojas
            df_ventas = pd.read_excel(self.archivo_excel, sheet_name='VENTAS')
            df_vehiculos = pd.read_excel(self.archivo_excel, sheet_name='VEHICULOS')
            df_nuevos = pd.read_excel(self.archivo_excel, sheet_name='NUEVOS REGISTROS')
            
            logger.info(f"VENTAS: {len(df_ventas)} registros")
            logger.info(f"VEHICULOS: {len(df_vehiculos)} registros") 
            logger.info(f"NUEVOS REGISTROS: {len(df_nuevos)} registros")
            
            # Limpiar columnas vacías en VENTAS
            df_ventas = df_ventas.drop(columns=['Unnamed: 13', 'Unnamed: 14'], errors='ignore')
            
            # Combinar VENTAS y NUEVOS REGISTROS (misma estructura)
            df_todas_ventas = pd.concat([df_ventas, df_nuevos], ignore_index=True)
            logger.info(f"Total ventas combinadas: {len(df_todas_ventas)} registros")
            
            # Combinar con información de VEHICULOS
            self.df = self._combinar_con_vehiculos(df_todas_ventas, df_vehiculos)
            
            # Estandarizar nombres de columnas
            self._estandarizar_columnas()
            
            logger.info(f"✅ Datos cargados exitosamente. Total: {len(self.df)} registros")
            logger.info(f"Columnas finales: {list(self.df.columns)}")
            
            return True
                
        except Exception as e:
            logger.error(f"Error al cargar datos múltiples: {str(e)}")
            return False
    
    def _combinar_con_vehiculos(self, df_ventas, df_vehiculos):
        """
        Combina datos de ventas con información de vehículos
        """
        # Renombrar columna para el merge
        df_vehiculos_renamed = df_vehiculos.rename(columns={'ID_Vehiculo': 'ID_Vehículo'})
        
        # Hacer merge para obtener modelo y marca del vehículo
        df_combinado = pd.merge(
            df_ventas, 
            df_vehiculos_renamed[['ID_Vehículo', 'MARCA', 'MODELO', 'TIPO VEHÍCULO', 'AÑO']],
            on='ID_Vehículo', 
            how='left'
        )
        
        logger.info(f"Después de combinar con vehículos: {len(df_combinado)} registros")
        return df_combinado
    
    def _estandarizar_columnas(self):
        """
        Estandariza nombres de columnas al formato esperado por el análisis
        """
        mapeo_columnas = {
            # Columnas del Excel del profesor -> Nombres estandarizados
            'Sede': 'SEDE',
            'MODELO': 'MODELO_VEHICULO', 
            'Canal': 'CANAL_VENTA',
            'Segmento': 'SEGMENTO_CLIENTE',
            'Precio Venta Real': 'PRECIO_VENTA',
            'IGV': 'IGV',
            'Cliente': 'CLIENTE',
            'Precio Venta sin IGV': 'PRECIO_SIN_IGV_ORIGINAL'
        }
        
        # Renombrar columnas
        self.df = self.df.rename(columns=mapeo_columnas)
        
        # Crear MODELO_VEHICULO combinado si no existe
        if 'MODELO_VEHICULO' not in self.df.columns:
            if 'MARCA' in self.df.columns and 'MODELO' in self.df.columns:
                self.df['MODELO_VEHICULO'] = self.df['MARCA'] + ' ' + self.df['MODELO']
            else:
                self.df['MODELO_VEHICULO'] = 'Modelo No Especificado'
    
    def validar_datos(self):
        """
        Valida que los datos tengan las columnas necesarias
        """
        columnas_requeridas = ['SEDE', 'MODELO_VEHICULO', 'CANAL_VENTA', 
                              'SEGMENTO_CLIENTE', 'PRECIO_VENTA', 'IGV', 'CLIENTE']
        
        columnas_faltantes = []
        for columna in columnas_requeridas:
            if columna not in self.df.columns:
                columnas_faltantes.append(columna)
        
        if columnas_faltantes:
            logger.error(f"Columnas requeridas faltantes: {columnas_faltantes}")
            logger.info(f"Columnas disponibles: {list(self.df.columns)}")
            return False
        
        logger.info("✅ Validación de columnas exitosa")
        
        # Mostrar información de los datos
        logger.info(f"📊 Resumen de datos cargados:")
        logger.info(f"   - Total registros: {len(self.df):,}")
        logger.info(f"   - Sedes únicas: {self.df['SEDE'].nunique()}")
        logger.info(f"   - Modelos únicos: {self.df['MODELO_VEHICULO'].nunique()}")
        logger.info(f"   - Canales únicos: {self.df['CANAL_VENTA'].nunique()}")
        logger.info(f"   - Segmentos únicos: {self.df['SEGMENTO_CLIENTE'].nunique()}")
        
        return True

    def calcular_precio_sin_igv(self):
        """
        Calcula el precio de venta sin IGV
        Según el Excel, ya viene 'Precio Venta sin IGV' pero lo calculamos por seguridad
        """
        if 'PRECIO_SIN_IGV_ORIGINAL' in self.df.columns:
            # Usar el valor original del Excel
            self.df['PRECIO_SIN_IGV'] = self.df['PRECIO_SIN_IGV_ORIGINAL']
        else:
            # Calcular restando IGV del precio total
            self.df['PRECIO_SIN_IGV'] = self.df['PRECIO_VENTA'] - self.df['IGV']
        
        logger.info("✅ Precio sin IGV calculado/obtenido")

    # LOS MÉTODOS DE ANÁLISIS SE MANTIENEN IGUAL (pero actualizados para los nuevos datos)
    def analizar_ventas_por_sede(self):
        """Calcula ventas sin IGV por sede"""
        ventas_sede = self.df.groupby('SEDE')['PRECIO_SIN_IGV'].sum().sort_values(ascending=False)
        self.resultados['ventas_por_sede'] = ventas_sede
        logger.info(f"✅ Ventas por sede calculadas: {len(ventas_sede)} sedes")
        return ventas_sede
    
    def top_modelos_vendidos(self, top_n=5):
        """Identifica los modelos más vendidos"""
        top_modelos = self.df['MODELO_VEHICULO'].value_counts().head(top_n)
        self.resultados['top_modelos'] = top_modelos
        logger.info(f"✅ Top {top_n} modelos identificados")
        return top_modelos
    
    def canales_mas_ventas(self):
        """Analiza canales con más ventas"""
        canales_ventas = self.df.groupby('CANAL_VENTA')['PRECIO_SIN_IGV'].sum().sort_values(ascending=False)
        self.resultados['canales_ventas'] = canales_ventas
        logger.info("✅ Canales de ventas analizados")
        return canales_ventas
    
    def segmento_clientes_ventas(self):
        """Analiza segmento de clientes por ventas sin IGV"""
        segmento_ventas = self.df.groupby('SEGMENTO_CLIENTE')['PRECIO_SIN_IGV'].sum()
        self.resultados['segmento_ventas'] = segmento_ventas
        logger.info("✅ Segmento de clientes analizado")
        return segmento_ventas
    
    def metricas_generales(self):
        """Calcula métricas generales del dataset"""
        metricas = {
            'clientes_unicos': self.df['CLIENTE'].nunique(),
            'total_ventas': len(self.df),
            'venta_total_con_igv': self.df['PRECIO_VENTA'].sum(),
            'venta_total_sin_igv': self.df['PRECIO_SIN_IGV'].sum(),
            'igv_total': self.df['IGV'].sum(),
            'sedes_unicas': self.df['SEDE'].nunique(),
            'modelos_unicos': self.df['MODELO_VEHICULO'].nunique()
        }
        self.resultados['metricas'] = metricas
        logger.info("✅ Métricas generales calculadas")
        return metricas

    # MANTENER TODOS LOS MÉTODOS DE GRÁFICOS Y REPORTES (se mantienen igual)
    def generar_graficos(self, carpeta_salida='graficos'):
        """Genera todos los gráficos requeridos"""
        try:
            os.makedirs(carpeta_salida, exist_ok=True)
            
            # Configuración de estilo
            plt.style.use('seaborn-v0_8')
            sns.set_palette("husl")
            
            # 1. Gráfico de barras: Ventas sin IGV por sede
            plt.figure(figsize=(12, 6))
            ventas_sede = self.resultados['ventas_por_sede']
            bars = plt.bar(ventas_sede.index, ventas_sede.values)
            plt.title('Ventas sin IGV por Sede', fontsize=14, fontweight='bold')
            plt.xlabel('Sede', fontweight='bold')
            plt.ylabel('Ventas sin IGV (S/)', fontweight='bold')
            plt.xticks(rotation=45)
            
            # Añadir valores en las barras
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'S/ {height:,.0f}',
                        ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            plt.savefig(f'{carpeta_salida}/ventas_por_sede.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # 2. Gráfico de barras horizontales: Top 5 modelos
            plt.figure(figsize=(10, 6))
            top_modelos = self.resultados['top_modelos']
            bars = plt.barh(range(len(top_modelos)), top_modelos.values)
            plt.yticks(range(len(top_modelos)), [str(x)[:30] + '...' if len(str(x)) > 30 else x for x in top_modelos.index])
            plt.title('Top 5 Modelos Más Vendidos', fontsize=14, fontweight='bold')
            plt.xlabel('Cantidad Vendida', fontweight='bold')
            
            # Añadir valores en las barras
            for i, bar in enumerate(bars):
                width = bar.get_width()
                plt.text(width + 0.1, bar.get_y() + bar.get_height()/2.,
                        f'{int(width)}',
                        ha='left', va='center', fontweight='bold')
            
            plt.tight_layout()
            plt.savefig(f'{carpeta_salida}/top_modelos.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # 3. Gráfico de barras: Canales con más ventas
            plt.figure(figsize=(10, 6))
            canales_ventas = self.resultados['canales_ventas']
            bars = plt.bar(canales_ventas.index, canales_ventas.values)
            plt.title('Ventas por Canal', fontsize=14, fontweight='bold')
            plt.xlabel('Canal de Venta', fontweight='bold')
            plt.ylabel('Ventas sin IGV (S/)', fontweight='bold')
            plt.xticks(rotation=45)
            
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'S/ {height:,.0f}',
                        ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            plt.savefig(f'{carpeta_salida}/canales_ventas.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # 4. Gráfico circular: Segmento de clientes
            plt.figure(figsize=(8, 8))
            segmento_ventas = self.resultados['segmento_ventas']
            colors = plt.cm.Set3(np.linspace(0, 1, len(segmento_ventas)))
            wedges, texts, autotexts = plt.pie(segmento_ventas.values, 
                                             labels=segmento_ventas.index,
                                             autopct='%1.1f%%',
                                             colors=colors,
                                             startangle=90)
            
            plt.title('Distribución de Ventas por Segmento de Cliente', 
                     fontsize=14, fontweight='bold')
            
            # Mejorar la legibilidad
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            plt.tight_layout()
            plt.savefig(f'{carpeta_salida}/segmento_clientes.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # 5. Dashboard resumen
            self._generar_dashboard(carpeta_salida)
            
            logger.info("✅ Todos los gráficos generados exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error al generar gráficos: {str(e)}")
            return False

    def _generar_dashboard(self, carpeta_salida):
        """Genera un dashboard con las métricas clave"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('DASHBOARD RESUMEN - ANÁLISIS DE VENTAS', 
                    fontsize=16, fontweight='bold', y=0.95)
        
        metricas = self.resultados['metricas']
        
        # Métricas clave
        ax1 = axes[0, 0]
        ax1.axis('off')
        texto_metricas = f"""
        MÉTRICAS CLAVE
        
        • Total Ventas: {metricas['total_ventas']:,}
        • Clientes Únicos: {metricas['clientes_unicos']:,}
        • Sedes Únicas: {metricas['sedes_unicas']:,}
        • Modelos Únicos: {metricas['modelos_unicos']:,}
        • Venta Total (sin IGV): S/ {metricas['venta_total_sin_igv']:,.2f}
        • Venta Total (con IGV): S/ {metricas['venta_total_con_igv']:,.2f}
        • IGV Total: S/ {metricas['igv_total']:,.2f}
        """
        ax1.text(0.1, 0.9, texto_metricas, transform=ax1.transAxes, fontsize=12,
                verticalalignment='top', fontfamily='monospace', fontweight='bold')
        
        # Top modelos
        ax2 = axes[0, 1]
        top_modelos = self.resultados['top_modelos']
        ax2.barh(range(len(top_modelos)), top_modelos.values)
        ax2.set_yticks(range(len(top_modelos)))
        ax2.set_yticklabels([str(x)[:20] + '...' if len(str(x)) > 20 else x for x in top_modelos.index])
        ax2.set_title('Top 5 Modelos Más Vendidos', fontweight='bold')
        ax2.set_xlabel('Cantidad Vendida')
        
        # Ventas por sede
        ax3 = axes[1, 0]
        ventas_sede = self.resultados['ventas_por_sede']
        bars = ax3.bar(ventas_sede.index, ventas_sede.values)
        ax3.set_title('Ventas sin IGV por Sede', fontweight='bold')
        ax3.set_ylabel('Ventas sin IGV (S/)')
        ax3.tick_params(axis='x', rotation=45)
        
        # Segmento clientes
        ax4 = axes[1, 1]
        segmento_ventas = self.resultados['segmento_ventas']
        ax4.pie(segmento_ventas.values, labels=segmento_ventas.index, autopct='%1.1f%%')
        ax4.set_title('Ventas por Segmento de Cliente', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{carpeta_salida}/dashboard_resumen.png', dpi=300, bbox_inches='tight')
        plt.close()

    def ejecutar_analisis_completo(self):
        """Ejecuta el análisis completo de los datos"""
        logger.info("🚀 Iniciando análisis completo...")
        
        if not self.cargar_datos_multiple_hojas():
            return False
        
        if not self.validar_datos():
            return False
        
        # Realizar cálculos
        self.calcular_precio_sin_igv()
        self.analizar_ventas_por_sede()
        self.top_modelos_vendidos()
        self.canales_mas_ventas()
        self.segmento_clientes_ventas()
        self.metricas_generales()
        
        # Generar gráficos
        if not self.generar_graficos():
            return False
        
        logger.info("✅ Análisis completado exitosamente")
        return True

    def generar_reporte_texto(self):
        """Genera un reporte en texto con los resultados"""
        if not self.resultados:
            return "No hay resultados disponibles"
        
        metricas = self.resultados['metricas']
        reporte = f"""
        📊 REPORTE DE ANÁLISIS DE VENTAS (Excel del Profesor)
        📅 Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        📈 Datos procesados: {metricas['total_ventas']:,} ventas combinadas
        
        📈 MÉTRICAS GENERALES:
        • Total de Ventas: {metricas['total_ventas']:,}
        • Clientes Únicos: {metricas['clientes_unicos']:,}
        • Sedes Únicas: {metricas['sedes_unicas']:,}
        • Modelos Únicos: {metricas['modelos_unicos']:,}
        • Venta Total sin IGV: S/ {metricas['venta_total_sin_igv']:,.2f}
        • Venta Total con IGV: S/ {metricas['venta_total_con_igv']:,.2f}
        • IGV Total: S/ {metricas['igv_total']:,.2f}
        
        🏢 VENTAS POR SEDE:
        """
        
        for sede, venta in self.resultados['ventas_por_sede'].items():
            reporte += f"  • {sede}: S/ {venta:,.2f}\n"
        
        reporte += "\n🚗 TOP 5 MODELOS MÁS VENDIDOS:\n"
        for modelo, cantidad in self.resultados['top_modelos'].items():
            reporte += f"  • {modelo}: {cantidad} unidades\n"
        
        reporte += "\n📞 CANALES CON MÁS VENTAS:\n"
        for canal, venta in self.resultados['canales_ventas'].items():
            reporte += f"  • {canal}: S/ {venta:,.2f}\n"
        
        return reporte