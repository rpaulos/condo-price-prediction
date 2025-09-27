<div>
  <img src="https://i.imgur.com/3Vbzw56.png" /> 
</div>
<h2 align="center" id="pinpoint">Demand Just Got Predictable</h2>

<p align="center">
  <a href="https://github.com/rpaulos/condo-price-prediction">
    <img src="https://img.shields.io/badge/-🏢%20OccuPie-blue?style=for-the-badge" alt="OccuPie" />
  </a>
  <a href="https://www.canva.com/design/DAGw-uexZzo/Q5nBn2KkSMCg6PWsHWlg_Q/edit?fbclid=IwY2xjawMZTTNleHRuA2FlbQIxMQABHhgOrkz-EJ9nvr1iCIGcevqiDvREcgcTkmbU_ZhjuX3jISVLY9GDu2Z4zgk-_aem_g_SkdNZJxn36IaDneFHnAA">
    <img src="https://img.shields.io/badge/-📊%20Pitch%20Deck-gold?style=for-the-badge" alt="Final Pitch Deck" />
  </a>
</p>

---

## 📚 Table of Contents
- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Data Acquisition](#data-acquisition-and-storage)
- [Feature Highlights](#feature-highlights)
- [Monthly Rent Prediction](#price)
- [Demand Prediction](#demand)
- [Nearby Establishments](#nearby)
- [AI Analyst](#gemini)
- [Repository Structure](#repository-structure)
- [How to Access PinPoint](#how-to-access-occupie-locally)
- [Team Details](#team-details)

---

<h2 id="project-overview">🧠 Project Overview</h2>

<!-- OccuPie Overview Image -->
<p align="center">
  <img src="https://i.imgur.com/LZv4EsL.png" alt="PinPoint Overview" width="100%"/>
</p>

<!-- Project Description -->
<p align="justify" style="font-size: 16px; line-height: 1.6;">
  <strong>OccuPie</strong> is a condo price and occupancy prediction tool designed to help property owners, buyers, and investors make data-driven decisions. It streamlines the process of evaluating condominium listings by analyzing key factors such as location, unit size, furnishing type, available amenities, and nearby establishments. By leveraging machine learning and real-time data from Google Maps, OccuPie provides accurate rental price estimates and predicts occupancy rates, reducing guesswork and improving investment planning.
</p>

<p align="justify" style="font-size: 16px; line-height: 1.6;">
  Users can input details such as location, neighborhood or district, floor area, number of bedrooms and bathrooms, furnishing status, and available amenities. OccuPie’s predictive model then analyzes these factors together with local demand patterns to provide clear, easy-to-understand occupancy forecasts.
</p>

<p align="justify" style="font-size: 16px; line-height: 1.6;">
  The tool helps property owners plan pricing strategies, supports real estate agents in advising clients, and enables investors to identify high-potential areas. By presenting insights in an intuitive dashboard, OccuPie simplifies complex market analysis and empowers users to act with confidence in the competitive rental market.
</p>

---

<h2 id="tech-stack">🛠️ Tech Stack</h2>

<!-- PinPoint Techstack Overview Image -->
<p align="center">
  <img src="https://i.imgur.com/1wEJSz2.png" alt="PinPoint Techstack Overview" width="100%"/>
</p>

<!-- Techstack Summary -->
<p align="justify" style="font-size: 16px; line-height: 1.6;"> 
  This section outlines the core technologies and tools that power <strong>OccuPie</strong>. It covers the end-to-end stack, from the backend responsible for orchestrating the machine learning models, to the data processing workflows, external API integrations, and frontend design tools. Each component plays an essential role in ensuring accurate predictions and evaluations, efficient data handling, and a seamless user experience for those who own or planning to own condos in Quezon City.
</p>

<div align="center" style="width: 100%;">
  <table style="width: 100%;">
    <thead>
      <tr>
        <th>#</th>
        <th>Tool / Technology</th>
        <th>Category</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <!-- Programming Language -->
      <tr><td>1</td><td>Python</td><td>Programming Language</td><td>Core backend logic and data handling.</td></tr>
      <!-- APIs -->
      <tr><td>2</td><td>Google Maps API</td><td>API</td><td>Enables location and mapping features such as geocoding and interactive map rendering.</td></tr>
      <tr><td>3</td><td>Gemini API</td><td>API</td><td>Performs AI analysis and generates intelligent results based on input data.</td></tr>
      <!-- Frameworks -->
      <tr><td>4</td><td>Flask</td><td>Framework</td><td>Backend web application framework that handles routing and API endpoints.</td></tr>
      <tr><td>5</td><td>Streamlit</td><td>Framework</td><td>Prototype and data visualization framework for quick interactive dashboards.</td></tr>
      <!-- Frontend -->
      <tr><td>6</td><td>HTML</td><td>Frontend</td><td>Structures the content of the web application.</td></tr>
      <tr><td>7</td><td>CSS</td><td>Frontend</td><td>Styles the web pages and defines the visual appearance of the user interface.</td></tr>
      <tr><td>8</td><td>JavaScript</td><td>Frontend</td><td>Adds interactivity and dynamic behavior to the frontend.</td></tr>
      <!-- Tools -->
      <tr><td>9</td><td>VSCode</td><td>Tools / IDE</td><td>Code editing and debugging environment.</td></tr>
      <tr><td>10</td><td>Conda</td><td>Tools / Package & Environment Manager</td><td>Manages project dependencies and isolated Python environments.</td></tr>
      <!-- Web Scraping -->
      <tr><td>11</td><td>BeautifulSoup</td><td>Library</td><td>Extracts and parses data from HTML content.</td></tr>
      <tr><td>12</td><td>Selenium</td><td>Library</td><td>Automates browser interactions for scraping dynamic websites.</td></tr>
      <tr><td>13</td><td>Undetected Chrome Driver</td><td>Library</td><td>Bypasses bot detection while automating Chrome for web scraping.</td></tr>
      <!-- Data Handling & Analysis -->
      <tr><td>14</td><td>pandas</td><td>Library</td><td>Organizes data into dataframes and exports to CSV files for analysis.</td></tr>
      <tr><td>15</td><td>NumPy</td><td>Library</td><td>Provides numerical arrays as required input for the predictive models.</td></tr>
      <tr><td>16</td><td>googlemaps</td><td>Library</td><td>Python client library for the Google Maps API.</td></tr>
      <tr><td>17</td><td>google.generativeai</td><td>Library</td><td>Python SDK for interacting with the Gemini API.</td></tr>
      <tr><td>18</td><td>requests</td><td>Library</td><td>Handles HTTP requests to retrieve web data and interact with APIs.</td></tr>
      <tr><td>19</td><td>pickle</td><td>Library</td><td>Loads the pre-trained model by deserializing the saved model file.</td></tr>
      <tr><td>20</td><td>folium</td><td>Library</td><td>Generates interactive maps for prototyping and project feasibility checks.</td></tr>
      <tr><td>21</td><td>pprint</td><td>Library</td><td>Displays JSON and structured data in a readable format.</td></tr>
    </tbody>
  </table>
</div>

---

<h2 id="data-acquisition-and-storage">📦 Data Acquisition and Storage </h2>

## Data Sources and Methodology

<p align="justify" style="font-size: 16px; line-height: 1.6;">
  OccuPie focuses on the Quezon City condominium market, leveraging web-scraped data from Rentpad to capture detailed property information. This dataset is enhanced with geolocation and nearby establishment data from Google Maps, providing context for both rental prices and occupancy demand. Using automated scraping tools such as Selenium, BeautifulSoup, and Undetected ChromeDriver, the platform collects, cleans, and structures the data to feed its predictive models. This methodology ensures that users receive accurate, evidence-based insights tailored to the Quezon City market.
</p>

<h3> 🗺️ Data Sources </h3>
<p align="center">
  <img src="https://i.imgur.com/j1NYozv.png" alt="PinPoint Data Sources" width="100%"/>
</p>

### 🏢 Condo Listings Data
- **Source:** Rentpad (web-scraped)
- **Process:** Data collected using Selenium, BeautifulSoup, and Undetected ChromeDriver; cleaned and structured for model input
- **Purpose:** Provides detailed property information such as rental price, floor area, bedrooms, bathrooms, and furnishing status to train predictive models

### 🏬 Nearby Establishments Data
- **Source:** Google Maps API
- **Coverage:** Quezon City, including schools, hospitals, shopping centers, and transportation hubs
- **Purpose:** Enriches condo listings with contextual information that impacts rental value and occupancy demand
  
---

<h2 id="feature-highlights">✨ Feature Highlights </h2>

<img src = "https://i.imgur.com/3pz6sPO.png" width="100%">

<p align="justify" style="font-size: 16px; line-height: 1.6;">
This section showcases OccuPie's key features that work together to provide data-driven insights for price and demand prediction. By combining advanced data collection, geospatial analysis, and machine learning models, the platform enables users to make informed decisions about condominium investments and rentals.
</p>

<h3 id="price">📊 Monthly Rent Prediction</h3>

<p align="justify" style="font-size: 16px; line-height: 1.6;">
  OccuPie’s rent prediction feature leverages historical condo listing data and nearby establishment context to forecast accurate monthly rental prices. By analyzing property details, amenities, and location factors, this feature helps property owners, investors, and renters make informed pricing decisions that reflect current market conditions in Quezon City.
</p>

<h3 id="#demand">📍 Condo Unit Demand Prediction</h3>

<p align="justify" style="font-size: 16px; line-height: 1.6;">
  OccuPie’s demand prediction feature estimates the expected occupancy rate for each condo unit. By considering property characteristics, neighborhood features, and nearby amenities, the platform identifies high-demand units and areas, helping owners and investors optimize rental strategies and maximize returns.
</p>

<h3 id="nearby">🔍 Nearby Establishment Mapping</h3>

<p align="justify" style="font-size: 16px; line-height: 1.6;">
  OccuPie maps key establishments surrounding each condominium, including schools, hospitals, shopping centers, and transportation hubs. This contextual information allows users to evaluate how nearby facilities impact rental value and occupancy, supporting smarter investment and rental decisions.
</p>

<h3 id="gemini">🤖 Gemini AI Analysis and Recommendation</h3>

<p align="justify" style="font-size: 16px; line-height: 1.6;">
  OccuPie integrates AI-driven analysis using the Gemini API to provide actionable insights on rental pricing and demand. The system synthesizes property details, location data, and market trends to generate clear, data-backed recommendations, helping users understand the factors driving each prediction and make confident, evidence-based decisions.
</p>

---

<h2 id="how-to-access-occupie-locally"> 📶 How to Access OccuPie Locally</h2>

## 1) Launching the System Locally

### a) Clone the Repository – Get a copy of the source code on your machine
```bash
git clone https://github.com/rpaulos/condo-price-prediction
cd condo-price-prediction/OccuPie
```

### b) Install Dependencies – Make sure Python is installed, then install all required packages
```bash
pip install -r requirements.txt
```

### c) Set Up API Keys – Create a file named keys.py inside the OccuPie directory
``` bash
googlemaps_api_key = "YOUR_GOOGLE_MAPS_API_KEY"
gemini_api_key = "YOUR_GEMINI_API_KEY"
```

### d) Run the Application – Start the Flask backend that powers the project
``` bash
python backend.py
```

### e) Access the App – Open a browser and navigate to the local development server
``` bash
http://127.0.0.1:5000
```

<p align="justify" style="font-size: 16px; line-height: 1.6;">
You can access Occupie repository by pressing the button below or by manually entering the link (https://github.com/rpaulos/condo-price-prediction) into your browser.
</p>


<p align="center">
  <a href="https://github.com/rpaulos/condo-price-prediction">
    <img src="https://img.shields.io/badge/-🏢%20OccuPie-blue?style=for-the-badge" alt="OccuPie" />
  </a>
</p>

---

<h2>👨‍💻 Team Details 👨‍💻</h2>

<table align="center" width="100%">
  <tr>
    <!-- Rae -->
    <td align="center" width="33%">
      <img src="https://i.imgur.com/xHKeiUq.png" alt="Rae Paulos" style="border-radius: 50%; width: 120px; height: 120px;"><br><br>
      <strong>Rae Paulos</strong><br>
      <p align="center">
        <a href="https://github.com/rpaulos">
          <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
        </a>
        <a href="https://linkedin.com/in/rae-paulos-8969b5249">
          <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
        </a>
      </p>
    </td>
    <!-- Leon -->
    <td align="center" width="33%">
      <img src="https://i.imgur.com/noZCXby.png" alt="Leon Marco" style="border-radius: 50%; width: 120px; height: 120px;"><br><br>
      <strong>Leon Marco Devela</strong><br>
      <p align="center">
        <a href="https://github.com/leonnmarcoo">
          <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
        </a>
        <a href="https://www.linkedin.com/in/leon-marco-devela-ba861026b/">
          <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
        </a>
      </p>
    </td>
    <!-- Kurt Almadrones -->
    <td align="center" width="33%">
      <img src="https://i.imgur.com/xHKeiUq.png" alt="Kurt Justine Almadrones" style="border-radius: 50%; width: 120px; height: 120px;"><br><br>
      <strong>Kurt Almadrones</strong><br>
      <p align="center">
        <a href="https://github.com/justjstine">
          <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
        </a>
        <a href="https://www.linkedin.com/in/kurt-justine-almadrones-964765195/">
          <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
        </a>
      </p>
    </td>
    <!-- Lance Kenneth -->
    <td align="center" width="33%">
      <img src="https://i.imgur.com/xHKeiUq.png" alt="Rae Paulos" style="border-radius: 50%; width: 120px; height: 120px;"><br><br>
      <strong>Lance Kenneth Dela Paz</strong><br>
      <p align="center">
        <a href="https://github.com/lowvey">
          <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
        </a>
        <a href="https://www.linkedin.com/in/lance-kenneth-dela-paz-a26567386/">
          <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
        </a>
      </p>
    </td>
  </tr>
</table>

<div align="center">
  <img src="https://i.imgur.com/3Vbzw56.png" />
</div>
