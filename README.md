# Group 5: Automata Simulator

## Project Structure
Ensure all files are in the same directory before running:
* `app.py` (The main Streamlit application code)
* `requirements.txt` (Python dependencies)
* `PDA-Reg1.drawio.png` (Static PDA flowchart for Regex 1)
* `PDA-Reg2.drawio.png` (Static PDA flowchart for Regex 2)

---

## ⚙️ Installation & Setup

### Step 1: Install System Requirements (Graphviz)
Because this app generates dynamic state-machine graphics, your computer must have the open-source Graphviz software installed.
* **Windows:** Download and install from [graphviz.org/download](https://graphviz.org/download/). **Crucial:** During installation, make sure to check the box that says *"Add Graphviz to the system PATH for all users"*.
* **Mac:** Open terminal and run `brew install graphviz`
* **Linux:** Open terminal and run `sudo apt-get install graphviz`

### Step 2: Install Python Dependencies
Open your terminal/command prompt, navigate to the folder containing this project, and run:
```bash
pip install -r requirements.txt