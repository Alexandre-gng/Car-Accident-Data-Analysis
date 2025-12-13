# What Characterizes Car Accidents in France?

[Old Streamlit link](https://car-accident-data-analysis.streamlit.app/)

This project is a data analysis and visualization application built with **Streamlit** that explores a dataset of car accidents in France between **2015 and 2020**.

The goal is to answer critical questions about road safety: Are current measures effective? Are they targeting the right demographics or issues?

## 📊 Project Overview

The Streamlit application presents a multi-tab analysis covering five key areas:

1.  **Age:** Analyzing the age distribution of drivers and pedestrians involved in accidents.
2.  **Sex:** Investigating the "sexist stereotype" about drivers and comparing accident involvement and severity based on gender.
3.  **Type of Vehicle:** Determining which vehicle types are most frequently involved and their dangerosity to both the driver and pedestrians.
4.  **Speed Limit:** Examining the relationship between speed limits, the proportion of deaths, and the proportion of injuries.
5.  **Where:** Visualizing where most accidents occur, broken down by road type, and a geographical map of accident locations.

## 💾 Data Source and Preprocessing

The underlying data comes from the French government's public datasets on road traffic accidents.

* **Source:** [Bases de données annuelles des accidents corporels de la circulation routière](www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024)
* **Time Period:** 2015 to 2020. Data from 2020-2022 was excluded due to the impact of the Covid-19 pandemic on traffic.
* **Original Files:** The analysis began by merging four separate CSV files: `caracteristiques.csv`, `lieux.csv`, `usagers.csv`, and `vehicules.csv`.
* **Preprocessing:** The files were filtered for the 2015-2020 period, irrelevant columns were dropped, and the final dataset was merged on the accident number (`num_acc`).

## 🛠 Technologies Used

* **Python:** Programming language
* **Streamlit:** For creating the interactive web application and data visualization interface.
* **Pandas & NumPy:** For data loading and manipulation.
* **Plotly & Matplotlib/Seaborn:** For generating interactive and static statistical charts (pie charts, bar charts, heatmaps).
* **PyDeck & Folium (indirectly):** For geographical mapping and visualization of accident clusters.

## 🚀 How to Run the App

### Prerequisites

You need Python installed on your system. It's recommended to use a virtual environment.

### Installation

1.  **Clone the repository** (or download the files):
    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```
2.  **Install the required libraries:**
    The project uses the following libraries. You should create a `requirements.txt` file (or run the install commands manually).
    ```bash
    pip install pandas streamlit matplotlib plotly seaborn pydeck streamlit-folium numpy
    ```
    *(Note: The data file `data/merged_data.csv` is assumed to be present in a `data` subdirectory for the `load_data` function to work.)*

### Execution

1.  **Run the Streamlit application:**
    ```bash
    streamlit run main.py
    ```
2.  The application will open automatically in your web browser (usually at `http://localhost:8501`).

## 🔑 Key Findings

The analysis reveals several insights into French road safety:

* **Age:** Drivers most frequently involved in accidents are **young (18-37)**, while pedestrian involvement is more evenly spread across all ages, except for the very young (3-21).
* **Sex:** Men are significantly more represented as drivers involved in accidents and are **more likely to cause any type of injury**, including fatal ones.
* **Vehicle Dangerosity:**
    * **Truck drivers** have the highest proportion of fatalities among drivers involved in accidents.
    * For **pedestrians**, heavy vehicles like **trucks and cars** are associated with more severe injuries and fatalities due to the higher kinetic energy involved in a crash ($E = \frac{1}{2} m v^{2}$).
* **Speed Limit:**
    * The **80 km/h** speed limit roads show the highest proportion of deaths, possibly due to a lack of infrastructure safety compared to highways.
    * **Highways (130 km/h)**, while generally safer overall, are disproportionately dangerous for **trucks and scooters**.
* **Location:** The highest number of accidents occur on **Communal Roads**, but the largest proportion of **severe accidents (dead or hospitalized)** occur on **Departmental Roads**, which aligns with the finding that 80 km/h zones are the deadliest.
