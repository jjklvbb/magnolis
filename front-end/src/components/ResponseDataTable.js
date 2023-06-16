import React from 'react'

export default function ResponseDataTable({responseData}) {

    return (
        <table>
        <thead>
            <tr>
                <th>Документ</th>
                <th>Сущность</th>
                <th>Атрибут</th>
                <th>Значение</th>
            </tr>
        </thead>
        <tbody>
            {responseData.map((row, i) => {
            return (
                <tr key={i} >
                    <td>{row.doc}</td>
                    <td>{row.entity_name}</td>
                    <td>{row.attr}</td>
                    <td>{row.value}</td>
                </tr>
            )
            })}
        </tbody>
        </table>
    )
}
