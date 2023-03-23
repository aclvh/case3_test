#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st


# In[ ]:


def intro():
    import streamlit as st

    st.write("""# Case 3 – Van data naar informatie:
             Een dashboard over elektrisch mobiliteit en laadpalen""")

    st.markdown(
    """
    Streamlit is een open-source app framework wat specifiek is gemaakt voor
    Machine Learning en Data Science projecten.
    In dit project is een dashboard gemaakt over elektrisch mobiliteit en laadpalen.
    Deze is gemaakt aan de hand van meerdere datasets:
    * Een dataset die verkregen is via OpenChargeMap
    * Laadpaaldata.csv (gekregen van docenten van de HvA)
    * 2 Datasets van de RDW
        1. Open-Data-RDW-Gekentekende_voertuigen
        2. Open-Data-RDW-Gekentekende_voertuigen_brandstof
    
    Om vervolgens meer informatie over het project te lezen
    
    **👈 Selecteer dan een keuze uit de balk hiernaast**.""")


# In[ ]:


def OpenChargeMap():
    import streamlit as st
    import pandas as pd
    import requests
    
    # Informatie over wat er te lezen is op deze pagina
    st.write("""
        # Laadpaaldata OpenChargeMap
        Op deze pagina is informatie te lezen over de informatie die is verkregen uit de dataset die is verkregen
        met behulp van de OpenChargeMap.""")
    
    Laadpalen = pd.read_csv("Laadpalen.csv")
    Laadpalen.head()

    st.write(Laadpalen.head(3))
    


# In[ ]:


def laadpaaldata():
    import streamlit as st
    import pandas as pd
    import plotly.figure_factory as ff
    
    # Informatie over wat er te lezen is op deze pagina
    st.write("""
        # Laadpaaldata.csv
        Op deze pagina is informatie te lezen over de informatie die is verkregen uit de dataset Laadpaaldata.csv
        die is gedeeld door de HvA docenten van de minor Data Science.""")
    
    laadpalen = pd.read_csv('laadpaaldata.csv')
    laadpalen.head()
    st.write(laadpalen.head())
    
    laadpalen_met_drop = pd.read_csv('laadpalen_met_drop.csv')
    laadpalen_zonder_drop = pd.read_csv('laadpalen_zonder_drop.csv')
    
    #############################################################################################
    # Plot verdeling laaddtijden met extremen
    #############################################################################################
    
    # Het gemmidelde en de mediaan worden hier bepaald met de data met outliers
    median_charge_zonder = laadpalen_zonder_drop['ChargeTime'].median()
    mean_charge_zonder = laadpalen_zonder_drop['ChargeTime'].mean()
    median_connected_zonder = laadpalen_zonder_drop['ConnectedTime'].median()
    mean_connected_zonder = laadpalen_zonder_drop['ConnectedTime'].mean()
    
    # Add histogram data
    x1 = laadpalen_zonder_drop["ChargeTime"]
    x2 = laadpalen_zonder_drop["ConnectedTime"]

    # Group data together
    hist_data = [x1, x2]

    group_labels = ["Laad tijd", "Aangesloten tijd"]
    colors = ['#A6ACEC', '#F66095']

    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data,
                             group_labels,
                             bin_size = .2,
                             colors = colors)

    fig.update_layout(title_text = "Verdeling laadtijden (met extreme tijden)",
                     xaxis_title = "Aantal uren",
                     yaxis_title = "Kans")

    annotation1 = {"xref":"paper",
                  "yref":"paper",
                  "x":1.00,
                  "y":1,
                  "showarrow":False,
                  "text": "Mediaan chargetime: " + str(round(median_charge_zonder,2)) + " gemiddelde chargetime: " +
                  str(round(mean_charge_zonder,2))}

    annotation2 = {"xref":"paper",
                  "yref":"paper",
                  "x":1.0,
                  "y":0.9,
                  "showarrow":False,
                  "text": "Mediaan connectedtime: " + str(round(median_connected_zonder,2)) + " gemiddelde connectedtime: " +
                  str(round(mean_connected_zonder,2))}

    # Add an annotation and show
    fig.update_layout({"annotations":[annotation1, annotation2]})
    st.plotly_chart(fig)
    
    #############################################################################################
    # Plot verdeling laaddtijden zonder extremen
    #############################################################################################
    
    # Het gemmidelde en de mediaan worden hier bepaald met de data zonder outliers
    median_charge = laadpalen_met_drop["ChargeTime"].median()
    mean_charge = laadpalen_met_drop["ChargeTime"].mean()
    median_connected = laadpalen_met_drop["ConnectedTime"].median()
    mean_connected = laadpalen_met_drop["ConnectedTime"].mean()
    
    # Add histogram data
    x1 = laadpalen_met_drop["ChargeTime"]
    x2 = laadpalen_met_drop["ConnectedTime"]

    # Group data together
    hist_data = [x1, x2]

    group_labels = ["Laad tijd", "Aangesloten tijd"]
    colors = ["#A6ACEC", "#F66095"]

    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data,
                             group_labels,
                             bin_size = .2,
                             colors = colors)

    fig.update_layout(title_text = "Verdeling laadtijden (zonder extreme tijden)",
                     xaxis_title = "Aantal uren",
                     yaxis_title = "Kans")

    annotation1 = {"xref":"paper",
                  "yref":"paper",
                  "x":1.00,
                  "y":1,
                  "showarrow":False,
                  "text": "Mediaan chargetime: " + str(round(median_charge,2)) + " gemiddelde chargetime: " +
                  str(round(mean_charge,2))}

    annotation2 = {"xref":"paper",
                  "yref":"paper",
                  "x":1.0,
                  "y":0.9,
                  "showarrow":False,
                  "text": "Mediaan connectedtime: " + str(round(median_connected,2)) + " gemiddelde connectedtime: " +
                  str(round(mean_connected,2))}

    # Add an annotation and show
    fig.update_layout({"annotations":[annotation1, annotation2]})
    st.plotly_chart(fig)
    


