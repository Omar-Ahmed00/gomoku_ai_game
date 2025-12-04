import tkinter as tk
from ui.gui import ModernGomokuGUI

if __name__ == "__main__":
    print("=" * 60)
    print("🎮 INTELLIGENT GOMOKU AI PLAYER")
    print("Course Project - AI310 & CS361 Artificial Intelligence")
    print("Helwan University - Faculty of Computing & Artificial Intelligence")
    print("=" * 60)
    
    try:
        root = tk.Tk()
        app = ModernGomokuGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")