from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
import json
import random
import time
from datetime import datetime, timedelta
import sqlite3
import threading
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'systemix-ai-secret-key-2024')
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize database
def init_db():
    conn = sqlite3.connect('systemix_ai.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Leads table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            company TEXT,
            phone TEXT,
            score INTEGER DEFAULT 0,
            status TEXT DEFAULT 'new',
            ai_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # AI Actions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_type TEXT NOT NULL,
            description TEXT,
            confidence REAL,
            status TEXT DEFAULT 'completed',
            result TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Messages table for HUDDL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            channel TEXT DEFAULT 'general',
            message TEXT NOT NULL,
            message_type TEXT DEFAULT 'text',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Workflows table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workflows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'active',
            automation_level TEXT DEFAULT 'manual',
            success_rate REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Autonomous AI Engine
class AutonomousAI:
    def __init__(self):
        self.confidence_threshold = 0.85
        self.learning_rate = 0.001
        self.neural_network_status = "active"
        self.tasks_completed = 1247
        self.success_rate = 98.7
        
    def process_lead(self, lead_data):
        """Autonomous lead processing with ML scoring"""
        # Simulate neural network processing
        time.sleep(0.1)  # Simulate processing time
        
        # AI scoring algorithm
        score = 0
        confidence = 0.0
        
        # Company size scoring
        if lead_data.get('company'):
            score += 25
            confidence += 0.2
            
        # Email domain scoring
        email = lead_data.get('email', '')
        if any(domain in email for domain in ['gmail.com', 'yahoo.com']):
            score += 10
        elif any(domain in email for domain in ['.edu', '.gov', '.org']):
            score += 30
        else:
            score += 20
            
        confidence += 0.3
        
        # Phone number scoring
        if lead_data.get('phone'):
            score += 15
            confidence += 0.2
            
        # Random AI insights
        ai_insights = [
            "High engagement potential based on industry analysis",
            "Strong conversion probability detected",
            "Recommended for immediate follow-up",
            "Matches ideal customer profile",
            "Priority lead - schedule demo within 24 hours"
        ]
        
        confidence += random.uniform(0.2, 0.3)
        confidence = min(confidence, 1.0)
        
        return {
            'score': min(score, 100),
            'confidence': round(confidence, 3),
            'ai_notes': random.choice(ai_insights),
            'recommended_action': 'schedule_demo' if score > 60 else 'nurture_sequence'
        }
    
    def optimize_workflow(self, workflow_data):
        """Autonomous workflow optimization"""
        optimizations = [
            "Reduced manual steps by 34%",
            "Automated email sequences",
            "Implemented smart routing",
            "Added predictive analytics",
            "Optimized resource allocation"
        ]
        
        return {
            'optimization': random.choice(optimizations),
            'efficiency_gain': random.randint(15, 45),
            'confidence': random.uniform(0.85, 0.98)
        }
    
    def generate_insights(self):
        """Generate AI business insights"""
        insights = [
            {
                'type': 'lead_opportunity',
                'title': 'High-Value Lead Detected',
                'description': 'AI identified 23 leads ready for immediate outreach',
                'confidence': 0.94,
                'action': 'Schedule follow-up calls'
            },
            {
                'type': 'workflow_optimization',
                'title': 'Process Improvement Opportunity',
                'description': 'Automation can save 25 hours per week',
                'confidence': 0.89,
                'action': 'Implement suggested workflow'
            },
            {
                'type': 'revenue_prediction',
                'title': 'Revenue Forecast Update',
                'description': 'Projected 18% increase based on current trends',
                'confidence': 0.92,
                'action': 'Review sales strategy'
            }
        ]
        
        return random.choice(insights)

# Initialize AI engine
ai_engine = AutonomousAI()

@app.route('/')
def dashboard():
    """Main dashboard with autonomous AI features"""
    # Get recent AI actions
    conn = sqlite3.connect('systemix_ai.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM leads')
    total_leads = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM ai_actions WHERE DATE(created_at) = DATE("now")')
    daily_actions = cursor.fetchone()[0]
    
    cursor.execute('SELECT * FROM ai_actions ORDER BY created_at DESC LIMIT 5')
    recent_actions = cursor.fetchall()
    
    conn.close()
    
    # Generate AI insights
    ai_insight = ai_engine.generate_insights()
    
    dashboard_data = {
        'total_revenue': '$2.4M',
        'revenue_change': '+18.2%',
        'active_workflows': 47,
        'automated_today': 12,
        'ai_tasks_completed': ai_engine.tasks_completed,
        'success_rate': f"{ai_engine.success_rate}%",
        'team_members': 156,
        'online_now': 8,
        'total_leads': total_leads,
        'daily_actions': daily_actions,
        'recent_actions': recent_actions,
        'ai_insight': ai_insight,
        'neural_network_status': ai_engine.neural_network_status
    }
    
    return render_template('dashboard.html', data=dashboard_data)

@app.route('/api/ai/process_lead', methods=['POST'])
def process_lead():
    """Autonomous lead processing endpoint"""
    lead_data = request.json
    
    # Process with AI
    ai_result = ai_engine.process_lead(lead_data)
    
    # Store in database
    conn = sqlite3.connect('systemix_ai.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO leads (name, email, company, phone, score, ai_notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        lead_data.get('name', ''),
        lead_data.get('email', ''),
        lead_data.get('company', ''),
        lead_data.get('phone', ''),
        ai_result['score'],
        ai_result['ai_notes']
    ))
    
    # Log AI action
    cursor.execute('''
        INSERT INTO ai_actions (action_type, description, confidence, result)
        VALUES (?, ?, ?, ?)
    ''', (
        'lead_processing',
        f"Processed lead: {lead_data.get('name', 'Unknown')}",
        ai_result['confidence'],
        f"Score: {ai_result['score']}, Action: {ai_result['recommended_action']}"
    ))
    
    conn.commit()
    conn.close()
    
    # Update AI stats
    ai_engine.tasks_completed += 1
    
    return jsonify({
        'success': True,
        'ai_result': ai_result,
        'message': 'Lead processed autonomously by AI'
    })

