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
        
        # Salarios base por departamento
        salario_base = {
            'Albañilería': 80000, 'Electricidad': 95000, 
            'Plomería': 85000, 'Herrería': 110000, 'Pintura': 75000
        }[dept]
        
        salario = salario_base * np.random.uniform(0.8, 1.5)
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
            'nombre': np.random.choice(nombres),
            'apellido': np.random.choice(apellidos),
            'genero': genero,
            'edad': edad,
            'departamento': dept,
            'especialidad': np.random.choice(especialidades[dept]),
            'cargo': f"{dept} {'Senior' if experiencia > 60 else 'Junior' if experiencia > 24 else 'Aprendiz'}",
            'salario': round(salario, 2),
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
            'puesto': np.random.choice(puestos),
            'consultora': np.random.choice(consultoras),
            'empleado_contratado': np.random.choice([True, False], p=[0.3, 0.7])
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
        
        asistencias.append({
            'empleado_id': emp['id'],
            'obra_id': obra['id'],
            'fecha': fecha,
            'horas_trabajadas': np.random.randint(6, 10),
            'horas_extra': np.random.choice([0, 0, 0, 1, 2, 3], p=[0.4, 0.2, 0.15, 0.15, 0.07, 0.03]),
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
        costo_total = df_empleados[df_empleados['activo']]['salario'].sum()
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
        st.subheader("🌐 Distribución por Área y Ciudad")
        
        # Gráfico de distribución geográfica
        distribucion_geo = df_empleados[df_empleados['activo']].groupby(['area', 'ciudad']).size().reset_index(name='count')
        
        fig = px.treemap(
            distribucion_geo,
            path=['area', 'ciudad'],
            values='count',
            title='Distribución de Empleados por Área y Ciudad',
            color='count',
            color_continuous_scale='Blues'
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
            values='salario',
            color='salario',
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
        consultora_dist = df_empleados[df_empleados['empleado_contratado']].groupby('consultora').size()
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

def show_financial_analysis(df_gastos_beneficios, df_obras, df_empleados):
    st.markdown('<div class="section-header">💰 Análisis Financiero Integral</div>', unsafe_allow_html=True)
    
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
    
    # Gráficos de análisis financiero
    col1, col2 = st.columns(2)
    
    with col1:
        # Gastos vs Beneficios por obra
        gb_por_obra = df_gastos_beneficios.merge(df_obras, left_on='obra_id', right_on='id')
        gb_pivot = gb_por_obra.pivot_table(
            values='monto', 
            index='nombre', 
            columns='tipo', 
            aggfunc='sum'
        ).fillna(0)
        
        fig = px.bar(
            gb_pivot.reset_index(),
            x='nombre',
            y=['Gasto', 'Beneficio'],
            title='Gastos vs Beneficios por Obra',
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Evolución temporal de gastos y beneficios
        df_gastos_beneficios['fecha'] = pd.to_datetime(df_gastos_beneficios['fecha'])
        df_gastos_beneficios['mes'] = df_gastos_beneficios['fecha'].dt.to_period('M').astype(str)
        
        evolucion_mensual = df_gastos_beneficios.groupby(['mes', 'tipo'])['monto'].sum().reset_index()
        
        fig = px.line(
            evolucion_mensual,
            x='mes',
            y='monto',
            color='tipo',
            title='Evolución Mensual de Gastos y Beneficios',
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Análisis detallado por concepto
    st.subheader("📊 Análisis Detallado por Concepto")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gastos por concepto
        gastos_concepto = df_gastos_beneficios[df_gastos_beneficios['tipo'] == 'Gasto']
        gastos_por_concepto = gastos_concepto.groupby('concepto')['monto'].sum().sort_values(ascending=False)
        
        fig = px.pie(
            values=gastos_por_concepto.values,
            names=gastos_por_concepto.index,
            title='Distribución de Gastos por Concepto'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Beneficios por concepto
        beneficios_concepto = df_gastos_beneficios[df_gastos_beneficios['tipo'] == 'Beneficio']
        beneficios_por_concepto = beneficios_concepto.groupby('concepto')['monto'].sum().sort_values(ascending=False)
        
        fig = px.bar(
            x=beneficios_por_concepto.values,
            y=beneficios_por_concepto.index,
            title='Beneficios por Concepto',
            orientation='h'
        )
        st.plotly_chart(fig, use_container_width=True)

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
    
    # Análisis geográfico de rotación
    st.subheader("🗺️ Análisis Geográfico de Rotación")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Rotación por área
        rotacion_area = filtered_rotacion.groupby('area')['rotacion_mensual'].mean().sort_values(ascending=False)
        
        fig = px.pie(
            values=rotacion_area.values * 100,
            names=rotacion_area.index,
            title='Distribución de Rotación por Área (%)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Rotación por ciudad
        rotacion_ciudad = filtered_rotacion.groupby('ciudad')['rotacion_mensual'].mean().sort_values(ascending=False)
        
        fig = px.bar(
            x=rotacion_ciudad.index,
            y=rotacion_ciudad.values * 100,
            title='Rotación Promedio por Ciudad (%)',
            labels={'x': 'Ciudad', 'y': 'Rotación (%)'},
            color=rotacion_ciudad.values,
            color_continuous_scale='Purples'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap de rotación (corregido)
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
        # Alternativa si falla el heatmap
        st.info("Mostrando datos en formato tabla:")
        st.dataframe(heatmap_data)


if __name__ == "__main__":
    main()
