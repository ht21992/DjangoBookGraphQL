import "./App.css";

function App() {
  const books = [];

  return (
    <div className="bg-base-100">
      <div className="navbar bg-base-200 shadow-lg">
        <div className="flex-1">
          <a href="#" className="btn btn-ghost normal-case text-xl">
            📚 Book Manager
          </a>
        </div>
        <div className="flex-none">
          <a href="#" className="btn btn-primary">
            ➕ Add New Book
          </a>
        </div>
      </div>
      <div className="container mx-auto mt-10"></div>
    </div>
  );
}

export default App;
