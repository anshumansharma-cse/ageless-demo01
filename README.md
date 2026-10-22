# Ageless Demo UI

Disposable Streamlit interface for demonstrating the existing local Ageless FastAPI recording endpoint. This project intentionally does not modify `ageless-backend`, `ageless_audio/recorder.py`, or the Flutter app (`ageless_companion_app`).

## Current API behavior

The existing backend exposes `GET /record`, which calls the recorder and prompts for recording duration in the terminal running FastAPI. This UI calls that endpoint as-is. The duration slider is only a preview/future UI control; its value is **not** sent to the backend yet.

The current endpoint also does not return a WAV path or audio bytes, so browser playback and confirmation of the saved file are intentionally deferred until the API contract is updated.

## Run locally

Open a terminal in the backend directory and start the existing API using your current command. With the code currently shared, the server listens at `http://127.0.0.1:8090`.

In another terminal:

```bash
cd ageless-demo
uv sync
uv run streamlit run app.py
```

Open the local URL printed by Streamlit (typically `http://localhost:8501`). Click **Check connection** to test the root endpoint. To trigger the current recording endpoint, click **Call /record**, then enter the recording duration in the FastAPI terminal when prompted.

## Configure the API URL

Default: `http://127.0.0.1:8090`. You can change it in the sidebar or set the environment variable before launch:

```bash
AGELESS_API_BASE=http://127.0.0.1:8090 uv run streamlit run app.py
```

## Deliberate limitations in this phase

- No changes to the backend or recorder.
- Duration is not passed from the UI yet.
- No WAV retrieval or playback until the API exposes the recording result.
- The UI makes a synchronous request and waits for it to finish.
