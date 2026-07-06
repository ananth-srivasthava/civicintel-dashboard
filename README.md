# 🏛️ CivicIntel Dashboard

**Autonomous Municipal Triage & Workflow Automation Platform**

CivicIntel is a smart-city grievance reporting dashboard designed to modernize how municipal governments ingest, categorize, and route citizen reports. By leveraging an autonomous agentic workflow, multimodal LLMs, and real-time geocoding, CivicIntel instantly transforms messy, unstructured citizen complaints (text and images) into structured, actionable data for city dispatchers.

---

## 🚀 Key Features

- **Autonomous Agentic Workflow:** Eliminates manual drop-downs and spoon-feeding. Citizens provide a raw, unstructured description, and the AI agent autonomously extracts the issue category, severity matrix, and local context.

- **Real-Time Geocoding Integration:** Offloads coordinate hallucination risks from the LLM. The AI extracts a highly specific location string, which is dynamically passed to the **OpenStreetMap (Nominatim) API** to plot database-verified map coordinates.

- **Localized Department Routing:** Injects dynamic regional context (State/UT and District) into the AI prompt, allowing the system to accurately assign issues to the appropriate local municipal agency or utility board anywhere in India.

- **Dynamic Model Routing (MLOps):** Seamlessly switch between inference engines (`gemini-2.5-flash`, `gemini-1.5-flash`, and `gemini-2.5-pro`) directly from the UI to compare extraction quality, latency, and token economy.

- **Cost-Optimized Semantic Caching:** Implements a mock semantic cache layer that intercepts duplicate or previously known issues (e.g., a known pothole report), bypassing the LLM entirely to reduce API costs and latency.

- **Executive Document Generation:** Compiles the structured JSON output into an official Markdown or Text Dispatch Brief, ready for one-click download.

---

## 💻 Local Setup & Installation

Follow these steps to run the CivicIntel Dashboard locally.

### 1. Clone the Repository

```bash
git clone https://github.com/ananth-srivasthava/civicintel-dashboard.git
cd civicintel-dashboard
```

### 2. Install Dependencies

Ensure you have **Python 3.9+** installed.

```bash
pip install -r requirements.txt
```

**Optional:** If you use `uv`, install the dependencies using:

```bash
uv pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root and add your Google Gemini API key.

```env
GEMINI_API_KEY="your_api_key_here"
```

### 4. Run the Application

Launch the Streamlit server:

```bash
streamlit run frontend/app.py
```

The dashboard will automatically open in your browser at:

**http://localhost:8501**

---

## 🧪 Demo Scenarios

### 1. Agentic Geocoding & Routing

**Input**

> "There is a transformer blast right next to St. Joseph's Degree College on Sunkesula Road."

**Expected Result**

- Assigns **High** severity.
- Extracts the location string for **OpenStreetMap (Nominatim)** geocoding.
- Plots the exact map location.
- Routes the complaint to the appropriate State Electricity Board.

---

### 2. MLOps Semantic Cache Hit

**Input**

> "I need to report a severe pothole on main crossroad."

**Expected Result**

- Detects a semantically similar complaint.
- Bypasses LLM inference.
- Reduces API compute cost to **$0**.
- Returns the response in **< 0.1 s**.
- Displays a duplicate-report notification.

---

> 🚀 **Built for rapid municipal response and scalable AI-powered civic infrastructure management.**