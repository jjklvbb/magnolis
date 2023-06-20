import  {useState, useEffect } from "react";

export const OntDropdown = ({selected, setSelected, result}) => {
    const [isActive, setIsActive] = useState(false);

    return (
        <div className="ont-dropdown">
            <div className="ont-dropdown-btn" onClick={e => 
                    {setIsActive(!isActive)}
                }>{selected.name}</div>
            
            {isActive && (
                <div className="ont-dropdown-content">
                    {result.map(option => (
                        <div key={option.id} onClick={(e) => {
                            setSelected(option)
                            setIsActive(false)
                        }} 
                        className="ont-dropdown-item">
                        {option.name}
                    </div>
                    ))}
            </div>
            )}
        </div>
    )
}