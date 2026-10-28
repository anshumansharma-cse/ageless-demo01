# Ageless Demo UI

Disposable Streamlit interface for demonstrating the local Ageless FastAPI recording and playback endpoints. This is a demo UI and does not modify the Flutter app (`ageless_companion_app`).

## Current API behavior

The UI uses the following FastAPI endpoints:

- `GET /` — checks the backend connection.
- `POST /record` — records audio using the microphone on the machine running FastAPI. The UI sends `duration_seconds` in the JSON request body.
- `GET /recordings` — returns the filenames of available WAV recordings.
- `GET /recordings/{record_name}` — serves the selected WAV recording for playback.

Recordings are saved locally in `ageless_audio/audio_file/`. The Streamlit UI fetches the available filenames and lets you select and play a recording using the audio player.

## Run locally

Start the FastAPI backend in a terminal using your current backend command. With the current configuration, the server listens at:

`http://127.0.0.1:8090`

In another terminal, open the demo UI directory and run:

```bash
uv sync
uv run streamlit run app.py
```

Open the local URL printed by Streamlit (typically `http://localhost:8501`).

Use **Check connection** in the sidebar to test the backend. Select a recording duration and click **Start Recording**. Once recording completes, select the saved WAV from **Saved recordings** to play it.

## Configure the API URL

Default: `http://127.0.0.1:8090`. You can change it in the sidebar or set the environment variable before launch:

```bash
AGELESS_API_BASE=http://127.0.0.1:8090 uv run streamlit run app.py
```

## Current limitations

- Audio is captured by the microphone on the machine running FastAPI, not the browser.
- Recording requests are synchronous; the UI waits for the recording to finish.
- Recordings are stored locally and served by the development backend.
- This demo does not yet include STT, TTS, an LLM, SER, or conversational processing.
- Keeps the backend and Streamlit development server local; do not expose them to untrusted networks.
