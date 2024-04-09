import logo from './assets/kwizinebkg.jpg';
import Layout from './components/Layout';
import Card from './components/Card';

function App() {
  return (
    <Layout>
      <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Kwizine - A recipe sharing app
        </p>
      </header>
    </div>
    </Layout>
    
  );
}

export default App;
