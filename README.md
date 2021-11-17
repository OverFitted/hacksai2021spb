# Hacks AI 2021 (Spb)

Repo for Hacks AI 2021 in SPB

## Parsers

Parsers part was mainly written by @doogeemodulny.
For people "*feedback*" we parsed:
Хабр (habr.com) and cnews (cnews.ru)

For companies "*feedback*" we parsed:
Хабр (habr.com), Главная Портал Закупок (zakupki.gov.ru), тинькофф журнул (journal.tinkoff.ru), vc.ru (vc.ru) and cnews (cnews.ru)

### Usage

To parse everything just run `parse_all.py` using python3

### Input

As the input, parser takes `input.txt` formated like

```text
Company - People (Person, Person, Person etc) - nomination
Company - People (Person, Person, Person etc) - nomination
```

### Output

Parsers output json file with all the data

```json
[{
  company: {
    "company": {
      "goszakupki": [{
        "id": int,
        "value": int,
        "description": string,
        "date": string (d.m.y format)
      }],
      "habr": {
        "company_info": {
          "description": string,
          "industries": [
            string
          ],
          "rate": float,
          "subscribers_str": string,
          "subscribers_quantity": int
        },
        "references": [
          string
        ],
        "references_quantity": int
      },
      "vcru": {
        "company": string,
        "texts": [
          string
        ]
      },
      "tinkoff_journal": {
        "company": string,
        "texts": [
          string
        ]
      },
      "cnews": [{
        "date": string (d.m.y h:M format),
        "text": string
      }]
    },
    "people": [{
      "cnews": [{
        "date": string (d.m.y h:M format),
        "text": string
      }],
      "habr": {
        "company_info": {
          "description": string,
          "industries": [
            string
          ],
          "rate": float,
          "subscribers_str": string,
          "subscribers_quantity": int
        },
        "references": [
          string
        ],
        "references_quantity": int
      }
    }]
  }
}]
```

### Parsers TODO

* Add more sources
  * Twitter
* Make data format same for all sources

## AI

AI part was mainly written by @mike-yasunov.

### Structure

#### BERT

We used BERT (bert-base-multilingual-uncased) from simpletransformers to predict *real* organization category (nomination)

#### CatBoost

We used catboost (and text features) from Yandex to classify comments and reviews about organization

### Models input

As the input, the ai-script takes parsed json (aka dataset.json). Then it concatenates all texts and *sends* this data to the models.

### Models output

#### BERT output

The output of BERT network is a class of comment or review (0, 1 or 2), where 0 states for negative, 1 for positive and 2 for neutral

#### CatBoost output

The output of CatBoost is the probability of each nomination

## Web

Web part was mainly written by @OverFitted.

### Backend

As main framework we decided to go with express.js (aka fast, unopinionated, minimalist web framework)

### Frontend

And as templating language with Handlebars

## Web TODO and FIXIT

For now data from python can't be sent to web part.
