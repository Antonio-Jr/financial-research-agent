"""Gradio UI entrypoint for the Financial Research Agent.

This module provides a small Gradio-based interface that accepts a
research query, optional recipient email and a maximum source count.
It composes a list of pipeline `tasks`, constructs a `ReportManager`
with a fresh `ResearchPipeline` and streams progress messages back to
the UI as the pipeline executes.

Important behaviour notes:
- The `tasks_catalog` explicitly includes an `EmailSenderTask` entry.
    The task itself is responsible for deciding whether to run (it may
    skip execution if no recipient is present in the context). Thus the
    manager is explicit about which tasks to run while allowing tasks to
    be conditional.
"""

import gradio as gr

from src.core.logging_config import setup_logging
from src.core.pipeline import ResearchPipeline
from src.services.report_manager import ReportManager
from src.services.tasks.email_sender import EmailSenderTask
from src.services.tasks.report_generator import ReportGeneratorTask
from src.services.tasks.search_planner import SearchPlannerTask
from src.services.tasks.web_searcher import WebSearcherTask


async def run_research(query: str, email: str, max_sources: int = 3):
    """Bridge between Gradio inputs and the research pipeline.

    This coroutine validates the `query` input, assembles the ordered
    `tasks_catalog` and constructs a `ReportManager` (dependency-injected
    with a new `ResearchPipeline`). It then consumes the asynchronous
    generator returned by `ReportManager.execute`, yielding each block
    so Gradio can display live progress and the final markdown report.

    The `EmailSenderTask` is included in `tasks_catalog`, but the task
    will skip sending if no recipient email is provided. This keeps the
    UI simple while ensuring task-level control of side-effects.

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

    tasks_catalog = [
        SearchPlannerTask(),
        WebSearcherTask(),
        ReportGeneratorTask(),
        EmailSenderTask(),
    ]

    manager = ReportManager(pipeline=ResearchPipeline(), tasks=tasks_catalog)

    async for block in manager.execute(query, email, max_sources):
        yield block


def main():
    """Create and launch the Gradio UI.

    The UI presents inputs for query, optional email and source count,
    and wires the `run_research` coroutine to a button click handler.
    """
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="emerald")) as ui:
        gr.Markdown("F📊 Financial Researcher Tool")
        gr.Markdown("Leverage AI Agents to perform deep market research and receive reports via email.")

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


if __name__ == "__main__":  # pragma: no cover
    setup_logging()
    main()
