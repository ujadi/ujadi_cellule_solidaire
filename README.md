# Cellule Solidaire UJADI

Un module Odoo pour la gestion des **cellules solidaires de l’UJADI** (Union des Jeunes Actifs pour le Développement Intégral).

## 🔍 Fonctionnalités principales

- Création et gestion des **cellules solidaires**
- Enregistrement des **membres** avec leurs informations
- Attribution de **responsables** par cellule
- Vue d'ensemble structurée via un menu clair et intuitif

## 🧩 Modèles inclus

### 1. `cellule.solidaire`
- Nom de la cellule  
- Date de création  
- Responsable lié

### 2. `membre.cs`
- Nom, prénom, sexe, date de naissance  
- Cellule d’appartenance  
- Contact, rôle, etc.

### 3. `responsable.cs`
- Nom complet  
- Coordonnées  
- Cellule dirigée

## 📁 Arborescence

```bash
cellule_solidaire_ujadi/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── cellule_solidaire.py
│   ├── membre_cs.py
│   └── responsable_cs.py
├── security/
│   └── ir.model.access.csv
├── views/
│   ├── cellule_solidaire_views.xml
│   ├── membre_cs_views.xml
│   ├── responsable_cs_views.xml
│   └── cellule_solidaire_menus.xml
└── README.md
```
## 🚀 Installation

1. Cloner le dépôt dans le dossier `custom_addons` :

   ```bash
   cd /chemin/vers/odoo/custom_addons
   git clone https://github.com/ujadi/ujadi_cellule_solidaire.git




- Ici, la ligne avec les commandes est dans un **bloc de code** délimité par trois backticks ```` ```bash ```` pour que ça s’affiche joliment en console.
- Le reste est en liste numérotée ou simple texte, avec des retours à la ligne doubles `  ` pour faire un saut de ligne simple.

---

### 2. Section ✅ À venir

```markdown
## ✅ À venir

- Exportation des rapports PDF  
- Intégration avec des groupes WhatsApp/Telegram  
- Historique de contribution solidaire


## 👩🏽‍💻 Auteur

**Annette Bwemere Salama**  
_Anny Consulting_  
📧 [bwemereannette@gmail.com](mailto:bwemereannette@gmail.com)  
📞 +243 850 081 145

## 📌 Licence

Ce module est publié sous licence **Odoo LGPL v3**.
