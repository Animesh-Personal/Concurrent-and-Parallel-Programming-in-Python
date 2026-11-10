# MCP Inspector for this project

MCP Inspector is a local UI for listing and calling the tools in `server.py` without going through the LangChain agent. The server hosts `get_weather` and `get_location` from `tools/tools_live.py`.

## Before you start

From the project root:

```powershell
python -m pip install -r requirements.txt
```

`get_weather` reads `OPENWEATHER_API_KEY` from the project `.env` file. `get_location` uses your public IP and does not need that key.

Inspector is a Node app. Install Node.js so `npx` is on your PATH, then run every command below from the project root.

## Connect over stdio

This is the usual way to test this server. Inspector starts `python server.py` and talks to it on stdin and stdout.

```powershell
npx -y @modelcontextprotocol/inspector python server.py
```

The terminal prints a local URL that includes a session token. Open that URL. In the Inspector UI:

1. Leave the transport on **STDIO**.
2. Confirm the command is `python` and the argument is `server.py`.
3. Click **Connect**.
4. Open **Tools**. You should see `get_location` and `get_weather`.

Call them from the Tools tab:

| Tool | Arguments | What you get back |
| --- | --- | --- |
| `get_location` | none | A string such as `Hyderabad, India` |
| `get_weather` | `city`: `Hyderabad` | JSON with the OpenWeatherMap payload and `temperature_fahrenheit` |

`get_weather` returns Celsius in `weather.main.temp` and a converted Fahrenheit value beside it. OpenWeatherMap still lists Prayagraj as `Allahabad`.

## Read a resource

Open **Resources** after connecting. These URIs are available:

| URI | What you get back |
| --- | --- |
| `location://current` | The same city and country string as `get_location` |
| `weather://Hyderabad` | The same JSON as `get_weather`. Replace `Hyderabad` with another city. |
| `weather://units` | Which fields are Celsius, and how `temperature_fahrenheit` is calculated |
| `prompt://weather-assistant` | The text of `prompts/system_prompt.txt` |
| `doc://mcp-inspector` | This guide |

`weather://{city}` is a template, so it shows under resource templates. Type the full URI, such as `weather://Hyderabad`, to read one city. `weather://units` is a fixed resource and is not a city lookup.

## Connect over HTTP

Start the server in one terminal:

```powershell
python server.py --transport streamable-http
```

It listens at `http://127.0.0.1:8000/mcp`. In a second terminal:

```powershell
npx -y @modelcontextprotocol/inspector
```

In the UI, set the transport to **Streamable HTTP**, enter `http://127.0.0.1:8000/mcp`, and click **Connect**. The same two tools are available.

`--host` and `--port` change the bind address. The path stays `/mcp`.

## SDK launcher

If both Node.js and [uv](https://docs.astral.sh/uv/) are installed, the SDK can open Inspector for you:

```powershell
mcp dev server.py
```

That command starts Inspector and a fresh uv environment, then runs this server. The direct `npx` command above uses the Python environment where you installed `requirements.txt`, which is the one that already has this project's packages and `.env`.

`mcp run server.py` starts the stdio server by itself. The process waits for a client and does not print a prompt.

## When a call fails

- **Weather lookup failed / invalid API key.** Put a real `OPENWEATHER_API_KEY` in `.env` at the project root and connect again. The server loads that file itself, so you do not paste the key into Inspector.
- **City not found.** Pass a city name OpenWeatherMap recognizes, for example `Hyderabad`. For Prayagraj, pass `Allahabad`.
- **Location lookup failed.** `get_location` calls `https://ipapi.co/json/`. A blocked network or a rate limit makes that call fail.
- **`npx` is not recognized.** Install Node.js and open a new terminal.
- **Inspector cannot connect.** Start it from the project root so `server.py` is the argument, and use the token URL printed in the terminal.
