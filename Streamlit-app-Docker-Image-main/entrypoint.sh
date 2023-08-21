#!/bin/bash
python3 user_login_consumer.py &
streamlit run streamlit_producer_app.py --server.port 8501 --server.address=0.0.0.0
