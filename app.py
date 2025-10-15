import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np 

# =======================
# CONFIGURACION GENERAL
# =======================
st.set_page_config(
    page_title="Dashboard PETI - Droguerias San Jorge",
    page_icon="", # Sin icono
    layout="wide"
)

# =======================
# ESTILOS PERSONALIZADOS
# =======================
st.markdown("""
    <style>
        /* Estilo de la barra lateral */
        [data-testid="stSidebar"] {
            background-color: #f0f5f9;
            background-image: linear-gradient(180deg, #e8f0ff 0%, #ffffff 100%);
            background-size: cover;
            color: #003366;
        }
        /* Alineacion y estilo para metricas */
        .metric {text-align: center; font-size: 22px; font-weight: bold; color: #005fa3;}
    </style>
""", unsafe_allow_html=True)

# =======================
# BARRA LATERAL
# =======================
# Nota: La imagen 'imagenes/logo_sanjorge.png' debe existir en tu proyecto
try:
    st.sidebar.image("imagenes/logo_sanjorge.png", use_container_width=True)
except:
    st.sidebar.title("Logo San Jorge")
    
st.sidebar.title("Panel de Control PETI")
st.sidebar.markdown("---")
st.sidebar.markdown("**Entidad:** Droguerias San Jorge de Colombia")
st.sidebar.markdown("**Version:** PETI 2025 - 2027")
st.sidebar.markdown("**Responsable:** Gerencia de TI")
st.sidebar.markdown("---")
view = st.sidebar.radio("Navegacion:", ["Inicio", "Proyectos", "KPI Estrategicos", "Balanced Scorecard"])

# =======================
# DATOS BASE 
# =======================

# --- Proyectos estrategicos (Actividad 13) ---
proyectos = pd.DataFrame({
    "Nombre del Proyecto": [
        "Implementar la gobernanza de datos", "Migrar infraestructura tecnologica a SAP",
        "Fortalecimiento de ciberseguridad y confianza digital", "Fomentar el comercio seguro y multicanal",
        "Desarrollar el talento y fortalecer capacidades TI", "Automatizacion de procesos con RPA",
        "Sistema de analitica de datos (Business Intelligence)", "Transformacion digital en atencion al cliente"
    ],
    "Fecha Inicio Estimada": pd.to_datetime([
        "2025-09-10", "2025-10-15", "2025-11-01", "2026-01-15",
        "2025-09-20", "2026-03-01", "2026-05-01", "2026-07-01"
    ]),
    "Duracion (meses)": [6, 9, 12, 10, 6, 8, 7, 9],
    "Categoria": [
        "Datos", "Infraestructura", "Seguridad", "Comercial",
        "Talento Humano", "Automatizacion", "Analitica", "Atencion Digital"
    ],
    "Avance (%)": [45, 30, 25, 60, 50, 40, 35, 55]
})
proyectos["Fin Estimada"] = proyectos["Fecha Inicio Estimada"] + pd.to_timedelta(proyectos["Duracion (meses)"] * 30, unit="D")

# --- KPI Estrategicos ---
kpis = pd.DataFrame({
    "Indicador": [
        "Porcentaje de digitalizacion de procesos", "Disponibilidad de infraestructura critica (SLA)",
        "Nivel de satisfaccion del cliente digital", "Porcentaje de cumplimiento del PETI",
        "Numero de incidentes de ciberseguridad"
    ],
    "Valor Actual": [72, 99.3, 87, 65, 4],
    "Meta 2026": [90, 99.9, 95, 100, 0]
})

# --- Datos Detallados del BSC ---
bsc_ti = pd.DataFrame({
    "Perspectiva": [
        "Financiera", "Financiera", "Clientes", "Clientes", 
        "Procesos Internos", "Procesos Internos", "Aprendizaje y Crecimiento", "Aprendizaje y Crecimiento"
    ],
    "Objetivo Estrategico": [
        "Aumentar las ventas a traves de canales digitales", "Maximizar el ROI en proyectos de tecnologia",
        "Mejorar la experiencia digital y accesibilidad", "Garantizar la confianza digital en el manejo de datos",
        "Optimizar gestion de inventarios y suministros", "Garantizar seguridad de la informacion",
        "Impulsar toma de decisiones basada en datos (BI)", "Asegurar una Plataforma Tecnologica moderna"
    ],
    "Indicador Clave (KPI - Resultado)": [
        "% incremento de ventas en canales digitales", "ROI promedio de proyectos tecnologicos",
        "Indice de satisfaccion del cliente (NPS)", "N de incidentes de seguridad reportados",
        "% reduccion de quiebres de stock", "Nivel de cumplimiento normativo (ISO 27001)",
        "N decisiones estrategicas soportadas en BI", "% infraestructura actualizada / operativa"
    ],
    "Avance (%)": [70, 40, 75, 55, 60, 85, 45, 90]
})


