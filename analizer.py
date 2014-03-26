import sys
import math

class Analizer:
    def __init__(self, file):
        with open(file, "r") as f:
            data_list = f.readlines()
        self.data_values = []
        for element in data_list:
            self.data_values.append((float(element.split(", ")[0]),int(math.ceil(float(element.split(", ")[1]))/10)*10))

    def find_positions(self):
        values = {}
        checked = []
        for i in range(len(self.data_values)):
            current = self.data_values[i][1]
            if current not in checked:
                values.update(self.search(current))
                checked.append(current)
        return values

    def search(self, value):
        positions = []
        for i in range(len(self.data_values)):
            if value == self.data_values[i][1]:
                positions.append(i)
        return {str(value):positions}

    def best_match(self, patterns):
        best_matches = []
        for element in self.patterns:
            for _dict in element:
                for key in _dict:
                    pattern = _dict[key]
                    p_size = len(pattern)
                    for m_element in patterns:
                        for m_dict in m_element:
                            for m_key in m_dict:
                                m_pattern = m_dict[m_key]
                                m_size = len(m_pattern)
                                validator = []
                                p_last = 0
                                m_last = 0
                                size = p_size if p_size <= m_size else m_size
                                for iterator in range(size):
                                    if iterator == 0:
                                        p_last = pattern[iterator]
                                        m_last = m_pattern[iterator]
                                    else:
                                        p_value = pattern[iterator]
                                        m_value = m_pattern[iterator]
                                        p_comparator = (p_value >= p_last)
                                        m_comparator = (m_value >= m_last)
                                        comparator = (p_comparator == m_comparator)
                                        validator.append(comparator)
                                comparator = True
                                for value in validator:
                                    if not value:
                                        comparator = False
                                if comparator:
                                    if size != 1:
                                        best_matches.append((key, m_key, validator))
                                        #print size, key, m_key, validator
                                        #print "*************"
        return best_matches
                                
    def find_patterns(self):
        chk_values = []
        chk_positions = []
        self.patterns = []
        self.positions = self.find_positions()
        for i in range(len(self.data_values)):
            value = str(self.data_values[i][1])
            if value not in chk_values and i not in chk_positions:
                patterns = []
                for j in self.positions[value]:
                    pattern = []
                    k = 1
                    pattern.append(int(value))
                    while j+k not in self.positions[value]:
                        if j+k < len(self.data_values):
                            next_value = self.data_values[j+k][1]
                            pattern.append(next_value)
                        else:
                            break
                        k+=1
                    patterns.append({self.data_values[j][0]:pattern})
                self.patterns.append(patterns)
                chk_values.append(value)
        return self.patterns

if __name__ == '__main__':
    a = Analizer(sys.argv[1])
    a.find_patterns()
    b = Analizer(sys.argv[2])
    matches = a.best_match(b.find_patterns())
    for match in matches:
        print match
