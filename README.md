# Requirements
- Running Dremio Software cluster (v24+)
- Dremio's JVM `extraStartParams` (in helm charts) or `DREMIO_JAVA_SERVER_EXTRA_OPTS` (all deployments) are set to include the following: `-Ddebug.allowTestApis=true -DcellSizeLimit=50000000`
- A valid Dremio username with password or PAT (no special `ADMIN` privileges on the cluster are required)
  
# Render Dremio Job Profiles to HTML
- Place your zipped Dremio Job Profiles in the `profiles/` folder
- Run `python3 main.py "https://DREMIO_ENDPOINT" "DREMIO_USERNAME" "DREMIO_PAT_OR_PASSWORD"` to generate the HTML files
- Open the rendered job files in the `rendered/` folder