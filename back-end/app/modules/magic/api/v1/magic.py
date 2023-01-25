import json
from io import BytesIO
import docx
import pymorphy2
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from app.modules.magic.utils import parser
from app.modules.magic.utils import tree
from app.modules.magic.models import TextDoc, Ontology, Value, Attribute, MainTable, User
from app.common.db import get_db

router = APIRouter()

user_id = 1
user_ont = 6


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
                "name": x.login,
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
                "name": x.ont_name,
            } for x in session.query(Ontology).all()
        ]
        return JSONResponse(status_code=200, content=content)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=404, content="No data to return")


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
                "name": x.attr_name,
                "ont": x.ont.ont_name,
            } for x in session.query(Attribute).all()
        ]
    except Exception as e:
        print(e)
        return {"status": "no data to return"}


@router.get("/values")
def read_values(session: Session = Depends(get_db)):
    try:
        return [
            {
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
async def upload_ontology(file: UploadFile | None = None, session: Session = Depends(get_db)):
    if not file:
        return {"message": "No upload file sent"}

    # нужно загрузить онтологию, а затем ее узлы
    json_data = json.load(file.file)
    result = parser.FindMetaAttr(json_data)

    new_ont = Ontology(ont_name=file.filename, ont_owner=user_id, attr_entity_name=result[0], attr_date=result[1])

    try:
        count = session.query(Ontology).filter(Ontology.ont_name == file.filename, Ontology.ont_owner == user_id).count()
        if count == 0:
            session.add(new_ont)
            session.commit()
        ont_id = session.query(Ontology).filter(Ontology.ont_name == file.filename,
                                                Ontology.ont_owner == user_id).first().ont_id
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content="Error")

    for x in json_data['nodes']:
        new_attr = Attribute(attr_name=x['name'], attr_ont=ont_id)
        try:
            if session.query(Attribute).filter(Attribute.attr_name == new_attr.attr_name,
                                           Attribute.attr_ont == new_attr.attr_ont).count() == 0:
                session.add(new_attr)
                session.commit()
        except Exception as e:
            print(e)
            return JSONResponse(status_code=400, content="Error")
    return {
        "id": ont_id,
        "attributes": [{
            "name": x['name'],
        } for x in json_data['nodes']
    ]}


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
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content="Error")
    return "ok"


@router.delete("/deleteont/{ont_id}")
async def delete_ont(ont_id: int, session: Session = Depends(get_db)):
    try:
        x = session.query(Ontology).filter(Ontology.ont_id == ont_id).first()
        if x:
            session.delete(x)
            session.commit()
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content="Error")
    return "ok"


@router.delete("/deletedocs/{ont_id}")
async def delete_docs(ont_id: int, session: Session = Depends(get_db)):
    try:
        ont = session.query(Ontology).filter(Ontology.ont_id == ont_id).first()
        for x in session.query(TextDoc).filter(TextDoc.ont == ont).all():
            session.delete(x)
            session.commit()
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content="Error")
    return "ok"


@router.get("/maintable/{ont_id}/{question}")
def read_question(ont_id: int, question: str, session: Session = Depends(get_db)):
    try:
        attributes = session.query(Attribute).filter(Attribute.attr_ont == ont_id).all()
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content="Error")

    nltk.download('punkt')
    nltk.download('stopwords')
    # nltk.download('corpus')
    questWords = word_tokenize(question, language="russian")
    stop = stopwords.words("russian")
    stop.append("?")
    stop.append(",")
    stop.append("(")
    stop.append(")")
    stop.append("в")
    stop.append("#")
    stop.append(".")
    questNormal = []
    morph = pymorphy2.MorphAnalyzer()
    for word in questWords:
        questNormal.append(morph.parse(word)[0].normal_form)
    for word in questNormal:
        if word in stop:
            questNormal.remove(word)

    print(questNormal)

    findDic = {}  # {attr_id, кол-во совпадений}
    for attr in attributes:
        attrWords = word_tokenize(attr.attr_name, language="russian")
        attrNormal = []
        for word in attrWords:
            if word not in stop:
                attrNormal.append(morph.parse(word)[0].normal_form)
        wordIntersection = list(set(questNormal) & set(attrNormal))
        findDic[attr.attr_id] = len(wordIntersection)
        #print(attrNormal, len(wordIntersection))

    sortedFindDict = dict(sorted(findDic.items(), key=lambda item: item[1], reverse=True))
    #print(sortedFindDict)

    findAttr = []
    intersection = list(sortedFindDict.values())[0]
    for key in sortedFindDict:
        if sortedFindDict[key] == intersection and intersection != 0:
            findAttr.append(key)
    print(findAttr)

    result = []
    for aid in findAttr:
        try:
            result += session.query(MainTable).filter(MainTable.main_attr == aid).all()
        except Exception as e:
            print(e)
            return JSONResponse(status_code=400, content="Error")

    meta1name = session.query(Ontology).filter(Ontology.ont_id == ont_id).first().attr_entity_name
    meta1id = session.query(Attribute).filter(Attribute.attr_ont == ont_id, Attribute.attr_name == meta1name).first().attr_id
    print(meta1name)
    print(meta1id)

    final_result = []
    for res in result:
        print()
        meta1data = session.query(MainTable).filter(MainTable.doc == res.doc, MainTable.main_attr == meta1id).first().value.value
        final_result.append(meta1data)
        print(meta1data)

    return [
        {
            "doc": result[x].doc.doc_name,
            "attr": result[x].attr.attr_name,
            "value": result[x].value.value,
            "entity_name": final_result[x]
        } for x in range(len(result))
    ]


"""@router.get("/maintable/{doc_name}/{attr_name}")
def read_item(doc_name: str, attr_name: str, session: Session = Depends(get_db)):
    doc_id = session.query(TextDoc).filter(TextDoc.doc_name == doc_name,
                                           TextDoc.doc_ont == user_ont).first().doc_id
    attr_id = session.query(Attribute).filter(Attribute.attr_name == attr_name,
                                              Attribute.attr_ont == user_ont).first().attr_id
    result = session.query(MainTable).filter(MainTable.main_doc == doc_id,
                                             MainTable.main_attr == attr_id).all()
    return [
        {
            "doc": x.doc.doc_name,
            "attr": x.attr.attr_name,
            "value": x.value.value,
        } for x in result
    ]"""
