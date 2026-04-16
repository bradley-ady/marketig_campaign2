Marketing Analytics & Customer Scoring — 2026 
Bradley Belizaaire et Fethi Ouzaa
Objectif du Projet 

Ce projet vise à optimiser la stratégie marketing d'une entreprise orientée performance commerciale en utilisant la Data Science et la Business Intelligence. L'objectif est de segmenter la base clients et de prédire le potentiel de réponse à une campagne pour cibler les actions marketing de manière plus efficace et réduire le coût d'acquisition. 

Stack Technique 

Analyse & Machine Learning : Python (Pandas, NumPy, Scikit-Learn, Statsmodels, SciPy) 

Algorithmes : K-Means (Clustering) et Régression Logistique (Scoring) 

Visualisation : Plotly Dash (dashboard interactif) · Matplotlib · Seaborn 

Gestion de version : Git / GitHub 

 

Étapes Clés 

Audit & Nettoyage des données : Traitement des valeurs manquantes (imputation médiane sur Income), suppression des outliers, correction des anomalies de codage (Marital_Status), suppression des colonnes à variance nulle. 

Feature Engineering : Construction de 10 variables métier (Age, TotalSpend, CustomerDays, TotalAccepted, SpendPerIncome, RFM_score, etc.). 

Analyse Multidimensionnelle : Matrice de corrélation, ANOVA, MANOVA, corrélation partielle, détection de multicolinéarité (VIF). 

Segmentation Clients (K-Means, k=4) : Identification de 4 profils types — Champions, Fidèles Actifs, Clients Modérés, Petits Budgets. 

Modèle de Scoring : Régression logistique prédisant la probabilité de réponse à une campagne marketing, avec score appliqué à l'ensemble du portefeuille. 

Dashboard Décisionnel : Outil interactif Dash permettant de piloter la stratégie par segment. 

 

Résultats 

Segmentation — 4 profils identifiés : 

Segment 

Revenu moy. 

Dépense moy. 

Taux de réponse 

Champions 
~80 000€ 
~1 620€ 
~60% 

Fidèles Actifs 
~69 000€ 
~1 083€ 
~10% 

Clients Modérés 
~45 000€ 
~240€ 
~10% 

Petits Budgets 
~32 000€ 
~148€ 
~10% 

Modèle de scoring : 

AUC-ROC : 0.86 sur le jeu de test 

Cross-validation 5-fold : AUC stable à ±0.02 

Cibler les déciles 8–10 (score > 0.40) permet de concentrer 70% du budget sur les 30% de clients les plus susceptibles de répondre 

Dashboard interactif — 4 vues : 

Portefeuille clients (distribution revenus, éducation, dépenses) 

Segmentation (scatter interactif avec axes au choix) 

Performance campagnes (taux d'acceptation par campagne et par segment) 

KPI exécutifs filtrables par segment (RFM, canaux d'achat, scores) 

 

Robustesse, Limites & Risques 

Robustesse : Test de sensibilité aux outliers réalisé — l'AUC varie de moins de 0.01 selon le seuil de nettoyage retenu. Résultat jugé stable. 

Risques : Le dataset est un snapshot statique (2012–2014) ; les comportements pré-2024 peuvent biaiser les prédictions face aux évolutions économiques récentes (inflation, nouveaux canaux digitaux). 

Data leakage : Les variables AcceptedCmp1-5 sont des signaux de campagnes passées, légitimement utilisés comme features comportementales et non comme proxies de la cible. 

Amélioration : Une industrialisation via une API (FastAPI) permettrait de scorer les nouveaux clients en temps réel. L'usage de Random Forest ou XGBoost pourrait améliorer l'AUC au-delà de 0.90. 

 

Recommandations Business Finales 

Focus Champions : Allouer 60% du budget marketing sur le segment Champions avec des offres exclusives sur les vins premium et les produits carnés — taux de réponse ~60%, ROI maximal. 

Activation Fidèles Actifs : Proposer des programmes de fidélisation et des offres de cross-selling (bundles Vin & Viande) pour augmenter le panier moyen et la réactivité aux campagnes. 

Ciblage par score : Utiliser le score de conversion pour prioriser les envois — ne contacter que les clients avec ScoreCampagne > 0.40 afin de réduire les coûts de contact de ~70%. 

Suivi mensuel : Monitorer le taux de réponse global, le score RFM moyen et l'AUC du modèle pour détecter tout drift comportemental. 

Installation & Lancement 

# Installer les dépendances 
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels scipy plotly dash dash-bootstrap-components 
 
# Lancer le dashboard 
python dashboard.py 
# → Ouvrir http://127.0.0.1:8050

---

*Dataset source : [Kaggle — Marketing Campaign](https://www.kaggle.com/datasets/rodsaldanha/arketing-campaign) · Bachelor 3 YNOV — IA & Data · 2026*
