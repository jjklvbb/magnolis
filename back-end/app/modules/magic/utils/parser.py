def DeleteFirstSpaces(str):
    if len(str) == 0: return "";
    while str[0] == ' ':
        str = str[1:]
    return str


def TextParsing(doc_id, text, attributes):
    dic = []
    readyData = []

    for p in attributes:
        index = text.find(p.attr_name)
        new = [index, p.attr_name, p.attr_id]
        if not index == -1:
            dic.append(new)
        #print(new)

    dic.sort()
    print(dic)
    for i in range(len(dic)):
        key = dic[i][1]
        idx = i + 1
        length = 0 - dic[i][0] - len(key)
        if i != len(dic) - 1:
            length += dic[idx][0]
        if length != 0:
            if i != len(dic) - 1:
                begin = dic[i][0] + len(key)
                end = length
                s = text[begin:begin + end]
            else:
                s = text[dic[i][0] + len(key):]
            if s != "":
                if s[0] == ':':
                    s = s[1:]
                s = DeleteFirstSpaces(s)
                if not [doc_id, dic[i][2], s] in readyData:
                    readyData.append([doc_id, dic[i][2], s])
    return readyData


def FindMetaAttr(json_data):
    global id_meta_date, id_meta_name, id_entity_date, id_entity_name, entity_name, entity_data

    id_meta_date = -123456
    id_meta_name = -123456
    id_entity_date = -123456
    id_entity_name = -123456
    for x in json_data['nodes']:
        if x['name'] == '#Дата':
            id_meta_date = x['id']
        if x['name'] == '#Имя сущности':
            id_meta_name = x['id']

    if id_meta_date == -123456 or id_meta_name == -123456:
        return ["500", "", ""]

    for x in json_data['relations']:
        if x['source_node_id'] == id_meta_date:
            id_entity_date = x['destination_node_id']
        if x['source_node_id'] == id_meta_name:
            id_entity_name = x['destination_node_id']

    if id_entity_date == -123456 or id_entity_name == -123456:
        return ["500", "", ""]

    for x in json_data['nodes']:
        if x['id'] == id_entity_date:
            entity_data = x['name']
        if x['id'] == id_entity_name:
            entity_name = x['name']

    return ["200", entity_name, entity_data]
