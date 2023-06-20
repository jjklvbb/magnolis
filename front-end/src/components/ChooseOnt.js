import { useState, useEffect } from 'react';
import axios from 'axios';
import { OntDropdown } from "./OntDropdown";
import useFileDownload from "./useFileDownload";

export const ChooseOnt = ({ selectedOnt, setSelectedOnt, setSelectedDoc, setResult, messageDoc, setName }) => {

    const [message, setMessage] = useState()
    let user_id = localStorage.getItem("user_id")

    useEffect(() => {
        async function getMessage(e) {
            if (localStorage.getItem("user_id") === null) return [];
            try {
                let url = 'http://127.0.0.1:8000/api/v1/magic/user_ontologies/';
                let res = await axios(url, {
                    method: 'GET',
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
                let print = res.data.map((data) => data);
                setMessage(print)
            }
            catch (e) {
                console.log(e);
            }
        }
        getMessage();
    }, [messageDoc])

    async function handleSubmit(event) {
        localStorage.setItem("user_ont", selectedOnt.id.toString())
        localStorage.setItem("user_ont_name", selectedOnt.name)
        setSelectedDoc({ id: 0, name: "Выберите документ", text: "" })
        setResult(await messageDoc());
        setName(selectedOnt.name !== null ? selectedOnt.name : "");
    };


    return (
        <>
            <OntDropdown selected={selectedOnt} setSelected={setSelectedOnt} result={message} />
            <button className='ont-upload-file-submit' type="button" onClick={handleSubmit}>Подтвердить выбор</button>
        </>
    )
}