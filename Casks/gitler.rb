cask "gitler" do
  version "0.5.2-rc.4"
  sha256 "0b04929cc9d0dd1cf2413886f016104180b34e90cf7ffa7e228cd230000912f0"

  url "https://github.com/lebedev-nikita/gitler/releases/download/v#{version}/Gitler_#{version}_macos-arm64.app.tar.gz"
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
  depends_on arch: :arm64
  depends_on :macos

  app "Gitler.app"
  binary "#{appdir}/Gitler.app/Contents/MacOS/gitler"
end
