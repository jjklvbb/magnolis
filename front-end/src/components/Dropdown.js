import  {useState, useEffect } from "react";
import useFileDownload from "./useFileDownload";

function Dropdown ({selected, setSelected, result, setResult}) {
    const [isActive, setIsActive] = useState(false);

    const {message} = useFileDownload();

    useEffect(() => {
        async function loadData () {
            setResult(await message());
        }
        loadData();
    }, [])

    return (
        <div className="dropdown">
            <div className="dropdown-btn" onClick={e => 
                    {setIsActive(!isActive)}
                }>{selected.name}</div>
            
            {isActive && (
                <div className="dropdown-content">
                    {result.map(option => (
                        <div key={option.id} onClick={(e) => {
                            setSelected(option)
                            setIsActive(false)
                        }} 
                        className="dropdown-item">
                        {option.name}
                    </div>
                    ))}
            </div>
            )}
        </div>
    )
}

export default Dropdown