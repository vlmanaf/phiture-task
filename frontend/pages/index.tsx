import { useState, ChangeEvent } from "react";

interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  rating: number;
}

export default function Home() {
  const [budget, setBudget] = useState<string>("");
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchProducts = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(
        `http://localhost:8000/team-builder?budget=${encodeURIComponent(budget)}`,
        {
          method: "GET",
        }
      );

      if (!res.ok) {
        throw new Error("Failed to fetch products");
      }

      const data: Product[] = await res.json();
      setProducts(data);
    } catch (err: any) {
      setError(err.message);
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setBudget(e.target.value);
  };

  // ✅ Calculate total price
  const totalPrice = products.reduce((sum, p) => sum + p.price, 0);

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "Arial" }}>
      <h1>Product Recommendations</h1>
      <input
        type="number"
        placeholder="Enter your budget"
        value={budget}
        onChange={handleInputChange}
        style={{ padding: "0.5rem", width: "100%", marginBottom: "1rem" }}
      />
      <button onClick={fetchProducts} disabled={!budget || loading}>
        {loading ? "Loading..." : "Get Recommendations"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {products.length > 0 && (
        <>
          <table
            style={{
              marginTop: "1rem",
              borderCollapse: "collapse",
              width: "100%",
            }}
          >
            <thead>
              <tr>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>
                  Name
                </th>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>
                  Category
                </th>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>
                  Price
                </th>
                <th style={{ border: "1px solid #ddd", padding: "8px" }}>
                  Rating
                </th>
              </tr>
            </thead>
            <tbody>
              {products.map(({ id, name, category, price, rating }) => (
                <tr key={id}>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    {name}
                  </td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    {category}
                  </td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    ${price.toFixed(2)}
                  </td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    {rating.toFixed(1)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* ✅ Total Price Display */}
          <p
            style={{
              marginTop: "1rem",
              textAlign: "right",
              fontWeight: "bold",
              fontSize: "1rem",
            }}
          >
            Total Price: ${totalPrice.toFixed(2)}
          </p>
        </>
      )}
    </div>
  );
}
