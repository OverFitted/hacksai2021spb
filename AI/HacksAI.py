from sklearn.metrics import classification_report,accuracy_score
import pandas as pd
import numpy as np 
import json 
import io

import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split

import pymorphy2
from tqdm import tqdm
from catboost import CatBoostClassifier, Pool


def predict_func(data):
    company = data['company']
    gos = company['goszakupki']
    habr = company['habr']
    vcru = company['vcru']
    tj = company['tinkoff_journal']
    people = data['people']

    texts_kw = habr["company_info"]["description"] if habr["company_info"] else '' + ' '  + ' '.join(habr["company_info"]["industries"] if habr["company_info"] else []) + ' '  + ' '.join(tj['texts']) + ' ' + ' '.join([x['text'] for x in company["cnews"]]) + ' '.join([x['description'] for x in gos] if gos else []) 

    encode_company_classes = {'10-летие домена .РФ + “Универсальное принятие”': 0,
    'Государство и общество': 1,
    'Детский Рунет': 2,
    'Здоровье и отдых': 3,
    'Игровая индустрия и киберспорт': 4,
    'Культура, СМИ и Массовые коммуникации': 5,
    'Образование и кадры': 6,
    'Счастьеесть': 7,
    'Технологии vs Коронавирус': 8,
    'Технологии и инновации': 9,
    'Укрепление цифрового иммунитета Рунета': 10,
    'Цифровой туризм': 11,
    'Экономика и бизнес': 12}

    cv = CountVectorizer()
    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)

    def get_kw(text, first=True):
      sw = '''что из есть он том они сейчас быть который время например поэтому несколько раз тут а е и ж м о на не ни об но он мне мои мож она они оно мной много многочисленное многочисленная многочисленные многочисленный мною мой мог могут можно может можхо мор моя моё мочь над нее оба нам нем  нами ними мимо немного одной одного менее однажды однако меня нему меньше ней наверху него ниже мало надо один одиннадцать одиннадцатый назад наиболее недавно миллионов недалеко между низко меля нельзя нибудь непрерывно наконец никогда никуда нас наш нет нею неё нихмира наша наше наши ничего начала нередко несколько обычно опять около мы ну нх от отовсюду особенно нужно очень отсюда в во вон вниз внизу вокруг вот восемнадцать восемнадцатый восемь восьмой вверх вам вами важное важнаяважные важный  вдали везде ведь вас ваш ваша ваше ваши впрочем весь вдруг вы все второй всем всеми времени время всему всего всегда всех всею всю вся всё всюду г год говорил говорит года году где да ееза из ли же им до по ими под иногда довольно именно долго позже более должно пожалуйста значит иметь больше пока ему имя пор пора потом потому после почему почти посреди ей два две двенадцать двенадцатый двадцать двадцатый двух его дел или без день занят занята занято заняты действительно давно девятнадцать девятнадцатый девять девятый даже алло жизнь далеко близко здесь дальше для лет зато даром первый перед затем зачем лишь десять десятый ею её их бы еще прибыл про  процентов против просто бывает бывь если люди была были было  будем  будет будете будешь прекрасно буду будь будто будут ещё пятнадцать пятнадцатый друго другое другой другие другая других есть пять быть лучше пятый к ком конечно кому кого когда которой которого которая которые который которых кем каждое каждая каждые каждый кажется как какой какая кто кроме  куда кругом с  т у я та те уж со то том снова тому совсем того тогда тоже собой тобой собою тобою сначалатолько уметь  тот тою хорошо хотеть хочешь хоть хотя свое свои твой своей своего своих свою твоя твоё раз уже сам там тем чем сама сами теми само рано самом самому самой самого семнадцать семнадцатый самим самими самихсаму семь  чему раньше сейчас чего сегодня себе тебе сеаой человек разве теперь себя тебя седьмой спасибо слишком так такое такой такие также такая сих тех чаще четвертый через  часто шестой шестнадцать шестнадцатый шесть четыре четырнадцать четырнадцатый сколько сказал сказала сказать ту ты три эта эти что это чтоб этом этому этой этого чтобы этот стал туда этим этимирядом тринадцать  тринадцатый этих третий тут эту суть чуть тысяч'''.split()
    def lemmatize(texts):
        m = pymorphy2.MorphAnalyzer() 
        texts = [m.parse(x)[0].normal_form for x in texts]
        return texts

    def pre_process(text, sw):
        
        text=text.lower()
        
        text=re.sub("</?.*?>"," <> ",text)
        
        text=re.sub("(\\d|\\W)+"," ",text)
        text_splitted = []
        for word in text.split():
          if word not in sw:
            text_splitted.append(word)
        lem = lemmatize(text_splitted)
        text_splitted_n = []
        for word in lem:
          if word not in sw:
            text_splitted_n.append(word)   
        return text_splitted_n

    text_n = pre_process(text, sw)
    if first:
      word_count_vector = cv.fit_transform(text_n)
      tfidf_transformer.fit(word_count_vector)
    else:
      word_count_vector = cv.transform(text_n)

    def sort_coo(coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    def extract_topn_from_vector(feature_names, sorted_items, topn=10):
        
        sorted_items = sorted_items[:topn]

        score_vals = []
        feature_vals = []

        for idx, score in sorted_items:
            fname = feature_names[idx]
            
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])

        results= {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]]=score_vals[idx]
        
        return results

    def sort_coo(coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    def extract_topn_from_vector(feature_names, sorted_items, topn=10):
        
        sorted_items = sorted_items[:topn]

        score_vals = []
        feature_vals = []

        for idx, score in sorted_items:
            fname = feature_names[idx]
            
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])

        results= {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]]=score_vals[idx]
        
        return results
    feature_names=cv.get_feature_names()

    tf_idf_vector=tfidf_transformer.transform(cv.transform([' '.join(text_n)]))

    sorted_items=sort_coo(tf_idf_vector.tocoo())

    keywords=extract_topn_from_vector(feature_names,sorted_items, 100)

    return keywords

    decode_dict_classes = {0: '10-летие домена .РФ + “Универсальное принятие”',
                          1: 'Государство и общество',
                          2: 'Детский Рунет',
                          3: 'Здоровье и отдых',
                          4: 'Игровая индустрия и киберспорт',
                          5: 'Культура, СМИ и Массовые коммуникации',
                          6: 'Образование и кадры',
                          7: 'Счастьеесть',
                          8: 'Технологии vs Коронавирус',
                          9: 'Технологии и инновации',
                          10: 'Укрепление цифрового иммунитета Рунета',
                          11: 'Цифровой туризм',
                          12: 'Экономика и бизнес'}
    kw = get(texts_kw)
    model = CatBoostClassifier().load_model('model_classif', format='cbm')
    pred = model.predict_proba(kw)
    nomination = [decode_dict_classes[pred.argmax()], round(pred.max(), 3) * 1000]
    return nomination
