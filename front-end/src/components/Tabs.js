import { useState, useRef, useEffect } from "react";
import Dropdown from "./Dropdown";
import { UploadFile } from "./UploadFile";
import DBSchema from "../СхемаБД.png";
import { UploadOnt } from "./UploadOnt";
import DataTable from "./DataTable";
import ResponseDataTable from "./ResponseDataTable";
import axios from 'axios';

function Tabs() {
  const [toggleState, setToggleState] = useState(1);

  const toggleTab = (index) => {
    setToggleState(index);
  };

  //выбранный документ
  const [selected, setSelected] = useState({ id: 0, name: "Выберите документ", text: "" })

  //Выбранная онтология
  const [selectedOnt, setSelectedOnt] = useState({ id: 0, name: "Выбрать онтологию" })

  //
  const [result, setResult] = useState([]);

  const questionRef = useRef()
  const AnswerTextRef = useRef()

  //результат ответа на вопрос
  const [responseData, setResponseData] = useState([]);

  //название текущей онтологии
  const [name, setName] = useState(localStorage.getItem("user_ont_name") || "онтология не выбрана");


  async function handleAskQuestion(e) {
    const quest = questionRef.current.value
    if (quest === '') return;
    console.log(quest);
    try {
      let url = 'http://127.0.0.1:8000/api/v1/magic/maintable/' + localStorage.getItem("user_ont") + '/' + quest;
      let res = await axios(url, {
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
      console.log(res.data.length)
      if (res.data.length > 0)
        AnswerTextRef.current.value = "ДА"
      else
        AnswerTextRef.current.value = "НЕТ"
    }
    catch (e) {
      console.log(e);
    }
  }

  async function deleteOnt(e) {
    if (localStorage.getItem("user_ont") === null) return
    try {
      let url = 'http://127.0.0.1:8000/api/v1/magic/deletedatauser/';
      await axios(url, {
        method: 'DELETE',
        mode: 'no-cors',
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json',
        },
        withCredentials: true,
        credentials: 'same-origin',
        params: {
          user_id: localStorage.getItem("user_id"),
      }
      })
        .then(async function (response) {
          console.log(response);
          setSelected({ id: 0, name: "Выберите документ", text: "" })
          setSelectedOnt({ id: 0, name: "Выбрать онтологию" })
          setResult([])
          questionRef.current.value = ""
          setResponseData([])
          localStorage.removeItem("user_ont_name")
          localStorage.removeItem("user_ont")
          setName("онтология не выбрана")
        })
        .catch(function (response) {
        });


    }
    catch (e) {
      console.log(e);
    }
  }

  const [words, setWords] = useState(['В данный момент данные загружаются']);
  const [value, setValue] = useState('');
  const [lastValue, setLastValue] = useState(' ');

  /*useEffect(() => {
    async function getWords(e) {
      try {
        if (localStorage.getItem("user_ont")) {
          let url = 'http://127.0.0.1:8000/api/v1/magic/get_words/' + localStorage.getItem("user_ont");
          let res = await axios(url, {
            method: 'GET',
            mode: 'no-cors',
            headers: {
              'Access-Control-Allow-Origin': '*',
              'Content-Type': 'application/json',
            },
            withCredentials: true,
            credentials: 'same-origin',
          })
          if (Array.isArray(res.data)) {
            console.log(res);
            setWords(res.data);
          }
        }
      }
      catch (e) {
        console.log(e);
      }
    }
    getWords();
  }, [name])*/

  const filteredWords = words.filter(word => { return word.toLowerCase().includes(lastValue.toLowerCase()); })
  //console.log(filt.map(word => {return value + ' ' + word}));


  const [isOpen, setIsOpen] = useState(true);

  const itemClickHandler = (e) => {
    var str = value;
    var str = str.substring(0, str.length - lastValue.length);

    //console.log('Длина всего введенного' + str.length);
    //console.log('Длина последнего слова ' + lastValue.length);
    //console.log('Осталось ' + str);
    //console.log('Будет ' + str + e.target.textContent);

    setValue(str + e.target.textContent);
    setIsOpen(!isOpen);
  }

  const inputClickHandler = () => {
    setIsOpen(true);
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
          <UploadOnt selectedOnt={selectedOnt} setSelectedOnt={setSelectedOnt} setResult={setResult} setSelected={setSelected} name={name} setName={setName} deleteOnt={deleteOnt} />
          <div>
            <img className="DBSchema" src={DBSchema} alt="да" />
          </div>
        </div>

        <div
          className={toggleState === 2 ? "content  active-content" : "content"}
        >
          <h2>Добавление и удаление документов, просмотр их содержимого</h2>
          <h2>Для добавления выберите документы, а затем нажмите "Загрузить"</h2>
          <hr />
          <UploadFile setResult={setResult} setSelected={setSelected} />

          <Dropdown selected={selected} setSelected={setSelected} result={result} setResult={setResult} />
          <div className="selected-text">{selected.text}</div>
        </div>

        <div
          className={toggleState === 3 ? "content  active-content" : "content"}
        >
          <h2>Просмотр извлеченных фактов</h2>
          <hr />
          <Dropdown selected={selected} setSelected={setSelected} result={result} setResult={setResult} />
          <DataTable className="data-table" selectedFileId={selected.id} />
        </div>

        <div
          className={toggleState === 4 ? "content  active-content" : "content"}
        >
          <h2>Задайте интересующий Вас вопрос по содержимому документов!</h2>
          <hr />
          <form className="search_form">
            <input
              ref={questionRef}
              type='text'
              placeholder="Поиск"
              className="search_input"
              value={value}
              onChange={(event) => {
                setValue(event.target.value);
                var array = event.target.value.split(' ');
                setLastValue(array[array.length - 1]);
                console.log(array[array.length - 1]);
              }}
              onClick={inputClickHandler}
            />
            <ul className="autocomplete">
              {
                value && lastValue && isOpen
                  ?
                  filteredWords.map((word, index) => {
                    return (
                      <li className="autocomplete_item" key={index}
                        onClick={itemClickHandler}
                      >
                        {word}
                      </li>
                    )
                  })
                  : null
              }
            </ul>
          </form>
          <button onClick={handleAskQuestion} className="ask-question">Задать вопрос</button>
          <input ref={AnswerTextRef} className="answer-text" type="text" disabled />

          <ResponseDataTable responseData={responseData} className="data-table" />
        </div>
      </div>
    </div>
  );
}

export default Tabs;