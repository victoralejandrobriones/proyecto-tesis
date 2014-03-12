import sys
import math

class Analizer:
    def __init__(self, file):
        with open(file, "r") as f:
            data_list = f.readlines()
        self.data_values = []
        for element in data_list:
            self.data_values.append((int(math.ceil(float(element.split(", ")[0]))),int(math.ceil(float(element.split(", ")[1]))/10)*10))

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

    def find_patterns(self):
        chk_values = []
        chk_positions = []
        self.patterns = []
        self.positions = self.find_positions()
        for i in range(len(self.data_values)):
            value = str(self.data_values[i][1])
            if value not in chk_values and i not in chk_positions:
                #print value, self.positions[value]
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
                    print j, pattern
                    patterns.append(pattern)
                self.patterns.append(patterns)
                chk_values.append(value)

if __name__ == '__main__':
    a = Analizer(sys.argv[1])
    a.find_patterns()
