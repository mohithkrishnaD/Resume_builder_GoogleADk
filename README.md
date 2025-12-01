# AI-Powered Resume Optimizer

An intelligent resume analysis and optimization tool built with Google's Agent Development Kit (ADK). This application helps job seekers improve their resumes by analyzing them against job descriptions and providing actionable recommendations.

## ✨ Features

- **Resume Parsing**: Extract and analyze content from PDF  resumes
- **Job Description Analysis**: Compare your skills against job requirements
- **Skill Gap Analysis**: Identify missing skills for your target roles
- **Personalized Recommendations**: Get tailored suggestions to improve your resume
- **AI-Powered Insights**: Leverage Google's AI for in-depth analysis

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Google Cloud Project with ADK access
- Required Python packages (see `requirements.txt`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/resume-builder-google-adk.git
   cd resume-builder-google-adk
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables in `.env`:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   GOOGLE_CLOUD_PROJECT=your-project-id
   ```

## 🛠 Usage

Run the application:
```bash
python main.py
```

### Example Query
```
Please analyze my resume and compare it with this job description.

Resume: /path/to/your/resume.pdf

Job Description:
[Paste job description here]
```

## 🤖 Agents

The application uses specialized agents for different tasks:
- **Coordinator Agent**: Manages the analysis workflow
- **Resume Parser**: Extracts and processes resume content
- **Job Analyzer**: Analyzes job descriptions
- **Skill Gap Analyzer**: Identifies skill gaps
- **Recommendation Engine**: Suggests improvements

## 📁 Project Structure

```
.
├── agents/               # Agent implementations
├── tools/                # Utility functions and tools
├── main.py               # Application entry point
├── config.py             # Configuration settings
└── requirements.txt      # Project dependencies
```


## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Key
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 3. Run via ADK Web
```bash
adk web .
# Opens: http://localhost:8000
```

### 4. Or Run via Streamlit
```bash
streamlit run app.py
```

## 💡 How It Works

### Architecture

```
User Resume (PDF)
        ↓
Resume Parser Agent
        ↓
Extract: Contact, Skills, Experience, Education
        ↓
Job Description (Text)
        ↓
Job Analyzer Agent
        ↓
Extract: Required Skills, Responsibilities, Experience Level
        ↓
Skill Gap Agent
        ↓
Calculate: Missing Skills, Similarity Score
        ↓
Recommendation Agent (Gemini AI)
        ↓
Generate: Tailored Resume Sections, Cover Letter, Learning Resources
        ↓
User Gets: Actionable Recommendations
```

### Key Agents

1. **Resume Parser Agent**
   - Extracts text from resume files
   - Parses contact information
   - Identifies resume sections
   - Extracts skills and experience

2. **Job Analyzer Agent**
   - Parses job descriptions
   - Identifies required skills
   - Extracts experience requirements

3. **Skill Gap Agent**
   - Compares resume skills vs job requirements
   - Calculates TF-IDF similarity scores
   - Identifies skill gaps

4. **Recommendation Agent**
   - Uses Gemini AI to generate tailored suggestions
   - Creates optimized resume sections
   - Generates cover letters
   - Suggests learning resources

5. **Coordinator Agent**
   - Orchestrates all agents
   - Manages data flow
   - Provides unified interface


## 🔑 Key Features

### ✅ Multi-Format Support
- PDF resumes
- Text job descriptions

### ✅ AI-Powered Analysis
- Uses Google Gemini for intelligent recommendations
- Context-aware suggestions
- Personalized learning paths

### ✅ Web Interface
- Interactive ADK Web UI
- Real-time analysis
- Download recommendations

### ✅ Scalable Architecture
- Multi-agent system
- Modular design
- Easy to extend

## 🎯 Use Cases

1. **Job Seekers**: Optimize resume for target positions
2. **Career Changers**: Identify required skills to learn
3. **Recruiters**: Find skill gaps in candidates
4. **Students**: Prepare resumes for internships

## 📦 Dependencies

See `requirements.txt` for full list:
- google-genai
- google-cloud-generative-ai (for Vertex AI)
- python-docx
- PyPDF2
- scikit-learn
- streamlit (optional)

## 🔧 Configuration

Update `config.py`:

```python
class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-2.5-flash"
    APP_NAME = "Resume Optimizer"
    MAX_RESUME_LENGTH = 5000
    MIN_SKILLS_TO_EXTRACT = 3
```



## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Google's Agent Development Kit (ADK)
- Powered by Google's Generative AI

---

💡 **Tip**: For best results, ensure your resume is in PDF  format and includes relevant skills and experiences.