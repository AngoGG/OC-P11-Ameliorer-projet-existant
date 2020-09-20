# OpenClassrooms Projet 11: Améliorez un projet existant en python

Ce répertoire contiendra les développemments du projet 11. L'objectif de ce projet est d'améliorer un projet existant, qui consistera ici à ajouter 2 fonctionnalités au projet 8.

## Fonctionnalités à ajouter

3 fonctionnalités vont être ajoutées suite à une demande client:

- Possibilité de changer le mot de passe utilisateur
- Possibilité de réinitialiser le mot de passe d'un utilisateur
- Possibilité de choisir les catégories à importer depuis l'API Open Food Facts

## Evolution de fonctionnalité

La commande de récupération et d'insertion des produits en base de données va également être revue afin de ne plus être vidée entièrement à chaque nouvel import et de pouvoir permettre une mise à jour régulière de la base de données en production.

## Correction de bug

Un bug empêchant l'insertion de données en base a été remonté par le client. Le bug doit être corrigé et le test refactorisé afin de résoudre ce dernier.
