import dict_key_finder

def parse_contract(contract, keys=['fz', 'regionCode', 'regNum', 'purchaseNoticeNumber', 
                ('customer', 'fullName'), ('customer', 'inn'), 
                ('suppliers', 'inn'), ('suppliers', 'organizationName'), 
                ('products', 'name'), 'signDate', 'contractUrl', 'price']):
    obj = dict()
    for key in keys:
        if isinstance(key, tuple):
            tup_key = f'{key[0]}_{key[1]}'
            try:
                value = next(dict_key_finder.find(key[0], contract))
                if isinstance(value, list):
                    final_value = value[0].get(key[1])
                elif isinstance(value, dict):
                    final_value = value.get(key[1])
                obj[tup_key] = final_value
            except StopIteration:
                obj[tup_key] = None
        else:
            try:
                value = next(dict_key_finder.find(key, contract))
                obj[key] = value
            except StopIteration:
                obj[key] = None
    if 'contractUrl' in keys and obj['contractUrl'] is None and obj['purchaseNoticeNumber'] is not None:
        obj['contractUrl'] = f"https://zakupki.gov.ru/{obj['fz']}/purchase/public/purchase/info/common-info.html?regNumber={obj['purchaseNoticeNumber']}"
    else:
        pass
    
    return obj
