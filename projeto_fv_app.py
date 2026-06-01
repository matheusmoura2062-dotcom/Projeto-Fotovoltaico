import streamlit as st
import pandas as pd
import numpy as np
import io
import altair as alt
from fpdf import FPDF, XPos, YPos
from pathlib import Path
 
# --- CONFIGURAÇÃO ---

st.set_page_config(page_title="Engenharia Solar Pro", layout="wide")
st.title("☀️ Sistema de Gestão de Projetos Fotovoltaicos")
 
# --- SIDEBAR ---

st.sidebar.header("Parâmetros do Projeto")
estado = st.sidebar.selectbox("Estado", options=[
    "AC – Acre",
    "AL – Alagoas",
    "AP – Amapá",
    "AM – Amazonas",
    "BA – Bahia",
    "CE – Ceará",
    "DF – Distrito Federal",
    "ES – Espírito Santo",
    "GO – Goiás",
    "MA – Maranhão",
    "MT – Mato Grosso",
    "MS – Mato Grosso do Sul",
    "MG – Minas Gerais",
    "PA – Pará",
    "PB – Paraíba",
    "PR – Paraná",
    "PE – Pernambuco",
    "PI – Piauí",
    "RJ – Rio de Janeiro",
    "RN – Rio Grande do Norte",
    "RS – Rio Grande do Sul",
    "RO – Rondônia",
    "RR – Roraima",
    "SC – Santa Catarina",
    "SP – São Paulo",
    "SE – Sergipe",
    "TO – Tocantins",
], index=1)  
 
cidade = st.sidebar.selectbox("Cidade", options=[
    "Angra dos Reis", 
    "Aperibé", 
    "Araruama", 
    "Areal",
    "Armação dos Búzios", 
    "Arraial do Cabo", 
    "Barra do Piraí",
    "Barra Mansa", 
    "Belford Roxo", 
    "Bom Jardim",
    "Bom Jesus do Itabapoana", 
    "Cabo Frio", 
    "Cachoeiras de Macacu",
    "Cambuci", 
    "Cantagalo", 
    "Carapebus", 
    "Cardoso Moreira", 
    "Carmo",
    "Casimiro de Abreu", 
    "Comendador Levy Gasparian",
    "Conceição de Macabu", 
    "Cordeiro", 
    "Duas Barras", 
    "Duque de Caxias",
    "Engenheiro Paulo de Frontin", 
    "Guapimirim", 
    "Iguaba Grande",
    "Itaboraí", 
    "Itaguaí", 
    "Italva", 
    "Itaocara", 
    "Itaperuna",
    "Itatiaia", 
    "Japeri", 
    "Laje do Muriaé", 
    "Macaé", 
    "Macuco", 
    "Magé",
    "Mangaratiba", 
    "Maricá", 
    "Mendes", 
    "Mesquita", 
    "Miguel Pereira",
    "Miracema", 
    "Natividade", 
    "Nilópolis", 
    "Niterói", 
    "Nova Friburgo",
    "Nova Iguaçu", 
    "Paracambi", 
    "Paraíba do Sul", 
    "Paraty",
    "Paty do Alferes", 
    "Petrópolis", 
    "Pinheiral", 
    "Piraí",
    "Porciúncula", 
    "Porto Real", 
    "Quatis", 
    "Queimados", 
    "Quissamã",
    "Resende", 
    "Rio Bonito", 
    "Rio Claro", 
    "Rio das Flores",
    "Rio das Ostras", 
    "Rio de Janeiro", 
    "Santa Maria Madalena",
    "Santo Antônio de Pádua", 
    "São Fidélis",
    "São Francisco de Itabapoana", 
    "São Gonçalo", 
    "São João da Barra",
    "São João de Meriti", 
    "São José de Ubá",
    "São José do Vale do Rio Preto", 
    "São Pedro da Aldeia",
    "São Sebastião do Alto", 
    "Sapucaia", 
    "Saquarema", 
    "Seropédica",
    "Silva Jardim", 
    "Sumidouro", 
    "Tangará", 
    "Tanguá", 
    "Teresópolis",
    "Trajano de Moraes", 
    "Três Rios", 
    "Valença", 
    "Varre-Sai",
    "Vassouras", 
    "Volta Redonda",
], index=1) 
 
