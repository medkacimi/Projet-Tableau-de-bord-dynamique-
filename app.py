# =============================================================================
# IMPORTATION DES BIBLIOTHÈQUES
# =============================================================================
# Ces bibliothèques sont essentielles pour le fonctionnement de l'application:
# - dash : framework pour créer des applications web interactives
# - pandas : manipulation des données
# - plotly : création de graphiques interactifs
# - dash_bootstrap_components : composants UI modernes avec Bootstrap
# - os : gestion des chemins de fichiers et des opérations système

import os  # Pour la gestion des chemins de fichiers et des opérations système
import dash_bootstrap_components as dbc  # Pour un design moderne avec Bootstrap
import pandas as pd  # Pour la manipulation et l'analyse des données
import plotly.express as px  # Pour la création rapide de graphiques interactifs
import plotly.graph_objects as go  # Pour des graphiques personnalisés plus avancés
from dash import Dash, dcc, html, Input, Output  # Composants pour l'application web
import sys

# =============================================================================
# FONCTION DE CHARGEMENT DES DONNÉES
# =============================================================================
def load_data(file_path):
    """
    Charge et valide les données depuis un fichier Excel.

    Structure attendue du fichier Excel :
    - Nom : nom de famille de l'étudiant
    - Prenom : prénom de l'étudiant
    - Matière : intitulé du cours
    - Note : note obtenue sur 20
    - UE : unité d'enseignement
    
    Cette fonction assure plusieurs vérifications :
    1. Existence du fichier
    2. Présence des colonnes requises
    3. Gestion des erreurs de lecture

    Args:
        file_path (str): Chemin vers le fichier Excel

    Returns:
        pd.DataFrame: DataFrame contenant les données ou DataFrame vide si erreur
    """
    # Vérification de l'existence du fichier
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        return pd.DataFrame()

    try:
        # Tentative de lecture du fichier Excel
        df = pd.read_excel(file_path, engine='openpyxl')

        # Vérification de la présence des colonnes nécessaires
        required_columns = {'Nom', 'Prenom', 'Matière', 'Note', 'UE'}
        if not required_columns.issubset(df.columns):
            print("Erreur : Colonnes manquantes dans le fichier Excel.")
            return pd.DataFrame()

        return df
    except Exception as e:
        print(f"Erreur lors du chargement du fichier : {e}")
        return pd.DataFrame()


# =============================================================================
# INITIALISATION DE L'APPLICATION
# =============================================================================
# Chargement initial des données
if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_path = sys.argv[1]  # Récupère le chemin du fichier depuis la ligne de commande
    else:
        file_path = 'data_tdb.xlsx'  # Valeur par défaut si aucun argument n'est fourni
    
    df = load_data(file_path)  # Chargement des données

# Vérification des données chargées
if df.empty:
    print("Aucune donnée disponible. Vérifiez votre fichier Excel.")

# Création de l'application Dash avec le thème Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# =============================================================================
# PRÉPARATION DES DONNÉES POUR L'INTERFACE
# =============================================================================
# Création de la liste des étudiants pour le menu déroulant
# On combine prénom et nom, on élimine les doublons, et on trie par ordre alphabétique
student_options = []
if not df.empty:
    # Extraction des étudiants uniques et formatage pour l'affichage
    unique_students = sorted(df.drop_duplicates(subset=['Nom', 'Prenom'])[['Nom', 'Prenom']].apply(
        lambda x: f"{x['Prenom']} {x['Nom']}", axis=1
    ).tolist())
    student_options = [{'label': student, 'value': student} for student in unique_students]

