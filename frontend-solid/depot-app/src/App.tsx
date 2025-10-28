import ExampleComponent from "./components/ExampleComponent";
import Home from "./pages/Home";

export default function App() {
  return (
    <div>
      <header>
        <h1>Depot App (Solid)</h1>
      </header>
      <main>
        <Home />
        <ExampleComponent />
      </main>
    </div>
  );
}