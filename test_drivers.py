from httpx import post, get, delete, request
from random import randint


URL = 'http://127.0.0.1:5000/drivers/driver/'
URL_LATER = URL + '?created_at__gte=13-12-2021'
URL_EARLIER = URL + '?created_at__lte=13-12-2021'
URL_ID_DRIVER = URL + '3'
URL_DELETE = URL + '6'
URL_UPDATE_DRIVER = URL + '2'


if __name__ == '__main__':
    input_ = input('Post/Get/Lte/Earle/Driver/Delete/Update?')
    if input_.startswith('Post'):
        r = post(URL, json={'first_name': f'jhon',
                            'last_name': f'doe_{randint(10**5, 9 * 10**5)}'}), None
    elif input_.startswith('Get'):
        r = get(URL)
        r = r, len(r.json()['drivers'])
    elif input_.startswith('Later'):
        r = get(URL_LATER)
        r = r, len(r.json()['drivers'])
    elif input_.startswith('Early'):
        r = get(URL_EARLIER)
        r = r, len(r.json()['drivers'])
    elif input_.startswith('Driver'):
        r = get(URL_ID_DRIVER), None
    elif input_.startswith('Delete'):
        r = delete(URL_DELETE), None
    elif input_.startswith('Update'):
        r = request('UPDATE', URL_UPDATE_DRIVER,
                    json={'first_name': f'Nick',
                    'last_name': f'doe_{randint(10**5, 9 * 10**5)}'}), None

    print(r[0].status_code, r[1], r[0].json())
