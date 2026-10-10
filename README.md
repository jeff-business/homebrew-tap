# Better Software Homebrew tap

## Gitler

Install [Gitler](https://github.com/lebedev-nikita/gitler) on macOS, on Apple Silicon or Intel:

```sh
brew install --cask jeff-business/tap/gitler
```

This installs `Gitler.app` and the `gitler` command, with Git as a dependency:

```sh
gitler /path/to/repository
```

The cask tracks the newest published Gitler version, including release candidates.
Upgrade with `brew update && brew upgrade --cask gitler`.

## Concentration Slop

Install [Concentration Slop](https://github.com/lebedev-nikita/concentration-slop) on macOS 14+, on Apple Silicon or Intel:

```sh
brew install --cask lebedev-nikita/tap/concentration-slop
```

This installs `Concentration Slop.app` with yt-dlp and Deno for YouTube playback.
Open it from Applications. Window binding requires Accessibility access in System Settings.
Releases are ad-hoc signed and not notarized by Apple; macOS may require approval in Privacy & Security.

Concentration Slop has moved to [lebedev-nikita/tap](https://github.com/lebedev-nikita/homebrew-tap).
For an existing installation, run `brew update`, then `brew reinstall --cask lebedev-nikita/tap/concentration-slop`.

## Maintenance

The Gitler update workflow checks upstream releases hourly. It validates both macOS archive
checksums against GitHub's asset digests before updating the cask. Run it manually
from Actions to pick up a release sooner.

```sh
python3 -m unittest discover -s scripts
python3 scripts/update_cask.py
```

Maintain the Concentration Slop cask in [lebedev-nikita/homebrew-tap](https://github.com/lebedev-nikita/homebrew-tap).
