import streamlit as st
import pandas as pd
import altair as alt
from fpdf import FPDF

# Configuração
st.set_page_config(page_title="Engenharia Solar Pro", layout="wide")
st.title("☀️ Sistema de Gestão de Projetos Fotovoltaicos")

# Sidebar
st.sidebar.header("Parâmetros do Projeto")
local_instalacao = st.sidebar.text_input("Local da Instalação", value="Niterói/RJ")
consumo = st.sidebar.number_input("Consumo Médio Mensal (kWh)", value=161.83, step=0.1)
tarifa = st.sidebar.number_input("Tarifa (R$/kWh)", value=0.95, step=0.01)

st.sidebar.subheader("Especificações Técnicas")
modelo_modulo = st.sidebar.text_input("Modelo do Módulo", value="JKM480N-60HL4")
potencia = st.sidebar.number_input("Potência Painel (Wp)", value=480, step=1)
n_modulos = st.sidebar.number_input("Quantidade de Módulos", value=3, step=1)
inversor = st.sidebar.text_input("Modelo do Inversor", value="MIC 1500TL-X")
cabo_cc = st.sidebar.number_input("Secção do Cabo CC Solar (mm²)", value=4.0, step=0.25, format="%.2f")
cabo_ca = st.sidebar.number_input("Secção do Cabo CA (mm²)", value=2.5, step=0.25, format="%.2f")

st.sidebar.subheader("Composição de Custos")
custo_equip = st.sidebar.number_input("Custo Equipamentos (R$)", value=4000.0, step=100.0)
custo_serv = st.sidebar.number_input("Custo Serviços (R$)", value=2000.0, step=100.0)
custo_total = custo_equip + custo_serv

# Cálculos
geracao_ideal = (n_modulos * potencia * 4.98 * 30) / 1000
geracao_real = geracao_ideal * 0.75 
co2_evitado = geracao_real * 12 * 0.08 
payback = custo_total / ((geracao_real * tarifa)) if (geracao_real * tarifa) > 0 else 0

# Gráfico Customizado com Altair
st.subheader("Análise de Performance")

df_cenario = pd.DataFrame({'Cenário': ['Ideal', 'Real'], 'Energia': [geracao_ideal, geracao_real]})
chart = alt.Chart(df_cenario).mark_bar().encode(
    x=alt.X('Cenário', axis=alt.Axis(labelAngle=0)), 
    y=alt.Y('Energia', title='Energia Gerada (kWh)'), 
    color='Cenário'
).properties(width=600, height=400)
st.altair_chart(chart, use_container_width=True)

# Alerta condicional baseado no Payback
if payback > 60:
    st.warning(f"⚠️ Payback de {payback:.1f} meses: Considere ajustar o custo ou a eficiência do arranjo.")
elif payback > 0:
    st.success(f"✅ Payback de {payback:.1f} meses: Viabilidade financeira atrativa.")

# Layout de métricas com colunas organizadas
c1, c2, c3, c4 = st.columns(4)
c1.metric("Potência Instalada", f"{(n_modulos*potencia)/1000:.2f} kWp")
c2.metric("Geração Real", f"{geracao_real:.1f} kWh/mês")
c3.metric("Payback", f"{payback:.1f} meses")
c4.metric("CO2 Evitado", f"{co2_evitado:.2f} kg/ano")

# Uploader de foto para análise preliminar
st.subheader("Análise de Campo")
uploaded_file = st.file_uploader("Upload da foto do telhado (para análise de sombreamento)", type=['png', 'jpg', 'jpeg'])
if uploaded_file is not None:
    st.image(uploaded_file, caption=f'Imagem do local de instalação ({local_instalacao})', use_column_width=True)

# --- FUNÇÃO AUXILIAR PARA CRIAR TABELAS NO PDF ---
def desenhar_tabela(pdf, col_widths, row_data, is_header=False):
    if is_header:
        pdf.set_font("Arial", 'B', 8)
    else:
        pdf.set_font("Arial", '', 8)
    for width, text in zip(col_widths, row_data):
        pdf.cell(width, 7, str(text), border=1, align='C')
    pdf.ln()

