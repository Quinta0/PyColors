import cv2
import numpy as np
import mss
import pygetwindow as gw
from colorama import Fore, Style, init
from pynput import mouse

# Initialize colorama
init()

# Define a dictionary of color ranges and their names
colors = {
    "red": ([0, 50, 50], [10, 255, 255]),
    "green": ([36, 50, 50], [89, 255, 255]),
    "blue": ([90, 50, 50], [128, 255, 255]),
    "yellow": ([25, 50, 50], [35, 255, 255]),
    "orange": ([10, 50, 50], [24, 255, 255]),
    "purple": ([129, 50, 50], [158, 255, 255]),
    "pink": ([159, 50, 50], [179, 255, 255]),
    "cyan": ([90, 50, 50], [100, 255, 255])
}

# Function to detect the color at the given pixel
def detect_color(hsv_frame, x, y):
    pixel = hsv_frame[y, x]
    for color_name, (lower, upper) in colors.items():
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        if np.all(lower <= pixel) and np.all(pixel <= upper):
            return color_name
    return "unknown"

# Function to list all windows and let the user select one
def select_window():
    windows = gw.getAllTitles()
    windows = [w for w in windows if w]  # Filter out empty titles
    print("Available Windows:")
    for i, window in enumerate(windows):
        print(f"{i + 1}: {window}")

    choice = int(input("Select the window number: ")) - 1
    return windows[choice]

# Mouse position
mouse_x, mouse_y = 0, 0

# Mouse listener callback
def on_move(x, y):
    global mouse_x, mouse_y
    mouse_x, mouse_y = x, y

# Start mouse listener
listener = mouse.Listener(on_move=on_move)
listener.start()

# Screen capture setup
with mss.mss() as sct:
    # Get the selected window
    selected_window_title = select_window()
    selected_window = gw.getWindowsWithTitle(selected_window_title)[0]

    while True:
        # Capture the selected window
        monitor = {
            "top": selected_window.top,
            "left": selected_window.left,
            "width": selected_window.width,
            "height": selected_window.height,
            "mon": 1
        }
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # Convert the frame to HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Adjust mouse coordinates relative to the selected window
        relative_mouse_x = mouse_x - selected_window.left
        relative_mouse_y = mouse_y - selected_window.top

        # Check if mouse is within the window bounds
        if 0 <= relative_mouse_x < monitor["width"] and 0 <= relative_mouse_y < monitor["height"]:
            # Detect the color at the mouse position
            color_name = detect_color(hsv_frame, relative_mouse_x, relative_mouse_y)

            # Display the resulting frame
            cv2.putText(frame, f"Color: {color_name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.circle(frame, (relative_mouse_x, relative_mouse_y), 10, (255, 255, 255), -1)
            cv2.imshow('Color Detection', frame)

            # Print the color name to console with colorama
            colorama_color = {
                "red": Fore.RED,
                "green": Fore.GREEN,
                "blue": Fore.BLUE,
                "yellow": Fore.YELLOW,
                "orange": Fore.LIGHTRED_EX,
                "purple": Fore.MAGENTA,
                "pink": Fore.LIGHTMAGENTA_EX,
                "cyan": Fore.CYAN,
                "unknown": Fore.WHITE
            }
            print(f"Mouse Position: ({relative_mouse_x}, {relative_mouse_y}), Detected color: {colorama_color[color_name]}{color_name}{Style.RESET_ALL}")

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cv2.destroyAllWindows()
    listener.stop()