# =============================================================================
# DÉFINITION DU THÈME DE COULEURS
# =============================================================================
# Palette de couleurs professionnelle pour l'université
# Ces couleurs sont utilisées pour :
# - Les graphiques (barres, points, lignes)
# - L'interface utilisateur (textes, fonds, bordures)
# - Les indicateurs de performance (vert pour succès, rouge pour échec)
colors = {
    'background': '#f0f2f5',  # Fond général légèrement bleuté
    'text': '#2c3e50',  # Bleu foncé pour le texte
    'primary': '#3498db',  # Bleu vif pour les éléments principaux
    'secondary': '#95a5a6',  # Gris pour les éléments secondaires
    'success': '#2ecc71',  # Vert pour les indicateurs positifs
    'warning': '#e74c3c',  # Rouge pour les indicateurs négatifs
    'graph_bg': '#ffffff',  # Fond blanc pour les graphiques
    'panel': '#ffffff',  # Fond blanc pour les panneaux
    'accent': '#9b59b6',  # Violet pour les accents
    'min_max': '#34495e'  # Bleu foncé pour min/max
}

# =============================================================================
# STRUCTURE DE L'INTERFACE (LAYOUT)
# =============================================================================
app.layout = dbc.Container([
    # En-tête avec logo et titre
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("Tableau de Bord Académique",
                        className="text-primary mb-2",
                        style={'fontWeight': '600', 'letterSpacing': '0.5px'}),
                html.P("Suivi des performances et statistiques",
                       className="text-muted",
                       style={'fontSize': '1.1rem'})
            ], className="text-center py-4")
        ])
    ], className="mb-4"),

    # Zone de sélection et statistiques
    dbc.Row([
        # Panel de sélection (côté gauche)
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("Sélection de l'étudiant", className="text-white mb-0"),
                    className="bg-primary"
                ),
                dbc.CardBody([
                    html.Label("Étudiant :", className="font-weight-bold mb-2"),
                    dcc.Dropdown(
                        id='student-dropdown',
                        options=student_options,
                        value=student_options[0]['value'] if student_options else None,
                        clearable=False,
                        className="mb-4"
                    ),
                    html.Label("Unité d'Enseignement :", className="font-weight-bold mb-2"),
                    dcc.Dropdown(
                        id='ue-dropdown',
                        options=[],
                        multi=False,
                        clearable=True,
                        className="mb-3"
                    ),
                    dcc.Store(id='student-data-store'),
                ], className="px-4")
            ], className="shadow-sm h-100")
        ], md=12, lg=4),

        # Panel des statistiques globales
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("Statistiques globales", className="text-white mb-0"),
                    className="bg-primary"
                ),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Div(id="moyenne-generale",
                                     className="text-center p-3 border rounded shadow-sm")
                        ], width=6),
                        dbc.Col([
                            html.Div(id="nombre-matieres",
                                     className="text-center p-3 border rounded shadow-sm")
                        ], width=6)
                    ])
                ], className="px-4")
            ], className="shadow-sm h-100")
        ], md=12, lg=8)
    ], className="mb-4"),

    # Zone des graphiques
    dbc.Row([
        # Graphique principal des notes
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("Performance par matière", className="text-white mb-0"),
                    className="bg-primary"
                ),
                dbc.CardBody([
                    dcc.Graph(id='grades-graph')
                ], className="px-4")
            ], className="shadow-sm h-100")
        ], md=12, lg=8),

        # Graphique de répartition des UEs
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("Répartition par UE", className="text-white mb-0"),
                    className="bg-primary"
                ),
                dbc.CardBody([
                    dcc.Graph(id='average-grade-pie-chart')
                ], className="px-4")
            ], className="shadow-sm h-100")
        ], md=12, lg=4)
    ])
], fluid=True, style={
    'backgroundColor': colors['background'],
    'minHeight': '100vh',
    'padding': '2rem',
    'fontFamily': 'Segoe UI, Roboto, sans-serif'
})


# =============================================================================
# CALLBACKS (INTERACTIVITÉ)
# =============================================================================

