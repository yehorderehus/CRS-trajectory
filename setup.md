## Commands for command line to run the program

**Optional: Create virtual environment with name *venv***

Windows
```sh
python -m venv venv
```
Linux, WSL
```sh
python3 -m venv venv
```

**Optional: Activate virtual environment with name *venv***

Windows
```sh
venv\Scripts\activate
```
Linux, WSL
```sh
source venv/bin/activate
```

**Install requirements (in virtual environment)**
```sh
pip3 install -r requirements.txt
```

**Run the program (default local path for the running program is http://127.0.0.1:8050/**)

Windows
```sh
python main.py
```

Linux, WSL
```sh
python3 main.py
```

**Deactivate virtual environment (if needed)**
```sh
deactivate
```
