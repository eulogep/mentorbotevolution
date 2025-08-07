"""
Configuration Gunicorn pour Vercel
Auteur: MABIALA EULOGE
"""

workers = 4
bind = "0.0.0.0:8000"
worker_class = "gthread"
threads = 4
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
