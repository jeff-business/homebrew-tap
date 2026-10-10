import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import update_cask


def release(tag, draft=False):
    version = tag[1:]
    return {
        "tag_name": tag,
        "draft": draft,
        "published_at": None if draft else "2026-10-10T12:00:00Z",
        "assets": [
            {"name": f"Gitler_{version}_macos-{arch}.app.tar.gz", "size": 42,
             "digest": f"sha256:{checksum}"}
            for arch, checksum in (("arm64", "a" * 64), ("x64", "b" * 64))
        ],
    }


def checksums(item):
    return "".join(f"{asset['digest'][7:]}  {asset['name']}\n" for asset in item["assets"])


class UpdateCaskTests(unittest.TestCase):
    def test_release_order_includes_candidates_without_downgrading(self):
        releases = [release(tag) for tag in (
            "v0.1.1", "v0.2.0-rc.2", "v0.2.0-rc.10", "v0.2.0-beta.1",
        )]
        releases.insert(0, release("v0.3.0", draft=True))
        self.assertEqual(update_cask.newest_release(releases)["tag_name"], "v0.2.0-rc.10")
        releases.append(release("v0.2.0"))
        self.assertEqual(update_cask.newest_release(releases)["tag_name"], "v0.2.0")

    def test_both_architectures_and_cli_use_the_selected_release(self):
        item = release("v0.2.0-rc.2")
        text = update_cask.render_cask("lebedev-nikita/gitler", item, checksums(item))
        self.assertIn('version "0.2.0-rc.2"', text)
        self.assertIn('sha256 arm:   "' + "a" * 64 + '"', text)
        self.assertIn('intel: "' + "b" * 64 + '"', text)
        self.assertIn('https://github.com/lebedev-nikita/gitler/releases/download/v#{version}', text)
        self.assertIn('binary "#{appdir}/Gitler.app/Contents/MacOS/gitler"', text)

    def test_incomplete_and_mismatched_downloads_are_rejected(self):
        item = release("v0.2.0-rc.2")
        for modification in ("missing", "empty", "digest", "checksum", "duplicate", "draft"):
            with self.subTest(modification=modification):
                changed = copy.deepcopy(item)
                checksum_text = checksums(item)
                if modification == "missing":
                    changed["assets"].pop()
                elif modification == "empty":
                    changed["assets"][0]["size"] = 0
                elif modification == "digest":
                    changed["assets"][0]["digest"] = "sha256:" + "c" * 64
                elif modification == "checksum":
                    checksum_text = checksum_text.splitlines()[0] + "\n"
                elif modification == "duplicate":
                    checksum_text += checksum_text
                else:
                    changed["draft"] = True
                with self.assertRaises(ValueError):
                    update_cask.render_cask("lebedev-nikita/gitler", changed, checksum_text)

    def test_invalid_release_does_not_overwrite_existing_cask(self):
        import json

        item = release("v0.2.0-rc.2")
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "gitler.rb"
            output.write_text("existing cask\n")

            def fake_gh(*args):
                if args[0] == "api":
                    return json.dumps([[item]])
                destination = Path(args[args.index("--dir") + 1])
                (destination / "SHA256SUMS.txt").write_text("invalid\n")
                return ""

            with patch.object(update_cask, "gh", side_effect=fake_gh):
                with self.assertRaises(ValueError):
                    update_cask.update("lebedev-nikita/gitler", output)
            self.assertEqual(output.read_text(), "existing cask\n")


if __name__ == "__main__":
    unittest.main()