local_instalacao = f"{cidade} / {estado}"
consumo = st.sidebar.number_input("Consumo Médio Mensal (kWh)", value=161.83, step=0.1)
tarifa           = st.sidebar.number_input("Tarifa (R$/kWh)", value=0.95, step=0.01)
 
st.sidebar.subheader("Especificações Técnicas")
modelo_modulo = st.sidebar.selectbox(
    "Modelo do Módulo",
    options=[
        "JKM460N-60HL4", 
        "JKM460N-60HL4-V",
        "JKM465N-60HL4",
        "JKM465N-60HL4-V", 
        "JKM470N-60HL4",
        "JKM470N-60HL4-V",
        "JKM475N-60HL4",
        "JKM475N-60HL4-V",
        "JKM480N-60HL4",       
        "JKM480N-60HL4-V",
    ],
    index=0  
)
potencia      = st.sidebar.number_input("Potência Painel (Wp)", value=480, step=1)
n_modulos     = st.sidebar.number_input("Quantidade de Módulos", value=3, step=1)
inversor      = st.sidebar.selectbox(
    "Modelo do Inversor",
    options=[
        "MIC 750TL-X",
        "MIC 1000TL-X",
        "MIC 1500TL-X",
        "MIC 2000TL-X",
        "MIC 2500TL-X",
        "MIC 3000TL-X",
        "MIC 3300TL-X",
    ],
    index=0  
)
cabo_cc       = st.sidebar.number_input("Secção Cabo CC (mm²)", value=4.0, step=0.25, format="%.2f")
cabo_ca       = st.sidebar.number_input("Secção Cabo CA (mm²)", value=2.5, step=0.25, format="%.2f")
 
st.sidebar.subheader("Composição de Custos")
custo_equip = st.sidebar.number_input("Custo Equipamentos (R$)", value=4000.0, step=100.0)
custo_serv  = st.sidebar.number_input("Custo Serviços (R$)", value=2000.0, step=100.0)
custo_total = custo_equip + custo_serv
 
# --- CÁLCULOS ---

geracao_ideal = (n_modulos * potencia * 4.98 * 30) / 1000
geracao_real  = geracao_ideal * 0.80
co2_evitado   = geracao_real * 12 * 0.09
payback       = custo_total / (geracao_real * tarifa) if (geracao_real * tarifa) > 0 else 0
 
# --- MÉTRICAS ---

c1, c2, c3, c4 = st.columns(4)
c1.metric("Potência Instalada", f"{(n_modulos * potencia) / 1000:.2f} kWp")
c2.metric("Geração Real",       f"{geracao_real:.1f} kWh/mês")
c3.metric("Payback",            f"{payback:.1f} meses")
c4.metric("CO2 Evitado",        f"{co2_evitado:.2f} kg/ano")
 
if payback > 60:
    st.warning(f"⚠️ Payback de {payback:.1f} meses: Considere ajustar custo ou eficiência.")
elif payback > 0:
    st.success(f"✅ Payback de {payback:.1f} meses: Viabilidade financeira atrativa.")
 
# --- GRÁFICO ---

