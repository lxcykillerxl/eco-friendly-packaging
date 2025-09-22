# eco-friendly-packaging

High‑Level Summary – Eco‑Friendly Packaging Repository

Component	Description
Purpose	A Streamlit‑based web app that lets users compare a product’s current (“old”) packaging with up to three eco‑friendly alternatives. It visualises CO₂ emissions and decomposition time, and provides a quick summary of potential environmental gains.
Data	• eco_friendly.csv – main dataset containing product names, old packaging details, and up to three new packaging options (CO₂, shelf‑life, decomposition).
• eco_.csv – auxiliary/preview data (not directly used by the app).
Models	• model_co2.pkl – pre‑trained regression (or similar) model for predicting CO₂ impact of packaging.
• model_decomp.pkl – model for estimating decomposition time.
• encoder.pkl & encoder_product.pkl – label encoders for categorical features (e.g., packaging types, product names).
App Script	project_shell.py – the Streamlit application:
1. Loads eco_friendly.csv.
2. Accepts a product name (case‑insensitive).
3. Shows old packaging info in a red‑styled card.
4. Displays each available eco‑friendly alternative in expandable green cards.
5. Generates two bar charts (CO₂ and decomposition years) with shortened labels for readability.
6. Calculates and shows a summary card with average CO₂ reduction and average decomposition improvement.
Key Features	• Interactive UI with instant feedback.
• Automatic handling of missing data.
• Visual comparison via side‑by‑side bar charts.
• Summary metrics (percentage CO₂ reduction, average decomposition time).
Typical Workflow	1. Clone the repo.
2. Install dependencies (streamlit, pandas, matplotlib, numpy).
3. Ensure the CSV files are in the same directory as project_shell.py.
4. Run streamlit run project_shell.py.
5. Type a product name (e.g., Banana, Milk, Apple) to explore packaging alternatives.
Potential Extensions	• Add more products and packaging options.
• Incorporate additional environmental metrics (water usage, energy).
• Deploy the app on a cloud platform (e.g., Streamlit Community Cloud).
