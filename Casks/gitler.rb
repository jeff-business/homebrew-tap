cask "gitler" do
  arch arm: "arm64", intel: "x64"

  version "0.2.0-rc.2"
  sha256 arm:   "dd4fb4c7022c59f54a09ade72318521a5e6755f237b3eaf63745362dc26de75b",
         intel: "bc37f5861eecc54091d3853b3dc02b7f08c2c4cf3550b3c0760d3da968379bd1"

  url "https://github.com/jeff-business/gitler/releases/download/v#{version}/Gitler_#{version}_macos-#{arch}.app.tar.gz"
  name "Gitler"
  desc "Read-only Git graph for branches and worktrees"
  homepage "https://github.com/jeff-business/gitler"

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
