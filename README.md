Gestion des Requêtes et Threads
Afin d'éviter que des requêtes ne soient stoppées par le serveur Reddit, nous avons mis en place un système pour limiter le spam. Chaque thread attend 5 secondes avant d'envoyer 4 nouvelles requêtes. De plus, si des conflits surviennent, les requêtes en conflit attendent avant de tenter à nouveau (1/5s dans leur propre thread). Le nombre de requêtes et le temps d'attente peuvent être ajustés en fonction de votre connexion et des demandes bloquées par le serveur.

Points à noter :
Durée de vie des threads : Chaque thread a une durée de vie de 1 minute. Attention, j'ai remarqué un bug qui empêche la fermeture correcte d'un thread.

Modifications à apporter :

Le temps d'attente pour la fermeture de tous les threads est défini une fois que la liste d'URLs est terminée. Une fois la tâche d'un thread accomplie, il peut se fermer de manière autonome. Cependant, ceux qui rencontrent des erreurs ne pourront se fermer qu'une fois la liste traitée.

Certains threads rencontrent un bug et ne se ferment jamais correctement. Cela nécessite d'être investigué pour identifier la cause exacte.

Erreur spécifique :

Ligne 32 : ydl.extract_info(url, download=False) provoque une boucle infinie et empêche le thread de se fermer correctement malgré l'interruption demandée. Je n'ai pas encore trouvé la solution.
Idée 1 : Il est possible que le format demandé dans l'URL ne soit pas trouvé, ce qui lance une recherche en boucle.
Idée 2 : Trop de sous-liens associés à l'URL peuvent aussi être en cause.
