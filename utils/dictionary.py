class EncodingDictionary:
    def __init__(self, dict_, begin='START', end='END', unc='UNC', sep='SEP'):
        self._dict = dict_
        self._begin = begin
        self._end = end
        self._unc = unc
        self._sep = sep

    def __call__(self, element):
        if element in self._dict:
            return self._dict[element]
        else:
            return self.get_unc_char()

    def __len__(self):
        return len(self._dict)

    def __getitem__(self, item):
        if item in self._dict:
            return self._dict[item]
        else:
            return self.get_unc_char()

    def __contains__(self, item):
        return item in self._dict

    def get_end_char(self):
        return self._dict[self._end]

    def get_begin_char(self):
        return self._dict[self._begin]

    def get_unc_char(self):
        return self._dict[self._unc]

    def get_sep_char(self):
        return self._dict[self._sep]

    @staticmethod
    def read_dictionary(filename):
        dict_ = dict()
        with open(filename, 'r') as dict_file:
            for line in dict_file:
                tag, code = line.split('$')
                dict_[tag] = int(code)
        return EncodingDictionary(dict_)

