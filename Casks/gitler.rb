cask "gitler" do
  arch arm: "arm64", intel: "x64"

  version "0.2.0"
  sha256 arm:   "61d6a63fc5b2fbfe91417663951580ae26b2c918868ccc25c4ed3fe61d30946c",
         intel: "1055c74fec7f35e9b712e124b64451b64416c9d21cb78d29b99fb888b98a1bfb"

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
