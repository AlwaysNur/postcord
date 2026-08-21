import requests

def track(code: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0',
        'Referer': 'https://www.nzpost.co.nz/tools/tracking',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'pragma': 'no-cache',
        'Origin': 'https://www.nzpost.co.nz',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=4',
    }

    params = {
        'tracking_reference': code,
    }

    response = requests.get('https://tools.nzpost.co.nz/tracking/api/parceltrack/parcels', params=params, headers=headers)
    return response

if __name__ == "__main__":
    response = track("sry not giving you my tracking code :/").json()
    print(response['success'])
    print(response)