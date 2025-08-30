import subprocess
import shutil

# TODO: automatic semantic versioning

def main():
    # Clean dist
    shutil.rmtree("dist", ignore_errors=True)
    
    # Build
    subprocess.run(["uv", "build"], check=True)
    print("Build complete!")

if __name__ == "__main__":
    main()

