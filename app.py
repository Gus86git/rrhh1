import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Importaciones para gráficos avanzados
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

# Configuración de página
st.set_page_config(
    page_title="RRHH Analytics Pro",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados mejorados
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .alert-high {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #ff4757;
    }
    .alert-medium {
        background: linear-gradient(135deg, #ffd93d 0%, #ffcd3c 100%);
        color: black;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #ff9f1a;
    }
    .alert-low {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #219a52;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
        background: linear-gradient(90deg, #3498db, transparent);
        padding-left: 1rem;
    }
    .employee-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3498db;
    }
    .apto-card {
        border-left: 4px solid #2ecc71 !important;
    }
    .no-apto-card {
        border-left: 4px solid #e74c3c !important;
    }
    .manual-section {
        background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .project-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3498db;
    }
    .risk-high {
        border-left: 4px solid #e74c3c !important;
    }
    .risk-medium {
        border-left: 4px solid #f39c12 !important;
    }
    .risk-low {
        border-left: 4px solid #2ecc71 !important;
    }
    .description-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .efectivo-card {
        border-left: 4px solid #3498db !important;
    }
    .contratado-card {
        border-left: 4px solid #9b59b6 !important;
    }
    .manual-title {
        color: #2c3e50;
        font-size: 2.2rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .manual-description {
        background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
</style>
""", unsafe_allow_html=True)

def generar_datos_financieros_demo(df_obras):
    """Generar datos financieros de demostración completos"""
    gastos_beneficios = []
    
    conceptos_gastos = ['Materiales', 'Mano de Obra', 'Equipos', 'Logística', 'Administrativo']
    conceptos_beneficios = ['Avance de Obra', 'Eficiencia', 'Ahorro Materiales', 'Bonos Calidad', 'Incentivos']
    
    for obra in df_obras.to_dict('records'):
        # Generar gastos
        for _ in range(np.random.randint(8, 20)):
            gastos_beneficios.append({
                'obra_id': obra['id'],
                'tipo': 'Gasto',
                'concepto': np.random.choice(conceptos_gastos),
                'monto': np.random.uniform(5000, 150000),
                'fecha': datetime.now() - timedelta(days=np.random.randint(1, 180)),
                'descripcion': f"Gasto en {np.random.choice(conceptos_gastos)} para {obra['nombre']}",
                'categoria': 'Operativo' if np.random.random() > 0.3 else 'Administrativo'
            })
        
        # Generar beneficios
        for _ in range(np.random.randint(5, 15)):
            gastos_beneficios.append({
                'obra_id': obra['id'],
                'tipo': 'Beneficio',
                'concepto': np.random.choice(conceptos_beneficios),
                'monto': np.random.uniform(10000, 200000),
                'fecha': datetime.now() - timedelta(days=np.random.randint(1, 180)),
                'descripcion': f"Beneficio por {np.random.choice(conceptos_beneficios)} en {obra['nombre']}",
                'categoria': 'Ingreso'
            })
    
    return pd.DataFrame(gastos_beneficios)

@st.cache_data
def load_data():
    """Generar datos sintéticos completos para la demo"""
    np.random.seed(42)
    
    # Generar empleados con criterios de aptitud
    nombres = ['Sofia', 'Martina', 'Lucia', 'Ana', 'Carolina', 'Valentina', 
               'Carlos', 'Diego', 'Juan', 'Pablo', 'Ricardo', 'Javier', 
               'Miguel', 'Roberto', 'Fernando', 'Laura', 'Gabriela', 'Mariana']
    apellidos = ['Lopez', 'Gonzalez', 'Garcia', 'Martinez', 'Rodriguez', 
                 'Perez', 'Diaz', 'Gomez', 'Fernandez', 'Romero', 'Silva', 'Torres']
    
    # Especialidades por departamento
    especialidades = {
        'Albañilería': ['Albañil Maestro', 'Ayudante Albañil', 'Enfoscador', 'Colocador Cerámico'],
        'Electricidad': ['Electricista Industrial', 'Electricista Residencial', 'Técnico Electrónico'],
        'Plomería': ['Instalador Sanitario', 'Gasista Matriculado', 'Técnico HVAC'],
        'Herrería': ['Soldador Especializado', 'Herrero Estructural', 'Calderero'],
        'Pintura': ['Pintor Industrial', 'Pintor Decorativo', 'Aplicador Especializado']
    }
    
    certificaciones = {
        'Albañilería': ['Hormigón Armado', 'Encofrados', 'Seguridad en Altura'],
        'Electricidad': ['AT1', 'BT', 'Instalaciones MT', 'Automatización'],
        'Plomería': ['Gasista Matriculado', 'Termofusión', 'Sistemas HVAC'],
        'Herrería': ['Soldadura TIG', 'Soldadura MIG', 'Estructuras Metálicas'],
        'Pintura': ['Pintura Epoxi', 'Anticorrosivos', 'Texturas']
    }
    
    # Nuevas entidades basadas en el DER
    areas = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
    ciudades = ['Buenos Aires', 'Córdoba', 'Rosario', 'Mendoza', 'Tucumán', 'La Plata']
    puestos = ['Operario', 'Supervisor', 'Coordinador', 'Gerente', 'Director']
    rubros = ['Mano de Obra', 'Materiales', 'Equipos', 'Logística', 'Administrativo']
    
    # Consultoras con CUIT y nombre
    consultoras = [
        {'cuit': '30-61234568-9', 'nombre': 'Adecco Argentina S.R.L.'},
        {'cuit': '30-51234567-8', 'nombre': 'Manpower Argentina S.A.'},
        {'cuit': '30-71199762-4', 'nombre': 'Nexo Group Assistance S.R.L.'},
        {'cuit': '30-71609500-9', 'nombre': 'AP Soluciones en RRHH'},
        {'cuit': '30-70048023-9', 'nombre': 'Randstad Argentina S.A.'}
    ]
    
    empleados = []
    for i in range(200):
        genero = np.random.choice(['Femenino', 'Masculino'], p=[0.35, 0.65])
        dept = np.random.choice(['Albañilería', 'Electricidad', 'Plomería', 'Herrería', 'Pintura'], 
                               p=[0.3, 0.25, 0.2, 0.15, 0.1])
        
        # Determinar si es efectivo o contratado (70% efectivos, 30% contratados)
        tipo_empleado = np.random.choice(['efectivo', 'contratado'], p=[0.7, 0.3])
        
        if tipo_empleado == 'efectivo':
            # Salarios base por departamento para efectivos
            salario_base = {
                'Albañilería': 80000, 'Electricidad': 95000, 
                'Plomería': 85000, 'Herrería': 110000, 'Pintura': 75000
            }[dept]
            salario = salario_base * np.random.uniform(0.8, 1.5)
            precio_hora_comun = None
            precio_hora_extra = None
            consultora = None
            cuit_consultora = None
        else:
            # Precios por hora para contratados
            precio_base_hora = {
                'Albañilería': 1200, 'Electricidad': 1500, 
                'Plomería': 1300, 'Herrería': 1800, 'Pintura': 1100
            }[dept]
            precio_hora_comun = precio_base_hora * np.random.uniform(0.9, 1.3)
            precio_hora_extra = precio_hora_comun * 1.5
            salario = None
            consultora_info = np.random.choice(consultoras)
            consultora = consultora_info['nombre']
            cuit_consultora = consultora_info['cuit']
        
        experiencia = np.random.randint(6, 180)
        edad = np.random.randint(22, 60)
        
        # Determinar aptitud para obra compleja
        apto_obra_compleja = (
            (experiencia > 24) and 
            (np.random.random() > 0.3) and
            (edad >= 25 and edad <= 55)
        )
        
        # Certificaciones
        certs_disponibles = certificaciones[dept]
        num_certs = np.random.randint(1, min(4, len(certs_disponibles) + 1))
        certificaciones_empleado = np.random.choice(certs_disponibles, num_certs, replace=False)
        
        empleados.append({
            'id': f"EMP{i+1:03d}",
            'numero_legajo': f"LG{i+1:05d}",
            'nombre': np.random.choice(nombres),
            'apellido': np.random.choice(apellidos),
            'tipo_empleado': tipo_empleado,
            'genero': genero,
            'edad': edad,
            'departamento': dept,
            'especialidad': np.random.choice(especialidades[dept]),
            'cargo': f"{dept} {'Senior' if experiencia > 60 else 'Junior' if experiencia > 24 else 'Aprendiz'}",
            'salario': round(salario, 2) if salario else None,
            'precio_hora_comun': round(precio_hora_comun, 2) if precio_hora_comun else None,
            'precio_hora_extra': round(precio_hora_extra, 2) if precio_hora_extra else None,
            'consultora': consultora,
            'cuit_consultora': cuit_consultora,
            'fecha_contratacion': datetime.now() - timedelta(days=np.random.randint(30, 365*5)),
            'experiencia_meses': experiencia,
            'ubicacion': np.random.choice(['Sede Central', 'Obra Norte', 'Obra Sur', 'Obra Este', 'Obra Oeste']),
            'nivel_educacion': np.random.choice(['Secundario', 'Terciario', 'Universitario', 'Maestría'], 
                                              p=[0.4, 0.3, 0.2, 0.1]),
            'certificaciones': ', '.join(certificaciones_empleado),
            'apto_obra_compleja': apto_obra_compleja,
            'disponible_viaje': np.random.choice([True, False], p=[0.7, 0.3]),
            'vehiculo_propio': np.random.choice([True, False], p=[0.6, 0.4]),
            'activo': np.random.choice([True, False], p=[0.92, 0.08]),
            'evaluacion_desempeno': np.random.normal(85, 10),
            'ausencias_ultimo_mes': np.random.poisson(1.5),
            # Nuevos campos basados en el DER
            'area': np.random.choice(areas),
            'ciudad': np.random.choice(ciudades),
            'puesto': np.random.choice(puestos)
        })
    
    df_empleados = pd.DataFrame(empleados)
    df_empleados['evaluacion_desempeno'] = df_empleados['evaluacion_desempeno'].clip(50, 100)
    
    # Generar obras con requisitos específicos
    obras = []
    tipos_obra = ['Residencial', 'Comercial', 'Industrial', 'Infraestructura', 'Institucional']
    
    for i in range(15):
        tipo_obra = np.random.choice(tipos_obra)
        complejidad = np.random.choice(['Baja', 'Media', 'Alta'], p=[0.3, 0.5, 0.2])
        
        # Requisitos basados en tipo y complejidad
        requisitos = {
            'Residencial': {'apto_obra_compleja': False, 'exp_minima': 12},
            'Comercial': {'apto_obra_compleja': complejidad != 'Baja', 'exp_minima': 24},
            'Industrial': {'apto_obra_compleja': True, 'exp_minima': 36},
            'Infraestructura': {'apto_obra_compleja': True, 'exp_minima': 48},
            'Institucional': {'apto_obra_compleja': complejidad == 'Alta', 'exp_minima': 24}
        }[tipo_obra]
        
        obras.append({
            'id': f"OBR{i+1:03d}",
            'nombre': f"Proyecto {tipo_obra} {i+1}",
            'tipo': tipo_obra,
            'ubicacion': np.random.choice(['Nordelta', 'Pilar', 'Tigre', 'Escobar', 'San Isidro', 'Belgrano', 'Palermo']),
            'presupuesto': np.random.randint(5000000, 30000000),
            'fecha_inicio': datetime.now() - timedelta(days=np.random.randint(30, 400)),
            'duracion_estimada': np.random.randint(90, 540),
            'estado': np.random.choice(['En Planificación', 'En Progreso', 'En Riesgo', 'Completado', 'Pausado'], 
                                     p=[0.1, 0.5, 0.15, 0.1, 0.15]),
            'gerente': np.random.choice([f"{emp['nombre']} {emp['apellido']}" for emp in empleados[:25]]),
            'complejidad': complejidad,
            'requiere_apto_obra_compleja': requisitos['apto_obra_compleja'],
            'experiencia_minima_meses': requisitos['exp_minima'],
            'requiere_vehiculo': np.random.choice([True, False], p=[0.6, 0.4]),
            'zona_riesgo': np.random.choice([True, False], p=[0.3, 0.7])
        })
    
    df_obras = pd.DataFrame(obras)
    
    # Generar asistencias y rendimiento
    asistencias = []
    for _ in range(3000):
        emp_idx = np.random.randint(0, len(empleados))
        emp = empleados[emp_idx]
        obra_idx = np.random.randint(0, len(obras))
        obra = obras[obra_idx]
        
        fecha = datetime.now() - timedelta(days=np.random.randint(1, 180))
        
        # Calcular productividad basada en aptitud y experiencia
        productividad_base = np.random.normal(85, 10)
        if emp['apto_obra_compleja'] and obra['requiere_apto_obra_compleja']:
            productividad_base += 5
        if emp['experiencia_meses'] >= obra['experiencia_minima_meses']:
            productividad_base += 3
        
        horas_trabajadas = np.random.randint(6, 10)
        horas_extra = np.random.choice([0, 0, 0, 1, 2, 3], p=[0.4, 0.2, 0.15, 0.15, 0.07, 0.03])
        
        asistencias.append({
            'empleado_id': emp['id'],
            'obra_id': obra['id'],
            'fecha': fecha,
            'horas_trabajadas': horas_trabajadas,
            'horas_extra': horas_extra,
            'productividad': productividad_base,
            'calidad_trabajo': np.random.normal(90, 5),
            'incidentes_seguridad': np.random.poisson(0.05),
            'ausente': np.random.choice([True, False], p=[0.03, 0.97]),
            'rubro': np.random.choice(rubros)
        })
    
    df_asistencias = pd.DataFrame(asistencias)
    df_asistencias['productividad'] = df_asistencias['productividad'].clip(50, 100)
    df_asistencias['calidad_trabajo'] = df_asistencias['calidad_trabajo'].clip(70, 100)
    
    # Generar datos de rotación personal
    rotacion_data = []
    for dept in df_empleados['departamento'].unique():
        for area in areas:
            for ciudad in ciudades:
                for puesto in puestos:
                    rotacion_data.append({
                        'departamento': dept,
                        'area': area,
                        'ciudad': ciudad,
                        'puesto': puesto,
                        'rotacion_mensual': np.random.uniform(0.01, 0.15),
                        'empleados_salidos': np.random.randint(0, 5),
                        'costo_rotacion': np.random.uniform(10000, 50000)
                    })
    
    df_rotacion = pd.DataFrame(rotacion_data)
    
    # Generar datos de gastos y beneficios usando la nueva función
    df_gastos_beneficios = generar_datos_financieros_demo(obras)
    
    return df_empleados, df_obras, df_asistencias, df_rotacion, df_gastos_beneficios

def create_advanced_plotly_chart(data, title, chart_type='bar', **kwargs):
    """Función avanzada para crear gráficos Plotly con estilo Power BI"""
    try:
        if chart_type == 'sunburst':
            fig = px.sunburst(data, **kwargs)
        elif chart_type == 'treemap':
            fig = px.treemap(data, **kwargs)
        elif chart_type == 'violin':
            fig = px.violin(data, **kwargs)
        elif chart_type == 'density_heatmap':
            fig = px.density_heatmap(data, **kwargs)
        elif chart_type == 'parallel_categories':
            fig = px.parallel_categories(data, **kwargs)
        elif chart_type == 'funnel':
            fig = px.funnel(data, **kwargs)
        elif chart_type == 'waterfall':
            fig = go.Figure(go.Waterfall(**kwargs))
        elif chart_type == 'indicator':
            fig = go.Figure(go.Indicator(**kwargs))
        else:
            # Usar plotly express para tipos básicos
            if chart_type == 'bar':
                fig = px.bar(data, **kwargs)
            elif chart_type == 'pie':
                fig = px.pie(data, **kwargs)
            elif chart_type == 'scatter':
                fig = px.scatter(data, **kwargs)
            elif chart_type == 'line':
                fig = px.line(data, **kwargs)
            elif chart_type == 'histogram':
                fig = px.histogram(data, **kwargs)
            elif chart_type == 'box':
                fig = px.box(data, **kwargs)
            else:
                fig = px.bar(data, **kwargs)
        
        # Estilo Power BI
        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                xanchor='center',
                font=dict(size=20, color='#2c3e50')
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50'),
            height=400,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creando gráfico {title}: {str(e)}")
        return None

def main():
    # Header principal
    st.markdown('<h1 class="main-header">🏗️ RRHH Analytics Pro</h1>', unsafe_allow_html=True)
    
    # Cargar datos
    df_empleados, df_obras, df_asistencias, df_rotacion, df_gastos_beneficios = load_data()
    
    # Sidebar - Navegación
    st.sidebar.title("🏢 RRHH Analytics Pro")
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio(
        "📋 Módulos:",
        ["📊 Dashboard Ejecutivo", "👥 Gestión de Personal", "🏗️ Gestión de Obras", 
         "🎯 Aptitud para Obras", "📈 Analytics Avanzado", "⚠️ Alertas", 
         "💰 Análisis Financiero", "🔄 Rotación Personal", "📖 Manual del Dashboard", "⚙️ Configuración"]
    )
    
    # KPIs Principales - Siempre visibles
    st.markdown("### 📈 Métricas Clave en Tiempo Real")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_empleados = len(df_empleados[df_empleados['activo']])
        st.metric("👥 Empleados Activos", total_empleados, delta="+5%")
    
    with col2:
        aptos_obra_compleja = len(df_empleados[(df_empleados['activo']) & (df_empleados['apto_obra_compleja'])])
        st.metric("✅ Aptos Obra Compleja", aptos_obra_compleja, delta="+8%")
    
    with col3:
        productividad_promedio = df_asistencias['productividad'].mean()
        st.metric("📊 Productividad", f"{productividad_promedio:.1f}%", delta="+2.1%")
    
    with col4:
        rotacion = len(df_empleados[~df_empleados['activo']]) / len(df_empleados) * 100
        st.metric("🔄 Rotación", f"{rotacion:.1f}%", delta="-1.2%", delta_color="inverse")
    
    with col5:
        obras_activas = len(df_obras[df_obras['estado'] == 'En Progreso'])
        st.metric("🏗️ Obras Activas", obras_activas)
    
    st.markdown("---")
    
    # Contenido según menú seleccionado
    if menu == "📊 Dashboard Ejecutivo":
        show_executive_dashboard(df_empleados, df_obras, df_asistencias, df_rotacion, df_gastos_beneficios)
    elif menu == "👥 Gestión de Personal":
        show_person_management(df_empleados, df_asistencias)
    elif menu == "🏗️ Gestión de Obras":
        show_project_management(df_obras, df_asistencias, df_empleados)
    elif menu == "🎯 Aptitud para Obras":
        show_aptitude_analysis(df_empleados, df_obras)
    elif menu == "📈 Analytics Avanzado":
        show_advanced_analytics(df_empleados, df_asistencias)
    elif menu == "⚠️ Alertas":
        show_early_warnings(df_empleados, df_obras, df_asistencias)
    elif menu == "💰 Análisis Financiero":
        show_financial_analysis(df_gastos_beneficios, df_obras, df_empleados)
    elif menu == "🔄 Rotación Personal":
        show_turnover_analysis(df_rotacion, df_empleados)
    elif menu == "📖 Manual del Dashboard":
        show_dashboard_manual()
    elif menu == "⚙️ Configuración":
        show_configuration()

def show_executive_dashboard(df_empleados, df_obras, df_asistencias, df_rotacion, df_gastos_beneficios):
    st.markdown('<div class="section-header">📊 Dashboard Ejecutivo - Vista Power BI</div>', unsafe_allow_html=True)
    
    # Descripción General con mejor contraste
    st.markdown("""
    <div class="description-box">
    <h3 style='color: white; margin: 0;'>🎯 Descripción General</h3>
    <p style='color: white; font-size: 1.1rem; margin: 0.5rem 0 0 0;'>
    El <strong>RRHH Analytics Pro</strong> es un sistema integral de gestión de recursos humanos diseñado para la industria de la construcción. 
    Combina análisis avanzados, visualizaciones interactivas y herramientas de gestión para optimizar la fuerza laboral.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Primera fila - Métricas estratégicas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Calcular costo total considerando ambos tipos de empleados
        costo_efectivos = df_empleados[(df_empleados['activo']) & (df_empleados['tipo_empleado'] == 'efectivo')]['salario'].sum()
        
        # Para contratados, calcular costo basado en horas trabajadas
        asistencias_contratados = df_asistencias.merge(
            df_empleados[df_empleados['tipo_empleado'] == 'contratado'], 
            left_on='empleado_id', right_on='id'
        )
        costo_contratados = (
            asistencias_contratados['horas_trabajadas'] * asistencias_contratados['precio_hora_comun'] +
            asistencias_contratados['horas_extra'] * asistencias_contratados['precio_hora_extra']
        ).sum()
        
        costo_total = costo_efectivos + costo_contratados
        st.metric("💰 Costo Nómina Mensual", f"${costo_total:,.0f}")
    
    with col2:
        horas_extra_totales = df_asistencias['horas_extra'].sum()
        st.metric("⏰ Horas Extra Acumuladas", f"{horas_extra_totales} h")
    
    with col3:
        ausentismo_promedio = df_empleados['ausencias_ultimo_mes'].mean()
        st.metric("🏥 Ausentismo Promedio", f"{ausentismo_promedio:.1f} días")
    
    with col4:
        evaluacion_promedio = df_empleados['evaluacion_desempeno'].mean()
        st.metric("⭐ Evaluación Desempeño", f"{evaluacion_promedio:.1f}%")
    
    # Segunda fila - Gráficos avanzados
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 Distribución por Tipo de Empleado")
        
        # Gráfico de distribución por tipo de empleado
        tipo_dist = df_empleados[df_empleados['activo']]['tipo_empleado'].value_counts()
        fig = px.pie(
            values=tipo_dist.values,
            names=tipo_dist.index,
            title='Distribución de Empleados por Tipo',
            color=tipo_dist.index,
            color_discrete_map={'efectivo': '#3498db', 'contratado': '#9b59b6'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏢 Empleados por Consultora")
        
        # Gráfico de empleados por consultora
        consultora_data = df_empleados[df_empleados['tipo_empleado'] == 'contratado']
        if not consultora_data.empty:
            consultora_dist = consultora_data.groupby(['consultora', 'cuit_consultora']).size().reset_index(name='count')
            consultora_dist['etiqueta'] = consultora_dist['consultora'] + '<br>' + consultora_dist['cuit_consultora']
            
            fig = px.bar(
                consultora_dist,
                x='etiqueta',
                y='count',
                title='Empleados Contratados por Consultora',
                labels={'etiqueta': 'Consultora', 'count': 'Cantidad de Empleados'},
                color='count',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay empleados contratados para mostrar")
    
    # Tercera fila - Más visualizaciones
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎻 Distribución Salarial - Violin Plot")
        
        # Filtrar solo empleados efectivos para el gráfico de salarios
        empleados_efectivos = df_empleados[(df_empleados['activo']) & (df_empleados['tipo_empleado'] == 'efectivo')]
        if not empleados_efectivos.empty:
            fig = px.violin(
                empleados_efectivos,
                x='departamento',
                y='salario',
                title='Distribución Salarial por Departamento',
                color='departamento',
                box=True
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay empleados efectivos para mostrar")
    
    with col2:
        st.subheader("📈 Tendencia Temporal - Productividad")
        
        df_asistencias['fecha'] = pd.to_datetime(df_asistencias['fecha'])
        df_asistencias['mes'] = df_asistencias['fecha'].dt.to_period('M').astype(str)
        
        productividad_mensual = df_asistencias.groupby('mes')['productividad'].mean().reset_index()
        
        fig = px.line(
            productividad_mensual,
            x='mes',
            y='productividad',
            title='Evolución Mensual de Productividad',
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)

def show_person_management(df_empleados, df_asistencias):
    st.markdown('<div class="section-header">👥 Gestión de Personal</div>', unsafe_allow_html=True)
    
    # Filtros
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        dept_filter = st.selectbox(
            "🏢 Departamento",
            options=['Todos'] + df_empleados['departamento'].unique().tolist()
        )
    
    with col2:
        tipo_filter = st.selectbox(
            "👤 Tipo Empleado",
            options=['Todos', 'efectivo', 'contratado']
        )
    
    with col3:
        estado_filter = st.selectbox(
            "✅ Estado",
            options=['Todos', 'Activos', 'Inactivos']
        )
    
    with col4:
        aptitud_filter = st.selectbox(
            "🎯 Aptitud Obra Compleja",
            options=['Todos', 'Aptos', 'No Aptos']
        )
    
    # Aplicar filtros
    filtered_employees = df_empleados.copy()
    
    if dept_filter != 'Todos':
        filtered_employees = filtered_employees[filtered_employees['departamento'] == dept_filter]
    
    if tipo_filter != 'Todos':
        filtered_employees = filtered_employees[filtered_employees['tipo_empleado'] == tipo_filter]
    
    if estado_filter == 'Activos':
        filtered_employees = filtered_employees[filtered_employees['activo'] == True]
    elif estado_filter == 'Inactivos':
        filtered_employees = filtered_employees[filtered_employees['activo'] == False]
    
    if aptitud_filter == 'Aptos':
        filtered_employees = filtered_employees[filtered_employees['apto_obra_compleja'] == True]
    elif aptitud_filter == 'No Aptos':
        filtered_employees = filtered_employees[filtered_employees['apto_obra_compleja'] == False]
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total Filtrado", len(filtered_employees))
    
    with col2:
        # Calcular compensación promedio según tipo
        if tipo_filter == 'efectivo' or tipo_filter == 'Todos':
            avg_comp = filtered_employees['salario'].mean()
            st.metric("💰 Compensación Promedio", f"${avg_comp:,.0f}" if not pd.isna(avg_comp) else "N/A")
        else:
            avg_hora = filtered_employees['precio_hora_comun'].mean()
            st.metric("💰 Precio Hora Promedio", f"${avg_hora:,.0f}" if not pd.isna(avg_hora) else "N/A")
    
    with col3:
        avg_experience = filtered_employees['experiencia_meses'].mean()
        st.metric("📅 Experiencia Promedio", f"{avg_experience:.0f} meses")
    
    with col4:
        avg_performance = filtered_employees['evaluacion_desempeno'].mean()
        st.metric("⭐ Desempeño Promedio", f"{avg_performance:.1f}%")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribución por departamento
        dept_dist = filtered_employees['departamento'].value_counts()
        fig = px.pie(
            values=dept_dist.values,
            names=dept_dist.index,
            title='Distribución por Departamento'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Compensación vs Experiencia
        fig_data = filtered_employees.copy()
        if 'efectivo' in fig_data['tipo_empleado'].unique():
            fig_data.loc[fig_data['tipo_empleado'] == 'efectivo', 'compensacion'] = fig_data['salario']
        if 'contratado' in fig_data['tipo_empleado'].unique():
            fig_data.loc[fig_data['tipo_empleado'] == 'contratado', 'compensacion'] = fig_data['precio_hora_comun'] * 160  # Aprox mensual
        
        fig = px.scatter(
            fig_data,
            x='experiencia_meses',
            y='compensacion',
            color='tipo_empleado',
            title='Compensación vs Experiencia por Tipo',
            size='evaluacion_desempeno',
            hover_data=['nombre', 'apellido'],
            color_discrete_map={'efectivo': '#3498db', 'contratado': '#9b59b6'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar empleados con tarjetas diferenciadas
    st.subheader("📋 Detalle de Empleados")
    
    for _, emp in filtered_employees.iterrows():
        card_class = "efectivo-card" if emp['tipo_empleado'] == 'efectivo' else "contratado-card"
        
        st.markdown(f'<div class="employee-card {card_class}">', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        
        with col1:
            st.write(f"**{emp['nombre']} {emp['apellido']}**")
            st.write(f"*{emp['especialidad']} - {emp['departamento']}*")
            st.write(f"📅 Exp: {emp['experiencia_meses']} meses | 🎂 Edad: {emp['edad']} años")
            st.write(f"🔹 **Tipo:** {emp['tipo_empleado'].title()}")
        
        with col2:
            st.write(f"📊 Evaluación: {emp['evaluacion_desempeno']:.1f}%")
            st.write(f"🎓 Certificaciones: {emp['certificaciones']}")
            if emp['tipo_empleado'] == 'efectivo':
                st.write(f"💰 Salario: ${emp['salario']:,.0f}")
            else:
                st.write(f"💰 Precio Hora: ${emp['precio_hora_comun']:,.0f}")
                st.write(f"🏢 Consultora: {emp['consultora']}")
        
        with col3:
            aptitud_color = "🟢" if emp['apto_obra_compleja'] else "🔴"
            st.write(f"**{aptitud_color} Obra Compleja**")
            st.write(f"🚗 Vehículo: {'✅ Sí' if emp['vehiculo_propio'] else '❌ No'}")
        
        with col4:
            status_color = "🟢" if emp['activo'] else "🔴"
            st.write(f"**{status_color} {'ACTIVO' if emp['activo'] else 'INACTIVO'}**")
            if st.button("📋 Ver Detalles", key=f"detalles_{emp['id']}"):
                st.session_state[f"show_emp_details_{emp['id']}"] = True
        
        # Mostrar detalles expandidos
        if st.session_state.get(f"show_emp_details_{emp['id']}", False):
            st.info(f"Detalles completos de {emp['nombre']} {emp['apellido']}")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Legajo:** {emp['numero_legajo']}")
                st.write(f"**Área:** {emp['area']}")
                st.write(f"**Ciudad:** {emp['ciudad']}")
                st.write(f"**Puesto:** {emp['puesto']}")
            with col2:
                st.write(f"**Fecha Contratación:** {emp['fecha_contratacion'].strftime('%d/%m/%Y')}")
                st.write(f"**Disponible Viaje:** {'✅ Sí' if emp['disponible_viaje'] else '❌ No'}")
                st.write(f"**Ausencias último mes:** {emp['ausencias_ultimo_mes']}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_project_management(df_obras, df_asistencias, df_empleados):
    st.markdown('<div class="section-header">🏗️ Gestión de Obras</div>', unsafe_allow_html=True)
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        estado_filter = st.selectbox(
            "📊 Estado Obra",
            options=['Todos'] + df_obras['estado'].unique().tolist(),
            key="estado_obra"
        )
    
    with col2:
        tipo_filter = st.selectbox(
            "🏢 Tipo Obra",
            options=['Todos'] + df_obras['tipo'].unique().tolist()
        )
    
    with col3:
        complejidad_filter = st.selectbox(
            "⚡ Complejidad",
            options=['Todos'] + df_obras['complejidad'].unique().tolist()
        )
    
    # Aplicar filtros
    filtered_projects = df_obras.copy()
    
    if estado_filter != 'Todos':
        filtered_projects = filtered_projects[filtered_projects['estado'] == estado_filter]
    
    if tipo_filter != 'Todos':
        filtered_projects = filtered_projects[filtered_projects['tipo'] == tipo_filter]
    
    if complejidad_filter != 'Todos':
        filtered_projects = filtered_projects[filtered_projects['complejidad'] == complejidad_filter]
    
    # Métricas de obras
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_presupuesto = filtered_projects['presupuesto'].sum()
        st.metric("💰 Presupuesto Total", f"${total_presupuesto:,.0f}")
    
    with col2:
        obras_en_progreso = len(filtered_projects[filtered_projects['estado'] == 'En Progreso'])
        st.metric("🏗️ Obras en Progreso", obras_en_progreso)
    
    with col3:
        obras_en_riesgo = len(filtered_projects[filtered_projects['estado'] == 'En Riesgo'])
        st.metric("⚠️ Obras en Riesgo", obras_en_riesgo)
    
    with col4:
        avg_duration = filtered_projects['duracion_estimada'].mean()
        st.metric("📅 Duración Promedio", f"{avg_duration:.0f} días")
    
    # Mostrar obras como tarjetas
    st.subheader("📋 Detalle de Obras")
    
    for _, obra in filtered_projects.iterrows():
        # Determinar clase de riesgo
        if obra['estado'] == 'En Riesgo':
            risk_class = "risk-high"
        elif obra['estado'] == 'En Progreso':
            risk_class = "risk-medium"
        else:
            risk_class = "risk-low"
        
        st.markdown(f'<div class="project-card {risk_class}">', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        
        with col1:
            st.write(f"### {obra['nombre']}")
            st.write(f"**Ubicación:** {obra['ubicacion']} | **Gerente:** {obra['gerente']}")
            st.write(f"**Tipo:** {obra['tipo']} | **Complejidad:** {obra['complejidad']}")
        
        with col2:
            st.write(f"**Presupuesto:** ${obra['presupuesto']:,.0f}")
            st.write(f"**Duración:** {obra['duracion_estimada']} días")
            st.write(f"**Inicio:** {obra['fecha_inicio'].strftime('%d/%m/%Y')}")
        
        with col3:
            st.write(f"**Estado:** {obra['estado']}")
            st.write(f"**Apto Compleja:** {'✅' if obra['requiere_apto_obra_compleja'] else '❌'}")
            st.write(f"**Exp. Mínima:** {obra['experiencia_minima_meses']} meses")
        
        with col4:
            status_color = {
                'En Planificación': '🟡',
                'En Progreso': '🟢',
                'En Riesgo': '🔴',
                'Completado': '🔵',
                'Pausado': '🟠'
            }[obra['estado']]
            st.write(f"### {status_color}")
            
            if st.button("📊 Detalles", key=f"detalles_{obra['id']}"):
                st.session_state[f"show_details_{obra['id']}"] = True
        
        # Mostrar detalles si se hace clic
        if st.session_state.get(f"show_details_{obra['id']}", False):
            st.info(f"Detalles completos de {obra['nombre']}")
            # Aquí podrías mostrar más información específica de la obra
    
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Gráficos de análisis de obras
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribución de presupuesto por tipo
        fig = px.bar(
            filtered_projects.groupby('tipo')['presupuesto'].sum().reset_index(),
            x='tipo',
            y='presupuesto',
            title='Presupuesto por Tipo de Obra',
            color='tipo'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Estado de obras
        estado_counts = filtered_projects['estado'].value_counts()
        fig = px.pie(
            values=estado_counts.values,
            names=estado_counts.index,
            title='Distribución de Estados de Obras'
        )
        st.plotly_chart(fig, use_container_width=True)

def show_aptitude_analysis(df_empleados, df_obras):
    st.markdown('<div class="section-header">🎯 Análisis de Aptitud para Obras</div>', unsafe_allow_html=True)
    
    # Filtros para análisis de aptitud
    col1, col2, col3 = st.columns(3)
    
    with col1:
        obra_seleccionada = st.selectbox(
            "🏗️ Seleccionar Obra para Análisis",
            options=df_obras['nombre'].tolist(),
            index=0
        )
    
    with col2:
        departamento_filtro = st.selectbox(
            "🏢 Departamento",
            options=['Todos'] + df_empleados['departamento'].unique().tolist(),
            index=0
        )
    
    with col3:
        aptitud_filtro = st.selectbox(
            "✅ Estado Aptitud",
            options=['Todos', 'Aptos', 'No Aptos'],
            index=0
        )
    
    # Obtener datos de la obra seleccionada
    obra_info = df_obras[df_obras['nombre'] == obra_seleccionada].iloc[0]
    
    # Mostrar requisitos de la obra
    st.subheader(f"📋 Requisitos de la Obra: {obra_info['nombre']}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info(f"**Tipo:** {obra_info['tipo']}")
        st.info(f"**Complejidad:** {obra_info['complejidad']}")
    
    with col2:
        st.info(f"**Apto Obra Compleja:** {'✅ Sí' if obra_info['requiere_apto_obra_compleja'] else '❌ No'}")
        st.info(f"**Exp. Mínima:** {obra_info['experiencia_minima_meses']} meses")
    
    with col3:
        st.info(f"**Vehículo Requerido:** {'✅ Sí' if obra_info['requiere_vehiculo'] else '❌ No'}")
        st.info(f"**Zona de Riesgo:** {'⚠️ Sí' if obra_info['zona_riesgo'] else '✅ No'}")
    
    with col4:
        st.info(f"**Ubicación:** {obra_info['ubicacion']}")
        st.info(f"**Presupuesto:** ${obra_info['presupuesto']:,.0f}")
    
    # Filtrar empleados según aptitud
    empleados_filtrados = df_empleados[df_empleados['activo']].copy()
    
    if departamento_filtro != 'Todos':
        empleados_filtrados = empleados_filtrados[empleados_filtrados['departamento'] == departamento_filtro]
    
    # Calcular aptitud para la obra seleccionada
    def calcular_aptitud(empleado, obra):
        criterios_cumplidos = 0
        criterios_totales = 4
        
        # Criterio 1: Aptitud para obra compleja
        if not obra['requiere_apto_obra_compleja'] or empleado['apto_obra_compleja']:
            criterios_cumplidos += 1
        
        # Criterio 2: Experiencia mínima
        if empleado['experiencia_meses'] >= obra['experiencia_minima_meses']:
            criterios_cumplidos += 1
        
        # Criterio 3: Vehículo propio (si se requiere)
        if not obra['requiere_vehiculo'] or empleado['vehiculo_propio']:
            criterios_cumplidos += 1
        
        # Criterio 4: Evaluación de desempeño
        if empleado['evaluacion_desempeno'] >= 70:
            criterios_cumplidos += 1
        
        porcentaje_aptitud = (criterios_cumplidos / criterios_totales) * 100
        return porcentaje_aptitud, criterios_cumplidos
    
    # Aplicar cálculo de aptitud
    aptitudes = []
    for _, emp in empleados_filtrados.iterrows():
        aptitud, criterios = calcular_aptitud(emp, obra_info)
        aptitudes.append({
            'empleado': emp,
            'porcentaje_aptitud': aptitud,
            'criterios_cumplidos': criterios,
            'apto': aptitud >= 75
        })
    
    # Filtrar por aptitud si se seleccionó
    if aptitud_filtro == 'Aptos':
        aptitudes = [apt for apt in aptitudes if apt['apto']]
    elif aptitud_filtro == 'No Aptos':
        aptitudes = [apt for apt in aptitudes if not apt['apto']]
    
    # Mostrar resultados
    st.subheader(f"👥 Empleados {aptitud_filtro} - {len(aptitudes)} encontrados")
    
    # Métricas de aptitud
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_aptos = sum(1 for apt in aptitudes if apt['apto'])
        st.metric("✅ Total Aptos", total_aptos)
    
    with col2:
        aptitud_promedio = np.mean([apt['porcentaje_aptitud'] for apt in aptitudes])
        st.metric("📊 Aptitud Promedio", f"{aptitud_promedio:.1f}%")
    
    with col3:
        criterios_promedio = np.mean([apt['criterios_cumplidos'] for apt in aptitudes])
        st.metric("🎯 Criterios Cumplidos", f"{criterios_promedio:.1f}/4")
    
    with col4:
        porcentaje_aptos = (total_aptos / len(aptitudes)) * 100 if aptitudes else 0
        st.metric("📈 % de Aptos", f"{porcentaje_aptos:.1f}%")
    
    # Mostrar empleados con tarjetas
    st.subheader("📋 Detalle de Empleados")
    
    for aptitud in aptitudes:
        emp = aptitud['empleado']
        card_class = "apto-card" if aptitud['apto'] else "no-apto-card"
        
        st.markdown(f'<div class="employee-card {card_class}">', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        
        with col1:
            st.write(f"**{emp['nombre']} {emp['apellido']}**")
            st.write(f"*{emp['especialidad']} - {emp['departamento']}*")
            st.write(f"📅 Exp: {emp['experiencia_meses']} meses | 🎂 Edad: {emp['edad']} años")
            st.write(f"🔹 **Tipo:** {emp['tipo_empleado'].title()}")
        
        with col2:
            st.write(f"📊 Evaluación: {emp['evaluacion_desempeno']:.1f}%")
            st.write(f"🎓 Certificaciones: {emp['certificaciones']}")
            st.write(f"🚗 Vehículo: {'✅ Sí' if emp['vehiculo_propio'] else '❌ No'}")
        
        with col3:
            aptitud_color = "🟢" if aptitud['apto'] else "🔴"
            st.write(f"**{aptitud_color} Aptitud: {aptitud['porcentaje_aptitud']:.0f}%**")
            st.write(f"✅ {aptitud['criterios_cumplidos']}/4 criterios")
        
        with col4:
            if aptitud['apto']:
                st.success("**APTO**")
                if st.button("📋 Asignar", key=f"asignar_{emp['id']}"):
                    st.success(f"✅ {emp['nombre']} asignado a {obra_seleccionada}")
            else:
                st.error("**NO APTO**")
                st.button("📋 Asignar", key=f"asignar_{emp['id']}", disabled=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Gráfico de distribución de aptitud
    if aptitudes:
        st.subheader("📊 Análisis de Aptitud")
        
        aptitud_data = pd.DataFrame([{
            'Aptitud': apt['porcentaje_aptitud'],
            'Departamento': apt['empleado']['departamento'],
            'Apto': 'Apto' if apt['apto'] else 'No Apto'
        } for apt in aptitudes])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(
                aptitud_data,
                x='Aptitud',
                color='Apto',
                title='Distribución de Niveles de Aptitud',
                nbins=20,
                color_discrete_map={'Apto': '#2ecc71', 'No Apto': '#e74c3c'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            dept_aptitud = aptitud_data.groupby('Departamento')['Aptitud'].mean().reset_index()
            fig = px.bar(
                dept_aptitud,
                x='Departamento',
                y='Aptitud',
                title='Aptitud Promedio por Departamento',
                color='Aptitud',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig, use_container_width=True)

def show_advanced_analytics(df_empleados, df_asistencias):
    st.markdown('<div class="section-header">📈 Analytics Avanzado</div>', unsafe_allow_html=True)
    
    # Análisis predictivo de rotación
    st.subheader("🔮 Predicción de Rotación")
    
    # Simular análisis predictivo
    df_analytics = df_empleados[df_empleados['activo']].copy()
    
    # Crear características para el modelo (simulado)
    df_analytics['riesgo_rotacion'] = np.random.normal(0.3, 0.2, len(df_analytics))
    df_analytics['riesgo_rotacion'] = df_analytics['riesgo_rotacion'].clip(0, 1)
    
    # Clasificar riesgo
    def clasificar_riesgo(score):
        if score > 0.7:
            return 'Alto'
        elif score > 0.4:
            return 'Medio'
        else:
            return 'Bajo'
    
    df_analytics['nivel_riesgo'] = df_analytics['riesgo_rotacion'].apply(clasificar_riesgo)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        alto_riesgo = len(df_analytics[df_analytics['nivel_riesgo'] == 'Alto'])
        st.metric("🔴 Alto Riesgo", alto_riesgo)
    
    with col2:
        medio_riesgo = len(df_analytics[df_analytics['nivel_riesgo'] == 'Medio'])
        st.metric("🟡 Medio Riesgo", medio_riesgo)
    
    with col3:
        bajo_riesgo = len(df_analytics[df_analytics['nivel_riesgo'] == 'Bajo'])
        st.metric("🟢 Bajo Riesgo", bajo_riesgo)
    
    # Gráficos de análisis avanzado
    col1, col2 = st.columns(2)
    
    with col1:
        # Matriz de correlación
        numeric_cols = ['edad', 'experiencia_meses', 'evaluacion_desempeno', 'ausencias_ultimo_mes']
        
        # Filtrar solo columnas numéricas que existen
        available_numeric_cols = [col for col in numeric_cols if col in df_analytics.columns]
        
        if len(available_numeric_cols) >= 2:
            corr_matrix = df_analytics[available_numeric_cols].corr()
            
            fig = px.imshow(
                corr_matrix,
                title='Matriz de Correlación entre Variables',
                color_continuous_scale='RdBu_r',
                aspect='auto'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay suficientes datos numéricos para la matriz de correlación")
    
    with col2:
        # Segmentación por desempeño y potencial - CORREGIDO
        # Crear una columna de compensación unificada
        df_analytics['compensacion'] = df_analytics.apply(
            lambda x: x['salario'] if pd.notna(x['salario']) else (x['precio_hora_comun'] * 160 if pd.notna(x['precio_hora_comun']) else 0), 
            axis=1
        )
        
        # Filtrar datos válidos
        scatter_data = df_analytics[
            (df_analytics['evaluacion_desempeno'].notna()) & 
            (df_analytics['experiencia_meses'].notna()) &
            (df_analytics['compensacion'] > 0)
        ]
        
        if not scatter_data.empty:
            fig = px.scatter(
                scatter_data,
                x='evaluacion_desempeno',
                y='experiencia_meses',
                color='nivel_riesgo',
                size='compensacion',
                title='Segmentación: Desempeño vs Experiencia',
                hover_data=['nombre', 'apellido', 'departamento'],
                color_discrete_sequence=['red', 'orange', 'green']
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos suficientes para el gráfico de segmentación")
    
    # Análisis de clusters
    st.subheader("🎯 Segmentación Avanzada")
    
    # Simular clusters
    df_analytics['cluster'] = np.random.choice(['A - Alto Potencial', 'B - Estables', 'C - Necesitan Soporte'], 
                                              len(df_analytics), p=[0.2, 0.6, 0.2])
    
    col1, col2 = st.columns(2)
    
    with col1:
        cluster_counts = df_analytics['cluster'].value_counts()
        fig = px.bar(
            x=cluster_counts.index,
            y=cluster_counts.values,
            title='Distribución de Segmentos',
            color=cluster_counts.index,
            labels={'x': 'Segmento', 'y': 'Cantidad'},
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Análisis de composición salarial por segmento - CORREGIDO
        box_data = df_analytics[df_analytics['compensacion'] > 0]
        if not box_data.empty:
            fig = px.box(
                box_data,
                x='cluster',
                y='compensacion',
                title='Distribución de Compensación por Segmento',
                color='cluster',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de compensación para mostrar")

def show_early_warnings(df_empleados, df_obras, df_asistencias):
    st.markdown('<div class="section-header">⚠️ Sistema de Alertas Tempranas</div>', unsafe_allow_html=True)
    
    # Alertas de empleados
    st.subheader("👥 Alertas de Personal")
    
    # Generar alertas simuladas
    alertas_empleados = []
    
    # Alertas por bajo desempeño
    bajo_desempeno = df_empleados[
        (df_empleados['activo']) & 
        (df_empleados['evaluacion_desempeno'] < 70)
    ]
    for _, emp in bajo_desempeno.iterrows():
        alertas_empleados.append({
            'tipo': 'Bajo Desempeño',
            'nivel': 'Alto',
            'descripcion': f"{emp['nombre']} {emp['apellido']} - Evaluación: {emp['evaluacion_desempeno']:.1f}%",
            'departamento': emp['departamento']
        })
    
    # Alertas por alto ausentismo
    alto_ausentismo = df_empleados[
        (df_empleados['activo']) & 
        (df_empleados['ausencias_ultimo_mes'] > 3)
    ]
    for _, emp in alto_ausentismo.iterrows():
        alertas_empleados.append({
            'tipo': 'Alto Ausentismo',
            'nivel': 'Medio',
            'descripcion': f"{emp['nombre']} {emp['apellido']} - {emp['ausencias_ultimo_mes']} ausencias/mes",
            'departamento': emp['departamento']
        })
    
    # Mostrar alertas de empleados
    for alerta in alertas_empleados:
        if alerta['nivel'] == 'Alto':
            st.markdown(f'<div class="alert-high">', unsafe_allow_html=True)
        elif alerta['nivel'] == 'Medio':
            st.markdown(f'<div class="alert-medium">', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert-low">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.write(f"**{alerta['tipo']}**")
            st.write(f"Departamento: {alerta['departamento']}")
        
        with col2:
            st.write(alerta['descripcion'])
        
        with col3:
            if st.button("📋 Acción", key=f"accion_{alerta['descripcion']}"):
                st.success(f"Acción tomada para {alerta['descripcion']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Alertas de obras
    st.subheader("🏗️ Alertas de Obras")
    
    alertas_obras = []
    
    # Obras en riesgo
    obras_riesgo = df_obras[df_obras['estado'] == 'En Riesgo']
    for _, obra in obras_riesgo.iterrows():
        alertas_obras.append({
            'tipo': 'Obra en Riesgo',
            'nivel': 'Alto',
            'descripcion': f"{obra['nombre']} - {obra['ubicacion']}",
            'presupuesto': obra['presupuesto']
        })
    
    # Obras sin gerente asignado (simulado)
    for _, obra in df_obras.sample(2).iterrows():
        alertas_obras.append({
            'tipo': 'Falta Recursos',
            'nivel': 'Medio',
            'descripcion': f"{obra['nombre']} - Necesita más personal especializado",
            'presupuesto': obra['presupuesto']
        })
    
    # Mostrar alertas de obras
    for alerta in alertas_obras:
        if alerta['nivel'] == 'Alto':
            st.markdown(f'<div class="alert-high">', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert-medium">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.write(f"**{alerta['tipo']}**")
            st.write(f"Presupuesto: ${alerta['presupuesto']:,.0f}")
        
        with col2:
            st.write(alerta['descripcion'])
        
        with col3:
            if st.button("🔧 Resolver", key=f"resolver_{alerta['descripcion']}"):
                st.success(f"Problema resuelto para {alerta['descripcion']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Métricas de alertas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Alertas", len(alertas_empleados) + len(alertas_obras))
    
    with col2:
        alertas_altas = len([a for a in alertas_empleados + alertas_obras if a['nivel'] == 'Alto'])
        st.metric("🔴 Alertas Altas", alertas_altas)
    
    with col3:
        alertas_medias = len([a for a in alertas_empleados + alertas_obras if a['nivel'] == 'Medio'])
        st.metric("🟡 Alertas Medias", alertas_medias)
    
    with col4:
        st.metric("✅ Resueltas Hoy", np.random.randint(2, 8))

def show_financial_analysis(df_gastos_beneficios, df_obras, df_empleados):
    st.markdown('<div class="section-header">💰 Análisis Financiero Integral</div>', unsafe_allow_html=True)
    
    # Mejorar datos ficticios para el análisis financiero
    if df_gastos_beneficios.empty or 'obra_id' not in df_gastos_beneficios.columns:
        st.warning("Generando datos financieros de demostración...")
        df_gastos_beneficios = generar_datos_financieros_demo(df_obras)
    
    # Métricas financieras
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_gastos = df_gastos_beneficios[df_gastos_beneficios['tipo'] == 'Gasto']['monto'].sum()
        st.metric("💸 Gastos Totales", f"${total_gastos:,.0f}")
    
    with col2:
        total_beneficios = df_gastos_beneficios[df_gastos_beneficios['tipo'] == 'Beneficio']['monto'].sum()
        st.metric("💰 Beneficios Totales", f"${total_beneficios:,.0f}")
    
    with col3:
        balance = total_beneficios - total_gastos
        st.metric("⚖️ Balance Neto", f"${balance:,.0f}", 
                 delta=f"{(balance/total_gastos*100 if total_gastos > 0 else 0):.1f}%")
    
    with col4:
        roi = (total_beneficios / total_gastos * 100) if total_gastos > 0 else 0
        st.metric("📈 ROI", f"{roi:.1f}%")

    # Insights financieros
    st.subheader("💡 Insights Financieros")
    
    # Calcular métricas para insights
    gastos_por_obra = df_gastos_beneficios[df_gastos_beneficios['tipo'] == 'Gasto'].groupby('obra_id')['monto'].sum()
    beneficios_por_obra = df_gastos_beneficios[df_gastos_beneficios['tipo'] == 'Beneficio'].groupby('obra_id')['monto'].sum()
    
    obra_mayor_gasto = gastos_por_obra.idxmax() if not gastos_por_obra.empty else "N/A"
    obra_mayor_beneficio = beneficios_por_obra.idxmax() if not beneficios_por_obra.empty else "N/A"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**Obra con mayor gasto:** {obra_mayor_gasto}")
        st.info(f"**Obra con mayor beneficio:** {obra_mayor_beneficio}")
    
    with col2:
        gasto_promedio = gastos_por_obra.mean() if not gastos_por_obra.empty else 0
        beneficio_promedio = beneficios_por_obra.mean() if not beneficios_por_obra.empty else 0
        st.info(f"**Gasto promedio por obra:** ${gasto_promedio:,.0f}")
        st.info(f"**Beneficio promedio por obra:** ${beneficio_promedio:,.0f}")
    
    with col3:
        margen_beneficio = (total_beneficios - total_gastos) / total_beneficios * 100 if total_beneficios > 0 else 0
        st.info(f"**Margen de beneficio:** {margen_beneficio:.1f}%")
        st.info(f"**Total transacciones:** {len(df_gastos_beneficios)}")
    
    # Gráficos de análisis financiero
    col1, col2 = st.columns(2)
    
    with col1:
        # Gastos vs Beneficios por obra
        try:
            gb_por_obra = df_gastos_beneficios.merge(df_obras, left_on='obra_id', right_on='id')
            
            if not gb_por_obra.empty:
                gb_pivot = gb_por_obra.pivot_table(
                    values='monto', 
                    index='nombre', 
                    columns='tipo', 
                    aggfunc='sum'
                ).fillna(0)
                
                if not gb_pivot.empty:
                    fig = px.bar(
                        gb_pivot.reset_index(),
                        x='nombre',
                        y=['Gasto', 'Beneficio'],
                        title='Gastos vs Beneficios por Obra',
                        barmode='group',
                        color_discrete_map={'Gasto': '#e74c3c', 'Beneficio': '#2ecc71'}
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No hay datos suficientes para el gráfico de gastos vs beneficios")
            else:
                st.info("No hay datos de obras para mostrar")
                
        except Exception as e:
            st.error(f"Error al generar el gráfico: {str(e)}")
            # Mostrar datos alternativos
            st.info("Datos financieros disponibles:")
            st.dataframe(df_gastos_beneficios.head())
    
    with col2:
        # Evolución temporal de gastos y beneficios
        try:
            if 'fecha' in df_gastos_beneficios.columns:
                df_gastos_beneficios['fecha'] = pd.to_datetime(df_gastos_beneficios['fecha'])
                df_gastos_beneficios['mes'] = df_gastos_beneficios['fecha'].dt.to_period('M').astype(str)
                
                evolucion_mensual = df_gastos_beneficios.groupby(['mes', 'tipo'])['monto'].sum().reset_index()
                
                if not evolucion_mensual.empty:
                    fig = px.line(
                        evolucion_mensual,
                        x='mes',
                        y='monto',
                        color='tipo',
                        title='Evolución Mensual de Gastos y Beneficios',
                        markers=True,
                        color_discrete_map={'Gasto': '#e74c3c', 'Beneficio': '#2ecc71'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No hay datos para la evolución temporal")
            else:
                # Si no hay fecha, crear una evolución simulada
                st.info("Generando evolución temporal de demostración...")
                meses = ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06']
                datos_evolucion = []
                for mes in meses:
                    datos_evolucion.append({'mes': mes, 'tipo': 'Gasto', 'monto': np.random.uniform(50000, 200000)})
                    datos_evolucion.append({'mes': mes, 'tipo': 'Beneficio', 'monto': np.random.uniform(60000, 250000)})
                
                evolucion_mensual = pd.DataFrame(datos_evolucion)
                fig = px.line(
                    evolucion_mensual,
                    x='mes',
                    y='monto',
                    color='tipo',
                    title='Evolución Mensual de Gastos y Beneficios (Demo)',
                    markers=True,
                    color_discrete_map={'Gasto': '#e74c3c', 'Beneficio': '#2ecc71'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error en evolución temporal: {str(e)}")
    
    # Análisis detallado por concepto
    st.subheader("📊 Análisis Detallado por Concepto")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gastos por concepto
        gastos_concepto = df_gastos_beneficios[df_gastos_beneficios['tipo'] == 'Gasto']
        if not gastos_concepto.empty and 'concepto' in gastos_concepto.columns:
            gastos_por_concepto = gastos_concepto.groupby('concepto')['monto'].sum().sort_values(ascending=False)
            
            fig = px.pie(
                values=gastos_por_concepto.values,
                names=gastos_por_concepto.index,
                title='Distribución de Gastos por Concepto',
                color_discrete_sequence=px.colors.sequential.Reds
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de gastos por concepto")
            # Datos de demostración
            conceptos_gastos = ['Materiales', 'Mano de Obra', 'Equipos', 'Logística', 'Administrativo']
            montos_gastos = [45, 25, 15, 10, 5]
            fig = px.pie(values=montos_gastos, names=conceptos_gastos, 
                        title='Distribución de Gastos por Concepto (Demo)',
                        color_discrete_sequence=px.colors.sequential.Reds)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Beneficios por concepto
        beneficios_concepto = df_gastos_beneficios[df_gastos_beneficios['tipo'] == 'Beneficio']
        if not beneficios_concepto.empty and 'concepto' in beneficios_concepto.columns:
            beneficios_por_concepto = beneficios_concepto.groupby('concepto')['monto'].sum().sort_values(ascending=False)
            
            fig = px.bar(
                x=beneficios_por_concepto.values,
                y=beneficios_por_concepto.index,
                title='Beneficios por Concepto',
                orientation='h',
                color=beneficios_por_concepto.values,
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de beneficios por concepto")
            # Datos de demostración
            conceptos_beneficios = ['Avance de Obra', 'Eficiencia', 'Ahorro Materiales', 'Bonos Calidad']
            montos_beneficios = [120000, 80000, 60000, 40000]
            fig = px.bar(x=montos_beneficios, y=conceptos_beneficios, 
                        title='Beneficios por Concepto (Demo)',
                        orientation='h',
                        color=montos_beneficios,
                        color_continuous_scale='Greens')
            st.plotly_chart(fig, use_container_width=True)
    
    # Análisis de rentabilidad por obra
    st.subheader("🏗️ Rentabilidad por Obra")
    
    try:
        # Calcular rentabilidad por obra
        rentabilidad_obras = []
        for obra_id in df_gastos_beneficios['obra_id'].unique():
            gastos_obra = df_gastos_beneficios[
                (df_gastos_beneficios['obra_id'] == obra_id) & 
                (df_gastos_beneficios['tipo'] == 'Gasto')
            ]['monto'].sum()
            
            beneficios_obra = df_gastos_beneficios[
                (df_gastos_beneficios['obra_id'] == obra_id) & 
                (df_gastos_beneficios['tipo'] == 'Beneficio')
            ]['monto'].sum()
            
            rentabilidad = (beneficios_obra - gastos_obra) / gastos_obra * 100 if gastos_obra > 0 else 0
            
            # Obtener nombre de la obra
            obra_nombre = df_obras[df_obras['id'] == obra_id]['nombre'].iloc[0] if not df_obras[df_obras['id'] == obra_id].empty else f"Obra {obra_id}"
            
            rentabilidad_obras.append({
                'obra': obra_nombre,
                'gastos': gastos_obra,
                'beneficios': beneficios_obra,
                'rentabilidad': rentabilidad
            })
        
        df_rentabilidad = pd.DataFrame(rentabilidad_obras)
        
        if not df_rentabilidad.empty:
            fig = px.bar(
                df_rentabilidad.sort_values('rentabilidad', ascending=False).head(10),
                x='obra',
                y='rentabilidad',
                title='Top 10 Obras por Rentabilidad (%)',
                color='rentabilidad',
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de rentabilidad para mostrar")
            
    except Exception as e:
        st.error(f"Error en análisis de rentabilidad: {str(e)}")

def show_turnover_analysis(df_rotacion, df_empleados):
    st.markdown('<div class="section-header">🔄 Análisis de Rotación Personal</div>', unsafe_allow_html=True)
    
    # Métricas de rotación
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        rotacion_promedio = df_rotacion['rotacion_mensual'].mean() * 100
        st.metric("📊 Rotación Promedio", f"{rotacion_promedio:.1f}%")
    
    with col2:
        total_salidos = df_rotacion['empleados_salidos'].sum()
        st.metric("👋 Empleados Salidos", total_salidos)
    
    with col3:
        costo_total_rotacion = df_rotacion['costo_rotacion'].sum()
        st.metric("💸 Costo Total Rotación", f"${costo_total_rotacion:,.0f}")
    
    with col4:
        costo_promedio_rotacion = df_rotacion['costo_rotacion'].mean()
        st.metric("💰 Costo Promedio por Rotación", f"${costo_promedio_rotacion:,.0f}")
    
    # Filtros para análisis de rotación
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dept_filter = st.selectbox(
            "🏢 Departamento",
            options=['Todos'] + df_rotacion['departamento'].unique().tolist(),
            key="rotacion_dept"
        )
    
    with col2:
        area_filter = st.selectbox(
            "📍 Área",
            options=['Todos'] + df_rotacion['area'].unique().tolist(),
            key="rotacion_area"
        )
    
    with col3:
        ciudad_filter = st.selectbox(
            "🏙️ Ciudad",
            options=['Todos'] + df_rotacion['ciudad'].unique().tolist(),
            key="rotacion_ciudad"
        )
    
    # Aplicar filtros
    filtered_rotacion = df_rotacion.copy()
    
    if dept_filter != 'Todos':
        filtered_rotacion = filtered_rotacion[filtered_rotacion['departamento'] == dept_filter]
    
    if area_filter != 'Todos':
        filtered_rotacion = filtered_rotacion[filtered_rotacion['area'] == area_filter]
    
    if ciudad_filter != 'Todos':
        filtered_rotacion = filtered_rotacion[filtered_rotacion['ciudad'] == ciudad_filter]
    
    # Gráficos de análisis de rotación
    col1, col2 = st.columns(2)
    
    with col1:
        # Rotación por departamento
        rotacion_dept = filtered_rotacion.groupby('departamento')['rotacion_mensual'].mean().sort_values(ascending=False)
        
        fig = px.bar(
            x=rotacion_dept.index,
            y=rotacion_dept.values * 100,
            title='Rotación Promedio por Departamento (%)',
            labels={'x': 'Departamento', 'y': 'Rotación (%)'},
            color=rotacion_dept.values,
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Rotación por puesto
        rotacion_puesto = filtered_rotacion.groupby('puesto')['rotacion_mensual'].mean().sort_values(ascending=False)
        
        fig = px.bar(
            x=rotacion_puesto.index,
            y=rotacion_puesto.values * 100,
            title='Rotación Promedio por Puesto (%)',
            labels={'x': 'Puesto', 'y': 'Rotación (%)'},
            color=rotacion_puesto.values,
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap de rotación
    st.subheader("🌐 Mapa de Calor - Rotación por Departamento y Área")
    
    try:
        # Crear matriz para heatmap
        heatmap_data = filtered_rotacion.pivot_table(
            values='rotacion_mensual', 
            index='departamento', 
            columns='area', 
            aggfunc='mean'
        ).fillna(0) * 100
        
        fig = px.imshow(
            heatmap_data,
            title='Rotación por Departamento y Área (%)',
            color_continuous_scale='RdYlBu_r',
            aspect='auto',
            labels=dict(x="Área", y="Departamento", color="Rotación (%)")
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error generando el heatmap: {str(e)}")
        st.dataframe(filtered_rotacion.head(10))

def show_configuration():
    st.markdown('<div class="section-header">⚙️ Configuración del Sistema</div>', unsafe_allow_html=True)
    
    # Configuración de parámetros
    st.subheader("📋 Parámetros del Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input("Umbral Bajo Desempeño (%)", min_value=0, max_value=100, value=70)
        st.number_input("Umbral Alto Ausentismo (días/mes)", min_value=1, max_value=30, value=3)
        st.number_input("Porcentaje Mínimo Aptitud", min_value=0, max_value=100, value=75)
    
    with col2:
        st.number_input("Horas Extra Máximas Semanales", min_value=1, max_value=20, value=10)
        st.number_input("Experiencia Mínima Obra Compleja (meses)", min_value=1, max_value=60, value=24)
        st.number_input("Evaluación Mínima Promoción", min_value=0, max_value=100, value=80)
    
    # Configuración de notificaciones
    st.subheader("🔔 Configuración de Notificaciones")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.checkbox("Alertas de Bajo Desempeño", value=True)
        st.checkbox("Alertas de Alto Ausentismo", value=True)
        st.checkbox("Alertas de Rotación", value=True)
    
    with col2:
        st.checkbox("Notificaciones de Obras en Riesgo", value=True)
        st.checkbox("Reportes Semanales Automáticos", value=True)
        st.checkbox("Recordatorios de Evaluaciones", value=True)
    
    with col3:
        st.selectbox("Frecuencia de Reportes", ["Diario", "Semanal", "Mensual"])
        st.selectbox("Método de Notificación", ["Email", "SMS", "Ambos"])
        st.text_input("Email de Contacto", "admin@empresa.com")
    
    # Acciones del sistema
    st.subheader("🛠️ Acciones del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Sincronizar Datos", use_container_width=True):
            st.success("Datos sincronizados correctamente")
        if st.button("📊 Generar Reporte", use_container_width=True):
            st.success("Reporte generado y enviado")
    
    with col2:
        if st.button("💾 Respaldar Base", use_container_width=True):
            st.success("Respaldo completado exitosamente")
        if st.button("🧹 Limpiar Cache", use_container_width=True):
            st.success("Cache limpiado correctamente")
    
    with col3:
        if st.button("🔍 Ver Logs", use_container_width=True):
            st.info("Mostrando logs del sistema...")
        if st.button("🔄 Reiniciar Sistema", use_container_width=True):
            st.warning("Reiniciando sistema...")

def show_dashboard_manual():
    st.markdown('<div class="manual-title">📖 Manual del Dashboard RRHH Analytics Pro</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="manual-description">
    <h3 style='color: white; margin: 0; text-align: center;'>🎯 Descripción General</h3>
    <p style='color: white; font-size: 1.1rem; margin: 0.5rem 0 0 0; text-align: center;'>
    El <strong>RRHH Analytics Pro</strong> es un sistema integral de gestión de recursos humanos diseñado para la industria de la construcción. 
    Combina análisis avanzados, visualizaciones interactivas y herramientas de gestión para optimizar la fuerza laboral.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Módulos del Dashboard
    st.subheader("📋 Módulos Disponibles")
    
    modules_info = {
        "📊 Dashboard Ejecutivo": {
            "descripción": "Vista general con métricas clave y visualizaciones ejecutivas",
            "insights": [
                "Tendencias de productividad en tiempo real",
                "Distribución de costos por departamento", 
                "Análisis comparativo entre ubicaciones",
                "Evolución temporal de indicadores clave"
            ],
            "visualizaciones": ["Mapas de calor", "Sunburst charts", "Violin plots", "Gráficos de tendencia"]
        },
        "👥 Gestión de Personal": {
            "descripción": "Gestión completa del capital humano con filtros avanzados",
            "insights": [
                "Composición de la fuerza laboral por departamento",
                "Análisis de compensación y equidad salarial",
                "Distribución de habilidades y certificaciones",
                "Segmentación por nivel educativo y experiencia"
            ],
            "visualizaciones": ["Tablas interactivas", "Gráficos de barras", "Scatter plots", "Box plots"]
        },
        "🏗️ Gestión de Obras": {
            "descripción": "Seguimiento y control de proyectos de construcción",
            "insights": [
                "Estado y progreso de obras activas",
                "Asignación óptima de recursos por proyecto",
                "Análisis de riesgos y alertas tempranas",
                "Control de presupuestos y cronogramas"
            ],
            "visualizaciones": ["Tarjetas de proyecto", "Gráficos de estado", "Métricas de progreso"]
        },
        "🎯 Aptitud para Obras": {
            "descripción": "Sistema inteligente de matching empleado-obra",
            "insights": [
                "Evaluación automática de compatibilidad",
                "Identificación de brechas de habilidades",
                "Optimización de asignaciones",
                "Análisis de criterios de aptitud"
            ],
            "visualizaciones": ["Tarjetas de aptitud", "Histogramas de distribución", "Gráficos comparativos"]
        },
        "📈 Analytics Avanzado": {
            "descripción": "Análisis predictivo y segmentación avanzada",
            "insights": [
                "Predicción de rotación voluntaria",
                "Segmentación por desempeño y potencial",
                "Análisis de correlaciones entre variables",
                "Identificación de patrones de comportamiento"
            ],
            "visualizaciones": ["Matrices de correlación", "Scatter plots", "Gráficos de dispersión"]
        },
        "⚠️ Sistema de Alertas": {
            "descripción": "Monitoreo proactivo de riesgos y oportunidades",
            "insights": [
                "Detección temprana de problemas de rendimiento",
                "Alertas de rotación en departamentos críticos",
                "Monitoreo de cumplimiento de metas",
                "Identificación de oportunidades de mejora"
            ],
            "visualizaciones": ["Alertas codificadas por color", "Paneles de control", "Indicadores de riesgo"]
        },
        "💰 Análisis Financiero": {
            "descripción": "Control y optimización de costos y beneficios",
            "insights": [
                "Seguimiento de gastos vs beneficios",
                "Análisis de ROI por proyecto",
                "Optimización de costos laborales",
                "Proyecciones financieras"
            ],
            "visualizaciones": ["Gráficos de barras comparativos", "Líneas de tendencia", "Gráficos de torta"]
        },
        "🔄 Rotación Personal": {
            "descripción": "Análisis multidimensional de la rotación de personal",
            "insights": [
                "Identificación de causas de rotación",
                "Análisis de costos asociados",
                "Segmentación por departamento y área",
                "Estrategias de retención"
            ],
            "visualizaciones": ["Mapas de calor", "Gráficos de barras", "Análisis geográfico"]
        }
    }
    
    for module, info in modules_info.items():
        with st.expander(f"{module} - {info['descripción']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**🔍 Insights Principales:**")
                for insight in info['insights']:
                    st.write(f"• {insight}")
            
            with col2:
                st.write("**📊 Visualizaciones:**")
                for viz in info['visualizaciones']:
                    st.write(f"• {viz}")
    
    # Guías de Uso
    st.subheader("🛠️ Guías de Uso Rápido")
    
    usage_guides = {
        "Filtros Avanzados": "Utiliza los filtros multinivel para segmentar datos específicos por departamento, ubicación, aptitud, etc.",
        "Visualizaciones Interactivas": "Haz hover sobre los gráficos para ver detalles específicos. Usa zoom en gráficos complejos.",
        "Exportación de Datos": "Todos los dataframes son exportables haciendo clic en el ícono de exportación.",
        "Alertas Inteligentes": "Configura umbrales personalizados para recibir alertas proactivas.",
        "Sistema de Aptitud": "Selecciona una obra específica para analizar la compatibilidad automática con empleados."
    }
    
    for guide, description in usage_guides.items():
        st.info(f"**{guide}:** {description}")
    
    # KPIs y Métricas Explicadas
    st.subheader("📈 Explicación de Métricas Clave")
    
    kpis_explained = {
        "Productividad": "Mide la eficiencia del trabajo realizado vs. tiempo invertido. Meta: >85%",
        "Rotación": "Porcentaje de empleados que dejan la empresa. Meta: <8%", 
        "Aptitud Obra Compleja": "Porcentaje de empleados calificados para obras de alta complejidad",
        "Costo por Hora": "Costo laboral promedio por hora trabajada",
        "Ausentismo": "Días de ausencia no programados por empleado/mes. Meta: <3 días",
        "Evaluación Desempeño": "Calificación promedio en evaluaciones de desempeño. Meta: >80%"
    }
    
    for kpi, explanation in kpis_explained.items():
        st.write(f"**{kpi}:** {explanation}")
    
    # Consejos para Análisis
    st.subheader("💡 Consejos para Análisis Efectivo")
    
    tips = [
        "**Compara departamentos** para identificar mejores prácticas y oportunidades de mejora",
        "**Monitorea tendencias temporales** para detectar patrones estacionales o cambios graduales",
        "**Combina múltiples métricas** para obtener una visión holística del desempeño",
        "**Utiliza el sistema de aptitud** para optimizar asignaciones y reducir riesgos",
        "**Configura alertas personalizadas** para monitoreo proactivo de indicadores críticos",
        "**Exporta datos específicos** para análisis más profundos en otras herramientas"
    ]
    
    for tip in tips:
        st.write(f"• {tip}")

if __name__ == "__main__":
    main()
