cask "gitler" do
  arch arm: "arm64", intel: "x64"

  version "0.2.4"
  sha256 arm:   "2d8edf3efb9c07c3b09a2dc6da52c3c3ebfe4237b673ebfb8bb81ef75fabfc06",
         intel: "30c9297f5f7b4384c3bf4bc5d2d3227cc955fde3ee02e4a4ef4f51eda0582ca0"

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
