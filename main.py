from coder import ShannonFanoCoder

if __name__ == '__main__':
    print('Hello')
    coded: list = ShannonFanoCoder().encode_file('data/pan-tadeusz.txt.8bit.01')

    with open('encoded.txt', 'w') as file:
        file.write(''.join(coded))

    decoded: list = ShannonFanoCoder().decode_file_with_key('encoded.txt', 'key.bin')
    with open('decoded.txt', 'w') as file:
        for el in decoded:
            file.write(format(el, '08b'))
