import io
import os
import requests
import urllib3
import zipfile

urllib3.disable_warnings()


def log_in(DREMIO_ENDPOINT: str, DREMIO_ADMIN_USERNAME: str, DREMIO_PAT_TOKEN: str):
    headers = {"Content-Type": "application/json"}
    payload = '{"userName": "' + DREMIO_ADMIN_USERNAME + '","password": "' + DREMIO_PAT_TOKEN + '"}'
    payload = payload.encode(encoding='utf-8')
    response = requests.request(
        "POST",
        DREMIO_ENDPOINT + "/apiv2/login", 
        data=payload,
        headers=headers,
        timeout=600,
        verify=False
    )
    if response.status_code != 200:
        print("Authentication Error " + str(response.status_code))
        raise RuntimeError("Authentication error.")
    else:
        print("Successfully authenticated")

    token = '_dremio' + response.json()['token']
    return token

def render_profiles(DREMIO_ENDPOINT: str, DREMIO_ADMIN_USERNAME: str, DREMIO_PAT_TOKEN: str):
    auth_token = log_in(DREMIO_ENDPOINT, DREMIO_ADMIN_USERNAME, DREMIO_PAT_TOKEN)

    profiles_dir = 'profiles'
    target_dir = "rendered"
    all_files = [os.path.join(profiles_dir, f) for f in os.listdir(profiles_dir) if os.path.isfile(os.path.join(profiles_dir, f))]

    for filename in all_files:
        if not filename.endswith(".zip"):
            print(f"Skipping {filename}")
        else:
            print(f"Rendering {filename} ...")
            with open(filename, "rb") as readall:
                with zipfile.ZipFile(readall, "r") as z:
                    for zipped_file in z.namelist():
                        if zipped_file.startswith("profile_attempt"):
                            with z.open(zipped_file) as f:
                                data = f.read()
                                profile_attempt = data.decode('utf-8')
                            
                            headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": auth_token}
                            payload = {"profileJsonText": profile_attempt}
                            response = requests.post(DREMIO_ENDPOINT + '/apiv2/test/render_external_profile',
                                                    headers=headers, data=payload, timeout=None, verify=True)
                            rendered_profile = response.text
                            rendered_profile = rendered_profile.replace('/static/css/', DREMIO_ENDPOINT + '/static/css/')
                            rendered_profile = rendered_profile.replace('/static/js/', DREMIO_ENDPOINT + '/static/js/')

                            attempt = zipped_file.replace(".json", "")
                            target_file = filename.replace(".zip", f"_{attempt}.html").replace(profiles_dir, target_dir)

                            print(f"Creating {target_file} ...")
                            with open(target_file, "w") as t:
                                t.write(rendered_profile)