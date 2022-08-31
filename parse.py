repo_urls = [
	"https://github.com/nasa-jpl/explorer-1",
	"https://github.com/nasa-jpl/explorer-1.git",
	"git@github.com/nasa-jpl/explorer-1.git",
	"https://github.com/nasa-jpl/explorer-1/tree/branch-name",
	"https://github.jpl.nasa.gov/18x/WCP",
]

class LBGithub:
	@staticmethod
	def commits(repo_url, branch, token=None):


def parse(url):
	# Start
	for prefix in ["http://", "https://", "git@"]:
		if url.startswith(prefix):
			url = url[len(prefix):]
	# End
	if url.endswith(".git"):
		url = url[:-4]
	# Split
	parts = url.split("/")
	if len(parts) >= 3:
		# Params
		base_url = parts[0]
		owner = parts[1]
		repo = parts[2]
		# Check
		if base_url == "github.com":
			base_url = f"api.{base_url}"
		else:
			base_url = f"{base_url}/api/v3"
		# Result
		return {
			"base_url": base_url,
			"owner": owner,
			"repo": repo,
		}

for url in repo_urls:
	print(parse(url))
