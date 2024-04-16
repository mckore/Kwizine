import logo from './assets/kwizinebkg.jpg';
import Layout from './components/Layout';

function App() {
  return (
    <Layout>
      <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Morceau - new name for budding idea
        </p>
      </header>
    </div>
    </Layout>
    
  );
}

export default App;
