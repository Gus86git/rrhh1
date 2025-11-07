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
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #3498db;
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
</style>
""", unsafe_allow_html=True)

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
    consultoras = ['Constructora Norte', 'BuildCorp', 'Proyecta S.A.', 'Edifica Group']
    
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
        else:
            # Precios por hora para contratados
            precio_base_hora = {
                'Albañilería': 1200, 'Electricidad': 1500, 
                'Plomería': 1300, 'Herrería': 1800, 'Pintura': 1100
            }[dept]
            precio_hora_comun = precio_base_hora * np.random.uniform(0.9, 1.3)
            precio_hora_extra = precio_hora_comun * 1.5
            salario = None
            consultora = np.random.choice(consultoras)
        
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
    
    # Generar datos de gastos y beneficios
    gastos_beneficios = []
    for obra in obras:
        for _ in range(np.random.randint(5, 15)):
            gastos_beneficios.append({
                'obra_id': obra['id'],
                'tipo': 'Gasto',
                'concepto': np.random.choice(['Materiales', 'Mano de Obra', 'Equipos', 'Logística']),
                'monto': np.random.uniform(10000, 200000),
                'fecha': datetime.now() - timedelta(days=np.random.randint(1, 180))
            })
        
        for _ in range(np.random.randint(2, 8)):
            gastos_beneficios.append({
                'obra_id': obra['id'],
                'tipo': 'Beneficio',
                'concepto': np.random.choice(['Avance de Obra', 'Eficiencia', 'Ahorro Materiales']),
                'monto': np.random.uniform(50000, 300000),
                'fecha': datetime.now() - timedelta(days=np.random.randint(1, 180))
            })
    
    df_gastos_beneficios = pd.DataFrame(gastos_beneficios)
    
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
        st.subheader("📊 Sunburst - Distribución Jerárquica")
        
        sunburst_data = df_empleados[df_empleados['activo']].copy()
        fig = create_advanced_plotly_chart(
            sunburst_data,
            'Distribución de Empleados por Departamento y Especialidad',
            'sunburst',
            path=['departamento', 'especialidad'],
            values='experiencia_meses',
            color='experiencia_meses',
            color_continuous_scale='Blues'
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Tercera fila - Más visualizaciones
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎻 Distribución Salarial - Violin Plot")
        
        fig = create_advanced_plotly_chart(
            df_empleados[df_empleados['activo']],
            'Distribución Salarial por Departamento',
            'violin',
            x='departamento',
            y='salario',
            color='departamento',
            box=True
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Tendencia Temporal - Productividad")
        
        df_asistencias['fecha'] = pd.to_datetime(df_asistencias['fecha'])
        df_asistencias['mes'] = df_asistencias['fecha'].dt.to_period('M').astype(str)
        
        productividad_mensual = df_asistencias.groupby('mes')['productividad'].mean().reset_index()
        
        fig = create_advanced_plotly_chart(
            productividad_mensual,
            'Evolución Mensual de Productividad',
            'line',
            x='mes',
            y='productividad',
            markers=True
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Cuarta fila - Nuevos análisis basados en el DER
    st.subheader("🆕 Análisis Basados en el Modelo de Datos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Análisis de consultoras
        st.subheader("🏢 Empleados por Consultora")
        consultora_dist = df_empleados[df_empleados['tipo_empleado'] == 'contratado'].groupby('consultora').size()
        fig = px.bar(
            x=consultora_dist.index,
            y=consultora_dist.values,
            title='Distribución de Empleados Contratados por Consultora',
            labels={'x': 'Consultora', 'y': 'Cantidad de Empleados'},
            color=consultora_dist.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Análisis de rubros
        st.subheader("📦 Distribución por Rubro")
        rubro_dist = df_asistencias['rubro'].value_counts()
        fig = px.pie(
            values=rubro_dist.values,
            names=rubro_dist.index,
            title='Distribución de Horas por Rubro'
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

# ... (las otras funciones show_aptitude_analysis, show_advanced_analytics, show_early_warnings, 
# show_financial_analysis, show_turnover_analysis, show_configuration, show_dashboard_manual 
# se mantienen exactamente igual que en el código anterior que funcionaba bien)

# NOTA: Para mantener la respuesta dentro del límite, las funciones restantes son idénticas
# al código anterior que ya funcionaba. Solo se han modificado show_executive_dashboard y show_person_management
# para incluir la distinción entre empleados efectivos y contratados.

if __name__ == "__main__":
    main()
