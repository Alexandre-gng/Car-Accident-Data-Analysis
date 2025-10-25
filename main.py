import math
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import pydeck as pdk


st.title("What characterizes car accidents in France?")
st.text("In France in 2024, 3 193 people died in car crashes. More than 236 000 were injured and around 16 000 were seriously injured, however we frequently hear about new measures being taken to improve road safety. But are these measures effective ? Are they targeting the right people ? Are they addressing the right issues ?")
st.text("To answer these questions, we will analyze data from the French government on car crashes that occurred between 2015 and 2020.")
st.link_button("source", "www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024")



with st.expander("Data preprocessing"):
    st.text("The original dataset we can find on the French governement website is composed of 4 different csv files :")
    st.text("- caracteristiques.csv : characteristics of the accidents")
    st.text("- lieux.csv : location of the accidents")
    st.text("- usagers.csv : information about the people involved in the accidents")
    st.text("- vehicules.csv : information about the vehicles involved in the accidents")
    st.text("Each file contains no significant missing values (even if some specific variables are weird as we will see), but they are quite big (between 50 and 200 MB each) and we will need to merge them into a single file for our analysis.")
    st.text("Thus we decided to keep only the data between 2015 and 2020 (because from 2020 to 2022 the traffic was highly impacted by Covid-19, because before 2015 the data is less reliable and because there are currently no data after 2023). We also dropped some columns that we considered as not useful for our analysis.")
    st.text("Finally we merged the 4 files into a single one, using the column 'num_acc' as the key.")


@st.cache_data
def load_data():
    df = pd.read_csv("data/merged_data.csv", encoding='latin1')
    return df

Age, Sex, Type_of_vehicle, speed_limit, where, conclusion = st.tabs(["Age", "Sex", "Type of vehicle", "Speed Limit", "Where", "Conclusion"])

st.set_page_config(layout="centered")

df = load_data()

with Age:
    st.markdown("## I. Age: Who is more likely to be involved in a car crash ?")
    driver_by_age = df[df["catu"] == 1]
    pedestrian_by_age = df[df["catu"] == 3]
    age_count_driver = (driver_by_age['annee'] - driver_by_age['an_nais']).value_counts().sort_index()
    st.markdown("""
    <div style="
        background-color: #1c2841 ;
        padding: 15px;
        padding-bottom: 5px;
        margin-bottom: 20px;
        border-radius: 10px;
        align-items: center;
        justify-content: center;
    ">
    <p> One of the main idea is that old people are more likely to be involved in car crashes because of their age. </p>
    </div>
    """, unsafe_allow_html=True)
    st.subheader("Graph of the age repartion of drivers involved in a car crash")
    st.bar_chart(age_count_driver)
    st.markdown("""
    <div style="
        background-color: #1c2841 ;
        padding: 15px;
        padding-bottom: 5px;
        margin-bottom: 20px;
        border-radius: 10px;
        align-items: center;
        justify-content: center;
    ">
    <p> We can see that most of the drivers involved in a car crash are young (18-37). This can be explained by the fact that young people are more inclined to take risks and drive more often than older people.</p>
    </div>
    """, unsafe_allow_html=True)


    st.subheader("Graph of the age repartion of pedestrians involved in a car crash")
    age_count_pedestrian = (pedestrian_by_age['annee'] - pedestrian_by_age['an_nais']).value_counts().sort_index()
    st.bar_chart(age_count_pedestrian)
    st.markdown("""
    <div style="
        background-color: #1c2841 ;
        padding: 15px;
        padding-bottom: 5px;
        margin-bottom: 20px;
        border-radius: 10px;
        align-items: center;
        justify-content: center;
    ">
    <p> We observe that age repartition is not the same for the drivers and the pedestrians involved in a car crash. Contrary to the drivers, everyone seems to be equally affected by car crashes, excepted the young (3 - 21).</p>
    </div>
    """, unsafe_allow_html=True)

