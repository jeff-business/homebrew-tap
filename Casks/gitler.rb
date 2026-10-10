cask "gitler" do
  arch arm: "arm64", intel: "x64"

  version "0.2.1"
  sha256 arm:   "49340b2c295a9dacdb0b60dc2246813f47c6ff925e8b8d5bbe29a45bc0938fec",
         intel: "5ca1436a94c3d0b1222130f47ca0d7e65f11da3bc43eaba47e5c89f8b282d317"

  url "https://github.com/lebedev-nikita/gitler/releases/download/v#{version}/Gitler_#{version}_macos-#{arch}.app.tar.gz"
  name "Gitler"
  desc "Read-only Git graph for branches and worktrees"
  homepage "https://github.com/lebedev-nikita/gitler"

  livecheck do
    url :url
    regex(/^v?(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)$/i)
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
  binary "#{appdir}/Gitler.app/Contents/MacOS/gitler"
end
