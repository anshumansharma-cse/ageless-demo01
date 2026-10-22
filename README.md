# Ageless Demo UI

A disposable **Streamlit frontend** for demonstrating the local Ageless Companion audio-recording backend.

This project provides a simple UI to configure recording duration, trigger microphone recording through FastAPI, and inspect the response metadata.

## Current Features

- **Backend connection check** — verifies that the FastAPI server is reachable.
- **Configurable recording duration** — select a duration between 5 and 60 seconds.
- **Microphone recording** — triggers recording on the machine running FastAPI.
- **Request status and error handling** — displays HTTP status, elapsed time, and errors.
- **Recording metadata** — displays the returned filename, saved path, duration, sample rate, and channel count.

## Architecture

```text
Streamlit UI
    |
    | POST /record
    | {"duration_seconds": 10}
    v
FastAPI Backend
    |
    v
ageless_audio.recorder.record()
    |
    v
Local Microphone
    |
    v
WAV File + Recording Metadata
```

The Streamlit UI and FastAPI backend run as separate processes. The backend handles microphone access and file creation.

## Project Setup

### Prerequisites

- Python 3.11 or a compatible version supported by the project
- `uv`
- A working microphone
- The Ageless backend and its audio dependencies configured

### 1. Start the FastAPI backend

Open a terminal in the `ageless-backend` directory:

```bash
uv run uvicorn main:app --reload --port 8090
```

The API should be available at:

- API root: `http://127.0.0.1:8090/`
- Interactive API docs: `http://127.0.0.1:8090/docs`

Keep this terminal running.

### 2. Start the Streamlit UI

Open a second terminal in `ageless-demo01`:

```bash
uv sync
uv run streamlit run app.py
```

Open the local URL printed by Streamlit, typically:

`http://localhost:8501`

### 3. Record audio

1. Use **Check connection** in the sidebar to verify the backend.
2. Select a recording duration.
3. Click **Start Recording**.
4. Speak into the microphone connected to the machine running FastAPI.
5. Inspect the HTTP status and returned recording metadata.

The saved WAV file is written to the `audio_file` directory configured by the `ageless_audio` package.

## API Contract

### `GET /`

Checks backend availability and returns basic usage information.

### `POST /record`

Starts a recording for the requested duration.

Example request:

```json
{
  "duration_seconds": 10
}
```

The backend validates the duration and returns metadata similar to:

```json
{
  "filename": "input_<timestamp>.wav",
  "path": "/path/to/audio_file/input_<timestamp>.wav",
  "duration_seconds": 10,
  "sample_rate": 44100,
  "channels": 1
}
```

The filename and path are illustrative; actual values depend on the recording.

## Configuration

The default API base URL is:

`http://127.0.0.1:8090`

It can be changed in the UI sidebar or through the `AGELESS_API_BASE` environment variable:

```bash
AGELESS_API_BASE=http://127.0.0.1:8090 \
uv run streamlit run app.py
```

If the UI and backend run on different machines, configure a reachable backend address and ensure the network and firewall permit the connection.

## Current Limitations

- The UI makes a synchronous request and waits for recording to finish.
- Browser playback of the saved WAV is not implemented yet.
- Speech-to-text (STT), text-to-speech (TTS), LLM integration, and speech emotion recognition (SER) are not part of this demo.
- The current implementation is intended for local development, not public deployment.

## Scope

This repository is a temporary demonstration interface. The main Ageless Companion repository remains responsible for the audio package, while the FastAPI backend exposes the recording operation.

The long-term Flutter application is maintained separately.

## Status

**Working:** UI-to-FastAPI integration, duration-controlled recording, WAV file creation, and recording metadata response.

**Next:** Verify saved audio and implement an endpoint for retrieving and playing the recording in the UI.
