import { Link } from "react-router-dom"
const Card = ({ recipe }) => {
  let { title, ingredients, _id } = recipe


  return (
    <Link to={`/recipes/${_id}`}>
      <div className="shadow-lg p-5 flex flex-col bg-FarmWhite rounded-lg transition ease-in-out hover:scale-105 duration-300 font-mono">
        <div className="font-bold text-center text-lg text-FarmNavy"><span className="text-FarmLime">{title}</span></div>
        <div>Title: {title}</div>
        <div>Ingredients: {ingredients}</div>
      </div>
    </Link>
  )
}
export default Card