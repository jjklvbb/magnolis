import { useState, useRef } from "react";
import Dropdown from "./Dropdown";
import {UploadFile} from "./UploadFile";
import DBSchema from "../СхемаБД.png";
import {UploadOnt} from "./UploadOnt";
import DataTable from "./DataTable";
import ResponseDataTable from "./ResponseDataTable";
import axios from 'axios';

function Tabs() {
  const [toggleState, setToggleState] = useState(1);

  const toggleTab = (index) => {
    setToggleState(index);
  };

  //выбранный документ
  const [selected, setSelected] = useState({id: 0, name: "Выбирите документ", text: ""})

  //результат извлечения данных
  const [result, setResult] = useState([]);

  const questionRef = useRef()

  //результат ответа на вопрос
  const [responseData, setResponseData] = useState([ ]);

  //название текущей онтологии
  const [name, setName] = useState(localStorage.getItem("user_ont_name") || "онтология не выбрана");
  

  async function handleAskQuestion(e) {
    const quest = questionRef.current.value
    if (quest === '') return
    console.log(quest)
    try{
      let url = 'http://localhost:8000/api/v1/magic/maintable/' + localStorage.getItem("user_ont") + '/' + quest;
      let res =  await axios(url, {
          method: 'GET',
          mode: 'no-cors',
          headers: {
              'Access-Control-Allow-Origin': '*',
              'Content-Type': 'application/json',
          },
          withCredentials: true,
          credentials: 'same-origin',
          })
      console.log(res);
      setResponseData(res.data)
    }
    catch(e){
        console.log(e);
    }
  }

  async function deleteOnt(e){
    if (localStorage.getItem("user_ont") === null) return
    try{
      let url = 'http://localhost:8000/api/v1/magic/deleteont/' + localStorage.getItem("user_ont");
      let res =  await axios(url, {
          method: 'DELETE',
          mode: 'no-cors',
          headers: {
              'Access-Control-Allow-Origin': '*',
              'Content-Type': 'application/json',
          },
          withCredentials: true,
          credentials: 'same-origin',
          })
      console.log(res);
      setSelected({id: 0, name: "Выбирите документ", text: ""})
      setResult([])
      questionRef.current.value = ""
      setResponseData([])
      localStorage.removeItem("user_ont_name")
      setName("онтология не выбрана")
      localStorage.removeItem("user_ont")
    }
    catch(e){
        console.log(e);
    }
  }

  

  return (
    <div className="container">
      <div className="bloc-tabs">
        <button
          className={toggleState === 1 ? "tabs active-tabs" : "tabs"}
          onClick={() => toggleTab(1)}
        >
          База данных
        </button>
        <button
          className={toggleState === 2 ? "tabs active-tabs" : "tabs"}
          onClick={() => toggleTab(2)}
        >
          Документы
        </button>
        <button
          className={toggleState === 3 ? "tabs active-tabs" : "tabs"}
          onClick={() => toggleTab(3)}
        >
          Извлечение данных
        </button>
        <button
          className={toggleState === 4 ? "tabs active-tabs" : "tabs"}
          onClick={() => toggleTab(4)}
        >
          Запросы на ЕЯ
        </button>
      </div>

      <div className="content-tabs">
        <div
          className={toggleState === 1 ? "content  active-content" : "content"}
        >
          <h2>MagNolis</h2>
          <hr />
          <h2>Выберите онтологию и нажмите "Загрузить"</h2>
          <UploadOnt setResult={setResult} setSelected={setSelected} name={name} setName={setName} deleteOnt={deleteOnt}/> 
          <div>
            <img className="DBSchema" src={DBSchema} alt="да"/>
          </div>
        </div>

        <div
          className={toggleState === 2 ? "content  active-content" : "content"}
        >
          <h2>Добавление и удаление документов, просмотр их содержимого</h2>
          <h2>Для добавления выберите документы, а затем нажмите "Загрузить"</h2>
          <hr />
          <UploadFile setResult={setResult} setSelected={setSelected}/>
          
          <Dropdown selected={selected} setSelected={setSelected} result={result} setResult={setResult}/>
          <div className="selected-text">{selected.text}</div>
        </div>

        <div
          className={toggleState === 3 ? "content  active-content" : "content"}
        >
          <h2>Просмотр извлеченных фактов</h2>
          <hr />
          <Dropdown selected={selected} setSelected={setSelected} result={result} setResult={setResult}/>
          <DataTable className="data-table" selectedFileId={selected.id}/>
        </div>

        <div
          className={toggleState === 4 ? "content  active-content" : "content"}
        >
          <h2>Задайте интересующий Вас вопрос по содержимому документов!</h2>
          <hr />
          <input ref={questionRef} className="input-question" type="text" />
          <button onClick={handleAskQuestion} className="ask-question">Задать вопрос</button>
          <ResponseDataTable responseData={responseData} className="data-table"/>
        </div>
      </div>
    </div>
  );
}

export default Tabs;