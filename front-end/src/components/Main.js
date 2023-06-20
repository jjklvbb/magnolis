import React, {useEffect, useState} from 'react';
import {BrowserRouter, Route, Routes, Navigate, Link} from "react-router-dom";
import Tabs from "../components/Tabs";
import Auth from "../components/Auth";

export default function Main() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path ="/" element={<Auth />} />
                <Route path ="/main" element={<Tabs />} />
            </Routes>
        </BrowserRouter>
    );
}