from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import schedule
import time
import threading

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_run = db.Column(db.DateTime)
    next_run = db.Column(db.DateTime)
    interval = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Job {self.name}>'

db.create_all()

def run_jobs():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    return jsonify([{'id': job.id, 'name': job.name, 'last_run': job.last_run, 'next_run': job.next_run, 'interval': job.interval} for job in jobs])

@app.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify({'id': job.id, 'name': job.name, 'last_run': job.last_run, 'next_run': job.next_run, 'interval': job.interval})

@app.route('/jobs', methods=['POST'])
def create_job():
    data = request.json
    new_job = Job(name=data['name'], last_run=None, next_run=None, interval=data['interval'])
    db.session.add(new_job)
    db.session.commit()
    
    # Schedule the job
    if data['interval'] == 'weekly':
        schedule.every().monday.at("10:00").do(job_action, new_job.id)
    elif data['interval'] == 'daily':
        schedule.every().day.at("10:00").do(job_action, new_job.id)
    
    return jsonify({'message': 'Job created', 'job_id': new_job.id}), 201

def job_action(job_id):
    job = Job.query.get(job_id)
    job.last_run = datetime.now()
    job.next_run = job.last_run + timedelta(days=7) if job.interval == 'weekly' else job.last_run + timedelta(days=1)
    db.session.commit()
    print(f'Job {job.name} executed at {job.last_run}')

if __name__ == '__main__':
    threading.Thread(target=run_jobs).start()
    app.run(debug=True)
