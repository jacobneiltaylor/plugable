import sys
import semver

def main():
    _, tag = sys.argv
    if "-" in tag:
        ver, pre, git = tag.split("-")
        ver = semver.VersionInfo.parse(ver).bump_patch()
        print(f"{str(ver)}-pre.{pre}+build.{git}")
    else: 
        print(tag)

if __name__ == "__main__":
    main()
