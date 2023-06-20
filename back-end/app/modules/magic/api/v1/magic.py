import json
from io import BytesIO
import docx
import nltk
import pymorphy2
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
import bcrypt

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from app.modules.magic.utils import parser
from app.modules.magic.utils import tree
from app.modules.magic.models import TextDoc, Ontology, Value, Attribute, MainTable, User
from app.common.db import get_db

router = APIRouter()


@router.get("/gethello")
def get_hello():
    try:
        return [{"value": "hello world"}, {"value": "helloworld2"}]
    except Exception as e:
        print(e)
        return JSONResponse(status_code=404, content="No data to return")


@router.get("/users")
def read_users(session: Session = Depends(get_db)):
    try:
        content = [
            {
                "id": x.user_id,
                "name": x.login,
                "password": x.password,
            } for x in session.query(User).all()
        ]
        return JSONResponse(status_code=200, content=content)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=404, content="No data to return")


@router.get("/ontologies")
def read_ontologies(session: Session = Depends(get_db)):
    try:
        content = [
            {
                "id": x.ont_id,
                "name": x.ont_name,
                "attr_entity_name": x.attr_entity_name,
                "ont_owner": x.user.user_id,
                "attr_date": x.attr_date,
            } for x in session.query(Ontology).all()
        ]
        return JSONResponse(status_code=200, content=content)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content="No data to return")


@router.get("/user_ontologies")
def read_user_ontologies(user_id: int, session: Session = Depends(get_db)):
    try:
        return [
            {
                "id": x.ont_id,
                "name": x.ont_name,
                "attr_entity_name": x.attr_entity_name,
                "ont_owner": x.user.user_id,
                "attr_date": x.attr_date,
            } for x in session.query(Ontology).filter(Ontology.ont_owner == user_id).all()
        ]
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content=str(e))


@router.get("/textdocs")
def read_text_docs(session: Session = Depends(get_db)):
    try:
        return [
            {
                "id": x.doc_id,
                "name": x.doc_name,
                "ont": x.ont.ont_name,
                "text": x.doc_text
            } for x in session.query(TextDoc).all()
        ]
    except Exception as e:
        print(e)
        return {"status": "no data to return"}


@router.get("/attributes")
def read_attributes(session: Session = Depends(get_db)):
    try:
        return [
            {
                "id": x.attr_id,
                "name": x.attr_name,
                "ont": x.ont.ont_name,
            } for x in session.query(Attribute).all()
        ]
    except Exception as e:
        print(e)
        return {"status": "no data to return"}


@router.get("/get_words/{ont_id}")
def get_words(ont_id: int, session: Session = Depends(get_db)):
    try:
        global response
        try:
            response = session.query(Attribute).filter(Attribute.attr_ont == ont_id).all()
        except Exception as e:
            print(e)
            return {"status": "no data to return"}

        words = []
        for x in response:
            tokens = word_tokenize(x.attr_name, language="russian")
            morph = pymorphy2.MorphAnalyzer()

            for token in tokens:
                if token.lower() not in words and len(token) != 1:
                    words.append(token.lower())
                normal_form = morph.parse(token)[0].normal_form
                if normal_form not in words and len(normal_form) != 1:
                    words.append(normal_form)
        # words = words.sort()
        return words
    except Exception as e:
        return {"error": str(e)}


@router.get("/values")
def read_values(session: Session = Depends(get_db)):
    try:
        return [
            {
                "id": x.value_id,
                "value": x.value,
            } for x in session.query(Value).all()
        ]
    except Exception as e:
        print(e)
        return {"status": "no data to return"}


@router.get("/maintable")
def read_main_table(session: Session = Depends(get_db)):
    try:
        return [
            {
                "id": x.main_id,
                "doc": x.doc.doc_name,
                "attr": x.attr.attr_name,
                "value": x.value.value,
            } for x in session.query(MainTable).all()
        ]
    except Exception as e:
        print(e)
        return {"status": "no data to return"}


