from operator import itemgetter
import sys, glob, os

new_track = None
files = glob.glob(os.path.join(sys.argv[1], '*.wav'))
current_file = sys.argv[2]
real_duration = sys.argv[3]
files.remove(current_file)
print files

def data_analizer(current_file, current_patterns):
    patterns = []
    number = 0
    list_of_selections = []
    for file_name in files:
        if file_name+".dat" != current_file:
            try:
                _file = open(file_name+".dat", "r").readlines()
                analizer = Analizer(_file)
                analizer.find_patterns()
                patterns.append([file_name, analizer])
            except:
                pass
    for next_file in patterns:
        matches = next_file[1].best_match(current_patterns)
        match_filter = []
        for match in matches:
            if float(match[0]) < float(match[1]):
                match_filter.append([match[1], match[0], len(match[2])])
        last = None
        dict_list = []
        match_dict = []
        for match in sorted(match_filter, key=itemgetter(0)):
            if last != match[0]:
                if last!= None:
                    match_dict.append({last:dict_list})
                last = match[0]
                dict_list = []
            dict_list.append([match[1], match[2]])
        selection = []
        for match in reversed(match_dict):
            selection.append(best_option(match))
        allow_time = real_duration
        allow_time = allow_time-(allow_time*.15)
        filter_selection = []
        for element in selection:
            if element[0] > allow_time:
                filter_selection.append(element)
        small_time = 0
        for sel in sorted(filter_selection, key=itemgetter(1)):
            if sel[2]!=0:
                if small_time == 0:
                    small_time = sel
                if small_time[1] > sel[1]:
                    small_time = sel
        list_of_selections.append([next_file[0],small_time])
    best_selection = None
    small_time = None
    for i in range(len(list_of_selections)):
        if small_time == None:
            small_time = list_of_selections[i][1][1]
        if small_time < list_of_selections[i][1][1]:
            small_time = list_of_selections[i][1][1]
            best_selection = list_of_selections[i][0]
    return best_selection

def best_option(match):
    matching = float(match.keys()[0])
    times = []
    intn = []
    for element in reversed(sorted(match[match.keys()[0]], key=itemgetter(1))):
        times.append(element[0])
        intn.append(element[1])
    max = 0
    sel_time = 0
    for i in range(len(intn)):
        if matching - times[i] > matching/3:
            if intn[i]>max:
                max = intn[i]
                sel_time = times[i]
    return matching, sel_time, max

def next_track(current_file):
    _file = open(current_file, "r").readlines()
    a = Analizer(_file)
    patterns = a.find_patterns()
    new_track = self.data_analizer(current_file, patterns)