st.subheader("Análise de Performance")
df_cenario = pd.DataFrame({
    'Cenário': ['Ideal', 'Real'],
    'Energia': [geracao_ideal, geracao_real]
})
chart = alt.Chart(df_cenario).mark_bar().encode(
    x=alt.X('Cenário', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Energia', title='Energia Gerada (kWh)'),
    color='Cenário'
).properties(width=600, height=400)
st.altair_chart(chart, use_container_width=True)
 
# --- UPLOAD DE FOTO ---

st.subheader("Análise de Campo")
uploaded_file = st.file_uploader(
    "Upload da foto do telhado (análise de sombreamento)",
    type=['png', 'jpg', 'jpeg']
)
if uploaded_file is not None:
    st.image(uploaded_file, caption=f'Local: {local_instalacao}',
             use_container_width=True)
 
 
# ═══════════════════════════════════════════════════════════════════════════
# FUNÇÕES DO PDF
# ═══════════════════════════════════════════════════════════════════════════
 
def linha(pdf, larguras, celulas, is_header=False, fill_color=None):
    """Desenha uma linha de tabela."""
    if is_header:
        pdf.set_font("DejaVu", 'B', 8)
        pdf.set_fill_color(180, 180, 180)
        fill = True
    elif fill_color:
        pdf.set_font("DejaVu", 'B', 8)
        pdf.set_fill_color(*fill_color)
        fill = True
    else:
        pdf.set_font("DejaVu", '', 8)
        pdf.set_fill_color(255, 255, 255)
        fill = True
    for i, (larg, texto) in enumerate(zip(larguras, celulas)):
        align = 'L' if i == 0 else 'C'
        pdf.cell(larg, 7, str(texto), border=1, fill=fill, align=align)
    pdf.ln()
 
 
def titulo_secao(pdf, texto):
    """Título de seção padronizado."""
    pdf.set_font("DejaVu", 'B', 12)
    pdf.cell(190, 10, texto, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
 
 
def subtitulo(pdf, texto):
    pdf.set_font("DejaVu", 'B', 10)
    pdf.cell(190, 8, texto, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
 
 
def item(pdf, texto):
    pdf.set_font("DejaVu", '', 10)
    pdf.cell(190, 6, texto, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
 
 
def gerar_memorial():
    pdf = FPDF()

   # Fonte Unicode (resolve acentos, traços, símbolo °, etc.)
   fonte = r"C:\Windows\Fonts\DejaVuSans.ttf"
   fonte_bold = r"C:\Windows\Fonts\DejaVuSans-Bold.ttf"

   pdf.add_font("DejaVu", "", fonte)
   pdf.add_font("DejaVu", "B", fonte_bold)

   pdf.add_page()
 
    # ── CABEÇALHO ──────────────────────────────────────────────────────────

    pdf.set_font("DejaVu", 'B', 16)
    pdf.cell(190, 10, "Memorial Descritivo e Financeiro",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.set_font("DejaVu", '', 11)
    pdf.cell(190, 7, f"Local: {local_instalacao}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(4)
 
    # ── SEÇÃO 1: RESUMO EXECUTIVO ──────────────────────────────────────────

    titulo_secao(pdf, "1. Resumo Executivo do Sistema")
    linha(pdf, [95, 95], ["Indicador", "Valor"], is_header=True)
    linha(pdf, [95, 95], ["Potencia Instalada (kWp)",     f"{(n_modulos * potencia)/1000:.2f} kWp"])
    linha(pdf, [95, 95], ["Geracao Ideal Mensal (kWh)",   f"{geracao_ideal:.1f} kWh/mes"])
    linha(pdf, [95, 95], ["Geracao Real Mensal (kWh)",    f"{geracao_real:.1f} kWh/mes"])
    linha(pdf, [95, 95], ["Tarifa Utilizada (R$/kWh)",    f"R$ {tarifa:.2f}"])
    linha(pdf, [95, 95], ["Investimento Total (R$)",      f"R$ {custo_total:.2f}"])
    linha(pdf, [95, 95], ["Payback Estimado",             f"{payback:.1f} meses"])
    linha(pdf, [95, 95], ["CO2 Evitado (kg/ano)",         f"{co2_evitado:.2f} kg/ano"])
    pdf.ln(4)
 
    # ── SEÇÃO 2: CONSUMO HISTÓRICO ─────────────────────────────────────────

    titulo_secao(pdf, "2. Historico de Consumo Anual")
    lc = [25, 30, 15, 45, 30, 45]
    linha(pdf, lc, ["Mes", "Consumo (kWh)", "Dias",
                    "Media Diaria (kWh/dia)", "Tarifa (R$)", "Conta Est. (R$)"],
          is_header=True)
    for d in [
        ["Janeiro","145","31","4.68","0.95","137.75"],
        ["Fevereiro","152","28","5.43","0.95","144.40"],
        ["Marco","138","31","4.45","0.95","131.10"],
        ["Abril","160","30","5.33","0.95","152.00"],
        ["Maio","170","31","5.48","0.95","161.50"],
        ["Junho","158","30","5.27","0.95","150.10"],
        ["Julho","162","31","5.23","0.95","153.90"],
        ["Agosto","168","31","5.42","0.95","159.60"],
        ["Setembro","175","30","5.83","0.95","166.25"],
        ["Outubro","180","31","5.81","0.95","171.00"],
        ["Novembro","172","30","5.73","0.95","163.40"],
        ["Dezembro","165","31","5.32","0.95","156.75"],
    ]:
        linha(pdf, lc, d)
    linha(pdf, lc, ["TOTAL","1945","365","5.33","0.95","1847.75"],
          fill_color=(220, 220, 220))
    pdf.ln(4)
 
    # ── SEÇÃO 3: PARÂMETROS DO LOCAL ───────────────────────────────────────
    titulo_secao(pdf, "3. Parametros do Local e Projeto")
    subtitulo(pdf, "Parametros Base")
    linha(pdf, [95, 95], ["Parametro", "Valor"], is_header=True)
    linha(pdf, [95, 95], ["Local de referencia", local_instalacao])
    linha(pdf, [95, 95], ["Latitude / Longitude",         "-22.901 / -43.049"])
    linha(pdf, [95, 95], ["Irradiacao (kWh/m2.dia)",      "4.98"])
    linha(pdf, [95, 95], ["Inclinacao / Orientacao",       "~23 graus / Norte"])
    pdf.ln(4)
 
    # ── SEÇÃO 4: ESPECIFICAÇÃO TÉCNICA ─────────────────────────────────────
    titulo_secao(pdf, "4. Especificacao Tecnica dos Equipamentos")
    item(pdf, f"- Modelo do Modulo: {modelo_modulo}")
    item(pdf, f"- Quantidade e Potencia: {n_modulos} un. de {potencia}Wp")
    item(pdf, f"- Modelo do Inversor: {inversor}")
    item(pdf, f"- Seccao do Cabo CC: {cabo_cc} mm2")
    item(pdf, f"- Seccao do Cabo CA: {cabo_ca} mm2")
    pdf.ln(3)
    subtitulo(pdf, "Calculo de Energia e Paineis")
    linha(pdf, [95, 95], ["Formula/Criterio", "Valor"], is_header=True)
    linha(pdf, [95, 95], ["Emod = G x A x n x PR",        "1.91 kWh"])
    linha(pdf, [95, 95], ["N = Edia / Emod",               "2.79 (Adotado 3 paineis)"])
    linha(pdf, [95, 95], ["Etot = N x Emod",         "5.74 kWh"])
    pdf.ln(4)
 
    # ── SEÇÃO 5: VALIDAÇÃO ELÉTRICA DO INVERSOR ────────────────────────────
    pdf.add_page()
    titulo_secao(pdf, "5. Dimensionamento e Validacao Eletrica do Inversor")
    li = [65, 40, 40, 45]
    linha(pdf, li, ["Parametro","Formula","Projeto","Nominal Inversor"], is_header=True)
    for d in [
        ["Potencia do arranjo CC [W]",    "n x Pmax",        "1440",  "2100"],
        ["Potencia Nominal CA [W]",        "-",               "1500",  "1500"],
        ["Tensao de Maxima Potencia [V]",  "n x Vmp",         "106.14","50-500 V"],
        ["Tensao de Circuito Aberto [V]",  "n x Voc",         "128.13","500"],
        ["Tensao Maxima Corrigida [V]",    "1.2 x Voc",       "153.76","500 V"],
        ["Corrente de Curto-Circuito [A]", "Painel em serie", "14.31", "16"],
        ["Corrente Majorada [A]",          "1.1 x Isc",       "15.74", "16"],
        ["Corrente de Projeto [A]",        "1.25 x Isc",      "17.89", "-"],
        ["Corrente de Max. Potencia [A]",  "Painel em serie", "13.57", "13"],
        ["Numero de strings (serie)",      "-",               "1",     "1"],
        ["Numero de MPPTs Utilizadas",     "-",               "1",     "1"],
    ]:
        linha(pdf, li, d)
    pdf.ln(4)
 
    # ── SEÇÃO 6: DPS ───────────────────────────────────────────────────────

    titulo_secao(pdf, "6. Dimensionamento dos Dispositivos de Protecao contra Surtos (DPS)")
 
    # Cabeçalho duplo (CC / CA com sub-colunas Projeto / Selecionado)

    ld = [60, 30, 30, 35, 35]

    # linha 1 do cabeçalho (grupos)

    pdf.set_font("DejaVu", 'B', 8)
    pdf.set_fill_color(180, 180, 180)
    pdf.cell(60, 7, "Criterio",        border=1, fill=True)
    pdf.cell(60, 7, "Valores (CC)",    border=1, fill=True, align='C')
    pdf.cell(70, 7, "Valores (CA)",    border=1, fill=True, align='C')
    pdf.ln()

    # linha 2 do cabeçalho (sub-colunas)

    pdf.cell(60, 7, "",                border=1, fill=True)
    pdf.cell(30, 7, "Projeto",         border=1, fill=True, align='C')
    pdf.cell(30, 7, "Selecionado",     border=1, fill=True, align='C')
    pdf.cell(35, 7, "Projeto",         border=1, fill=True, align='C')
    pdf.cell(35, 7, "Selecionado",     border=1, fill=True, align='C')
    pdf.ln()
 
    for d in [
        ["Tensao maxima da string (Voc)",   "128,13 V", "—",         "127 V",    "—"],
        ["Tensao da rede",                  "—",        "—",         "220 V",    "—"],
        ["Tensao corrigida (1,2 x Voc)",    "153,76 V", "—",         "139,7 V",  "—"],
        ["Tensao maxima continua (UcPV)",   "> 153,76 V","600 Vcc",  "> 139,7 V","275 Vca"],
        ["Classe",                          "Tipo II",  "Tipo II",   "Tipo II",  "Tipo II"],
        ["Corrente nominal (In)",           "—",        "20 kA",     "—",        "20 kA"],
        ["Corrente maxima (Imax)",          "—",        "40 kA",     "—",        "40 kA"],
        ["Aplicacao FV",                    "Obrig.",   "Sim",       "Obrig.",   "Sim"],
        ["Situacao Final",                  "—",        "Conforme",  "—",        "Conforme"],
        ["DPS escolhido",                   "CLAMPER Solar SB 600 Vcc", "", "CLAMPER Front 275 V", ""],
    ]:
        linha(pdf, ld, d)
    pdf.ln(4)
 
    # ── SEÇÃO 7: ESPECIFICAÇÕES DOS CONDUTORES ─────────────────────────────

    titulo_secao(pdf, "7. Especificacoes dos Condutores")
    le = [70, 60, 60]
    linha(pdf, le, ["Caracteristica", "Cabo CC", "Cabo CA"], is_header=True)
    for d in [
        ["Fabricante",                  "SIL",                  "Prysmian"],
        ["Linha",                       "AtoxSil",              "Afumex Green"],
        ["Secao",                       "4,0 mm2",              "2,5 mm2"],
        ["Aplicacao",                   "Baixa tensao CC",      "Baixa tensao CA"],
        ["Material condutor",           "Cobre estanhado",      "Cobre eletrolitico"],
        ["Classe",                      "5 (flexivel)",         "5 (flexivel)"],
        ["Isolamento",                  "XLPO Termofixo",       "HEPR"],
        ["Tensao Nominal",              "1,8 kVcc",             "450 V - 750 V"],
        ["Temperatura Max. (regime)",   "90 °C",                "90 °C"],
        ["Nao propagante de chama",     "Sim",                  "Sim"],
        ["Livre de halogenios",         "Sim",                  "Sim"],
        ["Dupla isolacao",              "Sim",                  "Nao"],
        ["Protecao UV",                 "Sim",                  "Nao exigido"],
        ["Norma aplicavel",             "NBR 16612 e NBR 16690","NBR 5410 e NBR 13248"],
    ]:
        linha(pdf, le, d)
    pdf.ln(4)
 
    # ── SEÇÃO 8: DIMENSIONAMENTO DA STRING ─────────────────────────────────

    titulo_secao(pdf, "8. Dimensionamento da String")
    ls = [80, 60, 50]
    linha(pdf, ls, ["Parametros Eletricos (string)", "Formula/Criterio", "Valor"],
          is_header=True)
    for d in [
        ["Numero de Modulos",                    "-",            "3"],
        ["Corrente de Curto-Circuito [A]",       "Painel em serie", "14,31"],
        ["Corrente de Projeto [A]",              "1,25 x Isc",  "17,89"],
        ["Tensao de Circuito Aberto [V]",        "n x Voc",     "128,13"],
        ["Tensao Maxima Corrigida [V]",          "1,2 x Voc",   "153,756"],
        ["Distancia modulos-inversor [m]",       "—",           "15 (30 ida e volta)"],
        ["Corrente CA de Projeto [A]",           "P / V",       "6,82"],
        ["Distancia inversor-quadro [m]",          "—",           "10 (20 ida e volta)"],
    ]:
        linha(pdf, ls, d)
    pdf.ln(4)
 
    # ── SEÇÃO 9: VALIDAÇÃO TÉCNICA DOS CABOS ───────────────────────────────

    titulo_secao(pdf, "9. Validacao Tecnica dos Cabos (Comparativo)")
    lv = [60, 65, 65]
    linha(pdf, lv, ["Criterio", "CC", "CA"], is_header=True)
    for d in [
        ["Cabo",                    "SIL Atox 4 mm2",           "Afumex 2,5 mm2"],
        ["Corrente (Projeto/Cabo)", "17,89 A vs 40 A (OK)",     "6,82 A vs 31 A (OK)"],
        ["Tensao (Projeto/Cabo)",   "153,76 V vs 1800 V (OK)",  "220 V vs 750 V (OK)"],
        ["Metodo de Instalacao",    "B2 (aparente)",            "B1 (embutido)"],
        ["Norma/Exigencia",         "Atende NBR 16612",         "Atende NBR 5410"],
    ]:
        linha(pdf, lv, d)
    pdf.ln(4)
 
    # ── SEÇÃO 10: QUEDA DE TENSÃO ────────────────────────────────────────────

    titulo_secao(pdf, "10. Memoria de Calculo da Queda de Tensao")
    lq = [70, 60, 60]
    linha(pdf, lq, ["Etapa", "CC (cabo 4 mm2)", "CA (cabo 2,5 mm2)"],
          is_header=True)
    linha(pdf, lq, ["Formula",
                    "DV = (2 x L x Iv x rho) / S",
                    "DV = (2 x L x Iv x rho) / S"])
    linha(pdf, lq, ["Queda de Tensao (DV)",    "2,24 V",   "1,20 V"])
    linha(pdf, lq, ["Queda Percentual (DV%)",  "2,11 %",   "0,55 %"])
    linha(pdf, lq, ["Resultado (Limite 4%)",   "OK",       "OK"])
    pdf.ln(4)
 
    return bytes(pdf.output())
 
 
# --- BOTÃO PDF ---

st.write("---")
if st.button("📄 Gerar Memorial Técnico"):
    with st.spinner("Gerando PDF..."):
        try:
            pdf_bytes = gerar_memorial()
            st.download_button(
                label="📥 Baixar Memorial Técnico (PDF)",
                data=io.BytesIO(pdf_bytes),
                file_name="Memorial_Tecnico_Final.pdf",
                mime="application/pdf",
                key="dl_memorial"
            )
            st.success("✅ PDF gerado com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao gerar PDF: {type(e).__name__}: {e}")
 
