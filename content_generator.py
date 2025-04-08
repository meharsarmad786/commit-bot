import random
from datetime import datetime

def generate_content():
    """Generate unique content for each commit."""
    return f"Commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Random Value: {random.randint(1000, 9999)}"
