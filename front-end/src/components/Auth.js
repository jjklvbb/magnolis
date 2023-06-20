import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';

export default function Auth() {

    const navigate = useNavigate();

    const loginRef = useRef()
    const passwordRef = useRef()

    async function registrationHandle(e) {
        try {
            let login = loginRef.current.value
            let password = passwordRef.current.value
            let url = 'http://127.0.0.1:8000/api/v1/magic/registration/';
            await axios(url, {
                method: 'POST',
                mode: 'no-cors',
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json',
                },
                withCredentials: true,
                credentials: 'same-origin',
                params: {
                    login: login,
                    password: password,
                }
            })
                .then(async function (response) {
                    if (response.status === 200) {
                        console.log(response);
                        let id = response.data['id'];
                        console.log(id);
                        localStorage.setItem("user_id", id.toString());
                        navigate("/main");
                    }
                })
                .catch(function (response) {
                    if (response.response.data['status'] === "reg_error") {
                        alert(response.response.data['error']);
                    }
                });
        }
        catch (e) {
            console.log(e);
        }
    }

    async function authHandle(e) {
        try {
            let login = loginRef.current.value
            let password = passwordRef.current.value
            let url = 'http://127.0.0.1:8000/api/v1/magic/auth/';
            await axios(url, {
                method: 'POST',
                mode: 'no-cors',
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json',
                },
                withCredentials: true,
                credentials: 'same-origin',
                params: {
                    login: login,
                    password: password,
                }
            })
                .then(async function (response) {
                    if (response.status === 200) {
                        console.log(response);
                        let id = response.data['id'];
                        console.log(id);
                        localStorage.setItem("user_id", id.toString());
                        navigate("/main");
                    }
                })
                .catch(function (response) {
                    if (response.response.data['status'] === "auth_error") {
                        alert(response.response.data['error']);
                    }
                });
        }
        catch (e) {
            console.log(e);
        }
    }

    return (
        <div className='auth-container'>
            <input ref={loginRef} type="text" className="auth-input" placeholder='Введите логин' /><br />
            <input ref={passwordRef} type="password" className="auth-input" placeholder='Введите пароль' /><br />
            <button onClick={registrationHandle} className="auth-button">Зарегестрироваться</button>
            <button onClick={authHandle} className="auth-button">Войти</button>
        </div>
    );
}