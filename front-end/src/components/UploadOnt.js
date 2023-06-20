import { useState } from 'react';
import axios from 'axios';
import useFileDownload from "./useFileDownload";
import { useNavigate } from "react-router-dom";
import { ChooseOnt } from "./ChooseOnt";

export const UploadOnt = ({ selectedOnt, setSelectedOnt, setResult, setSelected, name, setName, deleteOnt }) => {

    const navigate = useNavigate();
    const [file, setFile] = useState(null);

    function handleChange(event) {
        setFile(event.target.files[0]);
        console.log(file);
    }

    const { message } = useFileDownload();

    async function handleSubmit(event) {
        console.log(file);
        event.preventDefault()
        try {
            let url = 'http://127.0.0.1:8000/api/v1/magic/uploadont';
            const formData = new FormData();
            formData.append('file', file);
            formData.append('fileName', file.name);
            await axios({
                method: "post",
                url: url,
                data: formData,
                headers: {
                    "accept": "application/json",
                    "Content-Type": "multipart/form-data",
                    'Access-Control-Allow-Origin': '*'
                },
                params: {
                    user_id: localStorage.getItem("user_id"),
                }

            })
                .then(async function (response) {
                    console.log(response.status);
                    if (response.status === 200) {
                        let id = response.data['id']
                        localStorage.setItem("user_ont", id.toString())
                        localStorage.setItem("user_ont_name", file.name)
                        console.log(id);
                        console.log(response);
                        setSelected({ id: 0, name: "Выберите документ", text: "" })
                        setResult(await message());
                        setName(file !== null ? file.name : "");
                    }
                })
                .catch(function (response) {
                    console.log("ошибочка");
                    alert("Ошибка в загрузке онтологии, проверьте наличие мета атрибутов #Имя сущности и #Дата");
                    console.log(response);
                });
        }
        catch (e) {
            console.log(e);
        }
    };

    async function outHandle(e) {
        localStorage.removeItem("user_id")
        localStorage.removeItem("user_ont_name")
        localStorage.removeItem("user_ont")
        navigate('/');
    }


    return (
        <>
            <form onSubmit={handleSubmit}>
                <h2>Текущая онтология: {name}</h2>
                <h2>Вы можете выбрать онтологию, с которой работали ранее</h2>
                <ChooseOnt selectedOnt={selectedOnt} setSelectedOnt={setSelectedOnt} setSelectedDoc={setSelected} setResult={setResult} messageDoc={message} setName={setName} />
                <h2>Также вы можете загрузить новую онтологию</h2>
                <input className='upload-file-btn' type="file" onChange={handleChange} />
                <button className='upload-file-submit' type="submit">Загрузить онтологию</button>
                <h2>Очистить базу данных</h2>
                <button className='ClearDB' onClick={deleteOnt} type='button'>Очистить БД</button>
                <h2>Выйти из аккаунта</h2>
                <button onClick={outHandle} className="out-button" type='button'>Выйти</button>
            </form>
        </>
    )
}