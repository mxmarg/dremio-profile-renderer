import sys
from render_profiles import render_profiles


if __name__ == '__main__':
    DREMIO_ENDPOINT = sys.argv[1]
    DREMIO_ADMIN_USERNAME = sys.argv[2]
    DREMIO_PAT_TOKEN = sys.argv[3]
    render_profiles(DREMIO_ENDPOINT, DREMIO_ADMIN_USERNAME, DREMIO_PAT_TOKEN)