# ==============================================================================
# VISTA: INICIO
# ==============================================================================
if view == "Inicio":
    st.title("Dashboard PETI - Droguerias San Jorge")
    st.markdown("### Plan Estrategico de Tecnologias de la Informacion (2025 - 2027)")
    # Nota: La imagen 'imagenes/portada_sanjorge.png' debe existir en tu proyecto
    try:
        st.image("imagenes/portada_sanjorge.png", use_container_width=True)
    except:
        st.write("Placeholder para Portada")
        
    st.markdown("""
    Este panel resume los **proyectos estrategicos de TI**, los **indicadores clave (KPI)** y el **Balance Scorecard**
    del PETI de **Droguerias San Jorge**, alineado con los objetivos de transformacion digital, ciberseguridad y desarrollo organizacional.
    """)

# ==============================================================================
# VISTA: PROYECTOS (CON FILTRO INTERACTIVO)
# ==============================================================================
elif view == "Proyectos":
    st.header("Cronograma y Avance de Proyectos de TI")

    # --- ELEMENTO INTERACTIVO: Filtro de Categoria ---
    categorias = ["TODAS LAS CATEGORIAS"] + proyectos["Categoria"].unique().tolist()
    filtro_categoria = st.selectbox("Seleccione la Categoria de Proyectos a visualizar:", categorias)
    
    # Aplicar el filtro al DataFrame
    if filtro_categoria != "TODAS LAS CATEGORIAS":
        df_filtrado = proyectos[proyectos["Categoria"] == filtro_categoria]
    else:
        df_filtrado = proyectos
        
    st.markdown("---")

    # 1. Gráfico de Gantt (usa df_filtrado)
    st.subheader("Cronograma de ejecucion")
    fig_gantt = px.timeline(
        df_filtrado,
        x_start="Fecha Inicio Estimada",
        x_end="Fin Estimada",
        y="Nombre del Proyecto",
        color="Categoria",
        title=f"Cronograma (Proyectos: {filtro_categoria})",
        color_discrete_sequence=px.colors.qualitative.Set2,
        height=400 
    )
    fig_gantt.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig_gantt, use_container_width=True)

    st.subheader("Estado de avance de los proyectos")
    
    # 2. Gráfico de Barras (usa df_filtrado y con animacion)
    fig_bar = px.bar(
        df_filtrado,
        x="Nombre del Proyecto",
        y="Avance (%)",
        color="Categoria",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        text="Avance (%)",
        animation_group="Nombre del Proyecto", # Activa interactividad y animacion en Plotly
        height=500 # Mas vertical
    )
    fig_bar.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)

# ==============================================================================
# VISTA: KPI ESTRATEGICOS
# ==============================================================================
elif view == "KPI Estrategicos":
    st.header("Indicadores Clave de Desempeno (KPI)")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Digitalizacion de procesos", "72%", "Meta: 90%")
    col2.metric("Satisfaccion cliente digital", "87%", "Meta: 95%")
    col3.metric("Cumplimiento PETI", "65%", "Meta: 100%")

    st.markdown("### Comparativo de indicadores actuales vs metas 2026")
    
    # Grafico comparativo
    fig_kpi = px.bar(
        kpis,
        x="Indicador",
        y=["Valor Actual", "Meta 2026"],
        barmode="group",
        color_discrete_sequence=["#0077b6", "#00b4d8"],
        height=500 # Mas vertical
    )
    st.plotly_chart(fig_kpi, use_container_width=True)

