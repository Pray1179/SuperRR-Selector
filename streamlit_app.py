"""
streamlit_app.py
----------------
Root entrypoint for Streamlit Community Cloud and cloud deployments.
Automatically invokes the Rajasthan Royals SupeRR Selector analytics dashboard.
"""
import os
import sys
import runpy

CURR_DIR = os.path.abspath(os.path.dirname(__file__))

# Resolve path to dashboard application
target_app = os.path.join(CURR_DIR, "dashboard", "app.py")
if not os.path.exists(target_app):
    target_app = os.path.join(CURR_DIR, "final_submission", "dashboard", "app.py")

if not os.path.exists(target_app):
    raise FileNotFoundError(f"Dashboard app.py could not be located from {CURR_DIR}")

# Execute application in main namespace
runpy.run_path(target_app, run_name="__main__")