@router.get("/textdocs/{ont_id}")
def read_text_docs_ont(ont_id: int, session: Session = Depends(get_db)):
    try:
        return [
            {
                "id": x.doc_id,
                "name": x.doc_name,
                "ont": x.ont.ont_name,
                "text": x.doc_text
            } for x in session.query(TextDoc).filter(TextDoc.doc_ont == ont_id).all()
        ]
    except Exception as e:
        print(e)
        return {"status": "no data to return"}


@router.post("/registration")
def registration(login: str, password: str, session: Session = Depends(get_db)):
    try:
        if len(login) == 0 or len(password) == 0:
            return JSONResponse(status_code=500, content={"status": "reg_error",
                                                          "error": "Пустой логин или пароль"})
        hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        hashed = hash.decode('utf8')
        user_entity = session.query(User).filter(User.login == login).first()
        if not user_entity:
            user_entity = User(login=login, password=hashed)
            session.add(user_entity)
            session.commit()
            return JSONResponse(status_code=200, content={
                "status": "ok",
                "id": user_entity.user_id,
                })
        else:
            return JSONResponse(status_code=500, content={"status": "reg_error",
                "error": "Пользователь с таким логином уже существует"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={"status": "error", "error": str(e)})


@router.post("/auth")
def auth(login: str, password: str, session: Session = Depends(get_db)):
    try:
        if len(login) == 0 or len(password) == 0:
            return JSONResponse(status_code=500, content={"status": "auth_error",
                                                          "error": "Пустой логин или пароль"})
        user = session.query(User).filter(User.login == login).first()
        if bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
            return JSONResponse(status_code=200, content={
                "status": "ok",
                "id": user.user_id,
            })
        else:
            return JSONResponse(status_code=500, content={"status": "auth_error",
                                                          "error": "Неправильный пароль!"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={"status": "error", "error": str(e)})


@router.get("/maintable/{doc_id}")
def read_main_table_doc(doc_id: int, session: Session = Depends(get_db)):
    try:
        return [
            {
                "id": str(x.main_doc) + str(x.main_attr) + str(x.main_value),
                "doc": x.doc.doc_name,
                "attr": x.attr.attr_name,
                "value": x.value.value,
            } for x in session.query(MainTable).filter(MainTable.main_doc == doc_id).all()
        ]
    except Exception as e:
        print(e)
        return {"status": "no data to return"}


@router.post("/uploadont")
async def upload_ontology(user_id: int, file: UploadFile | None = None, session: Session = Depends(get_db)):
    try:
        if not file:
            return {"message": "No upload file sent"}

        # нужно загрузить онтологию, а затем ее узлы
        json_data = json.load(file.file)
        result = parser.FindMetaAttr(json_data)

        if result[0] == '500':
            return JSONResponse(status_code=500, content="Error in ontology")

        try:
            ontology_entity = session.query(Ontology).filter(Ontology.ont_name == file.filename,
                                                   Ontology.ont_owner == user_id).first()
            if not ontology_entity:
                ontology_entity = Ontology(ont_name=file.filename, ont_owner=user_id, attr_entity_name=result[1],
                                   attr_date=result[2])
                session.add(ontology_entity)
                session.commit()
            ont_id = ontology_entity.ont_id
        except Exception as e:
            print(e)
            return JSONResponse(status_code=400, content={"error": str(e)})
        for x in json_data['nodes']:
            new_attr = Attribute(attr_name=x['name'], attr_ont=ont_id)
            try:
                if session.query(Attribute).filter(Attribute.attr_name == new_attr.attr_name,
                                                   Attribute.attr_ont == new_attr.attr_ont).count() == 0:
                    session.add(new_attr)
                    session.commit()
            except Exception as e:
                print(e)
                return JSONResponse(status_code=400, content={"error": str(e)})
        return JSONResponse(status_code=200, content={
            "id": ont_id,
            "attributes": [{
                "name": x['name'],
            } for x in json_data['nodes']
            ]})
    except Exception as e:
        return {"error": str(e)}


@router.post("/uploaddoc/{ont_id}")
async def upload_text_document(ont_id: int, file: UploadFile | None = None, session: Session = Depends(get_db)):
    if not file:
        return {"message": "No upload file sent"}

    text = ''
    doc = docx.Document(BytesIO(await file.read()))
    all_paras = doc.paragraphs
    for para in all_paras:
        text += para.text

    # добавление документа
    new_doc = TextDoc(doc_name=file.filename, doc_ont=ont_id, doc_text=text)
    try:
        count = session.query(TextDoc).filter(TextDoc.doc_name == new_doc.doc_name,
                                              TextDoc.doc_ont == new_doc.doc_ont).count()
        if count == 0:
            session.add(new_doc)
            session.commit()
        doc_id = session.query(TextDoc).filter(TextDoc.doc_name == new_doc.doc_name,
                                               TextDoc.doc_ont == new_doc.doc_ont).first().doc_id
        attributes = session.query(Attribute).filter(Attribute.attr_ont == ont_id).all()  # все атрибуты
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content="Error")

    result = parser.TextParsing(doc_id, text, attributes)  # [doc_id, attr_id, value]
    # print("Результат парсинга:", result)

    # нужно удалить неиспользуемые атрибуты атрибуты
    """attr_ids = [] # нужные аттрибуты
    for x in result:
        attr_ids.append(x[1])

    for x in attributes:
        if x.attr_id not in attr_ids: #если этого атрибута нет в нужных, то его удаляем
            try:
                session.delete(x)
                session.commit()
            except Exception as e:
                print(e)
                return JSONResponse(status_code=400, content="Error")"""

    # добавление значений
    for x in result:
        new_value = Value(value=x[2])
        try:
            if session.query(Value).filter(Value.value == new_value.value).count() == 0:
                session.add(new_value)
                session.commit()
        except Exception as e:
            print(e)
            return JSONResponse(status_code=400, content="Error")

    # добавление в главную таблицу
    for x in result:
        try:
            value_id = session.query(Value).filter(Value.value == x[2]).first().value_id
            new_main = MainTable(main_doc=x[0], main_attr=x[1], main_value=value_id)
            if session.query(MainTable).filter(MainTable.main_doc == new_main.main_doc,
                                               MainTable.main_attr == new_main.main_attr,
                                               MainTable.main_value == new_main.main_value).count() == 0:
                session.add(new_main)
                session.commit()
        except Exception as e:
            print(e)
            return JSONResponse(status_code=400, content="Error")

    return text


# ВНИМАНИЕ ПЕРЕДЕЛАТЬ ЧТОБЫ УДАЛЯЛОСЬ ТОЛЬКО У КОНКРЕТНОГО ПОЛЬЗОВАТЕЛЯ
@router.delete("/deletedata")
async def delete_data(session: Session = Depends(get_db)):
    try:
        for x in session.query(MainTable).all():
            session.delete(x)
            session.commit()
        for x in session.query(Attribute).all():
            session.delete(x)
            session.commit()
        for x in session.query(TextDoc).all():
            session.delete(x)
            session.commit()
        for x in session.query(Ontology).all():
            session.delete(x)
            session.commit()
        for x in session.query(Value).all():
            session.delete(x)
            session.commit()
        for x in session.query(User).all():
            session.delete(x)
            session.commit()
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content="Error")
    return "ok"


