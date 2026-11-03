# AI Agent

This project uses Python 3.11 and LangChain's OpenAI integration.

## Set up the virtual environment

In PowerShell, create a virtual environment with Python 3.11:

```powershell
py -3.11 -m venv .venv
```

If PowerShell blocks activation scripts, allow them for the current PowerShell
session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

In VS Code, select `.venv\Scripts\python.exe` as the project interpreter.

After activation, install the project dependencies and run the application:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