with Sex:

    st.markdown("## II. Sex: Who is more likely to cause a car crash ?")
    st.markdown("""
    <div style="
        background-color: #1c2841 ;
        padding: 15px;
        padding-bottom: 5px;
        margin-bottom: 20px;
        border-radius: 10px;
        align-items: center;
        justify-content: center;
    ">
    <p> In France, there existed a very sexist stereotype that women are worse drivers than men, there is even a popular saying \"femmes au volant, mort au tournant\".</p>
    <p> To check if this stereotype is true, we will look at the repartition of drivers involved in a car crash by sex, and the conclusion is interesting. </p>
    <p> The first question is a brut comparaison of the repartition of pedestrians and drivers involved in a car crash by sex
    </div>
    """, unsafe_allow_html=True)

    
    # Data for drivers
    labels = ["Men", "Women"]
    hommes_drivers = df[(df['catu'] == 1) & (df["sexe"] == 1)].shape[0]
    femmes_drivers = df[(df['catu'] == 1) & (df["sexe"] == 2)].shape[0]
    driver_data = [hommes_drivers, femmes_drivers]
    colors = ['#66b3ff', '#ff9999']
    
    # Interactive pie chart for drivers
    fig_drivers = go.Figure(data=[go.Pie(
        labels=labels,
        values=driver_data,
        hovertemplate='<b>%{label}</b><br>' +
                     'Number of drivers: %{value:,}<br>' +
                     'Percentage: %{percent}<br>' +
                     '<extra></extra>',
        textinfo='label+percent',
        textposition='auto',
        textfont_size=14,
        marker=dict(
            colors=colors,
            line=dict(color='#FFFFFF', width=2)
        )
    )])
    
    fig_drivers.update_layout(
        title={
            'text': 'Distribution of Drivers by Sex',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        showlegend=True,
        height=400,
        margin=dict(l=20, r=20, t=70, b=20)
    )
    
    hommes_pedestrians = df[(df['catu'] == 3) & (df["sexe"] == 1)].shape[0]
    femmes_pedestrians = df[(df['catu'] == 3) & (df["sexe"] == 2)].shape[0] 
    pedestrian_data = [hommes_pedestrians, femmes_pedestrians]
    
    fig_pedestrians = go.Figure(data=[go.Pie(
        labels=labels,
        values=pedestrian_data,
        hovertemplate='<b>%{label}</b><br>' +
                     'Number of pedestrians: %{value:,}<br>' +
                     'Percentage: %{percent}<br>' +
                     '<extra></extra>',
        textinfo='label+percent',
        textposition='auto',
        textfont_size=14,
        marker=dict(
            colors=colors,
            line=dict(color='#FFFFFF', width=2)
        )
    )])
    
    fig_pedestrians.update_layout(
        title={
            'text': 'Distribution of Pedestrians by Sex',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        showlegend=True,
        height=400,
        margin=dict(l=20, r=20, t=70, b=20)
    )
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_pedestrians, use_container_width=True)
    with col2:
        st.plotly_chart(fig_drivers, use_container_width=True)
    
    st.markdown("""
    <div style="
        background-color: #1c2841 ;
        padding: 15px;
        padding-bottom: 5px;
        margin-bottom: 20px;
        border-radius: 10px;
        align-items: center;
        justify-content: center;
    ">
    <p> We observe that there is a significant difference of representation between male and female drivers involved in a car crash.
    </div>
    """, unsafe_allow_html=True)



    gravites = {
        1: "Unharmed",
        2: "Killed",
        3: "Hospitalized",
        4: "Slight injury"
    }
    hommes_counts = []
    femmes_counts = []
    labels = []
    for grav, label in gravites.items():
        accidents_homme = df[(df['catu'] == 1) & (df['sexe'] == 1)]['num_acc'].unique()
        accidents_femme = df[(df['catu'] == 1) & (df['sexe'] == 2)]['num_acc'].unique()

        pietons_homme = df[(df['catu'] == 3) & (df['num_acc'].isin(accidents_homme)) & (df['grav'] == grav)]
        pietons_femme = df[(df['catu'] == 3) & (df['num_acc'].isin(accidents_femme)) & (df['grav'] == grav)]
        hommes_counts.append(pietons_homme.shape[0])
        femmes_counts.append(pietons_femme.shape[0])
        labels.append(label)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels,
        y=hommes_counts,
        name='Man driver',
        marker_color='#66b3ff',
        hovertemplate='Man driver<br>%{x}: %{y} pedestrians<extra></extra>'
    ))
    fig.add_trace(go.Bar(
        x=labels,
        y=femmes_counts,
        name='Woman driver',
        marker_color='#ff9999',
        hovertemplate='Woman driver<br>%{x}: %{y} pedestrians<extra></extra>'
    ))
    fig.update_layout(
        barmode='group',
        title='Number of pedestrians injured based on the sex of the driver',
        xaxis_title='Type of injury',
        yaxis_title='Amount of pedestrians injured',
        legend_title='Sex of the driver',
        height=600,
        width=1000
    )
    
    st.plotly_chart(fig)
    st.markdown("""
        <div style="
        background-color: #1c2841 ;
        padding: 15px;
        padding-bottom: 5px;
        margin-bottom: 20px;
        border-radius: 10px;
        align-items: center;
        justify-content: center;
    ">
    <p> We can see that men are more likely to cause any type of injury, including fatal, in road accidents. The difference between the two sex in term of proportion for the killed is huge (3.56) and is little bit reduced for the seriously injured (2.64), and around 2.72 for the minor injuries.)</p>
    <p> The sexist sterotype is completely false and denote a miscomprehension of the data, men drivers are more likely to cause injuries or killings in a car accident. This can be partially explained by the fact that men drive more than women.</p>
    <p> Men are also more likely to take risks, wich can lead to more severe accidents. (\"Gender Differences in Risk Aversion and Ambiguity Aversion\" by Lex Borghans and al., 2009) </p>

    """, unsafe_allow_html=True)

