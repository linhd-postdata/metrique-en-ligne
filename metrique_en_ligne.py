#!/usr/bin/env python
# -*- coding: utf-8 -*-
# !pip install -q requests-html tqdm
import json
import os
import time
import sys
from collections import Counter
from optparse import OptionParser
from pathlib import Path
from urllib import parse

from requests_html import HTML
from requests_html import HTMLSession
from tqdm.auto import tqdm


def download(html_folder):
    session = HTMLSession()
    base_url = os.environ.get("AUTHORS_URL", "https://crisco2.unicaen.fr/verlaine/index.php?navigation=textesanalyses&choix_liste=poemes")
    base_response = session.get(base_url)
    authors = base_response.html.find("#constrainer2 > table:nth-child(1) > tbody:nth-child(2) > tr > td:nth-child(1) > a:nth-child(1)")
    visited = set()
    for author in tqdm(authors, "Downloading authors"):
        if author.absolute_links:
            works_url = list(author.absolute_links)[0]
            if works_url in visited:
                continue
            else:
                visited.add(works_url)
            works_response = session.get(works_url)
            works = works_response.html.find(".ref_ouvrage a")
            for workd_id, work in enumerate(tqdm(works, "Works", leave=False)):
                work_url = list(work.absolute_links)[0]
                # print("WORK", work_url)
                if work_url in visited:
                    continue
                else:
                    visited.add(work_url)
                parts_response = session.get(work_url)
                parts = parts_response.html.find(".ref_ouvrage a")
                texts = {}
                author_code = None
                for part in tqdm(parts, "Texts", leave=False):
                    part_url = list(part.absolute_links)[0]
                    if "code_text=" in part_url:
                        query = parse.urlsplit(part_url).query
                        params = dict(parse.parse_qsl(query))
                        author_code = params["auteur"]
                        text_code = params["code_text"]
                        # URLs ending with "_7" for rhyme and stanzas
                        params["code_text"] = f"{params['code_text']}_7"
                        part_url = part_url.replace(
                            query, parse.urlencode(params)
                        )
                        if part_url in visited:
                            continue
                        else:
                            visited.add(part_url)
                        part_response = session.get(part_url)
                        try:
                            texts_html = part_response.html.find(
                                "#textes", first=True
                            ).html
                        except AttributeError:
                            print(part_url)
                            continue
                        texts[text_code] = {
                            "url": part_url,
                            "html": texts_html,
                        }
                        time.sleep(0.2)
                if texts and author_code:
                    filename = f"{author_code}-{workd_id + 1}.json"
                    with open(html_folder / filename, "w") as raw:
                        json.dump(texts, raw, indent=4)


def parse(html_folder, json_folder):
    authors_works = {}
    for json_file in tqdm(list(html_folder.rglob("*.json")), "Parsing"):
        author_code = json_file.name.split("-")[0].split("_")[0]
        if author_code not in authors_works:
            authors_works[author_code] = []
        pairs = json.loads(json_file.open().read()).values()
        for pair in tqdm(pairs, author_code, leave=False):
            html = pair["html"]
            url = pair["url"]
            chunk = HTML(html=html)
            code = chunk.find(".div_code_poeme", first=True).text
            author = chunk.find(".div_auteur", first=True).text
            work = chunk.find(".div_recueil_titre_main", first=True).text
            date = chunk.find(".div_date", first=True).text
            title_main = chunk.find(".td_titre_main", first=True)
            title_num = chunk.find(".td_titre_num", first=True)
            if title_main:
                title = title_main.text
            elif title_num:
                title = title_num.text
            else:
                title = work
            profile = chunk.find(".td_profil > .span_infos_analyse_contenu",
                first=True).text
            structure = chunk.find(".td_forme > .span_infos_analyse_contenu",
                first=True).text
            author_work = {
                "code": code, "author": author, "work": work,
                "date": date, "title": title, "profile": profile,
                "structure": structure, "url": url,
            }
            stanzas = []
            for stanza in chunk.find(".table_lg"):
                verses = [s.text for s in stanza.find(".td_vers")]
                metres = [s.text for s in stanza.find("td[class^='td_met']")]
                rhymes = [s.text for s in stanza.find("td[class^='td_rime']")]
                stanzas.append([
                    {"verse": verse, "metre": metre, "rhyme": rhyme}
                    for verse, metre, rhyme in zip(*[verses, metres, rhymes])
                ])
            author_work["text"] = stanzas
            authors_works[author_code].append(author_work)
    for author_code, author_works in authors_works.items():
        with open(json_folder / f"{author_code}.json", "w") as author_json:
            json.dump(author_works, author_json, indent=4)


def build(json_folder, corpus_file):
    corpus = []
    for json_file in tqdm(list(json_folder.rglob("*.json")), "Building"):
        corpus.extend(json.loads(json_file.open().read()))
    with open(corpus_file, "w") as corpus_json:
        json.dump(corpus, corpus_json, indent=4)
    counter = Counter()
    author_set = set()
    stanza_counter = 0
    line_counter = 0
    word_counter = 0
    for work in corpus:
        author_set.add(work["author"])
        for stanza in work["text"]:
            stanza_counter += 1
            for line in stanza:
                counter.update([len(line["verse"])])
                line_counter += 1
                word_counter += len(line["verse"].split())
    print("Statistics\n----------")
    print("- Authors:", len(author_set))
    print("- Works:", len(corpus))
    print("- Stanzas:", stanza_counter)
    print("- Verses:", line_counter)
    print("- Words:", word_counter)
    print("- Characters:", sum(k * v for k, v in counter.items()))


if __name__ == '__main__':
    parser = OptionParser(
        "Generates a JSON corpus from the website 'Métrique en Ligne' "
        "(https://crisco2.unicaen.fr/verlaine/)"
    )
    parser.add_option("--steps",
            help="steps to run (comma separated values): "
                 "1 download, 2 parse, 3 generate. "
                 "Defaults to 1,2,3",
            default="1,2,3")
    parser.add_option("--html-folder",
            help="path to downloaded html content. "
                 "Defaults to './html'",
            default="html")
    parser.add_option("--json-folder",
            help="path to parsed json content. "
            "Defaults to './json'",
            default="json")
    parser.add_option("--corpus-file",
            help="path to generated json corpus. "
                 "Defaults to './metrique_en_ligne.json'",
            default="metrique_en_ligne.json")
    options, _ = parser.parse_args()
    steps = set([
        int(step.strip()) for step in options.steps.split(",") if step.strip()
    ])
    if 1 in steps:
        download(Path(options.html_folder))
    if 2 in steps:
        parse(Path(options.html_folder), Path(options.json_folder))
    if 3 in steps:
        build(Path(options.json_folder), options.corpus_file)
