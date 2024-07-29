import subprocess

def is_ffmpeg_installed():
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            # ffmpeg is installed
            return True
        else:
            # ffmpeg is not installed
            return False
    except FileNotFoundError:
        # ffmpeg command not found
        return False

# Example usage:
if is_ffmpeg_installed():
    print("ffmpeg is installed on this system.")
else:
    print("ffmpeg is not installed on this system.")
