import os
import sys

# Add the src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.web import main

if __name__ == "__main__":
    main()
