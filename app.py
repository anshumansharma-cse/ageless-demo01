"""Disposable Streamlit demo UI for the existing Ageless FastAPI backend.

This UI intentionally does not modify or duplicate the backend recorder.
With the current API, GET /record calls record() and asks for the recording
length in the FastAPI process's terminal. The duration selector below is
therefore a preview/future UI control only; it is not sent to the recorder yet.
"""

from __future__ import annotations

import os
import time
from datetime import datetime
from typing import Any

import requests
import streamlit as st

DEFAULT_API_BASE = os.getenv("AGELESS_API_BASE", "http://127.0.0.1:8090").rstrip("/")
REQUEST_TIMEOUT_SECONDS = 180

st.set_page_config(
    page_title="Ageless Companion · Demo",
    page_icon="🎙️",
    layout="centered",
)

st.markdown(
    """
    <style>
      .block-container { max-width: 820px; padding-top: 2.2rem; }
      .ageless-subtitle { color: #8b8b8b; margin-top: -0.6rem; }
      div[data-testid="stMetric"] { border: 1px solid rgba(128,128,128,.25); padding: 1rem; border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎙️ AGELESS")
st.markdown('<p class="ageless-subtitle">Voice companion · Local backend demo</p>', unsafe_allow_html=True)
st.write("A temporary interface for demonstrating the existing local recording endpoint.")

with st.sidebar:
    st.header("Backend connection")
    api_base = st.text_input("FastAPI base URL", value=DEFAULT_API_BASE).strip().rstrip("/")
    st.caption("Default matches the current backend host: 127.0.0.1:8090")
    if st.button("Check connection", use_container_width=True):
        try:
            response = requests.get(f"{api_base}/", timeout=5)
            response.raise_for_status()
            st.session_state["connection_result"] = (True, f"Connected (HTTP {response.status_code})")
        except requests.RequestException as exc:
            st.session_state["connection_result"] = (False, str(exc))
    if "connection_result" in st.session_state:
        ok, message = st.session_state["connection_result"]
        (st.success if ok else st.error)(message)

st.subheader("Voice input")
duration = st.slider(
    "Planned recording duration",
    min_value=5,
    max_value=60,
    value=10,
    step=5,
    help="UI control preview only. The current backend still asks for duration in its terminal.",
)

st.info(
    "**Current API limitation:** the existing `GET /record` endpoint prompts for duration in the "
    "terminal running FastAPI. This slider is not wired to the recorder yet, because the backend "
    "endpoints are being left unchanged for this phase."
)

st.markdown("#### Start a recording")
st.write(
    "Click below to call the current endpoint. Keep the FastAPI terminal visible and enter the "
    "duration there when prompted. The browser will wait for the recording request to finish."
)

if "last_request" not in st.session_state:
    st.session_state["last_request"] = None

if st.button("🎤 Call /record", type="primary", use_container_width=True):
    started = time.monotonic()
    st.session_state["last_request"] = None
    status = st.status("Contacting FastAPI…", expanded=True)
    status.write(f"Request: `GET {api_base}/record`")
    status.write(f"Planned UI duration: {duration} seconds (not yet sent to backend)")
    try:
        status.update(label="Recording request in progress", state="running")
        response = requests.get(api_base + "/record", timeout=REQUEST_TIMEOUT_SECONDS)
        elapsed = time.monotonic() - started
        content_type = response.headers.get("content-type", "")
        try:
            payload: Any = response.json()
        except ValueError:
            payload = response.text[:2000]

        if response.ok:
            st.session_state["last_request"] = {
                "ok": True,
                "http_status": response.status_code,
                "elapsed": elapsed,
                "content_type": content_type,
                "payload": payload,
                "at": datetime.now().strftime("%H:%M:%S"),
            }
            status.update(label="Endpoint responded successfully", state="complete", expanded=False)
        else:
            st.session_state["last_request"] = {
                "ok": False,
                "http_status": response.status_code,
                "elapsed": elapsed,
                "payload": payload,
                "at": datetime.now().strftime("%H:%M:%S"),
            }
            status.update(label=f"Backend returned HTTP {response.status_code}", state="error")
    except requests.Timeout:
        status.update(label="Request timed out", state="error")
        st.session_state["last_request"] = {
            "ok": False,
            "error": f"No response within {REQUEST_TIMEOUT_SECONDS} seconds. The recording may still be running in the backend process.",
            "at": datetime.now().strftime("%H:%M:%S"),
        }
    except requests.RequestException as exc:
        status.update(label="Could not reach FastAPI", state="error")
        st.session_state["last_request"] = {
            "ok": False,
            "error": str(exc),
            "at": datetime.now().strftime("%H:%M:%S"),
        }

result = st.session_state.get("last_request")
if result:
    st.divider()
    st.subheader("Latest request")
    if result.get("ok"):
        st.success("FastAPI returned a successful HTTP response.")
    else:
        st.error("The request did not complete successfully.")

    col1, col2 = st.columns(2)
    col1.metric("HTTP status", str(result.get("http_status", "—")))
    col2.metric("Elapsed", f"{result.get('elapsed', 0):.1f}s" if "elapsed" in result else "—")

    if "payload" in result:
        st.caption("Response body")
        if isinstance(result["payload"], (dict, list)):
            st.json(result["payload"])
        else:
            st.code(str(result["payload"]) or "(empty response)")
    if result.get("error"):
        st.code(result["error"])
    st.caption(f"Last attempted at {result.get('at', '—')}")

st.divider()
st.subheader("Next integration step")
st.write(
    "The current endpoint does not return a recording path or audio bytes, so this UI cannot yet "
    "confirm the saved WAV or play it in the browser. Once the API is updated, we can add those "
    "features without changing the overall UI structure."
)
st.caption("Local prototype · Do not expose this development server to an untrusted network.")