@app.route('/api/ai/optimize_workflow', methods=['POST'])
def optimize_workflow():
    """Autonomous workflow optimization"""
    workflow_data = request.json
    
    # AI optimization
    optimization = ai_engine.optimize_workflow(workflow_data)
    
    # Store optimization
    conn = sqlite3.connect('systemix_ai.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO ai_actions (action_type, description, confidence, result)
        VALUES (?, ?, ?, ?)
    ''', (
        'workflow_optimization',
        f"Optimized workflow: {workflow_data.get('name', 'Unknown')}",
        optimization['confidence'],
        optimization['optimization']
    ))
    
    conn.commit()
    conn.close()
    
    ai_engine.tasks_completed += 1
    
    return jsonify({
        'success': True,
        'optimization': optimization,
        'message': 'Workflow optimized autonomously'
    })

@app.route('/api/ai/status')
def ai_status():
    """Get AI engine status"""
    return jsonify({
        'status': 'active',
        'neural_networks': ai_engine.neural_network_status,
        'tasks_completed': ai_engine.tasks_completed,
        'success_rate': ai_engine.success_rate,
        'confidence_threshold': ai_engine.confidence_threshold,
        'learning_rate': ai_engine.learning_rate,
        'uptime': '99.99%',
        'last_update': datetime.now().isoformat()
    })

@app.route('/huddl')
def huddl_messenger():
    """HUDDL Team Messenger interface"""
    return render_template('huddl.html')

@app.route('/api/messages', methods=['GET', 'POST'])
def handle_messages():
    """Handle team messages"""
    if request.method == 'POST':
        message_data = request.json
        
        conn = sqlite3.connect('systemix_ai.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO messages (user_id, channel, message, message_type)
            VALUES (?, ?, ?, ?)
        ''', (
            message_data.get('user_id', 1),
            message_data.get('channel', 'general'),
            message_data.get('message', ''),
            message_data.get('type', 'text')
        ))
        
        conn.commit()
        conn.close()
        
        # Emit to all connected clients
        socketio.emit('new_message', message_data, room=message_data.get('channel', 'general'))
        
        return jsonify({'success': True})
    
    else:
        # Get messages
        channel = request.args.get('channel', 'general')
        
        conn = sqlite3.connect('systemix_ai.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM messages WHERE channel = ? 
            ORDER BY created_at DESC LIMIT 50
        ''', (channel,))
        
        messages = cursor.fetchall()
        conn.close()
        
        return jsonify({'messages': messages})

# WebSocket events for real-time features
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('status', {'msg': 'Connected to SystemIX AI'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join_channel')
def handle_join_channel(data):
    channel = data['channel']
    join_room(channel)
    emit('status', {'msg': f'Joined {channel}'})

@socketio.on('leave_channel')
def handle_leave_channel(data):
    channel = data['channel']
    leave_room(channel)
    emit('status', {'msg': f'Left {channel}'})

@socketio.on('send_message')
def handle_message(data):
    channel = data.get('channel', 'general')
    
    # Store message
    conn = sqlite3.connect('systemix_ai.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO messages (user_id, channel, message, message_type)
        VALUES (?, ?, ?, ?)
    ''', (
        data.get('user_id', 1),
        channel,
        data.get('message', ''),
        data.get('type', 'text')
    ))
    
    conn.commit()
    conn.close()
    
    # Broadcast to channel
    emit('new_message', data, room=channel)

# Background AI processing
def background_ai_processing():
    """Background thread for autonomous AI processing"""
    while True:
        try:
            # Simulate autonomous AI actions
            time.sleep(30)  # Process every 30 seconds
            
            # Generate random AI action
            actions = [
                'lead_qualification',
                'workflow_optimization', 
                'data_analysis',
                'customer_communication',
                'performance_monitoring'
            ]
            
            action = random.choice(actions)
            
            conn = sqlite3.connect('systemix_ai.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO ai_actions (action_type, description, confidence, result)
                VALUES (?, ?, ?, ?)
            ''', (
                action,
                f"Autonomous {action.replace('_', ' ')} completed",
                random.uniform(0.85, 0.99),
                "Successfully executed by AI engine"
            ))
            
            conn.commit()
            conn.close()
            
            ai_engine.tasks_completed += 1
            
            # Emit real-time update
            socketio.emit('ai_action_completed', {
                'action': action,
                'timestamp': datetime.now().isoformat(),
                'tasks_completed': ai_engine.tasks_completed
            })
            
        except Exception as e:
            print(f"Background AI processing error: {e}")
            time.sleep(60)

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Start background AI processing
    ai_thread = threading.Thread(target=background_ai_processing, daemon=True)
    ai_thread.start()
    
    # Get port from environment (Railway sets this automatically)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    socketio.run(app, host='0.0.0.0', port=port, debug=False)

