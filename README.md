# Métrique en Ligne Corpus
This corpus is a subset in JSON format of the available poems in [métrique en ligne](https://crisco2.unicaen.fr/verlaine/index.php?navigation=accueil) (accessed on June 1st, 2020).

It containes more than 5000 poems from over 60 authors, with metrical information (metrical length), rhyme, metrical profile, and structure (where available).

Statistics
----------
- Authors: 61
- Works: 5081
- Stanzas: 41274
- Verses: 247248
- Words: 1850222
- Characters: 10131087


The file [`metrique_en_ligne.json`](./metrique_en_ligne.json) contains the corpus. The format of each entry is as follows:
```json
{
    "code": "RIC_1/RIC1",
    "author": "Jean Richepin",
    "work": "LA CHANSON DES GUEUX",
    "date": "1881",
    "title": "BALLADE DU ROI DES GUEUX",
    "profile": "8",
    "structure": "petite ballade",
    "url": "https://crisco2.unicaen.fr/verlaine/index.php?navigation=textesauteurs&auteur=RIC_1&code_text=RIC1_7",
    "text": [
        [
            {
                "verse": "Venez \u00e0 moi, claquepatins,",
                "metre": "8",
                "rhyme": "a"
            },
            {
                "verse": "Loqueteux, joueurs de musettes,",
                "metre": "8",
                "rhyme": "b"
            },
            ...
        ],
        ...
    ]
}
```

Folder [`json`](./json) contains the works by author, and [`html`](./html) contains the raw downloads of the pages.

The script [`metrique_en_ligne.py`](./metrique_en_ligne.py) was used to download and extract all the data.
```bash
$ ./metrique_en_ligne.py --help
Usage: Generates a JSON corpus from the website 'Métrique en Ligne' (https://crisco2.unicaen.fr/verlaine/)

Options:
  -h, --help            show this help message and exit
  --steps=STEPS         steps to run (comma separated values): 1 download, 2
                        parse, 3 generate. Defaults to 1,2,3
  --html-folder=HTML_FOLDER
                        path to downloaded html content. Defaults to './html'
  --json-folder=JSON_FOLDER
                        path to parsed json content. Defaults to './json'
  --corpus-file=CORPUS_FILE
                        path to generated json corpus. Defaults to
                        './metrique_en_ligne.json'

```