# Les callbacks gèrent toute l'interactivité de l'application.
# Chaque callback est déclenché par une action utilisateur spécifique :
# - Sélection d'un étudiant
# - Changement d'UE
# - Interaction avec les graphiques
# Chaque callback met à jour un ou plusieurs éléments de l'interface utilisateur.
# Callback 1: Préparation des données de l'étudiant sélectionné
@app.callback(
    Output('student-data-store', 'data'),
    Input('student-dropdown', 'value')
)
def prepare_student_data(selected_student):
    """
    Prépare les données pour l'étudiant sélectionné.
    Cette fonction est appelée chaque fois qu'un nouvel étudiant est sélectionné.

    Args:
        selected_student (str): Nom complet de l'étudiant sélectionné

    Returns:
        dict: Données de l'étudiant formatées pour l'affichage
    """
    if not selected_student or not isinstance(selected_student, str) or df.empty:
        return None

    try:
        # Séparation du prénom et du nom avec gestion d'erreur
        parts = selected_student.split(' ', 1)
        if len(parts) != 2:
            print(f"Format de nom d'étudiant incorrect: {selected_student}")
            return None

        prenom, nom = parts
        student_mask = (df['Prenom'] == prenom) & (df['Nom'] == nom)

        if not student_mask.any():
            print(f"Aucune donnée trouvée pour l'étudiant: {selected_student}")
            return None

        # Préparation du dictionnaire de données
        student_data = df[student_mask].to_dict('records')
        ues = sorted(list(set(item['UE'] for item in student_data)))

        return {
            'student_records': student_data,  # Notes et matières
            'available_ues': ues,  # Liste des UEs disponibles
            'student_name': selected_student  # Nom pour l'affichage
        }
    except Exception as e:
        print(f"Erreur lors de la préparation des données: {e}")
        return None


# Callback 2: Mise à jour du menu déroulant des UEs
@app.callback(
    Output('ue-dropdown', 'options'),
    Output('ue-dropdown', 'value'),
    Input('student-data-store', 'data')
)
def update_ue_dropdown(student_data):
    """
    Met à jour les options du menu déroulant des UEs en fonction de l'étudiant sélectionné.

    Args:
        student_data (dict): Données de l'étudiant actuel

    Returns:
        tuple: (Liste des options UE, Valeur sélectionnée (None par défaut))
    """
    if not student_data:
        return [], None

    # Création des options pour le dropdown des UEs
    ue_options = [{'label': ue, 'value': ue} for ue in sorted(student_data['available_ues'])]
    return ue_options, None  # Réinitialisation de la sélection




