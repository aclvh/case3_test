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
    from streamlit_folium import st_folium
    import folium
    
    # Informatie over wat er te lezen is op deze pagina
    st.write("""
        # Laadpaaldata OpenChargeMap
        Op deze pagina is informatie te lezen over de informatie die is verkregen uit de dataset die is verkregen
        met behulp van de OpenChargeMap.
        """)
        
    st.write("""
        Eerst is er een data analyse gedaan over de gehele dataset. Aangezien het doel was om een kaart te tonen van een
        gebied naar keuze waarin de laadpunten weergegeven worden, is er een data selectie gemaakt van de data die hiervoor
        nodig is. Er is gekeken naar provinciale data zodat het aantal laadpalen per gebied gekoppeld konden worden aan 
        de provincie, helaas ontbrak hier teveel data voor. Daaorm is gekozen om op basis van postcode, postcode groepen
        te maken. Aan de hand hiervan is te zien hoeveel laadpalen er per postcode groep is. Hieronder is een head te zien
        van de gemaakte dataset. Ook is data cleaning uitgevoerd op deze dataset.
        """)
    
    Laadpalen = pd.read_csv("Laadpalen.csv")
    st.write(Laadpalen.head(3))
  

    st.write("""
        ## Kaart met laadpalen
        Op de kaart die hieronder getoond wordt zijn alle laadpalen te zien in Nederland.
        De kleur geeft aan waar in Nederland veel of weinig laadpalen zijn. Wanneer de stipjes per laadpaal groen zijn,
        betekend dat er in diezelfde postcode soort veel laadpalen zijn. Hoe roder het stipje wordt,
        hoe minder laadpalen er in de postcode groep zullen zijn.

        De kaart is gemaakt m.b.v. folium.
        """)
    
    ####################################################################################################################

    def add_categorical_legend(folium_map, title, colors, labels):
        if len(colors) != len(labels):
            raise ValueError("colors and labels must have the same length.")

        color_by_label = dict(zip(labels, colors))
        
        legend_categories = ""     
        for label, color in color_by_label.items():
            legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
        legend_html = f"""
        <div id='maplegend' class='maplegend'>
          <div class='legend-title'>{title}</div>
          <div class='legend-scale'>
            <ul class='legend-labels'>
            {legend_categories}
            </ul>
          </div>
        </div>
        """
        script = f"""
            <script type="text/javascript">
            var oneTimeExecution = (function() {{
                        var executed = false;
                        return function() {{
                            if (!executed) {{
                                 var checkExist = setInterval(function() {{
                                           if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                              document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                              document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                              document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                              clearInterval(checkExist);
                                              executed = true;
                                           }}
                                        }}, 100);
                            }}
                        }};
                    }})();
                oneTimeExecution()
        </script>
          """
   

        css = """
    
        <style type='text/css'>
          .maplegend {
            z-index:9999;
            float:right;
            background-color: rgba(255, 255, 255, 1);
            border-radius: 5px;
            border: 2px solid #bbb;
            padding: 10px;
            font-size:12px;
            positon: relative;
          }
          .maplegend .legend-title {
            text-align: left;
            margin-bottom: 5px;
            font-weight: bold;
            font-size: 90%;
            }
          .maplegend .legend-scale ul {
            margin: 0;
            margin-bottom: 5px;
            padding: 0;
            float: left;
            list-style: none;
            }
          .maplegend .legend-scale ul li {
            font-size: 80%;
            list-style: none;
            margin-left: 0;
            line-height: 18px;
            margin-bottom: 2px;
            }
          .maplegend ul.legend-labels li span {
            display: block;
            float: left;
            height: 16px;
            width: 30px;
            margin-right: 5px;
            margin-left: 0;
            border: 0px solid #ccc;
            }
          .maplegend .legend-source {
            font-size: 80%;
            color: #777;
            clear: both;
            }
          .maplegend a {
            color: #777;
            }
        </style>
        """

        folium_map.get_root().header.add_child(folium.Element(script + css))

        return folium_map

    #########################################################################################################################

    def kleuren(type):
    
        if type > 1200:
            return "green"
        elif type > 1000:
            return "lime"
        elif type > 800:
            return "greenyellow"
        elif type > 600:
            return "yellow"
        elif type > 400:
            return "darkorange"
        elif type > 200:
            return "red"
        else:
            return "darkred"
    
    ################################################################################################################
    
    locatiedata = pd.DataFrame(data = {'Plaats': ['Nederland', 'Amsterdam', 'Utrecht'],
                                       'Locatie': [1,2,3]})

    locatiedata['Locatie'] = locatiedata['Locatie'].astype('object')
    locatiedata.at[0, 'Locatie'] = [[50.5, 5.4],[54.2, 4.66]]
    locatiedata.at[1, 'Locatie'] = [[52.35, 4.9],[52.4, 4.91]]
    locatiedata.at[2, 'Locatie'] = [[52.07, 5.10],[52.11, 5.15]]
    
    InvoerLocatie = st.selectbox("# Selecteer een locatie:", ("Nederland", "Amsterdam", "Utrecht"))
    
    long_lat = locatiedata[locatiedata['Plaats'] == InvoerLocatie]['Locatie']
    
    
    if InvoerLocatie == 'Utrecht':
        locatie = long_lat[2]
    elif InvoerLocatie == 'Amsterdam':
        locatie = long_lat[1]
    else:
        locatie = long_lat[0]
    
    m = folium.Map(tiles = 'cartodbpositron')
    
    m.fit_bounds(locatie)
    

    for index, row in Laadpalen.iterrows():
    
        color_circle = kleuren(row['Aantal_Laadpalen'])
        marker=(folium.CircleMarker(location =[row['AddressInfo.Latitude'], row['AddressInfo.Longitude']],
                                    popup = row["Postcode_Groep"],
                                    radius = 1,
                                    color = color_circle))
        marker.add_to(m)
    

        m = add_categorical_legend(m,
                               'Aantal laadpalen per postcode groep',
                               colors = ['green', 'lime', 'greenyellow', 'yellow', 'darkorange',
                                         'red', 'darkred'],
                               labels = ['> 1200', '> 1000', '> 800', '> 600', '> 400',
                                         '> 200', '0-200'])

    st_data = st_folium(m, width = 725)
    
    st.write("""
        ## Conclusie
        Op de kaart is duidelijk te zien dat hoe dichter men bij de randstad komt hoe meer laadpalen er zullen zijn in
        het gebied. Een logische uitkomst aangezien de randstad dichterbevolkt is, en de aanname gemaakt kan worden dat
        hierdoor dus meer elektrische auto's zullen rijden in deze gebieden. Die natuurlijk allemaal opgeladen dienen te
        worden.
        """)


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
    
    st.write("""
        ## Verdeling laadttijden elektrische auto's
        Op deze pagina is te zien wat de verdelingis van de laadtijden van elektrische auto's en hoe lang de auto's
        aangesloten zijn geweest op de laadpaal.""")
    
    st.write("""
        ### Verdeling laadtijden elektrische auto's met extremen
        Hieronder staat een histogram die de verdeling weergeeft van de laadtijd en aangesloten tijd van auto's
        op laadpalen. Ook is de kansdichtheidsfunctie weergegeven.
        Hierbij is te zien dat er een paar extreme waarden zijn waardoor de verdeling minder duidelijk is voor de meeste
        auto's die over het algemeen minder lang aangesloten zijn op de laadpalen. Dit kan men ook concluderen uit de
        waarden van de gemiddelden en medianen.
        """)
    
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
    
    st.write("""
        ### Verdeling laadtijden elektrische auto's met extremen
        Hieronder wordt dezelfde figuur getoond, die de procentuele dichtheid van de totale hoeveelheid opgeladen auto's
        weergeeft. Daarnaast is te zien hoelang de gemiddelde auto erover doet om op te laden. Ook is te zien
        hoe lang auto's gemiddeld aangesloten zijn op een laadpaal.
        Uit de kansdichtheid van de laadtijd blijkt dat de meeste auto's binnen 8 uur zijn opgeladen.
        Echter laat de spreiding van de aangesloten tijd zien dat mensen hun auto niet direct loskoppelen. 
        Na het verwijderen van de extreme aangesloten tijden aan laadpalen is te zien dat zowel de mediaan als
        het gemiddelde zijn veranderd.""")
    
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
        De eerste dataset bevat meer algemene informatie over de voertuigen en de tweede bevat ook informatie over
        de brandstofsoort. Deze twee datasets kunnen worden gecombineerd tot één dataset door ze te mergen op
        'kenteken'.
        
        Aangezien de datasets bestaan uit respectievelijk 15.1 miljoen rijen met 92 kolommen en 14.4 miljoen rijen met
        36 kolommen kan een normale laptop dit vanwege de grootte niet inladen.
        
        Om deze bestanden te kunnen gebruiken zijn een aantal kolommen geselecteerd die nodig waren voor het maken van
        specifieke grafieken. Ook is gefilterd op enkel de voertuigsoort, 'personenauto'.
        Op deze manier kunnen de benodigde kolommen en rijen van de datasets wel ingeladen en samengevoegd worden.
        Vervolgens wordt het samengevoegde bestand omgezet naar een csv bestand, zodat werken met de dataset sneller
        gaat.""")
        
    ######################################################################################
    # Plot crikeldiagram brandstof omschrijving
    ######################################################################################
    
    st.write("""
        ## Cirkel diagram van het type aandrijving
        Deze cirkel diagram laat zien welke soort aandrijving het meest voorkomt. 
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
        Deze lijndiagram geeft net zoals het cirkel diagram ook het type aandrijving weer die het meest voorkomt 
        in Nederland. Hierbij is een slider toegevoegd dat over de tijd heen weergeeft welke soort 
        aandrijving het meeste voor is gekomen. Ook hier kan uit worden opgehaald dat benzine auto's het meest
        dominant is in Nederland. Wel kan men zien dat de hoeveelheid elektrische auto's sterk aan het 
        toenemen zijn sinds ongeveer 2018.""")
    
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
        Dit zijn de top 10 automerken die de meeste elektrische auto's hebben verkocht, gebasseerd op de gegeven data
        van RDW. Zo is te zien dat Toyota een groter deel uit maakt van de totale hoeveelheid elektrische auto's.""")
    
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
        In deze lijndiagram is het cumulatieve aantal verkochte auto's te zien van 10 auto merken die de meeste elektrische
        auto's hebben verkocht tot nu toe. Dit geeft een beeld weer welke auto merken het meest populair zijn
        in Nederland. Wat opvalt is dat het merk Tesla in vergelijking met andere merken nog niet lang elektrische
        auto's verkoopt in Nederland, maar dat deze toch in de top 10 staat.""")
    
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
        ## Lineaire regressie model
        ### Regressie tussen emissiecode en cilinder inhoud
        De regressie tussen de emissiecode en de cilinderinhoud is een verband die is bedacht vanwege 
        de gedachte dat een grotere inhoud van de cilinders zou resulteren naar meer verbruik van brandstof. 
        Meer verbruik van brandstof zou resulteren in een lagere emissiecode.
        In de diagram is ook een positieve regressielijn te zien (echter is dit verband niet heel sterk).
        Dit geeft aan dat er dus een verband is tussen de uitstoot van de auto en de cilinder inhoud.
        In deze diagram zijn de elektrische auto's en waterstof auto's uit de dataset gehaald.
        Dit omdat elektrische en waterstof auto's niet aangedreven worden met cilinders.""")
    
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
        ### Regressie tussen cilinders en cilinder inhoud
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
    
    st.write("""
        ### Regressiemodel
        Met behulp van de relatie tussen aantal cilinders, cilinderinhoud en de emissiecode is een regressiemodel
        opgesteld. Wanneer men hieronder een kenteken invoerd, worden het aantal cilinders en de emissiecode van de
        bijbehorende auto opgezocht in de dataset. Hieruit volgt een voorspelde cilinderinhoud.""")
    
    # Een aantal kentekens en bijbehorende waarden inladen om het model uit te kunnen voeren
    df_kenteken = pd.read_csv("df_kenteken.csv")

    # Deel kentekens en bijbehorende waarden tonen
    deel_df_kenteken = df_kenteken.sort_values("emissiecode_omschrijving").iloc[30:40][:]
    st.write(deel_df_kenteken.head(10))
    
    # Kenteken invoeren
    kenteken = st.text_input("Voer een kenteken in:", "0050PK")
#     st.write("Het ingevoerde kenteken is: ", kenteken)
    
    # Het model
    X = df_model[["emissiecode_omschrijving","aantal_cilinders"]]
    y = df_model["cilinderinhoud"]
    reg = LinearRegression().fit(X.values, y.values)
    
    rij_kenteken = df_kenteken[df_kenteken["kenteken"] == kenteken]
    emissiecode = float(rij_kenteken.iloc[0]["emissiecode_omschrijving"])
    aantal_cilinders = rij_kenteken.iloc[0]["aantal_cilinders"]
    
    voorspelling_cilinderinhoud = round(reg.predict(np.array([[emissiecode, aantal_cilinders]]))[0],0)
    echte_cilinderinhoud = rij_kenteken.iloc[0]["cilinderinhoud"]
    
    # Voorspelling
    st.write("De voorspelde cilinderinhoud is:", voorspelling_cilinderinhoud)
    
    # Uitleg model
    regressiescore = reg.score(X.values, y.values)
    reg_emissie = reg.coef_[0]
    reg_cil = reg.coef_[1]
    intercept = reg.intercept_
    
    st.write("#### Extra informatie over het regressiemodel")
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

