import Layout from "../components/Layout";
import Card from "../components/Card";
import {useState, useEffect } from "react";

const Recipes = () => {
  const [recipes, setRecipes] = useState([])
  const [title, setTitle] = useState('')
  const [isPending, setIsPending] = useState(true)

  useEffect(() => {
    fetch(`https://localhost:8000/recipes?title=${title}`)
      .then(response => response.json())
      .then(json => setRecipes(json))
      setIsPending(false)
  }, [title])

  const handleChangeTitle = (event) => {
    setRecipes([])
    setTitle(event.target.value)
    setIsPending(true)
  }

  return (
    <Layout>
      <h2>Recipes - {title?title: "all recipes"} </h2>
          <div>
        <label htmlFor="recipes">Choose a Recipe: </label>
        <select name="recipes" id="recipes" onChange={handleChangeTitle}>
          <option value="">All Recipes</option>
          <option value="">Chantilly Marscapone Vanille</option> 
          </select>
          </div>
          <div>
            {isPending && <div><h2>Loading Recipes, title: {title}...</h2></div>}
            <div>
              {recipes && recipes.map((ele)=>{
                return (<Card key={ele.id} recipe={ele}/>)
                }
                )}
            </div>
          </div>
    </Layout>
  )

}
export default Recipes;