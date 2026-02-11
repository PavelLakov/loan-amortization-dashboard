
---

https://huggingface.co/spaces/pavellakov/loan-amortization-dashboard


# Loan Calculator Dashboard (Streamlit)

A Streamlit app that calculates loan payments and generates a full **amortization schedule** with an optional **interactive dashboard** (Plotly charts).

## Features
- Sidebar inputs:
  - Loan amount
  - Annual interest rate (%)
  - Loan term (years)
  - Currency selection (USD/EUR/GBP/JPY/CAD)
- Key metrics:
  - Monthly payment
  - Total payment
  - Total interest
  - Loan term
- Full amortization schedule table (payment #, interest, principal, remaining balance)
- Download the schedule as **CSV**
- Toggle a dashboard with 4 charts:
  - Remaining balance over time
  - Cumulative interest vs. cumulative principal (bars)
  - Total breakdown (pie)
  - Interest vs. principal per payment (scatter)

## Tech Stack
- Python
- Streamlit
- Pandas / NumPy
- Plotly (graph_objects + subplots)

## Run Locally

### 1) Create a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate  # Windows
```

### 2) Install dependencies
```bash
pip install streamlit pandas numpy plotly
```

### 3) Start the app
```bash
streamlit run loan_calculator.py
```

Then open the local URL shown in the terminal (usually http://localhost:8501).

## Project Structure (suggested for GitHub)
```
loan-calculator-dashboard/
  loan_calculator.py
  README.md
  requirements.txt
```

### Example `requirements.txt`
```txt
streamlit
pandas
numpy
plotly
```

## Notes
- Interest rate input is converted to a decimal internally (e.g., 5% → 0.05).
- If interest rate is 0%, the app uses a simple principal / number_of_payments calculation.

## License
Add a license if you plan to publish publicly (MIT is common for small demo projects).