# In[ ]:


def rdw_data():
    import streamlit as st
    
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.linear_model import LinearRegression
    
    # Informatie over wat er te lezen is op deze pagina
    st.write("""
        # Datasets van de RDW
        Op deze pagina is informatie te lezen over de informatie die is verkregen uit de twee gekozen datasets
        van de RDW:
        1. Open-Data-RDW-Gekentekende_voertuigen
        2. Open-Data-RDW-Gekentekende_voertuigen_brandstof
        
        Aangezien de datasets bestaan uit respectievelijk 15.1 miljoen rijen met 92 kolommen en 14.4 miljoen rijen met
        36 kolommen kan een normale laptop dit vanwege de grootte niet inladen.
        
        Om deze bestanden te kunnen gebruiken zijn een aantal kolommen geselecteerd die nodig waren voor specifieke
        grafieken om de bestanden wel in te kunnen laden, aangezien de bestanden dan minder groot zijn.
        Ook is gefilterd op enkel de voertuigsoort, 'personenauto'.
        Op deze manier kunnen de benodigde kolommen en rijen van de datasets wel ingeladen en samengevoegd worden.
        Vervolgens wordt het samengevoegde bestand omgezet naar een csv bestand, zodat werken met de dataset sneller
        gaat.""")
        
    ######################################################################################
    # Plot crikeldiagram brandstof omschrijving
    ######################################################################################
    
    st.write("""
        ## Cirkel diagram van het type aandrijving
        Deze cirkel diagram laat zien welke soort aandrijving het meest is voorgekomen. 
        Zo is te zien dat benzine aangedreven auto's het meeste voorkomen over de jaren heen. 
        Hierop volgen de elektrisch auto's en de diesel auto's. Verder is te zien dat er nog een aantal kleine groepen 
        zijn met een ander type krachtbron die in kleine hoeveelheden voorkomen.""")
    
    df_cirkel = pd.read_csv('df_cirkel.csv')
    
    #cirkel diagram van brandstof omschrijving
    fig_cirkel = px.pie(df_cirkel,
                        values = "Hoeveelheid", 
                        names = "Type brandstof")

    fig_cirkel.update_layout(title = "Aantal verkochte auto's per brandstof omschrijving (vanaf 1950 tot heden)",
                             legend_title = "Brandstof omschrijving")

    st.plotly_chart(fig_cirkel)
    
    ######################################################################################
    # Plot 1 met cum aantal auto's per brandstof omschrijving
    ######################################################################################
    
    st.write("""
        ## Lijndiagram van het aantal auto's per type aandrijving
        Deze lijndiagram geeft net zoals in het cirkel diagram ook het type aandrijving weer die het meest voorkomt 
        in Nederland. Hierbij is een slider toegevoegd dat over de tijd heen weergeeft welke soort 
        aandrijving het meeste voor is gekomen. Ook hier kan uit worden opgehaald dat benzine auto's het meest
        dominant is in Nederland.""")
    
    df_fig1 = pd.read_csv("df_fig1.csv")
    
    fig1 = px.line(df_fig1,
               y = "cum aantal",
               x = "datum",
               color = "brandstof_omschrijving")

    fig1.update_layout(title = "Cumulatief aantal auto's per brandstofsoort",
                   xaxis_title = "Datum",
                   yaxis_title = "Aantal auto's",
                   legend_title = "Brandstof soort",
                   xaxis = dict(rangeslider = dict(visible = True)))
    
    st.plotly_chart(fig1)
    
    ######################################################################################
    # Plot met top 10 vrekochte merken elektrische auto's
    ######################################################################################
    
    st.write("""
        ## Histogram van het aantal elektrische auto's voor de top 10 auto merken 
        Deze histogram laat de hoeveelheid geproduceerde elektrische auto's zien van auto merken. 
        Dit zijn de top 10 automerken die de meeste elektrische auto's hebben geproduceerd, gebasseerd op de gegeven data van RDW. 
        Zo is te zien dat Toyota een groter deel uit maakt van de totale hoeveelheid elektrische auto's.""")
    
    df_merk = pd.read_csv("df_merk.csv")
    
    fig_merk = px.histogram(df_merk,
                        x = "merk",
                        y = 'aantal_verkocht')

    fig_merk.update_layout(title = "Cumulatief aantal auto's per merk",
                           xaxis_title = "Auto merk",
                           yaxis_title = "Aantal auto's",
                           legend_title = 'Auto merk')

    st.plotly_chart(fig_merk)
    
    ######################################################################################
    # Plot met cum aantal auto's per brandstof omschrijving
    ######################################################################################
    st.write("""
        ## Lijndiagram van verschillende auto merken
        In deze lijndiagram is het aantal auto's te zien van 10 auto merken die het meeste voorkomen. 
        Dit geeft een beeld weer welke auto merken het meest populair zijn in Nederland.""")
    
    df_fig2 = pd.read_csv("df_fig2.csv")
    
    fig2 = px.line(df_fig2,
               y = "cum aantal",
               x = "datum",
               color = "merk")

    fig2.update_layout(title = "Cumulatief aantal auto's per merk",
                   xaxis_title = "Datum",
                   yaxis_title = "Aantal auto's",
                   legend_title = "Merk",
                   xaxis = dict(rangeslider = dict(visible = True)))
    
    st.plotly_chart(fig2)
    
    ######################################################################################
    # Regressiemodel met 2 losse plotjes
    ######################################################################################
    
    st.write("""
        ## Regressie tussen emissiecode en cilinder inhoud
        De regressie tussen de emissiecode en de cilinderinhoud is een verband die is bedacht vanwege 
        de gedachte dat een grotere inhoud van de cilinders zou resulteren naar meer verbruik van brandstof. 
        In de diagram is ook een positieve regressielijn te zien. Dit geeft aan dat er dus een verband is tussen 
        de uitstoot van de auto en de cilinder inhoud. In deze diagram zijn de elektrische auto's en waterstof 
        auto's uit de dataset gehaald. Dit omdat elektrische en waterstof auto's niet aangedreven worden met cilinders.""")
    
    df_model = pd.read_csv("df_model.csv")
    
    fig_model1 = px.scatter(df_model,
                        x = "emissiecode_omschrijving",
                        y ="cilinderinhoud",
                        opacity = 0.65,
                        trendline = "ols",
                        trendline_color_override = "red")

    fig_model1.update_layout(title = "Regressie tussen de emissiecode en de cilinderinhoud",
                             xaxis_title = "Emissiecode omschrijving",
                             yaxis_title = "Cilinderinhoud")

    st.plotly_chart(fig_model1)
    
    st.write("""
        ## Regressie tussen cilinders en cilinder inhoud
        In deze diagram is weergegeven wat de verhoudingen zijn tussen de hoeveelheid cilinders en de inhoud 
        van alle cilinders. Er is een verband te zien waarin de cilinderinhoud vergroot met de hoeveelheid 
        cilinders. Ook voor deze diagram zijn de elektrische auto's en waterstof auto's uit de dataset gehaald.""")    
    
    
    fig_model2 = px.scatter(df_model,
                        x = "aantal_cilinders",
                        y = "cilinderinhoud",
                        trendline = "ols",
                        trendline_color_override = "red")

    fig_model2.update_layout(title = "Regressie tussen het aantal cilinders en de cilinderinhoud",
                             xaxis_title = "Aantal cilinders",
                             yaxis_title = "Cilinderinhoud")

    st.plotly_chart(fig_model2)
    
    ######################################################################################
    # Regressiemodel uitvoeren
    ######################################################################################
    
    # Een aantal kentekens en bijbehorende waarden inladen om het model uit te kunnen voeren
    df_kenteken = pd.read_csv("df_kenteken.csv")

    # Deel kentekens en bijbehorende waarden tonen
    deel_df_kenteken = df_kenteken.sort_values("emissiecode_omschrijving").iloc[30:40][:]
    st.write(deel_df_kenteken.head(10))
    
    # Kenteken invoeren
    kenteken = st.text_input("Kenteken", "0050PK")
    st.write("Het ingevoerde kenteken is: ", kenteken)
    
    # Het model
    X = df_model[["emissiecode_omschrijving","aantal_cilinders"]]
    y = df_model["cilinderinhoud"]
    reg = LinearRegression().fit(X.values, y.values)
    
    rij_kenteken = df_kenteken[df_kenteken["kenteken"] == kenteken]
    emissiecode = float(rij_kenteken.iloc[0]["emissiecode_omschrijving"])
    aantal_cilinders = rij_kenteken.iloc[0]["aantal_cilinders"]
    
    voorspelling_cilinderinhoud = reg.predict(np.array([[emissiecode, aantal_cilinders]]))[0]
    echte_cilinderinhoud = rij_kenteken.iloc[0]["cilinderinhoud"]
    
    # Voorspelling
    st.write("De voorspelde cilinderinhoud is:", voorspelling_cilinderinhoud)
    st.write("De echte cilinderinhoud is:", echte_cilinderinhoud)
    
    # Uitleg model
    regressiescore = reg.score(X.values, y.values)
    reg_emissie = reg.coef_[0]
    reg_cil = reg.coef_[1]
    intercept = reg.intercept_
    
    st.write("## Extra informatie over het regressiemodel")
    st.write("Het model heeft een regressiescore", regressiescore, "en bevat de volgende parameters:")
    st.write("* De regressiecoëfficiënt van 'emissiecode_omschijving' is:", reg_emissie)
    st.write("* De regressiecoëfficiënt van 'aantal_cilinders' is:", reg_cil)
    st.write("* Het snijpunt bij de y-as is:", intercept)


# In[ ]:


page_names_to_funcs = {
    "Opdrachtomschrijving": intro,
    "Laadpaaldata OpenChargeMap": OpenChargeMap,
    "Laadpaaldata.csv": laadpaaldata,
    "Datasets van de RDW": rdw_data}

demo_name = st.sidebar.selectbox("Kies een pagina", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()

