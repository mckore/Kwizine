import Header from "./Header";
import Footer from "./Footer";

const Layout = ({ children }) => {
  return (
    <div className="flex flex-col h-screen bg-orange-50">
      <Header />
      <div className="flex-1">{children}</div>
      <Footer />
    </div>
  );
}
export default Layout;