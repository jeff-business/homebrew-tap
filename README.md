# Better Software Homebrew tap

Install [Gitler](https://github.com/better-software/gitler) on macOS, on Apple Silicon or Intel:

```sh
brew install --cask better-software/tap/gitler
```

This installs `Gitler.app` and the `gitler` command, with Git as a dependency:

```sh
gitler /path/to/repository
```

The cask tracks the newest published Gitler version, including release candidates.
Upgrade with `brew update && brew upgrade --cask gitler`.

## Maintenance

The update workflow checks upstream releases hourly. It validates both macOS archive
checksums against GitHub's asset digests before updating the cask. Run it manually
from Actions to pick up a release sooner.

```sh
python3 -m unittest discover -s scripts
python3 scripts/update_cask.py
```
