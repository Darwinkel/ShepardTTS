"""Tests to make sure Gradio works correctly."""

import gradio as gr
import requests
from fastapi import FastAPI

from shepardtts import app_helpers


def test_gradio_launches() -> None:
    """Checks if Gradio boots, does not publish any shared link, and results in a protected page."""
    with gr.Blocks(analytics_enabled=False) as demo, gr.Row():
        with gr.Column():
            gr.Markdown(app_helpers.description)
        with gr.Column():
            gr.Markdown(app_helpers.links)

    demo.queue(max_size=10)
    app, local_url, share_url = demo.launch(debug=False, show_api=True, share=False, auth=("shepard", "test"), prevent_thread_lock=True)
    page = requests.get(local_url, timeout=3)

    assert isinstance(app, FastAPI)
    assert share_url is None
    assert '"auth_required":true' in page.text

