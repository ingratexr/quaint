import subprocess
import sys


def main():
    argsmap = {
        "test": ["uv", "run", "twine", "upload", "--repository", "testpypi", "dist/*"],
        "pypi": ["uv", "run", "twine", "upload", "dist/*"]
    }

    # if no publish destination, abort 
    if len(sys.argv) < 2 or sys.argv[1] not in argsmap:
        print(f"Please specify where to publish. Options are: [{", ".join(argsmap.keys())}]")
        return
    dest = sys.argv[1]
    print("Publishing to: ", dest)

    subprocess.run(argsmap[sys.argv[1]], check=True)


if __name__ == "__main__":
    main()

