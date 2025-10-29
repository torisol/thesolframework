"""Simple Gradio app for interacting with the T5-small model."""

from __future__ import annotations

import argparse
from typing import Any

import gradio as gr
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

MODEL_NAME = "t5-small"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def generate_completion(
    prompt: str,
    max_new_tokens: int = 64,
    temperature: float = 1.0,
    top_p: float = 0.9,
    num_beams: int = 1,
) -> str:
    """Generate text from the model given a prompt."""
    cleaned_prompt = prompt.strip()
    if not cleaned_prompt:
        return "Please enter a prompt to generate text."

    inputs = tokenizer(cleaned_prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=num_beams == 1,
        temperature=temperature,
        top_p=top_p,
        num_beams=num_beams,
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def build_interface() -> gr.Blocks:
    with gr.Blocks(title="T5-small Prompt Playground") as demo:
        gr.Markdown(
            """
            # T5-small Prompt Playground
            Type in a prompt and select **Generate** to see how the
            [T5-small](https://huggingface.co/t5-small) model responds.
            """
        )

        with gr.Row():
            prompt = gr.Textbox(
                label="Prompt",
                lines=6,
                placeholder="e.g. translate English to German: How are you today?",
            )

        with gr.Row():
            max_new_tokens = gr.Slider(
                minimum=8,
                maximum=256,
                value=64,
                step=8,
                label="Max new tokens",
                info="Length of the generated text",
            )
            temperature = gr.Slider(
                minimum=0.1,
                maximum=2.0,
                value=1.0,
                step=0.1,
                label="Temperature",
                info="Higher values increase randomness",
            )
        with gr.Row():
            top_p = gr.Slider(
                minimum=0.1,
                maximum=1.0,
                value=0.9,
                step=0.05,
                label="Top-p",
                info="Cumulative probability for nucleus sampling",
            )
            num_beams = gr.Slider(
                minimum=1,
                maximum=4,
                value=1,
                step=1,
                label="Beams",
                info="Set above 1 to use beam search instead of sampling",
            )

        generate_btn = gr.Button("Generate")
        output = gr.Textbox(label="Model output", lines=8)

        generate_btn.click(
            fn=generate_completion,
            inputs=[prompt, max_new_tokens, temperature, top_p, num_beams],
            outputs=output,
        )

        gr.Examples(
            examples=[
                "translate English to German: That is a wonderful idea!",
                "summarize: The Sol Framework describes...",
                "answer the following question: What is the capital of France?",
            ],
            inputs=prompt,
        )

    return demo


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Launch the T5-small Gradio demo.")
    parser.add_argument(
        "--share",
        action="store_true",
        help=(
            "Create a temporary public Gradio link. Useful when running in Colab or "
            "accessing the UI from another device such as a phone."
        ),
    )
    parser.add_argument(
        "--server-name",
        default=None,
        help=(
            "Hostname to bind the server to. Use 0.0.0.0 to listen on all interfaces "
            "(required when tunneling from mobile devices)."
        ),
    )
    parser.add_argument(
        "--server-port",
        type=int,
        default=None,
        help="Port to bind the server to. Defaults to Gradio's automatic selection.",
    )
    return parser.parse_args()


def main() -> None:
    demo = build_interface()
    args = parse_args()
    launch_kwargs: dict[str, Any] = {}
    if args.share:
        launch_kwargs["share"] = True
    if args.server_name:
        launch_kwargs["server_name"] = args.server_name
    if args.server_port:
        launch_kwargs["server_port"] = args.server_port
    demo.launch(**launch_kwargs)


if __name__ == "__main__":
    main()
