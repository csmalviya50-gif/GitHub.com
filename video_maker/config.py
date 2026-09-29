# ============================================================
#  VIDEO CONFIGURATION — change any setting here, then re-run:
#      python3 make_video.py
# ============================================================

# --- Input / Output ---
INPUT_IMAGE  = "input.jpg"          # source photo
OUTPUT_VIDEO = "output/short.mp4"   # where the video is written

# --- Video basics ---
WIDTH        = 1080                 # output width  (px)
HEIGHT       = 1080                 # output height (px)  -> 1080x1080 = square
FPS          = 30                   # frames per second
DURATION_SEC = 6                    # total length of the video (seconds)

# --- Motion effect (Ken Burns: slow zoom + pan) ---
ZOOM_START   = 1.00                 # zoom at start (1.00 = fit)
ZOOM_END     = 1.15                 # zoom at end  (>1.0 zooms in)
PAN_X        = 0.00                 # horizontal drift: -1.0 (left) .. 1.0 (right)
PAN_Y        = -0.10                # vertical drift:   -1.0 (up)   .. 1.0 (down)

# --- Fades ---
FADE_IN_SEC  = 0.5                  # black -> image at the start
FADE_OUT_SEC = 0.5                  # image -> black at the end

# --- Encoding ---
BITRATE      = "5M"                 # video quality (higher = sharper, bigger file)
CODEC        = "libx264"            # H.264, plays on almost everything
