import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import CSRFToken from "./CSRFToken";
import "./App.css";

const App = () => {
  const [books, setBooks] = useState([]);
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");

  const renderedIds = new Set();

  const filteredBooks = books.filter((book) =>
    book.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleDelete = (id) => {
    setBooks(books.filter((book) => book.id !== id));
  };

  const fetchBooks = async (currentOffset) => {
    console.log("called");
    setLoading(true);

    const graphqlQuery = {
      query: `
              query GetAllBooks($limit: Int, $offset: Int) {
                  allBooks(limit: $limit, offset: $offset) {
                      id
                      title
                      image
                      description
                      author {
                          name
                      }
                  }
              }
          `,
      variables: {
        limit: 10,
        offset: currentOffset,
      },
    };

    try {
      const response = await axios.post("/graphql/", graphqlQuery, {
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });
      const fetchedBooks = response.data.data.allBooks;
      setBooks((prevBooks) => [...prevBooks, ...fetchedBooks]);

      setOffset((prevOffset) => prevOffset + fetchedBooks.length);
    } catch (error) {
      console.error("Error fetching books:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const handleScroll = () => {
      if (
        window.innerHeight + document.documentElement.scrollTop >=
          document.documentElement.offsetHeight - 100 &&
        !loading
      ) {
        setLoading(true);
        fetchBooks(offset);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [offset, loading]);

  useEffect(() => {
    console.log("from here 0");
    fetchBooks(0);
  }, []);

  return (
    <div className="library-container">
      <CSRFToken />
      <h1 className="title">Library</h1>
      <input
        type="text"
        placeholder="Search books..."
        className="search-bar"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <div className="book-list">
        {filteredBooks.map((book) => {
          if (renderedIds.has(book.id)) {
            return null;
          }
          renderedIds.add(book.id);

          return (
            <div key={book.id} className="book-card">
              <img src={book.image} alt={book.title} className="book-image" />
              <div className="book-info">
                <h4 className="book-title">{book.title}</h4>
                <p className="book-description">
                  {book.description.slice(0, 100)}
                </p>
                <div className="button-container">
                  <button className="btn btn-primary">Update</button>
                  <button
                    className="btn btn-danger"
                    onClick={() => handleDelete(book.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
      {loading && (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading...</p>
        </div>
      )}
    </div>
  );
};

export default App;
