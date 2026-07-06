# 🏛️ CivicIntel Dashboard
**AI-Driven Municipal Triage & Workflow Automation Platform**

CivicIntel is a smart-city grievance reporting dashboard designed to modernize how municipal governments ingest, categorize, and route citizen reports. By leveraging lightweight multimodal LLMs and MLOps cost-saving techniques, CivicIntel instantly transforms messy citizen complaints (text and images) into structured, actionable data for city dispatchers.

---

## 🚀 Key Features

*   **Multimodal AI Inference:** Utilizes Google's `gemini-2.5-flash-lite` to analyze both textual descriptions and visual evidence (images) of infrastructure issues.
*   **Cost-Optimized Semantic Caching:** Implements a mock semantic cache layer that intercepts duplicate/known issues (e.g., a reported pothole), bypassing the LLM entirely to save API compute costs and reduce latency by 95%.
*   **Automated Geospatial Mapping:** The AI acts as a geospatial engine, extracting contextual location data from citizen text and automatically projecting it onto a dynamic coordinate map (with strict hallucination safeguards).
*   **Intelligent Routing & Triage:** Automatically assigns an issue to the correct municipal department (e.g., Sanitation, Water Management, Public Works) and calculates a severity matrix (Low, Medium, High).
*   **Executive Document Generation:** Compiles the structured JSON output into an official Markdown Dispatch Brief, ready for one-click download by field crews.
*   **Real-Time Telemetry:** Features a custom CSS enterprise-grade UI that displays active pipeline latency, compute status, and token processing metrics.

---
## 💻 Local Setup & Installation

Follow these steps to run the CivicIntel Dashboard locally on your machine.

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

> **Optional:** If you use `uv`, you can install the dependencies using:
>
> ```bash
> uv pip install -r requirements.txt
> ```

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

| Scenario | Sample Input | Expected Outcome |
|----------|--------------|------------------|
| **Standard Multimodal Report** | *"A transformer just blew out near the main entrance of the academic block. There are live sparks falling near the pedestrian walkway."* | Routes the complaint to **Utilities → Electrical**, assigns **High** severity, maps the location, and generates an official incident brief. |
| **MLOps Semantic Cache Hit** | *"I need to report a severe pothole on main crossroad."* | Detects a semantically similar complaint, bypasses LLM inference, reduces API cost to **$0**, returns the response in **< 0.1 s**, and displays a duplicate-report notification. |

---

> 🚀 **Built for rapid municipal response, intelligent civic governance, and scalable AI-powered complaint management.**