# Callback 3: Mise à jour du graphique des notes
@app.callback(
    Output('grades-graph', 'figure'),
    Input('student-data-store', 'data'),
    Input('ue-dropdown', 'value')
)
def update_grades_graph(student_data, selected_ue):
    """
    Génère le graphique des notes avec les statistiques de classe.
    """
    if not student_data:
        return px.bar(title="Aucun étudiant sélectionné.")

    # Préparation des données
    student_df = pd.DataFrame(student_data['student_records'])

    if selected_ue:
        student_df = student_df[student_df['UE'] == selected_ue]

    if student_df.empty:
        return px.bar(title="Aucune note disponible.")

    # Calcul des statistiques de classe
    class_stats = df.groupby('Matière').agg({
        'Note': ['mean', 'min', 'max']
    }).reset_index()
    class_stats.columns = ['Matière', 'Moyenne_Classe', 'Min_Classe', 'Max_Classe']

    plot_data = student_df.merge(class_stats, on='Matière', how='left')

    fig = go.Figure()

    # Création d'un tableau de couleurs pour chaque note selon les critères
    colors_per_grade = []
    for note in plot_data['Note']:
        if note < 10:
            colors_per_grade.append('red')  # Rouge pour notes < 10
        elif note == 10:
            colors_per_grade.append('orange')  # Orange pour notes = 10
        else:
            colors_per_grade.append('green')  # Vert pour notes > 10

    # Barres des notes de l'étudiant avec couleurs conditionnelles
    fig.add_trace(go.Bar(
        x=plot_data['Matière'],
        y=plot_data['Note'],
        name="Note de l'étudiant",
        marker_color=colors_per_grade,
        hovertemplate="Note: %{y:.2f}/20<extra></extra>"
    ))

    # Points pour les moyennes de classe
    fig.add_trace(go.Scatter(
        x=plot_data['Matière'],
        y=plot_data['Moyenne_Classe'],
        name='Moyenne de classe',
        mode='markers',
        marker=dict(
            symbol='diamond',
            size=12,
            color=colors['accent'],
            line=dict(color='white', width=1)
        ),
        hovertemplate="Moyenne: %{y:.2f}/20<extra></extra>"
    ))

    # Min/Max de classe
    fig.add_trace(go.Scatter(
        x=plot_data['Matière'],
        y=plot_data['Min_Classe'],
        name='Minimum',
        mode='lines+markers',
        line=dict(color=colors['warning'], width=0),
        marker=dict(symbol='triangle-down', size=8, color=colors['warning']),
        hovertemplate="Min: %{y:.2f}/20<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=plot_data['Matière'],
        y=plot_data['Max_Classe'],
        name='Maximum',
        mode='lines+markers',
        line=dict(color=colors['success'], width=0),
        marker=dict(symbol='triangle-up', size=8, color=colors['success']),
        hovertemplate="Max: %{y:.2f}/20<extra></extra>"
    ))

    # Personnalisation avancée
    fig.update_layout(
        title=dict(
            text=f"Performance détaillée de {student_data['student_name']}",
            font=dict(size=20, family="Segoe UI, Roboto", color=colors['text']),
            x=0.5,
            y=0.95
        ),
        xaxis=dict(
            title="",
            tickangle=-45,
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        yaxis=dict(
            title="Note /20",
            range=[0, 20],
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0)',
        height=450,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        ),
        margin=dict(l=40, r=40, t=80, b=40),
        hovermode='closest'
    )

    # Ligne de la moyenne avec annotation
    fig.add_shape(
        type="line",
        x0=-0.5,
        y0=10,
        x1=len(plot_data['Matière'].unique()) - 0.5,
        y1=10,
        line=dict(
            color=colors['secondary'],
            width=1.5,
            dash="dot"
        )
    )

    # Ajout d'une annotation pour la ligne de moyenne
    fig.add_annotation(
        x=len(plot_data['Matière'].unique()) - 0.5,
        y=10,
        xref="x",
        yref="y",
        text="Moyenne requise",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1,
        ax=50,
        ay=-20,
        font=dict(size=10, color=colors['secondary'])
    )

    return fig

