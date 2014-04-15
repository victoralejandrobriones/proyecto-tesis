import sys
import math

class Analizer:
    def __init__(self, data_list):
        self.pattern_size = 20
        self.data_values = []
        for element in data_list:
            self.data_values.append((float(element.split(", ")[0]),int(math.ceil(float(element.split(", ")[1]))/10)*10))

    def find_positions(self):
        values = {}
        checked = []
        for value in self.data_values:
            if value[1] not in checked:
                values.update(self.search(value[1]))
                checked.append(value[1])
        return values

    def search(self, pos):
        positions = []
        for i in range(len(self.data_values)):
            if pos == self.data_values[i][1]:
                positions.append(i)
        return {str(pos):positions}

    def best_match(self, patterns):
        best_matches = []
        it = 0
        for element in self.patterns:
            for _dict in element:
                for key in _dict:
                    pattern = _dict[key]
                    p_size = len(pattern)
                    if p_size > self.pattern_size:
                        for m_element in patterns:
                            for m_dict in m_element:
                                for m_key in m_dict:
                                    m_pattern = m_dict[m_key]
                                    m_size = len(m_pattern)
                                    validator = []
                                    p_last = 0
                                    m_last = 0
                                    size = p_size if p_size <= m_size else m_size
                                    if size > self.pattern_size:
                                        for iterator in range(size):
                                            if iterator != 0:
                                                value = (pattern[iterator] >= p_last) == (m_pattern[iterator] >= m_last)
                                                if value == False:
                                                    validator = None
                                                    break
                                                validator.append(value)
                                            else:
                                                p_last = pattern[iterator]
                                                m_last = m_pattern[iterator]
                                        if validator != None:
                                            best_matches.append((key, m_key, validator))
                                            print it, "of", len(self.patterns), size, key, m_key
            it+=1
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
                chk_positions.append(i)
        return self.patterns

if __name__ == '__main__':
    import time
    t1 = time.time()
    filea = open(sys.argv[1], "r").readlines()
    a = Analizer(filea)
    a.find_patterns()
    fileb = open(sys.argv[2], "r").readlines()
    b = Analizer(fileb)
    matches = a.best_match(b.find_patterns())
    #for match in matches:
    #    print match
    print time.time()-t1
