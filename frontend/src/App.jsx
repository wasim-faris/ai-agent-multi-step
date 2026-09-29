import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/api/products/search/";

function App() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setResult(null);
    setError("");

    if (!message.trim()) {
      setError("Please enter what you are looking for.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message.trim() }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "The search could not be completed. Please try again.");
        return;
      }

      setResult(data);
    } catch {
      setError(
        "Cannot connect to the server. Make sure the Django backend is running."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <header className="page-header">
        <p className="eyebrow">A simpler way to compare</p>
        <h1>AI Product Finder</h1>
        <p className="intro">Find laptops and mobiles using your own words.</p>
      </header>

      <form className="search-form" onSubmit={handleSubmit}>
        <label htmlFor="product-request">What are you looking for?</label>
        <textarea
          id="product-request"
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Show me laptops under 50000 with 16GB RAM"
          rows="3"
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Searching..." : "Search products"}
        </button>
      </form>

      {loading && (
        <p className="loading-state" role="status">
          <span className="loading-spinner" aria-hidden="true" />
          Searching products...
        </p>
      )}

      {error && <p className="error-message" role="alert">{error}</p>}

      {result && (
        <section className="results" aria-live="polite">
          <div className="answer">
            <h2>AI response</h2>
            <p>{result.message}</p>
          </div>

          <div className="products-heading">
            <h2>Products</h2>
            <span>{result.products.length} found</span>
          </div>

          {result.products.length > 0 ? (
            <div className="product-list">
              {result.products.map((product) => (
                <article className="product" key={product.name}>
                  <div className="product-title">
                    <div>
                      <p className="brand">{product.brand}</p>
                      <h3>{product.name}</h3>
                    </div>
                    <p className="price">₹{product.price.toLocaleString("en-IN")}</p>
                  </div>
                  <dl>
                    <div><dt>RAM</dt><dd>{product.ram}</dd></div>
                    <div>
                      <dt>Storage</dt>
                      <dd>{product.storage}{product.storage_type ? ` ${product.storage_type}` : ""}</dd>
                    </div>
                    <div><dt>Color</dt><dd>{product.color}</dd></div>
                  </dl>
                </article>
              ))}
            </div>
          ) : (
            <p className="empty-results">
              No products found matching your requirements.
            </p>
          )}
        </section>
      )}
    </main>
  );
}

export default App;