# --- FUNÇÃO PDF COMPLETA ---
def gerar_memorial():
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Memorial Descritivo e Financeiro", ln=True, align='C')
    pdf.ln(5)
    
    # 1. Consumo Histórico Anual
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "1. Historico de Consumo Anual", ln=True)
    
    # Tabela de Consumo
    larguras_consumo = [25, 30, 15, 45, 30, 45]
    desenhar_tabela(pdf, larguras_consumo, ["Mes", "Consumo (kWh)", "Dias", "Media Diaria (kWh/dia)", "Tarifa (R$)", "Conta Est. (R$)"], is_header=True)
    desenhar_tabela(pdf, larguras_consumo, ["Janeiro", "145", "31", "4.68", "0.95", "137.75"])
    desenhar_tabela(pdf, larguras_consumo, ["Fevereiro", "152", "28", "5.43", "0.95", "144.40"])
    desenhar_tabela(pdf, larguras_consumo, ["Marco", "138", "31", "4.45", "0.95", "131.10"])
    desenhar_tabela(pdf, larguras_consumo, ["Abril", "160", "30", "5.33", "0.95", "152.00"])
    desenhar_tabela(pdf, larguras_consumo, ["Maio", "170", "31", "5.48", "0.95", "161.50"])
    desenhar_tabela(pdf, larguras_consumo, ["Junho", "158", "30", "5.27", "0.95", "150.10"])
    desenhar_tabela(pdf, larguras_consumo, ["Julho", "162", "31", "5.23", "0.95", "153.90"])
    desenhar_tabela(pdf, larguras_consumo, ["Agosto", "168", "31", "5.42", "0.95", "159.60"])
    desenhar_tabela(pdf, larguras_consumo, ["Setembro", "175", "30", "5.83", "0.95", "166.25"])
    desenhar_tabela(pdf, larguras_consumo, ["Outubro", "180", "31", "5.81", "0.95", "171.00"])
    desenhar_tabela(pdf, larguras_consumo, ["Novembro", "172", "30", "5.73", "0.95", "163.40"])
    desenhar_tabela(pdf, larguras_consumo, ["Dezembro", "165", "31", "5.32", "0.95", "156.75"])
    pdf.set_font("Arial", 'B', 8)
    desenhar_tabela(pdf, larguras_consumo, ["TOTAL", "1945", "365", "5.33", "0.95", "1847.75"])
    pdf.ln(5)

    # 2. Indicadores e Parâmetros
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "2. Parametros do Local e Projeto", ln=True)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(200, 8, "Parametros Base", ln=True)
    desenhar_tabela(pdf, [95, 95], ["Parametro", "Valor"], is_header=True)
    desenhar_tabela(pdf, [95, 95], ["Local de referencia", "Niteroi/RJ"])
    desenhar_tabela(pdf, [95, 95], ["Latitude / Longitude", "-22.901 graus / -43.049 graus"])
    desenhar_tabela(pdf, [95, 95], ["Irradiacao utilizada (kWh/m2.dia)", "4.98"])
    desenhar_tabela(pdf, [95, 95], ["Inclinacao / Orientacao recomendada", "~ 23 graus / Norte geografico"])
    pdf.ln(5)

    # 3. Especificação Técnica
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "3. Especificacao Tecnica dos Equipamentos", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 6, f"- Modelo do Modulo: {modelo_modulo}", ln=True)
    pdf.cell(200, 6, f"- Quantidade e Potencia: {n_modulos} un. de {potencia}Wp", ln=True)
    pdf.cell(200, 6, f"- Modelo do Inversor: {inversor}", ln=True)
    pdf.cell(200, 6, f"- Seccao do Cabo CC (Arranjo Solar): {cabo_cc} mm2", ln=True)
    pdf.cell(200, 6, f"- Seccao do Cabo CA (Rede Eletrica): {cabo_ca} mm2", ln=True)
    pdf.ln(3)

    pdf.set_font("Arial", 'B', 10)
    pdf.cell(200, 8, "Calculo de Energia e Paineis", ln=True)
    desenhar_tabela(pdf, [95, 95], ["Formula/Criterio", "Valor"], is_header=True)
    desenhar_tabela(pdf, [95, 95], ["Emod = G x A x n x PR", "1.93 kWh"])
    desenhar_tabela(pdf, [95, 95], ["N = Edia / Emod", "2.77 (Adotado 3 paineis)"])
    desenhar_tabela(pdf, [95, 95], ["Etot = n x G x A x n", "7.17 kWh"])
    pdf.ln(5)

    # Adiciona uma quebra de página manual para a validação elétrica não ficar cortada
    pdf.add_page()

    # 4. Tabela de Validação Elétrica do Inversor
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "4. Dimensionamento e Validacao Eletrica do Inversor", ln=True)
    
    desenhar_tabela(pdf, [65, 40, 40, 45], ["Parametro", "Formula", "Projeto", "Nominal Inversor"], is_header=True)
    desenhar_tabela(pdf, [65, 40, 40, 45], ["Potencia do arranjo CC [W]", "n x Pmax", "1440", "2100"])
    desenhar_tabela(pdf, [65, 40, 40, 45], ["Potencia Nominal CA [W]", "-", "1440", "1500"])
    desenhar_tabela(pdf, [65, 40, 40, 45], ["Tensao de Maxima Potencia [V]", "n x Vmp", "106.14", "50 V - 500 V"])
    desenhar_tabela(pdf, [65, 40, 40, 45], ["Tensao de Circuito Aberto [V]", "n x Voc", "128.13", "500"])
    desenhar_tabela(pdf, [65, 40, 40, 45], ["Tensao Maxima Corrigida [V]", "1.2 x Voc", "153.76", "500 V"])
    desenhar_tabela(pdf, [65, 40, 40, 45], ["Corrente de Curto-Circuito [A]", "Painel em serie", "14.31", "16"])
    desenhar_tabela(pdf, [65, 40, 40, 45], ["Corrente Majorada do Inversor [A]", "1.1 x Isc", "15.74", "16"])
    desenhar_tabela(pdf, [65, 40, 40, 45], ["Corrente de Projeto [A]", "1.25 x Isc", "17.89", "-"])
    desenhar_tabela(pdf, [65, 40, 40, 45], ["Corrente de Max. Potencia [A]", "Painel em serie", "13.57", "13"])
    desenhar_tabela(pdf, [65, 40, 40, 45], ["Numero de strings (serie)", "-", "1", "1"])
    desenhar_tabela(pdf, [65, 40, 40, 45], ["Numero de MPPTs Utilizadas", "-", "1", "1"])

    return pdf.output()

st.download_button("📥 Baixar Memorial Técnico Completo", data=gerar_memorial(), file_name="Memorial_Tecnico_Final.pdf", mime="application/pdf")
