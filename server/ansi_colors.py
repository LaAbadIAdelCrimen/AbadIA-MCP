# --- ANSI Escape Code Definitions ---
# \x1b is the Escape character (ESC)
# [ is the Control Sequence Introducer (CSI)
# m closes the Select Graphic Rendition (SGR) code.

# Standard Colors (Foreground)
BLACK = '\x1b[30m'  # Black text
RED = '\x1b[31m'    # Red text
GREEN = '\x1b[32m'  # Green text
YELLOW = '\x1b[33m' # Yellow text
BLUE = '\x1b[34m'   # Blue text
ORANGE = '\x1b[33m' # Orange is often the same as Yellow (33) in standard ANSI
WHITE = '\x1b[37m'  # White/Light Gray text

# Bright/Bold Colors (These often look better for visibility)
BRIGHT_RED = '\x1b[91m'
BRIGHT_YELLOW = '\x1b[93m'
BRIGHT_BLUE = '\x1b[94m'
BRIGHT_WHITE = '\x1b[97m' 

# Utility Code
RESET = '\x1b[0m'   # Resets all formatting (color, bold, etc.)
