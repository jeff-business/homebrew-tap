"""Update Gitler's cask from the newest published upstream version."""

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = re.compile(r"v(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?$")


def gh(*args):
    return subprocess.check_output(["gh", *args], text=True)


def version_key(tag):
    match = VERSION.fullmatch(tag)
    if not match:
        raise ValueError(f"Unsupported release tag: {tag}")
    major, minor, patch, prerelease = match.groups()
    identifiers = tuple(
        (0, int(part)) if part.isdecimal() else (1, part)
        for part in prerelease.split(".")
    ) if prerelease else ()
    return (int(major), int(minor), int(patch), prerelease is None, identifiers)


def newest_release(releases):
    published = [item for item in releases if not item["draft"] and item["published_at"]]
    if not published:
        raise ValueError("No published Gitler releases")
    return max(published, key=lambda item: version_key(item["tag_name"]))


def render_cask(repository, release, checksum_text):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("Expected repository in OWNER/REPO form")
    tag = release["tag_name"]
    version_key(tag)
    if release["draft"] or not release["published_at"]:
        raise ValueError("Cannot package an unpublished release")
    version = tag[1:]
    checksums = {}
    for line in checksum_text.splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (\S+)", line)
        if not match or match[2] in checksums:
            raise ValueError("Invalid or duplicate release checksum")
        checksums[match[2]] = match[1]

    assets = {asset["name"]: asset for asset in release["assets"]}
    hashes = {}
    for arch in ("arm64", "x64"):
        name = f"Gitler_{version}_macos-{arch}.app.tar.gz"
        asset = assets.get(name)
        if not asset or not asset["size"] or name not in checksums:
            raise ValueError(f"Missing macOS archive or checksum: {name}")
        checksum = checksums[name]
        if asset.get("digest") != f"sha256:{checksum}":
            raise ValueError(f"GitHub asset digest disagrees with checksum: {name}")
        hashes[arch] = checksum

    return f'''cask "gitler" do
  arch arm: "arm64", intel: "x64"

  version "{version}"
  sha256 arm:   "{hashes['arm64']}",
         intel: "{hashes['x64']}"

  url "https://github.com/{repository}/releases/download/v#{{version}}/Gitler_#{{version}}_macos-#{{arch}}.app.tar.gz"
  name "Gitler"
  desc "Read-only Git graph for branches and worktrees"
  homepage "https://github.com/{repository}"

  livecheck do
    url :url
    regex(/^v?(\\d+\\.\\d+\\.\\d+(?:-[0-9A-Za-z.-]+)?)$/i)
    strategy :github_releases do |json, regex|
      json.filter_map do |release|
        next if release["draft"]

        release["tag_name"]&.[](regex, 1)
      end
    end
  end

  depends_on formula: "git"
  depends_on :macos

  app "Gitler.app"
  binary "#{{appdir}}/Gitler.app/Contents/MacOS/gitler"
end
'''


def update(repository, output):
    pages = json.loads(gh("api", f"repos/{repository}/releases?per_page=100", "--paginate", "--slurp"))
    release = newest_release([item for page in pages for item in page])
    with tempfile.TemporaryDirectory() as directory:
        gh("release", "download", release["tag_name"], "--repo", repository,
           "--pattern", "SHA256SUMS.txt", "--dir", directory)
        text = render_cask(repository, release, (Path(directory) / "SHA256SUMS.txt").read_text())
    if output.exists() and output.read_text() == text:
        print(f"Gitler {release['tag_name']} is already current")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text)
    print(f"Updated {output} to Gitler {release['tag_name']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default="jeff-business/gitler")
    parser.add_argument("--output", type=Path, default=ROOT / "Casks/gitler.rb")
    args = parser.parse_args()
    update(args.repository, args.output)