with Type_of_vehicle:
    st.markdown("## III. Wich type of vehicle is the most dangerous ?")
    catv_groups = {
        "Cars": [7, 10, 16, 17],
        "Trucks": [13, 14, 15],
        "Scooters": [30, 31, 32, 33, 34, 41, 42, 43],
        "Bicycles/ skateboard": [1, 2, 50, 60, 80],
        "Exceptional / undetermined vehicles": [0, 3, 4, 5, 6, 8, 9, 11, 12,
                                                18, 19, 20, 21, 35, 36, 37, 38,
                                                39, 40, 99]
    }
    # Exceptional vehicles include quads, trams, tractors, military equipment ..

    group_counts = {}
    for group in catv_groups.keys():
        codes = catv_groups[group]
        count = df[df["catv"].isin(codes)].shape[0]
        group_counts[group] = count


    colors = ['#66b3ff', '#ff9999', '#99ff99', '#ffcc99', '#c2c2f0']

    fig_catv = go.Figure(data=[go.Pie(
        labels=list(group_counts.keys()),
        values=list(group_counts.values()),
        hovertemplate='<b>%{label}</b><br>' +
                     'Nombre de véhicules: %{value:,}<br>' +
                     'Pourcentage: %{percent}<br>' +
                     '<extra></extra>',
        textfont_size=14,
        marker=dict(
            colors=colors[:len(group_counts)],  # ajuste le nombre de couleurs
            line=dict(color='#FFFFFF', width=2)
        )
    )])

    fig_catv.update_layout(
        title={
            'text': 'Répartition des véhicules par catégorie',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        showlegend=True,
        height=400,
        margin=dict(l=20, r=20, t=70, b=20)
    )

    st.plotly_chart(fig_catv, use_container_width=True)

    st.text(
        "Exceptional / undetermined vehicles include vehicles such as tractors, "
        "construction equipment, trams, military vehicles, .. which are not very common in accidents."
    )

    grav_labels = {
        1: "Unharmed",
        2: "Killed",
        3: "Hospitalized",
        4: "Slightly injured"
    }
    pourcentages = {label: [] for label in grav_labels.values()}
    vehicules = []
    for vehicule, codes in catv_groups.items():
        vehicules.append(vehicule)
        total = len(df[(df['catv'].isin(codes)) & (df['catu'] == 1)])
        for grav, label in grav_labels.items():
            count = len(df[(df['grav'] == grav) & (df['catv'].isin(codes)) & (df['catu'] == 1)])
            pourcentages[label].append((count / total * 100) if total > 0 else 0)

    fig_bar = go.Figure()
    for label, values in pourcentages.items():
        fig_bar.add_trace(go.Bar(
            x=vehicules,
            y=values,
            name=label,
            hovertemplate=f"%{{y:.2f}}% de {label.lower()}<extra></extra>"
        ))

    fig_bar.update_layout(
        barmode='group',
        xaxis_title="Type of vehicle",
        yaxis_title="Percentage (%)",
        title="Statistics of the vehicule dangerosity for its driver",
        hovermode="x unified"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("""
    <div style="
        background-color: #1c2841 ;
        padding: 15px;
        padding-bottom: 5px;
        margin-bottom: 20px;
        border-radius: 10px;
        align-items: center;
        justify-content: center;
    ">
    <p> We observe that most of the accidents, regardless of the type of vehicule, do not result in any injury for the driver.</p>
    <p> We can see that trucks drivers are most likely to die in a car crash (4.73%), this can be explained by the fact that trucks are heavier and thus the impact is more violent for the driver.</p>
    <p> Even if the percentage of killed scooters drivers is not the highest (2.06%), this vehicule remains the second in term of total drivers killed per year (averagly 637 between 2015 and 2020).</p>
    <p> Generally we can see that the type of vehicule does not have a significant impact on the distribution of injuries for the drivers, however this observation is not true for the pedestrians involved in a car crash.</p>
    </div>
    """, unsafe_allow_html=True)

    for vehicule, codes in catv_groups.items():
        vehicules.append(vehicule)
        total = len(df[(df['catv'].isin(codes)) & (df['catu'] == 3)])
        for grav, label in grav_labels.items():
            count = len(df[(df['grav'] == grav) & (df['catv'].isin(codes)) & (df['catu'] == 3)])
            pourcentages[label].append((count / total * 100) if total > 0 else 0)
    fig = go.Figure()

    for label, values in pourcentages.items():
        fig.add_trace(go.Bar(
            x=vehicules,
            y=values,
            name=label,
            hovertemplate=f"%{{y:.2f}}% de {label.lower()}<extra></extra>"
        ))

    fig.update_layout(
        barmode='group',
        xaxis_title="Type of vehicle",
        yaxis_title="Percentage (%)",
        title="Statistics of the vehicule dangerosity for pedestrians",
        hovermode="x unified"
    )
    # Calculer le nombre d'atteintes pour chaque groupe de véhicule
    results = []
    for vehicule, codes in catv_groups.items():
        subset = df[df['catv'].isin(codes) & (df['catu'] == 3)]
        nb_blesses_legers = len(subset[subset['grav'] == 2])
        nb_blesses_graves = len(subset[subset['grav'] == 3])
        nb_tues = len(subset[subset['grav'] == 4])
        nb_total_blesses = nb_blesses_legers + nb_blesses_graves
        results.append({
            "Véhicule": vehicule,
            "Blessés légers": nb_blesses_legers,
            "Blessés graves": nb_blesses_graves,
            "Blessés (total)": nb_total_blesses,
            "Tués": nb_tues,
            "Échantillon total (piétons impliqués)": len(subset)
        })
    df_results = pd.DataFrame(results)

    top3_blessent = df_results.sort_values(by="Blessés (total)", ascending=False).head(5).reset_index(drop=True)

    st.subheader("Top 5 of the most involved vehicles in accidents (2015-2020)")
    st.dataframe(
        top3_blessent[["Véhicule", "Blessés légers", "Blessés graves", "Tués"]],
        hide_index=True
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div style="
        background-color: #1c2841 ;
        padding: 15px;
        padding-bottom: 5px;
        margin-bottom: 20px;
        border-radius: 10px;
        align-items: center;
        justify-content: center;
    ">
    <p> We observe that pedestrians are more likely to be slightly injured with light vehicles such as bicycles or scooters, while they are more likely to be injured with heavy vehcicules such as trucks or cars.</p>
    <p> The main reason is that the Energy involved in the crash is higher with heavy vehicules, we know that the kinetic energy is given by the formula:
    </div>
    """, unsafe_allow_html=True)
    st.latex("E = \\frac{1}{2} m v^{2}")
    st.markdown("""
    <div style="
        background-color: #1c2841 ;
        padding: 15px;
        padding-bottom: 5px;
        margin-bottom: 20px;
        border-radius: 10px;
        align-items: center;
        justify-content: center;
    ">
    <p>thus the more massive the vehicule is, the more energy will be involved in the crash.</p>
    <p>We can deduce that the type of vehicule has a significant impact on the distribution of injuries for the pedestrians involved in a car crash.</p>

    <p> Exceptional/ undetermined vehicules have 6.65% of killed pedestrians, it's the second highest percentage after trucks (23.84%). This can be explained by the fact that this category includes very heavy vehicules such as tractors, contruction equipment, tramways... which can cause particularly severe injuries to pedestrians. </p>
    </div>
    """, unsafe_allow_html=True)


# ===============================================================
# ===== B. Speed limit =====
with speed_limit:
    
    st.markdown("## IV. Speed limit: Does speed kill ?")
    st.markdown("""
    <div style="
        background-color: #1c2841 ;
        padding: 15px;
        padding-bottom: 5px;
        margin-bottom: 20px;
        border-radius: 10px;
        align-items: center;
        justify-content: center;
    ">
    <p> We often hear that speed is one of the main causes of car crashes, but is it true ? To answer this question, we will look at the proportion of deaths and injuries by speed limit </p>
    </div>
    """, unsafe_allow_html=True)
    speed_df = df[df["vma"] > 0]
    total_by_vma = speed_df.groupby("vma").size().sort_index()
    # Dropping the specific speed limits with very few accidents for better visualization
    total_by_vma = total_by_vma[total_by_vma > 100]

    killed_by_vma = speed_df[speed_df["grav"] == 2].groupby("vma").size().sort_index()
    total_injured_by_vma = speed_df[speed_df["grav"].isin([3, 4])].groupby("vma").size().sort_index()
    total_injured_by_vma = total_injured_by_vma[total_injured_by_vma > 100]
    prop_by_vma = (killed_by_vma / total_by_vma).fillna(0)
    prop_by_vma_injured = (total_injured_by_vma / total_by_vma).fillna(0)

    # ========= First plot for injured =========
    fig_deaths = go.Figure()
    fig_deaths.add_trace(go.Bar(
        x=prop_by_vma.index,
        y=prop_by_vma.values,
        name='Death Proportion',
        hovertemplate='<b>Speed Limit: %{x} km/h</b><br>' +
                     'Death Proportion: %{y:.3f}<br>' +
                     'Total Deaths: %{customdata[0]}<br>' +
                     'Total Accidents: %{customdata[1]}<extra></extra>',
        customdata=[[killed_by_vma.get(speed, 0), total_by_vma.get(speed, 0)] 
                   for speed in prop_by_vma.index]
    ))
    fig_deaths.update_layout(
        title='Proportion of Deaths by Speed Limit',
        xaxis_title='Speed Limit (km/h)',
        yaxis_title='Death Proportion',
        showlegend=False
    )
    st.plotly_chart(fig_deaths, use_container_width=True)
    st.markdown("""
    <div style="
        background-color: #1c2841 ;
        padding: 15px;
        padding-bottom: 5px;
        margin-bottom: 20px;
        border-radius: 10px;
        align-items: center;
        justify-content: center;
    ">
    <p> In France the average speed limit is 80 km/h on most of the roads, but it can go up to 130 km/h on highways. We can see that the proportion of deaths and injuries increases with the speed limit, which is logical because the higher the speed, the more energy is involved in the crash. </p>
    <p> We observe that the proportion of deaths increases significantly from 30km/h (1.1%) to 80km/h (6.4%), then it inscreases from 90 Km/h (1.4%) to 130 Km/h (3.8%).</p>
    <p> This can be explained by the fact that most of the accidents happen on roads with a speed limit of 80 km/h, thus the proportion of deaths is higher because there are more accidents.</p>
    </div>
    """, unsafe_allow_html=True)

    # ========= Second plot for injured =========
    fig_injuries = go.Figure()
    fig_injuries.add_trace(go.Bar(
        x=prop_by_vma_injured.index,
        y=prop_by_vma_injured.values,
        name='Injury Proportion',
        hovertemplate='<b>Speed Limit: %{x} km/h</b><br>' +
                     'Injury Proportion: %{y:.3f}<br>' +
                     'Total Injured: %{customdata[0]}<br>' +
                     'Total Accidents: %{customdata[1]}<extra></extra>',
        customdata=[[total_injured_by_vma.get(speed, 0), total_by_vma.get(speed, 0)] 
                   for speed in prop_by_vma_injured.index]
    ))
    fig_injuries.update_layout(
        title='Proportion of Injuries by Speed Limit',
        xaxis_title='Speed Limit (km/h)',
        yaxis_title='Injury Proportion',
        showlegend=False
    )
    st.plotly_chart(fig_injuries, use_container_width=True)
    st.markdown("""
    <div style="
        background-color: #1c2841 ;
        padding: 15px;
        padding-bottom: 5px;
        margin-bottom: 20px;
        border-radius: 10px;
        align-items: center;
        justify-content: center;
    ">
    <p>We can observe a global decrease of the proportion of injuries as the speed limit increases. A possible reason is that more the accidents happen at high speed, more the result is binary (death or unharmed). Thus the proportion of injuries decreases because there are more deaths and unharmed people.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Heatmap: Proportion of deaths by speed limit and vehicle type")
    speed_df_copy = speed_df.copy()
    speed_df_copy['vehicle_category'] = 'Other'
    
    for category, codes in catv_groups.items():
        mask = speed_df_copy['catv'].isin(codes)
        speed_df_copy.loc[mask, 'vehicle_category'] = category
    
    common_speeds = [30, 50, 70, 80, 90, 110, 130]
    heatmap_df = speed_df_copy[speed_df_copy['vma'].isin(common_speeds)]
    
    heatmap_data = []
    
    for speed in common_speeds:
        for vehicle in catv_groups.keys():
            total_accidents = len(heatmap_df[
                (heatmap_df['vma'] == speed) & 
                (heatmap_df['vehicle_category'] == vehicle)
            ])
            deaths = len(heatmap_df[
                (heatmap_df['vma'] == speed) & 
                (heatmap_df['vehicle_category'] == vehicle) &
                (heatmap_df['grav'] == 2)
            ])
            proportion = (deaths / total_accidents * 100) if total_accidents > 0 else 0
            
            heatmap_data.append({
                'Speed_Limit': speed,
                'Vehicle_Type': vehicle,
                'Death_Proportion': proportion,
                'Total_Accidents': total_accidents
            })
    
    heatmap_df_final = pd.DataFrame(heatmap_data)
    
    heatmap_pivot = heatmap_df_final.pivot(
        index='Vehicle_Type', 
        columns='Speed_Limit', 
        values='Death_Proportion'
    ).fillna(0)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(
        heatmap_pivot,
        annot=True,
        fmt='.1f',
        cmap='Reds',
        ax=ax,
        cbar_kws={'label': 'Death Proportion (%)'}
    )
    ax.set_title('Proportion of Deaths by Speed Limit and Vehicle Type (%)')
    ax.set_xlabel('Speed Limit (km/h)')
    ax.set_ylabel('Vehicle Type')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("""
    <div style="
        background-color: #1c2841 ;
        padding: 15px;
        padding-bottom: 5px;
        margin-bottom: 20px;
        border-radius: 10px;
        align-items: center;
        justify-content: center;
    ">
    <p> We can see that some vehicle types and specific speed limits are associated with a higher proportion of deaths. For example the 80 km/h speed limit is generally the deadliest, a possible reason can be that the roads with this speed limit does not have the safety measures applied to highways, while having the dangers of the low speed limits zone </p>
    <p> On the other hand, the 130 km/h speed limit is generally safer, possibly due to the better road infrastructure and safety measures in place on highways. </p>
    <p> Another interesting observation is that highways (130 Km/h) are particularly dangerous for trucks and scooters. Scooters are light vehicles and its drivers are less protected to accident than cars. A possible theory for the truck category is that truck drivers are more inclined to do long highway travel, and then develop fatigue. </p>
    </div>
    """, unsafe_allow_html=True)


with where:
    st.markdown("## V. Where do most accidents happen ?")
    # Sort by road code so that label order is consistent across charts (colors stay the same)
    df_catr = df.groupby('catr').size().sort_index()
    labels = {
        1: "Highways",
        2: "National roads",
        3: "Departmental roads",
        4: "Communal roads",
        5: "Outside public roads",
        6: "Public parking lots",
        7: "Urban roads",
        9: "Other"
    }
    df_catr.index = df_catr.index.map(labels)
    
    # Create interactive pie chart with better visibility for small segments
    fig = go.Figure(data=[go.Pie(
        labels=df_catr.index,
        values=df_catr.values,
        hovertemplate='<b>%{label}</b><br>' +
                     'Number of accidents: %{value:,}<br>' +
                     'Percentage: %{percent}<br>' +
                     '<extra></extra>',
        textfont_size=12,
        pull=[0.05 if val < df_catr.sum() * 0.05 else 0 for val in df_catr.values],  # Pull out small segments
        marker=dict(
            line=dict(color='#FFFFFF', width=2)
        )
    )])
    
    fig.update_layout(
        title={
            'text': 'Distribution of Accidents by Road Type',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        ),
        margin=dict(l=20, r=250, t=70, b=20),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add summary table for better visibility of all data
    st.subheader("Detailed breakdown by road type")
    summary_df = pd.DataFrame({
        'Road Type': df_catr.index,
        'Number of Accidents': df_catr.values,
        'Percentage': [(val/df_catr.sum())*100 for val in df_catr.values]
    }).round(2)
    
    st.dataframe(summary_df, hide_index=True, use_container_width=True)


    st.text("Where do most of the severe accidents happen ?")

    severe_accidents = df[df['grav'].isin([2, 3])]
    severe_by_catr = severe_accidents['catr'].value_counts().sort_index()
    severe_by_catr.index = severe_by_catr.index.map(labels)
   
    # Create interactive pie chart with better visibility for small segments
    fig = go.Figure(data=[go.Pie(
        labels=severe_by_catr.index,
        values=severe_by_catr.values,
        hovertemplate='<b>%{label}</b><br>' +
                     'Number of accidents: %{value:,}<br>' +
                     'Percentage: %{percent}<br>' +
                     '<extra></extra>',
        textfont_size=12,
        pull=[0.05 if val < df_catr.sum() * 0.05 else 0 for val in df_catr.values],  # Pull out small segments
        marker=dict(
            line=dict(color='#FFFFFF', width=2)
        )
    )])
    
    fig.update_layout(
        title={
            'text': 'Distribution of severe Accidents (dead or hospitalized) by Road Type',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        ),
        margin=dict(l=20, r=250, t=70, b=30),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    <div style="
        background-color: #1c2841 ;
        padding: 15px;
        padding-bottom: 5px;
        margin-bottom: 20px;
        border-radius: 10px;
        align-items: center;
        justify-content: center;
    ">
    <p>We observe that the biggest proportion of the severe accidents happen on Departemental roads, this fact corroborate the previous results with speed limit because most of the Departemental Roads have a speed limit of 80Km/h (between 2015 and 2020).</p>
    <p>We can also see that the proportion of severe accidents slightly decreases on Communal Roads for severe accidents. This can be explained because of the slower speed limit on this type of roads, indeed in France Communal Roads are limited at 50 km/h and most of them are limited at 30km/h.</p>
    <p>Contrary to the common misconception, only a few proportion of the accidents happen on highways, and even less for the severe accidents. This can be explained by the better road infrastructure and safety measures in place on highways.</p>
    </div>
    """, unsafe_allow_html=True)
    # Voir si la plupart des accidents graves sont en ville
    agg_severe = df[(df["agg"] == 1.0) & (df["grav"].isin([2, 3]))]
    no_agg_severe = df[(df["agg"] == 2.0) & (df["grav"].isin([2, 3]))]

    agg_severe = df[df["agg"] == 1.0]
    no_agg_severe = df[df["agg"] == 2.0]
    

    # === Map ===
    st.markdown(
    """
    <div style="display:flex; gap:20px;">
      <div style="color:red;">⬤ Tués</div>
      <div style="color:darkorange;">⬤ Hospitalisés</div>
      <div style="color:gold;">⬤ Blessés légers</div>
      <div style="color:green;">⬤ Indemnes</div>
    </div>
    """,
    unsafe_allow_html=True)
    df_loc = df[["num_acc", "lat", "long", "grav"]].copy()
    df_loc["lat"] = pd.to_numeric(df_loc["lat"], errors="coerce") / 100000
    df_loc["long"] = pd.to_numeric(df_loc["long"], errors="coerce") / 100000
    df_loc = df_loc.dropna(subset=['lat', 'long'])
    df_loc = df_loc[
        (df_loc["lat"].between(40, 52)) &
        (df_loc["long"].between(-6, 10))
    ].rename(columns={"long": "lon"})
    df_loc = df_loc.sample(n=10000)
    # Regrouper par accident pour collecter toutes les gravités associées
    df_colors = (
        df_loc.groupby("num_acc")
        .agg({"lat": "first", "lon": "first", "grav": list})
        .reset_index()
    )

    def clean_grav_list(values):
        cleaned = []
        for v in values:
            if v is None or (isinstance(v, float) and math.isnan(v)):
                continue
            try:
                cleaned.append(int(v))
            except (ValueError, TypeError):
                continue
        return cleaned

    def assign_color(gravity_values):
        g = clean_grav_list(gravity_values)
        if 2 in g:
            return [255, 0, 0, 200]         # rouge
        elif 3 in g:
            return [255, 140, 0, 200]       # orange foncé
        elif 4 in g:
            return [255, 255, 0, 200]       # jaune
        else:
            return [0, 180, 0, 200]         # vert

    df_colors["color"] = df_colors["grav"].apply(assign_color)

    def grav_summary(gravity_values):
        g = clean_grav_list(gravity_values)
        return {
            "killed": g.count(2),
            "hospitalized": g.count(3),
            "slight": g.count(4),
            "unharmed": g.count(1),
        }

    df_colors["summary"] = df_colors["grav"].apply(grav_summary)

    # Déplier le dict en colonnes
    df_colors["killed"] = df_colors["summary"].apply(lambda x: x["killed"])
    df_colors["hospitalized"] = df_colors["summary"].apply(lambda x: x["hospitalized"])
    df_colors["slight"] = df_colors["summary"].apply(lambda x: x["slight"])
    df_colors["unharmed"] = df_colors["summary"].apply(lambda x: x["unharmed"])

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_colors,
        get_position='[lon, lat]',
        get_radius=50,
        get_fill_color="color",
        pickable=True
    )

    view_state = pdk.ViewState(latitude=46.5, longitude=2.5, zoom=5, pitch=0)
    tooltip = {
        "html": (
            "<b>Accident:</b> {num_acc}<br/>"
            "<b>Tués:</b> {killed}<br/>"
            "<b>Hospitalisés:</b> {hospitalized}<br/>"
            "<b>Blessés légers:</b> {slight}<br/>"
            "<b>Indemnes:</b> {unharmed}"
        ),
        "style": {"backgroundColor": "white", "color": "black"}
    }


    r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)

    st.pydeck_chart(r)
    st.markdown("""
    <div style="
        background-color: #1c2841 ;
        padding: 15px;
        padding-bottom: 5px;
        margin-bottom: 20px;
        border-radius: 10px;
        align-items: center;
        justify-content: center;
    ">
    <p> As we can see on the map, even after we selected only the accidents with GPS coordinates inside a specific box around France, there are still some outliers points outside France or in the sea. These points can be explained by errors during the data collection or during the data entry. </p>
    <p> This map does not provide any clear conclusion but allows to vizualize the distribution of accidents in France. We observe clusters around cities and highways, which is logical because most of the traffic is more dense in these areas. It is confirmed by the high proportion of accidents in communal roads, however the most severe accidents remain on departemental roads and are then less visible on this map.</p>
    </div>
    """, unsafe_allow_html=True)

with conclusion:
    st.markdown("## VI. Conclusion")
    st.markdown("""
                    <div style="
            background-color: #1c2841 ;
            padding: 15px;
            padding-bottom: 5px;
            margin-bottom: 20px;
            border-radius: 10px;
            align-items: center;
            justify-content: center;
        ">
    <p>Our analysis of French car accident data from 2015 to 2020 highlights several critical factors that characterize road safety issues and suggests areas for more targeted intervention.</p>

    <h3>Who is most involved and causes the most harm?</h3>
    <ul>
        <li><strong>Drivers:</strong> The data shows that the majority of drivers involved in crashes are <strong>young adults (18-37)</strong>.</li>
        <li><strong>Sex:</strong> Contrary to a popular stereotype, <strong>male drivers are significantly more likely to be involved in and cause severe injury or death</strong> in car accidents. This suggests a need for road safety campaigns that specifically target high-risk male driving behaviors, such as risk-taking.</li>
    </ul>

    <h3>Where and how do the deadliest accidents occur?</h3>
    <ul>
        <li><strong>Location:</strong> While most accidents occur on Communal Roads (urban areas with low speed limits), the <strong>highest proportion of severe accidents (deaths and hospitalizations) occurs on Departmental Roads</strong>, which primarily have a speed limit of 80 km/h.</li>
        <li><strong>Speed:</strong> The <strong>80 km/h speed limit zone is proportionally the deadliest</strong>. This emphasizes that safety measures applied to these rural and secondary roads—such as infrastructure improvements, better signage, and police enforcement—are critical.</li>
    </ul>

    <h3>Vehicle Impact on Severity</h3>
    <ul>
        <li><strong>Vulnerability:</strong> **Truck drivers** face the highest fatality risk among all drivers involved in accidents, possibly due to vehicle mass and long driving hours (fatigue).</li>
        <li><strong>Pedestrian Danger:</strong> The severity of injury for pedestrians is strongly correlated with the vehicle's mass. **Heavy vehicles (Trucks and Cars)** are responsible for a much higher proportion of severe injuries and fatalities to pedestrians than light vehicles like scooters or bicycles, reinforcing the physics of $E = \frac{1}{2} m v^{2}$.</li>
    </ul>

    <p>In summary, future road safety policies should focus less on outdated gender stereotypes and more on **improving the safety of departmental roads, addressing high-risk driving behaviors in young men, and enhancing protective measures for vulnerable road users** (pedestrians and scooter riders), particularly in high-speed zones.</p>

    </div>
    """, unsafe_allow_html=True)