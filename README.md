# Projet_TAL_REN

Un programme de reconnaissance d'entités nommées (REN) qui applique une approche à base de règles et des ressources externes pour identifier les entités de type personne (PER), organization/entreprise (ORG) et lieu (LOC). 
Et établir un système d'évaluation.

## Chargement de corpus 
Dans un premier temps, nous allons convertir un corpus xml en txt à l'aide du programme `corpus_converter.py`.

A partir de la ligne de commande, dans le répertoire où on a téléchargé le dossier, on saisit la commande suivante : 

```
$ python corpus_converter.py
```

Et ensuite on saisit les noms des corpus qui sont présents dans le répertoire `Corpora` :

```
Enter the training corpus: Corpora/corpus_train_annotated_clean.xml
New file created: text_train_tokenized_clean.txt
Enter the test corpus: Corpora/corpus_test_annotated_clean.xml
New file created: text_test_tokenized_clean.txt
```

Les deux corpus sont maintenant tokenisés et étiquetés selon la représention BIO. On peut utiliser la commande `head` pour regarder le début du corpus :

```
$ head -n 50 Corpora/text_train_tokenized_clean.txt
```

## Reconnaissance des entités nommées et métriques d'évaluation

Après avoir obtenu les corpus au format txt, on passe à la phase du test du système.
On lance le programme : 

```
python ner_tagger.py
```

Au bout de quelques secondes, on saisit le nom du corpus que l'on va tester, dans ce cas, notre nouveau corpus de test :
```
Please choose a corpus: Corpora/text_test_tokenized_clean.txt
```

Ensuite, le programme effectuera une annotation et créera une nouveau fichier avec les étiquettes de prédiction qui s'appelle `output.txt`

Pour compter le nombre d'entités reconnues par type on se sert de `grep` : 

```
$ grep -c 'LOC' output.txt
```

A l'aide de `sort` et `uniq` on arrive à compter les entités reconnues les plus fréquentes :

```
$ sort output.txt | uniq -c | sort -n -r | grep 'B-' | head -n 20
```
