from httpx import post, get, delete, request
from random import randint


URL = 'http://127.0.0.1:5000/vehicles/vehicle/'
URL_WITH_DRIVER = URL + '?with_drivers=yes'
URL_WITHOUT_DRIVER = URL + '?with_drivers=no'
URL_ID_CAR = URL + '10'
URL_DELETE = URL + '5'
URL_UPDATE_CAR = URL + '6'


if __name__ == '__main__':
    input_ = input('Post/Get/Lte/Earle/Driver/Delete/Update/Add?')
    if input_.startswith('Post'):
        r = post(URL, json={'make': f'usa',
                            'model': f'model_{randint(10**5, 9 * 10**5)}',
                            'plate_number': f'AA {randint(1, 10)} II',
                            'driver_id': 'no'}), None
    elif input_.startswith('Get'):
        r = get(URL)
        r = r, len(r.json()['vehicles'])
    elif input_.startswith('With'):
        r = get(URL_WITH_DRIVER)
        r = r, len(r.json()['vehicles'])
    elif input_.startswith('Not'):
        r = get(URL_WITHOUT_DRIVER)
        r = r, len(r.json()['vehicles'])
    elif input_.startswith('Car'):
        r = get(URL_ID_CAR), None
    elif input_.startswith('Delete'):
        r = delete(URL_DELETE), None
    elif input_.startswith('Update'):
        r = request('UPDATE', URL_UPDATE_CAR, json={'make': f'germany',
                                                    'model': f'xxxx_{randint(10 ** 5, 9 * 10 ** 5)}',
                                                    'plate_number': f'XX {randint(4, 10)} AA'}), None
    elif input_.startswith('Add'):
        r = post(URL_UPDATE_CAR, json={'driver_id': f'yes'}), None
    result = r[0].json().get('vehicles')
    print(r[0].status_code, r[1], {id_['id'] for id_ in result})
