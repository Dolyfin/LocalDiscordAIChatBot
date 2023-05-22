IF NOT EXIST venv (
    echo <!> Creating virtual environment...
    python -m venv venv
)

venv\Scripts\activate

echo <!> Installing required packages...
pip install -r requirements.txt

echo <!> Starting the bot...
python main.py