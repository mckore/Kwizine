import React from 'react';
import ReactDOM from 'react-dom/client';
import {BrowserRouter, Routes,  Route} from 'react-router-dom';
import './index.css';
import Recipe from './pages/Recipe';
import Recipes from './pages/Recipes';
import NewRecipe from './pages/NewRecipe';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />}/>
      <Route path="recipes" element={<Recipes />}/> 
      <Route path="recipes/:id" element={<Recipe />}/>
      <Route path="recipes/new" element={<NewRecipe />}/>
    </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
