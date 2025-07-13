# CodeCatcher Debug Game (Gemini Edition)

This is a Python-based GUI game that helps students debug C++ code with the help of AI-powered hints using Google's Gemini API. It's designed for educational use, where users learn by asking questions rather than being shown direct solutions.

<img width="588" height="435" alt="image" src="https://github.com/user-attachments/assets/302b60d6-8bac-4cec-998d-f049d5b49b6f" />

---

## 🔧 Requirements

Install dependencies from the included `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Ensure your Python version is **3.8+**. `tkinter` should come pre-installed with standard Python distributions.

---

## 🚀 How to Run

```bash
python codecatcher.py
```

The game will open as a window where:
- You'll be shown buggy C++ code
- You can ask questions or submit answers
- Gemini will guide you without giving direct fixes
- Score is tracked based on attempts

---

## 🌐 Internet Required

This app uses **Gemini API**, so an internet connection is required.

Make sure to insert your API key in the script:
```python
GEMINI_API_KEY = 'your-api-key-here'
```

---

## 📁 Files

- `codecatcher_gui.py` – Main application
- `requirements.txt` – Python dependencies
- `README.md` – This file

---

## 🧠 Author
Piyush Deshpande  
AI-Powered Debugging Platform | Purdue University

Happy debugging! 🔍🧑‍💻
