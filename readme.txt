Milestones Project Quick Start
=============================

1. Clone the repository:
   git clone https://github.com/Speech-Summarizer-Application-IF-SB/Sonal-Verma.git
   cd Sonal-Verma

2. Create and activate a virtual environment:
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1   # (Windows PowerShell)
   # For macOS/Linux: source .venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Change to your desired milestone folder:
   cd milestone_1   # or cd milestone_2

5. Run the scripts as needed:
   python audio_cleaner.py          # For milestone_1
   python usingfilemodel.py         # For milestone_2
   python realtimemodel.py          # For milestone_2
   python report.py                 # For milestone_2

Notes:
- Make sure you have Python 3.x installed.
- For audio/video features, ffmpeg may be required and should be in your system PATH.
