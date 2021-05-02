def IsStay(data, price):
    if  (data['open'] == price and 
        data['high'] == price and
        data['low'] == price and
        data['close'] == price):
            return True
    else:
        return False

def MergeCandle(data):
    result = {
        'time': data[-1]['time'],
        'open': data[0]['open'],
        'close': data[-1]['close'],
        'high': data[0]['high'],
        'low': data[0]['low'],
        'volume': data[0]['volume'],
    }

    for i in range(1, len(data)):
        if result['high'] < data[i]['high']:
            result['high'] = data[i]['high']
        if result['low'] > data[i]['low']:
            result['low'] = data[i]['low']

        result['volume'] += data[i]['volume']
    return result


