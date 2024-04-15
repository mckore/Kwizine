imoprt Layout from "../../components/Layout";
import { useEffect } from "react";
import Card from "../../components/Card";

const Recipes = () => {
  const [recipes, setRecipes] = useState([])
  const [brand, setBrand] = useState('')
  const [isPending, setIsPending] = useState(true)

  useEffect(() => {
    fetch(`https://localhost:8000/recipes?title=${title}`)
      .then(response => response.json())
      .then(json => setRecipes(json))
      setIsPending(false)
  }, [title])

  return (
    <div>
      <h1>Recipes</h1>

    </div>
  )

}
export default Recipes;