# Callback 4: Mise à jour du graphique (barres verticales alignées avec le graphique principal)
@app.callback(
    Output('average-grade-pie-chart', 'figure'),
    Input('student-data-store', 'data')
)
def update_average_grade_chart(student_data):
    """
    Génère un diagramme à barres verticales montrant la moyenne par UE,
    avec un style visuel aligné sur le graphique principal.
    
    Args:
        student_data (dict): Données de l'étudiant

    Returns:
        go.Figure: Figure Plotly avec le diagramme à barres verticales
    """
    if not student_data:
        return go.Figure().update_layout(title="Aucun étudiant sélectionné.")

    # Préparation des données
    filtered_df = pd.DataFrame(student_data['student_records'])

    if filtered_df.empty:
        return go.Figure().update_layout(title="Aucune donnée disponible.")

    # Calcul des moyennes par UE
    average_grades = filtered_df.groupby('UE')['Note'].mean().reset_index()
    average_grades['Note'] = average_grades['Note'].round(1)  # Arrondi à 1 décimale pour plus de clarté
    
    # Ajout du nombre de matières par UE pour l'info au survol
    ue_counts = filtered_df.groupby('UE')['Matière'].nunique().reset_index()
    average_grades = average_grades.merge(ue_counts, on='UE')
    
    # Trier par UE pour une meilleure lisibilité
    average_grades = average_grades.sort_values('UE')
    
    # Générer les couleurs pour les barres en fonction des moyennes
    bar_colors = []
    for note in average_grades['Note']:
        if note < 10:
            bar_colors.append(colors['warning'])  # Rouge pour notes < 10
        elif note == 10:
            bar_colors.append('orange')  # Orange pour notes = 10
        else:
            bar_colors.append(colors['success'])  # Vert pour notes > 10

    # Création du diagramme à barres verticales
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=average_grades['UE'],
        y=average_grades['Note'],
        text=average_grades['Note'].apply(lambda x: f"{x:.1f}"),
        textposition='auto',
        marker_color=bar_colors,
        hovertemplate='<b>%{x}</b><br>Moyenne: %{y:.1f}/20<br>Nombre de matières: %{customdata}<extra></extra>',
        customdata=average_grades['Matière']
    ))
    
    # Ajout d'une ligne horizontale à 10/20 pour la moyenne requise
    fig.add_shape(
        type="line",
        x0=-0.5,
        y0=10,
        x1=len(average_grades['UE']) - 0.5,
        y1=10,
        line=dict(
            color=colors['secondary'],
            width=1.5,
            dash="dot"
        )
    )
    
    # Personnalisation du graphique pour l'aligner avec le graphique principal
    fig.update_layout(
        title=dict(
            text=f"Moyenne par UE",
            font=dict(size=20, family="Segoe UI, Roboto", color=colors['text']),
            x=0.5,
            y=0.95
        ),
        xaxis=dict(
            title="",
            tickangle=-45,  # Aligné avec le graphique principal
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        yaxis=dict(
            title="Note /20",
            range=[0, 20],
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True,
            tickvals=[0, 5, 10, 15, 20]
        ),
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0)',
        height=450,  # Même hauteur que le graphique principal
        margin=dict(l=40, r=40, t=80, b=40),  # Même marge que le graphique principal
        bargap=0.3
    )
    
    # Ajout d'une annotation pour la ligne de moyenne (alignée avec le graphique principal)
    fig.add_annotation(
        x=len(average_grades['UE']) - 0.5,
        y=10,
        xref="x",
        yref="y",
        text="Moyenne requise",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1,
        ax=50,
        ay=-20,
        font=dict(size=10, color=colors['secondary'])
    )
    
    return fig

# Callback 5: Mise à jour des statistiques globales
@app.callback(
    Output('moyenne-generale', 'children'),
    Output('nombre-matieres', 'children'),
    Input('student-data-store', 'data')
)
def update_statistics(student_data):
    """
    Calcule et affiche les statistiques globales de l'étudiant.

    Affiche :
    - La moyenne générale (en vert si ≥ 10, en rouge sinon)
    - Le nombre total de matières

    Args:
        student_data (dict): Données de l'étudiant

    Returns:
        tuple: (HTML pour la moyenne, HTML pour le nombre de matières)
    """
    if not student_data:
        return "Pas de données", "Pas de données"

    filtered_df = pd.DataFrame(student_data['student_records'])

    if filtered_df.empty:
        return "Pas de données", "Pas de données"

    # Calcul des statistiques
    moyenne = filtered_df['Note'].mean()
    nb_matieres = filtered_df['Matière'].nunique()

    # Création des éléments HTML avec style conditionnel
    moyenne_html = html.Div([
        html.H4("Moyenne générale", className="text-muted"),
        html.H2(f"{moyenne:.2f}/20",
                className=f"{'text-success' if moyenne >= 10 else 'text-danger'}",
                style={'fontWeight': 'bold'})
    ])

    matieres_html = html.Div([
        html.H4("Nombre de matières", className="text-muted"),
        html.H2(f"{nb_matieres}", className="text-primary", style={'fontWeight': 'bold'})
    ])

    return moyenne_html, matieres_html


# =============================================================================
# LANCEMENT DE L'APPLICATION
# =============================================================================
if __name__ == '__main__':
    app.run(debug=True)  # Mode debug activé pour le développement
     # Permet le rechargement automatique lors des modifications du code