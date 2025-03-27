import os
import asyncio
from flask import Flask, request, jsonify
from waitress import serve as waitress_serve

from .controllers.go_to_page import go_to_page as go_to_page_controller, ViewportSize

app = Flask(__name__)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok"})

@app.route('/health')
def root_health_check():
    """Root health check endpoint for Fly.io"""
    return jsonify({"status": "ok"})

@app.route('/api/go-to-url')
def go_to_url():
    """Visit a URL using Playwright"""
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400
    
    viewport_str = request.args.get('vp')
    viewport: ViewportSize | None = None
    if viewport_str:
        width, height = viewport_str.split('x')
        viewport = {"width": int(width), "height": int(height)}
        
    user_agent = request.args.get('ua')
    
    timeout_str = request.args.get('timeout')
    timeout = 10000
    
    trace_str = request.args.get('trace')
    trace = True
    if trace_str:
        trace = trace_str.lower() == 'true'
        
    if timeout_str:
        timeout = int(timeout_str)
    async def _go_to_page_controller():
        return await go_to_page_controller(
            url,
            headless=True,
            trace=trace,
            viewport=viewport,
            user_agent=user_agent,
            timeout=timeout,
        )
            
    
    # Use asyncio.run to run the async controller
    result = asyncio.run(_go_to_page_controller())
    
    return jsonify(result), 200 if result["success"] else 500


@app.route('/api/get-trace')
def get_trace():
    """Get the trace file"""
    try:
        with open('trace.zip', 'rb') as f:
            return f.read(), 200, {'Content-Type': 'application/zip'}
    except FileNotFoundError:
        return jsonify({"error": "Trace file not found"}), 404

def serve():
    """Start the waitress server for production"""
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting server on port {port}...")
    waitress_serve(app, host='0.0.0.0', port=port)

if __name__ == "__main__":
    serve()