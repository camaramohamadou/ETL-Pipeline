# Drug ETL Pipeline

Ce projet est un pipeline ETL pour traiter des données liées aux médicaments, aux essais cliniques et aux publications PubMed. Le pipeline extrait, transforme et charge les données pour générer un graphe JSON des liens entre les médicaments et les journaux où ils sont mentionnés.

## Installation

1. Clonez le repository.
git clone <URL_DU_REPOSITORY>
cd <NOM_DU_REPOSITORY>

2. make init

3. make run

4. make test

5. make clean

### 6. **Après Exécution**
Le graphe JSON généré sera disponible dans `data/output/drug_graph.json`.
Ainsi pipeline.log contient les logs du pipeline. dans le dossier data/output.
