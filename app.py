import sys
import streamlit as st
from datetime import datetime

# Lista de granolas
granolas = [
    "Clásica",
    "Completa",
    "Choco",
    "Completa con Frutas",
    "Mix Brasil",
    "Mix Picada",
    "Mix Especial",
    "Mix Salado",
    "Mix Pro"
]

st.title("Calculadora de Precios de Granola")

# Diccionarios para almacenar los precios y resultados
precios = {}
sobrecostos = {}
precios_con_rentabilidad = {}

st.header("Ingresar precios")

for granola in granolas:
    st.subheader(granola)
    precio_medio_kilo = st.number_input(f"Precio de medio kilo de {granola}", min_value=0.0, format="%.2f")
    precio_kilo = st.number_input(f"Precio de kilo por mayor de {granola}", min_value=0.0, format="%.2f")
    precios[granola] = {
        "medio_kilo": precio_medio_kilo,
        "kilo": precio_kilo
    }

if st.button("Calcular"):
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    texto_sobrecostos = f"Sobrecostos calculados el {fecha_actual}:\n\n"
    texto_precios_rentabilidad = f"Precios con 45% de rentabilidad calculados el {fecha_actual}:\n\n"

    for granola in granolas:
        medio_kilo = precios[granola]["medio_kilo"]
        kilo = precios[granola]["kilo"]

        if kilo == 0:
            st.error(f"El precio de kilo por mayor de {granola} no puede ser cero.")
            continue

        # Cálculo del sobrecosto de comprar 2 medios kilos en lugar de 1 kilo
        costo_2_medios = medio_kilo * 2
        sobrecosto_2_medios = ((costo_2_medios - kilo) / kilo) * 100

        # Cálculo del sobrecosto de comprar 4 medios kilos en lugar de 2 kilos
        # Asumimos que el precio de 2 kilos es el doble del precio de 1 kilo
        costo_4_medios = medio_kilo * 4
        costo_2_kilos = kilo * 2
        sobrecosto_4_medios = ((costo_4_medios - costo_2_kilos) / costo_2_kilos) * 100

        # Como no tenemos un precio mayorista especial para 2 kilos, asumimos que no hay sobrecosto adicional
        sobrecosto_2_kilos = 0  # Puedes ajustar esto si lo necesitas

        sobrecostos[granola] = {
            "2_medios_vs_1_kilo": sobrecosto_2_medios,
            "4_medios_vs_2_kilos": sobrecosto_4_medios,
            "2_kilos_vs_mayorista": sobrecosto_2_kilos
        }

        # Aplicar 45% de rentabilidad
        rentabilidad = 1.45
        precio_medio_kilo_rent = medio_kilo * rentabilidad
        precio_kilo_rent = kilo * rentabilidad
        precios_con_rentabilidad[granola] = {
            "medio_kilo": precio_medio_kilo_rent,
            "kilo": precio_kilo_rent
        }

        # Agregar al texto
        texto_sobrecostos += f"{granola}:\n"
        texto_sobrecostos += f"- Sobrecosto de 2 medios kilos vs 1 kilo: {sobrecosto_2_medios:.2f}%\n"
        texto_sobrecostos += f"- Sobrecosto de 4 medios kilos vs 2 kilos: {sobrecosto_4_medios:.2f}%\n"
        texto_sobrecostos += f"- Sobrecosto de 2 kilos vs mayorista: {sobrecosto_2_kilos:.2f}%\n\n"

        texto_precios_rentabilidad += f"{granola}:\n"
        texto_precios_rentabilidad += f"- Precio medio kilo con rentabilidad: ${precio_medio_kilo_rent:.2f}\n"
        texto_precios_rentabilidad += f"- Precio kilo con rentabilidad: ${precio_kilo_rent:.2f}\n\n"

    # Mostrar resultados en la aplicación
    st.header("Resultados de Sobrecostos")
    st.text(texto_sobrecostos)

    st.header("Precios con 45% de Rentabilidad")
    st.text(texto_precios_rentabilidad)

    # Generar archivos de texto para descargar
    st.download_button(
        label="Descargar Sobrecostos (.txt)",
        data=texto_sobrecostos,
        file_name="sobrecostos.txt",
        mime="text/plain"
    )

    st.download_button(
        label="Descargar Precios con Rentabilidad (.txt)",
        data=texto_precios_rentabilidad,
        file_name="precios_con_rentabilidad.txt",
        mime="text/plain"
    )
