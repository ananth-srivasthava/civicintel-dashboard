---

## 💻 Local Setup & Installation

Follow these steps to run the CivicIntel Dashboard on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/ananth-srivasthava/civicintel-dashboard.git
cd civicintel-dashboard
```

### 2. Install Dependencies

Ensure you have **Python 3.9 or later** installed.

Install all required packages:

```bash
pip install -r requirements.txt
```

**Optional (using `uv`):**

```bash
uv pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY="your_api_key_here"
```

> Replace `your_api_key_here` with your Google Gemini API key.

### 4. Launch the Dashboard

Run the Streamlit application:

```bash
streamlit run frontend/app.py
```

Once started, open your browser and navigate to:

**http://localhost:8501**

---

## 🧪 Demo Scenarios

| Scenario | Sample Input | Expected Outcome |
|----------|--------------|------------------|
| ⚡ **Agentic Geocoding & Department Routing** | *"There is a transformer blast right next to St. Joseph's Degree College on Sunkesula Road."* | The AI extracts the precise location, retrieves verified coordinates using **OpenStreetMap (Nominatim)**, assigns **High** severity, and routes the complaint to the appropriate State Electricity Board. |
| 🚧 **Semantic Cache Hit (Cost Optimization)** | *"I need to report a severe pothole on main crossroad."* | Detects a previously known complaint, bypasses LLM inference, reduces API cost to **$0**, returns results in **< 0.1 seconds**, and displays a duplicate-report notification. |
| 📝 **Automatic Dispatch Brief** | Any supported complaint | Generates a structured municipal incident report in **Markdown** or **Text** format, ready for download and field deployment. |

---

## 🏗️ Tech Stack

| Layer | Technologies |
|-------|--------------|
| **Frontend** | Streamlit |
| **LLM Models** | Google Gemini 2.5 Flash, Gemini 1.5 Flash, Gemini 2.5 Pro |
| **Mapping** | OpenStreetMap (Nominatim API) |
| **Language** | Python |
| **Document Generation** | Markdown, TXT |
| **Caching** | Semantic Cache (Mock MLOps Layer) |

---

## 🎯 Project Highlights

- 🤖 Autonomous AI-powered municipal complaint triage
- 🗺️ Real-time geocoding using OpenStreetMap
- 🏢 Intelligent department routing across Indian municipalities
- ⚡ Dynamic Gemini model selection
- 💰 Semantic caching for cost-efficient inference
- 📄 Automatic dispatch brief generation
- 🌐 Multimodal support (Text + Images)

---

> 🚀 **Built for intelligent civic governance, rapid municipal response, and scalable AI-powered public infrastructure management.**