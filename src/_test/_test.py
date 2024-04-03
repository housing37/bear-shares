decoded_data = ['hello','hello','hello','hello','hello','hello',]
d_ret_log = {'_from':decoded_data[0],
                '_to':decoded_data[1],
                '_usdAmnt':decoded_data[2],
                '_usdAmntPaid':decoded_data[3],
                '_usdFee':decoded_data[4],
                '_usdBurnValTot':decoded_data[5]}
print(decoded_data)
print(*decoded_data)
print(d_ret_log, sep='\n')
print(*d_ret_log, sep='\n')
[print(f'{key}: {val}') for key,val in d_ret_log.items()]