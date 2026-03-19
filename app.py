import gradio as gr
    import httpx
    import os
    
    OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY", "")
    
    async def check_grammar(text):
        if not text.strip():
            return "Please enter some text to check.", ""
        
        if not OPENROUTER_KEY:
            return "API key not configured.", ""
        
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "google/gemma-3-27b-it:free",
                        "messages": [
                            {"role": "system", "content": "You are a professional grammar checker. Analyze the input text and provide: 1) A corrected version of the text with all grammar, spelling, and punctuation errors fixed. 2) A detailed list of all errors found with explanations. Be thorough and helpful."},
                            {"role": "user", "content": f"Check and correct this text:\n\n{text}"}
                        ],
                        "max_tokens": 2048
                    },
                    timeout=30
                )
                
                if resp.status_code == 200:
                    result = resp.json()["choices"][0]["message"]["content"]
                    lines = result.split("\n")
                    corrected = ""
                    errors = ""
                    in_corrected = True
                    for line in lines:
                        if "error" in line.lower() and ":" in line.lower() and in_corrected:
                            in_corrected = False
                        if in_corrected:
                            corrected += line + "\n"
                        else:
                            errors += line + "\n"
                    return corrected.strip() or result, errors.strip()
                else:
                    return f"Error: {resp.status_code}", ""
        except Exception as e:
            return f"Error: {str(e)}", ""
    
    with gr.Blocks(title="AI Grammar Checker Pro", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# AI Grammar Checker Pro")
        gr.Markdown("Paste your text below and get instant grammar, spelling, and punctuation corrections.")
        
        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(label="Your Text", placeholder="Enter or paste your text here...", lines=8)
                check_btn = gr.Button("Check Grammar", variant="primary")
            with gr.Column():
                corrected_text = gr.Textbox(label="Corrected Text", lines=8, interactive=False)
                errors_list = gr.Textbox(label="Errors Found", lines=8, interactive=False)
        
        gr.Markdown("---")
        gr.Markdown("### Unlock Full Features")
        gr.Markdown("- Unlimited checks with no length limits\n- Advanced style and tone suggestions\n- Bulk document checking\n- API access for developers")
        gr.Markdown("#### Get Pro Access - $9.99")
        gr.HTML('<a href="https://nowpayments.io/payment/?iid=6136175542" target="_blank" style="display:inline-block;padding:12px 32px;background:#4CAF50;color:white;text-decoration:none;border-radius:8px;font-weight:bold;font-size:16px;">Pay with Crypto</a>')
        
        check_btn.click(fn=check_grammar, inputs=[input_text], outputs=[corrected_text, errors_list])
    
    if __name__ == "__main__":
        demo.launch()
    