# Travail de bachelor - Détection d'anomalies VPN

Le projet analyse 6 mois de logs d'accès VPN fournis par une entreprise partenaire anonymisée.
L'objectif est de repérer les connexions suspectes, par exemple depuis un pays inhabituel
ou à des heures anormales.

Le modèle retenu est un Isolation Forest, entraîné sur environ 120'000 connexions.
Il détecte 87 % des anomalies injectées lors des tests, avec un taux de faux positifs de 4 %.

Le superviseur du projet était le professeur Marc Dubois.
La principale difficulté a été le nettoyage des données : environ 15 % des logs étaient incomplets.