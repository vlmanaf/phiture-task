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

## Set up

```
$ docker-compose build
$ docker-compose up
```
## Usage

Direct your browser to http://localhost:3000 for a frontend app
or send a GET request to http://localhost:8000/team-builder?budget=YOUR_BUDGET to access backend directly.
