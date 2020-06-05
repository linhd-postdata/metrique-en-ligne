# Métrique en Ligne Corpus
This corpus is a subset in JSON format of the available poems in [métrique en ligne](https://crisco2.unicaen.fr/verlaine/index.php?navigation=accueil). It containes 5081 poems from 64 authors (41274 stanzas, 247248 verses, 1850222 words) with metrical information (metrical length), rhyme, metrical profile, and structure (where available).

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
