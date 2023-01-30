import { useState } from 'react';
import axios from 'axios';
import useFileDownload from "./useFileDownload";

export const UploadFile = ({setResult, setSelected}) =>{

    const [files, setFiles] = useState();

    async function handleChange(event) {
        setFiles(event.target.files);
        //console.log(files);
    }

    const {message} = useFileDownload();

    async function handleSubmit(event) {
        console.log(files);
        event.preventDefault()
        {(Array.from(files)).map(async file => {
            try{
                let url = 'http://77.222.42.117:8000/api/v1/magic/uploaddoc/' + localStorage.getItem("user_ont");
                const formData = new FormData();
                formData.append('file', file);
                formData.append('fileName', file.name);
                const response = await axios({
                    method: "post",
                    url: url,
                    data: formData,
                    headers: { 
                        "accept": "application/json",
                        "Content-Type": "multipart/form-data",
                        'Access-Control-Allow-Origin': '*' },
                  })
                    .catch(function (response) {
                      console.log(response);
                    });
                console.log(response);
                setResult(await message());
            }
            catch(e){
                console.log(e);
            }
            })}
    };

    async function deleteDocs(e){
        if (localStorage.getItem("user_ont") === null) return
        try{
          let url = 'http://77.222.42.117:8000/api/v1/magic/deletedocs/' + localStorage.getItem("user_ont");
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
        }
        catch(e){
            console.log(e);
        }
      }

    return (
        <>
           <form  onSubmit={handleSubmit}>
                <input className='upload-file-btn' type="file" onChange={handleChange} multiple/>
                <button className='upload-file-submit' type="submit">Загрузить</button>
                <button className='delete-docs' onClick={deleteDocs} >Удалить документы</button>
            </form>
        </>
    )
}