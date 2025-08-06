from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
from modules.analyzer.event_logger import ALL_SESSIONS_CSV_PATH # Import the global CSV path

app = Flask(__name__)
CURRENT_SESSION_ID = None # Will be set by main.py to default to the current session

@app.route('/')
def index():
    """Serve a página principal do dashboard."""
    return render_template('index.html')

@app.route('/api/sessions')
def get_sessions():
    """Retorna uma lista de todos os session_ids únicos no CSV."""
    if not os.path.exists(ALL_SESSIONS_CSV_PATH):
        return jsonify([]), 200 # Return empty list if file doesn't exist yet
    
    try:
        df = pd.read_csv(ALL_SESSIONS_CSV_PATH)
        sessions = df['session_id'].unique().tolist()
        return jsonify(sessions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/events')
def get_events():
    """Retorna os dados de eventos do CSV como JSON, filtrados por session_id."""
    session_id = request.args.get('session_id')

    if not os.path.exists(ALL_SESSIONS_CSV_PATH):
        return jsonify([]), 200 # Return empty list if file doesn't exist yet
    
    try:
        df = pd.read_csv(ALL_SESSIONS_CSV_PATH)
        
        if session_id:
            df_filtered = df[df['session_id'] == session_id]
        else:
            # If no session_id is provided, return data for the most recent session
            if not df.empty:
                latest_session_id = df['session_id'].iloc[-1] # Assumes last entry is from latest session
                df_filtered = df[df['session_id'] == latest_session_id]
            else:
                df_filtered = pd.DataFrame() # Empty dataframe

        return jsonify(df_filtered.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_dashboard_server(current_session_id):
    """Função para iniciar o servidor Flask."""
    global CURRENT_SESSION_ID
    CURRENT_SESSION_ID = current_session_id
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    # Example of how to run the server directly for testing
    # In production, it will be called by main.py
    print("Para testar o servidor, defina CURRENT_SESSION_ID antes de chamar run_dashboard_server.")
    print("Ex: run_dashboard_server('test_session_123')")
    # Ensure the reports directory exists for testing
    if not os.path.exists('reports'):
        os.makedirs('reports')
    # Create a dummy CSV for testing
    with open(ALL_SESSIONS_CSV_PATH, 'w', newline='') as f:
        import csv
        writer = csv.writer(f)
        writer.writerow(['session_id', 'timestamp', 'event_type', 'metric_value'])
        writer.writerow(['test_session_1', time.time(), 'olhos', 0.1])
        writer.writerow(['test_session_1', time.time() + 5, 'bocejo', 0.6])
        writer.writerow(['test_session_2', time.time() + 10, 'olhos', 0.15])
    run_dashboard_server('test_session_1')