@router.delete("/deletedatauser")
async def delete_data_user(user_id: int, session: Session = Depends(get_db)):
    try:
        xx = session.query(Ontology).filter(Ontology.ont_owner == user_id).all()
        for x in xx:
            session.delete(x)
            session.commit()
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content="Error")
    return "ok"


def text_preprocessing(text):
    text_token = word_tokenize(text, language="russian")
    stop = stopwords.words("russian")
    stop.remove("есть")
    stop.append("?")
    stop.append(",")
    stop.append("(")
    stop.append(")")
    stop.append("в")
    stop.append("#")
    stop.append(".")
    # print("Стоп-слова: ", stop)
    text_normal = []
    morph = pymorphy2.MorphAnalyzer()
    for token in text_token:
        text_normal.append(morph.parse(token)[0].normal_form)
    # print(text_normal)
    for lemm in text_normal:
        if lemm in stop:
            text_normal.remove(lemm)

    # возвращаем массив лемм
    return text_normal


@router.get("/maintable/{ont_id}/{question}")
def read_question(ont_id: int, question: str, session: Session = Depends(get_db)):
    try:
        attributes = session.query(Attribute).filter(Attribute.attr_ont == ont_id).all()
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content="Error")

    nltk.download('punkt')
    nltk.download('stopwords')
    quest_lemm = text_preprocessing(question)
    print("Предобработанный вопрос: ", quest_lemm)

    exist_first_word = False
    if quest_lemm[0] == "есть" or quest_lemm[0] == "существовать":
        exist_first_word = True

    inters_dic_w_attr = {}  # {attr_id, кол-во совпадений с атрибутом}
    for attr in attributes:
        attr_lemm = text_preprocessing(attr.attr_name)
        word_intersection = list(set(quest_lemm) & set(attr_lemm))
        inters_dic_w_attr[attr.attr_id] = len(word_intersection)
        # print(attrNormal, len(word_intersection))

    sorted_inters_dic_w_attr = dict(sorted(inters_dic_w_attr.items(), key=lambda item: item[1], reverse=True))
    print("Пересечение с названиями атрибутов:", sorted_inters_dic_w_attr)
    max_intersection_w_attr = 0
    if len(sorted_inters_dic_w_attr) > 0:
        max_intersection_w_attr = list(sorted_inters_dic_w_attr.values())[0]

    find_attr = []
    for key in sorted_inters_dic_w_attr:
        if sorted_inters_dic_w_attr[key] == max_intersection_w_attr and max_intersection_w_attr != 0:
            find_attr.append(key)
    #print(find_attr)

    meta1name = session.query(Ontology).filter(Ontology.ont_id == ont_id).first().attr_entity_name
    meta1id = session.query(Attribute).filter(Attribute.attr_ont == ont_id,
                                              Attribute.attr_name == meta1name).first().attr_id

    entity_names = session.query(MainTable).filter(MainTable.main_attr == meta1id).all()
    inters_dic_w_entity = {}  # {doc_id, кол-во совпадений по имени сущности}
    for name in entity_names:
        name_lemm = text_preprocessing(name.value.value)
        word_intersection = list(set(quest_lemm) & set(name_lemm))
        inters_dic_w_entity[name.doc.doc_id] = len(word_intersection)
    sorted_inters_dic_w_entity = dict(sorted(inters_dic_w_entity.items(), key=lambda item: item[1], reverse=True))
    print("Пересечение с именами сущностей: ", sorted_inters_dic_w_entity)
    max_intersection_w_ent = 0
    if len(sorted_inters_dic_w_entity) > 0:
        max_intersection_w_ent = list(sorted_inters_dic_w_entity.values())[0]
    find_entity = []
    for key in sorted_inters_dic_w_entity:
        if sorted_inters_dic_w_entity[key] == max_intersection_w_ent and max_intersection_w_ent > 0:
            find_entity.append(key)

    inters_dic_w_values = {}  # {строка из главной таблицы, кол-во совпадений по значению атрибута}
    for aid in find_attr:
        values = session.query(MainTable).filter(MainTable.main_attr == aid).all()
        for val in values:
            val_lemm = text_preprocessing(val.value.value)
            word_intersection = list(set(quest_lemm) & set(val_lemm))
            inters_dic_w_values[val] = len(word_intersection)
    sorted_inters_dic_w_values = dict(sorted(inters_dic_w_values.items(), key=lambda item: item[1], reverse=True))
    print("Пересечение со значениями атрибутов: ", sorted_inters_dic_w_values)
    max_intersection_w_val = 0
    if len(sorted_inters_dic_w_values) > 0:
        max_intersection_w_val = list(sorted_inters_dic_w_values.values())[0]
    find_values = []
    for key in sorted_inters_dic_w_values:
        if sorted_inters_dic_w_values[key] == max_intersection_w_val and max_intersection_w_val > 0:
            find_values.append(key)

    answer_for_6_type = []
    if max_intersection_w_ent > 0:
        for row in find_values:
            print(row.doc.doc_id)
            if row.doc.doc_id in find_entity:
                answer_for_6_type.append(row)

    print("Предобработанный вопрос: ", quest_lemm)
    print("Пересечение с названиями атрибутов:", find_attr)
    print("Пересечение с именами сущностей: ", find_entity)
    print("Пересечение со значениями атрибутов: ", find_values)
    print("max_intersection_w_attr: ", max_intersection_w_attr)
    print("max_intersection_w_ent: ", max_intersection_w_ent)
    print("max_intersection_w_val: ", max_intersection_w_val)
    print("answer_for_6_type: ", len(answer_for_6_type))

    type = 0
    if max_intersection_w_attr != 0 and len(find_attr) == 1 and max_intersection_w_ent == 0\
            and not exist_first_word and max_intersection_w_val == 0:
        print("Тип запроса:" + "1")
        type = 1
    if max_intersection_w_attr != 0 and len(find_attr) > 1 and max_intersection_w_ent == 0\
            and not exist_first_word and max_intersection_w_val == 0:
        print("Тип запроса:" + "2")
        type = 2
    if max_intersection_w_attr != 0 and max_intersection_w_ent != 0\
            and max_intersection_w_val == 0:
        print("Тип запроса:" + "3")
        type = 3
    if (max_intersection_w_attr != 0 or max_intersection_w_attr == 0) and max_intersection_w_ent == 0\
            and exist_first_word and max_intersection_w_val == 0:
        print("Тип запроса:" + "4")
        type = 4
    if max_intersection_w_attr != 0 and max_intersection_w_ent == 0\
            and max_intersection_w_val != 0:
        print("Тип запроса:" + "5")
        type = 5
    if max_intersection_w_attr != 0 and max_intersection_w_ent != 0\
            and max_intersection_w_val != 0:
        print("Тип запроса:" + "6")
        type = 6
    if max_intersection_w_attr == 0 and max_intersection_w_ent != 0\
            and max_intersection_w_val == 0:
        print("Тип запроса:" + "7")
        type = 7

    if type > 0:
        non_filt_result = []
        result = []
        meta_result = []

        if type == 7:
            for doc in find_entity:
                result += session.query(MainTable).filter(MainTable.main_doc == doc).all()

        for aid in find_attr:
            try:
                find_data = session.query(MainTable).filter(MainTable.main_attr == aid).all()
                non_filt_result += find_data
            except Exception as e:
                print(e)
                return JSONResponse(status_code=400, content="Error")

        for data in non_filt_result:
            if type == 1 or type == 2 or type == 4:
                result.append(data)
            if type == 3 and data.doc.doc_id in find_entity:
                result.append(data)
            if type == 5:
                result = find_values
            if type == 6:
                result = answer_for_6_type

        for data in result:
            meta1data = session.query(MainTable).filter(MainTable.doc == data.doc,
                                                        MainTable.main_attr == meta1id).first().value.value
            meta_result.append(meta1data)

        return [
            {
                "doc": result[x].doc.doc_name,
                "attr": result[x].attr.attr_name,
                "value": result[x].value.value,
                "entity_name": meta_result[x]
            } for x in range(len(result))
        ]

    return []