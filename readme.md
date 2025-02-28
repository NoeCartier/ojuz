# Projet "Problem Of The Week" ou POTW
En mai 2023, j'ai commencé à développer un bot Discord pour un projet nommé : "Problem Of The Day" ou POTD. Le but de ce projet était d'inciter les candidats (dont moi à l'époque) à réfléchir à des problèmes difficiles régulièrement, car en effet, un entraînement régulier vaut mieux qu'un effort bref et intense. Chaque jour était donc publié un problème aléatoire du site oj.uz (répertoriant des centaines de sujets d'olympiades nationales et internationales) et l'ensemble des candidats étaient invités à chercher ce problème et à soumettre une soumission si possible. J'ai pu tester cette méthode pendant deux mois (avec quelques candidats). Les résultats étaient très peu concluants. Les principaux problèmes qui émergeaient étaient tout d'abord que la cadence de publication était trop élevée, en effet un problème aussi complexe à résoudre tous les jours n'était clairement pas tenable pour le long terme. Un deuxième problème majeur était le fait que les problèmes publiés étaient choisis aléatoirement, les problèmes publiés étaient donc parfois inintéressants ou trop complexes...

En repensant au projet deux ans plus tard, je me suis mis en tête d'améliorer les choses qui n'allaient pas pour aider les candidats à progresser en vue des sélections IOI (et des IOI). 

## Les deux principales modifications apportées sont les suivantes :
- Les problèmes sont publiés tous les lundis au lieu de tous les jours. Les candidats ont alors une semaine pour réfléchir au problème.
- Les entraineurs peuvent suggérer (à l'aide d'une commande) des problèmes qui seront priorisés et publiés dès que possible (le lundi prochain si aucun autre problème n'est proposé).

## Fonctionnalités additionnelles :
- Soumission automatisée : Les participants peuvent soumettre leurs solutions sur oj.uz, et leurs scores sont automatiquement mis à jour toutes les 5 minutes (ou manuellement via la commande !update)
- Un leaderboard est publié à la fin de chaque semaine, pour valoriser les candidats qui se sont investis.

## État actuel et perspectives
Le bot est actuellement en phase de bêta-test depuis une semaine. Cette fois-ci, j'observe de meilleurs résultats. Une semaine semble être une durée optimale, pour ce genre de problèmes complexes. J'observe aussi une entraide entre certains candidats. Je constate aussi que le fait que des entraineurs proposent un problème est un vrai plus. En effet, les problèmes ainsi proposés sont donc adaptés aux candidats visant les IOI, plus éducatifs et intéressants.

J'aimerais partager ce projet à tous les membres du serveur avec votre accord. De plus **j'encourage tous les entraineurs qui le veulent à suggérer des problèmes pertinents (cela prend très peu de temps et rend le bot beaucoup plus utile)**. Ces entraineurs volontaires peuvent également s'ils le souhaitent donner un/des indices aux candidats en milieu de semaine si le problème obtient peu de réussite...

Note :le système est actuellement calibré pour les candidats préparant les sélections IOI et n'est donc pas adapté aux participants plus jeunes.
(Une future mise à jour pourrait introduire différents niveaux de difficulté, mais cette fonctionnalité n'est pas encore planifiée.)