import Header from "./Header";

const Layout = ({ children }) => {
  return (
    <div className="flex flex-col h-screen bg-orange-50">
      <Header />
      <div className="flex-1">{children}</div>
    </div>
  );
}
export default Layout;