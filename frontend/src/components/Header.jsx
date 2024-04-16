import { NavLink, Link } from "react-router-dom";

const Header = () => {
    return (
        <nav className="flex justify-between relative items-center font-mono h-16">
            <Link to ="/" className="pl-8 text-xl font-bold">The Morceau</Link>
            <div className="pr-8 font-semibold">
                <NavLink className = {({isActive}) => isActive ? "active-link": "p-4"} to="/">Home</NavLink>
                <NavLink className = {({isActive}) => isActive ? "active-link": "p-4"} to="/recipes">Recipes</NavLink>
                <NavLink className = {({isActive}) => isActive ? "active-link": "p-4"} to="/new">New Recipe</NavLink>
                </div>
        </nav>
    )
}
export default Header;