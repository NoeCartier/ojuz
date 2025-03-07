# Projet "Problem Of The Week" ou POTW


## Historique du projet

En mai 2023, j'ai commencé à développer un bot Discord pour un projet nommé : "Problem Of The Day" ou POTD. Le but de ce projet était d'inciter les candidats (dont moi à l'époque) à réfléchir à des problèmes difficiles régulièrement, car en effet, un entraînement régulier vaut mieux qu'un effort bref et intense. Chaque jour était donc publié un problème aléatoire du site oj.uz (répertoriant des centaines de sujets d'olympiades nationales et internationales) et l'ensemble des candidats étaient invités à chercher ce problème et à soumettre une soumission si possible. J'ai pu tester cette méthode pendant deux mois (avec quelques candidats). Les résultats étaient très peu concluants. Les principaux problèmes qui émergeaient étaient tout d'abord que la cadence de publication était trop élevée, en effet un problème aussi complexe à résoudre tous les jours n'était clairement pas tenable pour le long terme. Un deuxième problème majeur était le fait que les problèmes publiés étaient choisis aléatoirement, les problèmes publiés étaient donc parfois inintéressants ou trop complexes...

En repensant au projet deux ans plus tard, je me suis mis en tête d'améliorer les choses qui n'allaient pas pour aider les candidats à progresser en vue des sélections IOI (et des IOI). 

## Les deux principales modifications apportées sont les suivantes :
- Les problèmes sont publiés tous les lundis au lieu de tous les jours. Les candidats ont alors une semaine pour réfléchir au problème.
- Les entraineurs peuvent suggérer (à l'aide d'une commande) des problèmes qui seront priorisés et publiés dès que possible (le lundi prochain si aucun autre problème n'est proposé).

## Fonctionnalités additionnelles :
- Soumission automatisée : Les participants peuvent soumettre leurs solutions sur oj.uz, et leurs scores sont automatiquement mis à jour toutes les 5 minutes (ou manuellement via la commande !update)
- Un leaderboard est publié à la fin de chaque semaine, pour valoriser les candidats qui se sont investis.

## Commandes disponibles

- `?register <handle>` : Enregistre l'utilisateur avec son identifiant OJ.uz.
- `?update` : Met à jour la base de données avec les dernières soumissions.
- `?post_POTW` : Publie le problème de la semaine (POTW). Seuls les entraîneurs peuvent utiliser cette commande.
- `?add_problem <problem_code> <problem_title> <problem_priority> <problem_link>` : Ajoute un problème à la base de données. Seuls les entraîneurs peuvent utiliser cette commande.

Note :le système est actuellement calibré pour les candidats préparant les sélections IOI et n'est donc pas adapté aux participants plus jeunes.
(Une future mise à jour pourrait introduire différents niveaux de difficulté, mais cette fonctionnalité n'est pas encore planifiée.)