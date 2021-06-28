import json, csv 
from itertools import permutations

RANK_TO_DESCRIPTION = {
    1: "Round 1 Pick (1st choice)",
    2: "Round 2 Pick (2nd choice)",
    3: "Round 3 Pick (3rd choice)",
    4: "Round 4 Pick (4th choice)",
    5: "Round 5 Pick (5th choice)"
}

DESCRIPTION_TO_NUMBER = {
    "Room 1 (Basement - front of house)" : 1,
    "Room 2 (Basement - back of house)" : 2,
    "Room 3 (1st floor - front of house)" : 3,
    "Room 4 (1st floor - back of house)" : 4,
    "Room 6 (2nd floor - back of house)" : 6,
    "Room 7 (3rd floor - front of house)" : 7,
    "Room 8 (3rd floor - back of house)" : 8
}

NUMBER_TO_DESCRIPTION = {
    1: "Room 1 (Basement - front of house)",
    2: "Room 2 (Basement - back of house)",
    3: "Room 3 (1st floor - front of house)",
    4: "Room 4 (1st floor - back of house)",
    6: "Room 6 (2nd floor - back of house)",
    7: "Room 7 (3rd floor - front of house)",
    8: "Room 8 (3rd floor - back of house)"
}

ROOMS = [1,2,3,4,6,7,8]

# in each permutation, the person @ index...
# 0 is in Room 1
# 1 is in Room 2
# 2 is in Room 3
# 3 is in Room 4
# 4 is in Room 6
# 5 is in Room 7
# 6 is in Room 8

INDEX_TO_NUMBER = {
    0 : 1,
    1 : 2,
    2 : 3,
    3 : 4,
    4 : 6,
    5 : 7,
    6 : 8,
}

def make_draft_json(csvFilePath, jsonFilePath):
    ''' Converts provided CSV to JSON and writes the result to the provided file name.'''
     
    data = {}
     
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary and add it to data
        for rows in csvReader:
            rankings = [0 for i in range(5)]
            for i in RANK_TO_DESCRIPTION.keys():
                rankings[i-1] = DESCRIPTION_TO_NUMBER[rows[RANK_TO_DESCRIPTION[i]]]
            data[rows["First name"].lower()] = rankings

    write_json_to_file(data, jsonFilePath)


def write_json_to_file(data, file_name):
    # Open a json writer, and use the json.dumps() function to dump data
    with open(file_name, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
    

def load_json(json_file_name):
    with open(json_file_name, 'r') as file:
        json_object = json.load(file)
        return json_object


def init_point_values():
    initial_point_values = {}
    for i in ROOMS:
        initial_point_values[i] = 0
    return initial_point_values


def set_point_values(ranking_dict, file_name):
    points = {}
    for name in ranking_dict.keys():
        point_values = init_point_values()
        rankings = ranking_dict[name]
        last_choices = list(set(ROOMS) - set(rankings))
        for index, room in enumerate(rankings):
            point_values[room] += 20*(5-index)
        #     point_values[room] -= 5*index
        # for room in last_choices:
        #     point_values[room] -=5*5
        points[name] = point_values
    write_json_to_file(points, file_name)

def create_scenarios(names, rooms):
    # Get all permutations
    return permutations(names, len(names))


def get_best_scenario(perm_list, points):
    best_perm = []
    best_score = -200
    for p in perm_list:
        score = calc_perm_score(list(p), points)
        if score > best_score:
            best_score = score
            best_perm = [list(p)]
        elif score == best_score:
            best_perm.append(list(p))
    return [list(perm) for perm in best_perm], best_score


def calc_perm_score(perm, points):
    score = 0
    for ind, name in enumerate(perm):
        room_number = INDEX_TO_NUMBER[ind]
        score += points[name][str(room_number)]
    return score


if __name__ == '__main__':
    make_draft_json("Room Draft (Responses) - Form Responses 1.csv", "rankings.json")
    rankings = load_json("rankings.json")
    set_point_values(rankings, "points.json")
    points = load_json("points.json")
    names = list(rankings.keys())
    scenarios = create_scenarios(names, points)
    best_scenarios, best_score = get_best_scenario(scenarios, points)
    print("\nNumber of best case scenarios: " + str(len(best_scenarios)))
    print("Average value assigned: ", round(best_score/7, 2), "(100 = everyone got their first choice, 80 = everyone got their second choice)\n")
    for scenario in best_scenarios:
        for ind, name in enumerate(list(scenario)):
            print('\t' +name.title() + " in " + str(NUMBER_TO_DESCRIPTION[INDEX_TO_NUMBER[ind]]))
        print()