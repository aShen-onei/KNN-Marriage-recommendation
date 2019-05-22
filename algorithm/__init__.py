import analyse as recommend
import numpy as np
import sys
sys.path.append('../traindata/')
import manreplite as getlocal
def analyse_result(res):
    age = res[3]
    height = res[5]
    edu = getlocal.edu(res[4])
    marriage = getlocal.marrige(res[7])
    lng, lat = recommend.getlnglat(res[6])
    array = [age, height, edu, marriage, lng, lat]
    return array
if __name__ == "__main__":
    fr = open('../testdata/mantest.txt')
    for line in fr.readlines():
        array = analyse_result(line)
        Rate = recommend.main(array, line[9])
        print(Rate)