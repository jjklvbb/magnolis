import { useState } from 'react';
import axios from 'axios';
import useFileDownload from "./useFileDownload";

export const UploadOnt = ({setResult, setSelected, name, setName, deleteOnt}) =>{

    const [file, setFile] = useState(null);

    function handleChange(event) {
        setFile(event.target.files[0]);
        console.log(file);
    }

    const {message} = useFileDownload();

    async function handleSubmit(event) {
        console.log(file);
        event.preventDefault()
        try{
            let url = 'http://localhost:8000/api/v1/magic/uploadont';
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
                    'Access-Control-Allow-Origin': '*' },
              })
                .then(async function (response) {
                    let id = response.data['id']
                    localStorage.setItem("user_ont", id.toString())
                    localStorage.setItem("user_ont_name", file.name)
                    console.log(id);
                    console.log(response);
                    setSelected({id: 0, name: "Выбирите документ", text: ""})
                    setResult(await message());

                    setName(file !== null ? file.name : "");
                })
                .catch(function (response) {
                  console.log(response);
                });
        }
        catch(e){
            console.log(e);
        }
    };

    
    return (
        <>
           <form  onSubmit={handleSubmit}>
                <h2>Текущая онтология: {name}</h2>
                <input className='upload-file-btn' type="file" onChange={handleChange}/>
                <button className='upload-file-submit' type="submit">Загрузить онтологию</button>
                <button className='ClearDB' onClick={deleteOnt} >Очистить БД</button>
            </form>
        </>
    )
}