# ==============================================================================
# VISTA: BALANCED SCORECARD (OPTIMIZADO Y SIN RADAR)
# ==============================================================================
elif view == "Balanced Scorecard":
    st.header("Balanced Scorecard (BSC) de TI - Droguerias San Jorge")
    st.markdown("""
    El Dashboard Estrategico monitorea el avance de los objetivos por perspectiva y justifica la inversion a traves de la Matriz de Alineacion Proyecto-Estrategia.
    """)

    # --- KPI General ---
    avance_general = bsc_ti["Avance (%)"].mean()
    
    col_kpi_general, col_spacer, col_kpi_meta = st.columns([1.5, 3, 1.5])
    
    col_kpi_general.markdown(
        f'<div class="metric">Avance General del BSC</div>'
        f'<div style="font-size: 50px; font-weight: bold; color: #0077b6; text-align: center;">{avance_general:.1f}%</div>',
        unsafe_allow_html=True
    )
    col_kpi_meta.markdown(
        f'<div class="metric">Meta (BSC)</div>'
        f'<div style="font-size: 50px; font-weight: bold; color: #003366; text-align: center;">100.0%</div>',
        unsafe_allow_html=True
    )
    st.markdown("---")

    # ------------------------------------------------------------------------------
    # FILA 1: AVANCE POR PERSPECTIVA Y MATRIZ DE ALINEACION
    # ------------------------------------------------------------------------------
    col_avance, col_heatmap = st.columns([1, 1.8])

    # --- Columna Izquierda: Grafico de Barras (Vertical) ---
    with col_avance:
        st.subheader("Avance Promedio por Perspectiva")

        avance_por_perspectiva = bsc_ti.groupby("Perspectiva")["Avance (%)"].mean().reset_index()
        orden_bsc = ["Financiera", "Clientes", "Procesos Internos", "Aprendizaje y Crecimiento"]
        avance_por_perspectiva['Perspectiva'] = pd.Categorical(avance_por_perspectiva['Perspectiva'], categories=orden_bsc, ordered=True)
        avance_por_perspectiva = avance_por_perspectiva.sort_values('Perspectiva')

        fig_bar = px.bar(
            avance_por_perspectiva,
            x="Perspectiva",
            y="Avance (%)",
            color="Avance (%)",
            text="Avance (%)",
            color_continuous_scale="Viridis",
            height=550, # Incrementado para verticalidad
            title="Comparativo de cumplimiento"
        )
        fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_bar.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig_bar, use_container_width=True)


    # --- Columna Derecha: Matriz de Alineacion (Heatmap) ---
    with col_heatmap:
        st.subheader("Matriz de Alineacion (Proyectos vs. Estrategia)")
        st.markdown("El **nivel de impacto (1-5)** justifica la priorizacion de los proyectos de TI.")
        
        # --- Creacion de la Matriz de Alineacion (Datos MOCK/Simulados) ---
        data_alineacion = {
            'Proyecto': proyectos["Nombre del Proyecto"].tolist(),
            "Financiera": [2, 5, 3, 4, 1, 5, 4, 3],
            "Clientes": [3, 3, 5, 5, 2, 2, 3, 4],
            "Procesos Internos": [4, 5, 4, 3, 3, 4, 5, 4],
            "Aprendizaje y Crecimiento": [5, 4, 3, 2, 5, 3, 5, 3]
        }
        df_alineacion = pd.DataFrame(data_alineacion).set_index('Proyecto')

        # Visualizacion del Heatmap
        fig_heatmap = px.imshow(
            df_alineacion,
            text_auto=True,
            aspect="auto",
            color_continuous_scale=px.colors.sequential.Reds,
            labels=dict(x="Perspectiva del BSC", y="Proyecto de TI", color="Impacto (1-5)"),
            height=700 # Incrementado para verticalidad
        )
        fig_heatmap.update_xaxes(side="top")
        st.plotly_chart(fig_heatmap, use_container_width=True)

    # ------------------------------------------------------------------------------
    # FILA 2: ANALISIS DE RIESGOS Y TABLA DETALLADA
    # ------------------------------------------------------------------------------
    st.markdown("---")

    col_riesgos, col_tabla = st.columns([1, 1])

    with col_riesgos:
        st.subheader("Riesgos Tacticos: Objetivos con Menor Avance")
        st.markdown("Foco en los objetivos de menor avance para mitigar la desviacion estrategica.")
        
        riesgos_tacticos = bsc_ti.sort_values(by="Avance (%)", ascending=True).head(4)

        # Funcion para aplicar formato condicional (Semaforo)
        def highlight_risk(s):
            if s <= 45:
                return 'background-color: #f8d7da; color: black' # Rojo (Critica)
            elif s <= 60:
                return 'background-color: #fff3cd; color: black' # Amarillo (Media)
            return ''

        st.dataframe(
            riesgos_tacticos[['Perspectiva', 'Objetivo Estrategico', 'Avance (%)']]
            .style.applymap(
                highlight_risk,
                subset=['Avance (%)']
            ).format({'Avance (%)': '{:.1f}%'}),
            use_container_width=True,
            hide_index=True
        )

    with col_tabla:
        st.subheader("Tabla Detallada de Objetivos y KPIs de TI")
        st.dataframe(bsc_ti, use_container_width=True, hide_index=True)

# Fin del script
