# Team Builder API

This FastAPI service helps select an optimal team of products within a given budget.

## Approach

- **Data Model:** Each product has attributes — id, name, category, price, and rating.
- **Value Calculation:** Products are grouped by category, then ratings and prices are normalized within each category. A weighted score balances higher ratings and lower prices using a logarithmic adjustment.
- **Optimization:** Using Google OR-Tools, the solver maximizes the total value of selected products under these constraints:
  - Total price ≤ budget
  - At most one product per category
  - Exactly 5 products in the team
- **Result:** Returns the list of products forming the best-value team.

## Usage

Send a GET request to `/team-builder?budget=YOUR_BUDGET` to receive the optimized product team.

---

This method ensures a balanced, diverse, and cost-effective selection of products.
