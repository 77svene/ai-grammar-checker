import gradio as gr
    import httpx
    import os
    
    API_KEY = os.environ.get("OPENROUTER_KEY", "")
    
    USAGE_LIMIT = 10
    usage_count = {"value": 0}
    
    async def check_grammar(text):
        if not text.strip():
            return "Please enter some text to check."
        
        if usage_count["value"] >= USAGE_LIMIT:
            return "Daily free limit reached (10 checks). Come back tomorrow for more free checks, or try our other free tools at huggingface.co/spaces/orama-ai"
        
        usage_count["value"] += 1
        
        try:
            async with httpx.AsyncClient() as c:
                resp = await c.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                    json={
                        "model": "google/gemini-2.0-flash-001",
                        "messages": [
                            {"role": "system", "content": "You are a grammar checker. Fix all grammar, spelling, and punctuation errors in the user\'s text. Return ONLY the corrected text, nothing else. If no errors found, return the original text."},
                            {"role": "user", "content": text}
                        ],
                        "max_tokens": 2000
                    },
                    timeout=30
                )
                if resp.status_code == 200:
                    corrected = resp.json()["choices"][0]["message"]["content"]
                    return corrected
                else:
                    return f"API error: {resp.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    with gr.Blocks(title="Free AI Grammar Checker", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# Free AI Grammar Checker")
        gr.Markdown("Fix grammar, spelling, and punctuation mistakes in 1 click. No signup required.")
        gr.Markdown(f"**Free: {USAGE_LIMIT} checks per session**")
        
        with gr.Row():
            input_text = gr.Textbox(label="Your text", placeholder="Paste your text here...", lines=6)
            output_text = gr.Textbox(label="Corrected text", lines=6)
        
        check_btn = gr.Button("Check Grammar", variant="primary")
        check_btn.click(fn=check_grammar, inputs=input_text, outputs=output_text)
        
        gr.Markdown("---")
        gr.Markdown("More free AI tools: [Paraphrase Pro](https://huggingface.co/spaces/orama-ai/ai-paraphrase-pro) | [Sentence Rewriter](https://huggingface.co/spaces/orama-ai/ai-sentence-rewriter) | [Code Review](https://huggingface.co/spaces/orama-ai/ai-code-review-pro)")
    
    if __name__ == "__main__":
        demo.launch()
    