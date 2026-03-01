"""Small Gradio UI entrypoint for the financial research tool.

This module exposes a minimal Gradio-based user interface that
accepts a research query and optional recipient email, runs the
project's research pipeline and streams progress updates to the
interface. The `run_research` coroutine bridges the pipeline's
asynchronous generator with Gradio's callback mechanism.
"""

import gradio as gr

from src.core.logging_config import setup_logging
from src.services.report_manager import ReportManager


async def run_research(query: str, email: str, max_sources: int = 3):
    """Bridge between Gradio inputs and the research pipeline.

    This coroutine validates the `query` input and then consumes the
    asynchronous generator returned by `ReportManager.execute`, yielding
    each progress block so Gradio can display live updates.

    Args:
        query: The user's research query string.
        email: Optional recipient email address.
        max_sources: Maximum number of sources the planner should return.

    Yields:
        Strings representing progress updates or the final report.
    """
    if not query.strip():
        yield "⚠️ Please enter a research query."
        return

    async for block in ReportManager.execute(query, email, max_sources):
        yield block


def main():
    """Create and launch the Gradio UI.

    The UI presents inputs for query, optional email and source count,
    and wires the `run_research` coroutine to a button click handler.
    """
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="emerald")) as ui:
        gr.Markdown("F📊 Financial Researcher Tool")
        gr.Markdown(
            "Leverage AI Agents to perform deep market research and receive reports via email."
        )

        with gr.Column():
            with gr.Row():
                email_input = gr.Textbox(
                    label="Email Address (Optional)",
                    placeholder="Receive the HTML Report",
                    scale=3,
                )

                source_count = gr.Slider(
                    minimum=1,
                    maximum=10,
                    value=3,
                    step=1,
                    label="Max Sources to Research",
                    scale=1,
                    interactive=True,
                )

            with gr.Row():
                query_textbox = gr.Textbox(
                    label="Enter your Financial Research Query...",
                    placeholder="e.g., Analysis of NVIDIA stock performance vs competitors in 2025",
                )

        run_btn = gr.Button("🚀 Run Research Pipeline", variant="primary", scale=3)
        output_display = gr.Markdown(label="Execution Logs & Final Report")

        inputs = [query_textbox, email_input, source_count]
        run_btn.click(fn=run_research, inputs=inputs, outputs=output_display)

    ui.launch(inbrowser=True)


if __name__ == "__main__":
    setup_logging()
    main()
