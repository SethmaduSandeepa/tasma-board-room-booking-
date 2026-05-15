import sys
try:
    import main
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
