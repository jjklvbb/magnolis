import axios from 'axios';

export default function useFileDownload() {
    const message = async () => {
        if (localStorage.getItem("user_ont") === null) return [];
        try{
            let url = 'http://77.222.42.117:8000/api/v1/magic/textdocs/' + localStorage.getItem("user_ont");
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
            let print = res.data.map((data) => data);
            console.log(print);
            return print; 
        }
        catch(e){
            console.log(e);
        }
    };

    return {message}
}
