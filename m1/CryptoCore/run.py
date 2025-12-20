#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run CryptoCore without installation
Run: python run.py [arguments]
"""
import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    try:
        from cryptocore.main import main as cryptocore_main
        cryptocore_main()
    except ImportError as e:
        print(f"Import error: {e}")
        print("\nPossible reasons:")
        print("1. 'cryptocore' folder should be in the same folder as this script")
        print("2. Install pycryptodome: pip install pycryptodome")
        print("3. Folder structure:")
        print("CryptoCore/")
        print("├── cryptocore/     # code folder")
        print("│   ├── __init__.py")
        print("│   ├── main.py")
        print("│   └── ...")
        print("├── run.py         # this file")
        print("├── test.txt       # test file")
        print("└── setup.py")
        
        print(f"\nCurrent folder: {current_dir}")
        print("Contents:")
        for item in os.listdir(current_dir):
            full_path = os.path.join(current_dir, item)
            if os.path.isdir(full_path):
                print(f"  [DIR]  {item}/")
            else:
                print(f"  [FILE] {item}")
        
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()