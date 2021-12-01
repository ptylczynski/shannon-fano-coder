import pickle
import random
from copy import deepcopy
from typing import Tuple

from anytree import Node, RenderTree, PreOrderIter


class ShannonFanoCoder:
    def __init__(self):
        pass

    def encode_file(self, file_path: str) -> list:
        return self.encode(
            self._convert_to_bytes(
                self._read_and_parse_file(file_path)
            )
        )

    def _read_and_parse_file(self, file_path: str):
        content: str = ''
        with open(file_path, 'r') as file:
            for line in file:
                content += line
        return content.replace(' ', '')

    def _convert_to_bytes(self, data: str):
        bytess: list = []
        end_pos: int = 8
        while end_pos <= len(data):
            bytess.append(
                int(data[end_pos - 8:end_pos], 2)
            )
            end_pos += 8
        return bytess

    def encode(self, data: list) -> list:
        codes = self.generate_coding_key(data)
        return self._swap(data, codes)

    def generate_coding_key(self, data: list) -> dict:
        distributions = self._create_distribution(data)
        distributions = dict(sorted(distributions.items(), key=lambda item: item[0], reverse=True))
        root = self._create_tree(distributions, '')
        codes = self._scrap_codes(root)
        print('\nGenerated tree is: ')
        print(RenderTree(root))
        print('\nScraped codes are: ')
        print(codes)
        self._save_coding_key(codes)
        return codes

    def generate_coding_key_from_file(self, file_path: str) -> dict:
        return self.generate_coding_key(
            self._convert_to_bytes(
                self._read_and_parse_file(file_path)
            )
        )

    def _swap(self, orginal: list, codes: dict, is_decoding: bool = False):
        if not is_decoding:
            return [codes[el] for el in orginal]
        else:
            result = []
            pos = 0
            orginal = orginal[0]
            window = 1
            while pos < len(orginal):
                value = -1
                while value == -1:
                    end = pos + window
                    el = orginal[pos:end]
                    for key in codes:
                        if codes[key] == el:
                            value = key
                            break
                    window += 1
                result.append(value)
                pos += window - 1
                window = 1
            return result

    def _save_coding_key(self, codes: dict):
        with open('key.bin', 'wb') as file:
            pickle.dump(
                codes,
                file
            )

    def _create_distribution(self, data: list) -> dict:
        distributions: dict = {}
        for el in data:
            if el in distributions:
                distributions[el] += 1
            else:
                distributions[el] = 1

        for el in distributions:
            distributions[el] /= len(data)

        return distributions

    def _create_tree(self, distributions: dict, code: str):
        if len(distributions) == 1:
            return Node(chr(65 + random.randint(0, 25)), val=list(distributions.keys())[0], code=code)
        elif len(distributions) > 1:
            l, r = self._split_distributions_equally(distributions)
            l_node: Node = self._create_tree(l, code + '0')
            r_node: Node = self._create_tree(r, code + '1')
            return Node(chr(65 + random.randint(0, 25)), children=[l_node, r_node])

    def _split_distributions_equally(self, distributions: dict) -> Tuple[dict, dict]:
        l = deepcopy(distributions)
        r = dict()
        for k in distributions.keys():
            if self._distributions_sum(l) < self._distributions_sum(r):
                break
            if len(l) == 1:
                break
            r[k] = l.pop(k)
        return l, r

    def _distributions_sum(self, distributions: dict) -> float:
        sum = 0
        for k in distributions:
            sum += distributions[k]
        return sum

    def _scrap_codes(self, root_node: Node) -> dict:
        res = dict()
        for node in PreOrderIter(root_node):
            try:
                val = node.val
                code = node.code
                res[val] = code
            except AttributeError:
                pass
        return res

    def decode(self, data: str, codes: dict) -> list:
        return self._swap([data], codes, is_decoding=True)

    def decode_file_with_key(self, file_path: str, key_path: str):
        codes = self._unpickle_key(key_path)
        content = self._read_and_parse_file(file_path)
        return self.decode(content, codes)

    def _unpickle_key(self, key_path: str) -> dict:
        with open(key_path, 'rb') as file:
            return pickle.load(file)
