Climbing Route Chart Generator
==============================

[English version](README.md)

## Aperçu

__Climbing Route Chart Generator__ est une application Python conçue pour générer des graphiques de type camembert
pour visualiser les voies d'escalade en salle. Ces graphiques sont produits à partir d'une entrée CSV, illustrant
la distribution des cotations des voies et les ouvreurs associés. L'outil est idéal pour les gestionnaires de SAE
afin de mettre à jour rapidement et facilement les étiquettes après une campagne d'ouverture.

![Sample chart](screenshot.png)


## Outil en ligne

La manière la plus simple d'utiliser cet outil est d'utiliser la version en ligne hébergée par __Adrénaline Escalade__, un club d'escalade des Hauts de Seine (92) en France.

[https://etiquettes.adrenaline-escalade.com/](https://etiquettes.adrenaline-escalade.com/)


## Utilisation locale avec Docker

Ceci est l'option la plus simple, en supposant que vous avez déjà Docker installé :

      $ docker build -t climb-routes .
      $ docker run -p 8080:8080 climb-routes

Ouvrez votre navigateur et naviguez vers localhost:8080


## Utilisation locale avec CLI (interface en ligne de commande)

### Installation

Pour installer Climbing Route Chart Generator, suivez ces étapes :

1. Créez un environnement virtuel dans un dossier nommé "venv" :
   ```bash
   python -m venv venv
   ```
2. Activez l'environnement virtuel :
   - Sur Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Sur Linux or MacOS:
     ```bash
     source venv/bin/activate
     ```
3. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```

### Utilisation

Exécutez le script avec la commande suivante :

```bash
cd src
./route-charts.py -i <input_file.csv> [-o <output_file.pdf>]
```


### Arguments

Reportez-vous à la sortie de `./route-charts.py --help` pour une liste de tous les arguments optionnels.

### Format d'Entrée

L'entrée doit être un fichier CSV avec les colonnes suivantes :

- Relais
- Couleur
- Cotation
- Ouvreur

## Licence

Ce projet est libre de droit. Pour plus de détails, voir [UNLICENSE](UNLICENSE).
