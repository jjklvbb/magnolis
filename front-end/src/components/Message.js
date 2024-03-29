import React, { useState, useEffect } from 'react'
import axios from 'axios';

export default function Message() {

    const [result, setResult] = useState(null);

    const message = async () => {
        try{
            let url = 'http://127.0.0.1:8000/api/v1/magic/gethello';
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
            
            console.log(res.data)  
            let print = res.data.map((data) => data.value);
            setResult(print);
        }
        catch(e){
            console.log(e);
        }
    };

    useEffect(() => {
        message()
    }, [])

    return (
        <div>
            {result}
        </div>
    )
}
