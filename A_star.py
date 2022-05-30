from os import remove, replace, truncate
import sys
import re

Predicates = []
Variables = []
Constants = []
Functions = []
Clauses = []
Fol = []


def Count_breaket(x):
    count = 0
    for i in x:
        if i == "(" or i == ")":
            count += 1
    return count


def Negate(a):
    if a.find("!") != -1:
        a = a.replace("!", "")
    else:
        a = "!" + a[0:]
    return a


def Multiply_argv_function(x, y):
    x_term = x[x.find('(') + 1:x.rfind(')')]
    y_term = y[y.find('(') + 1:y.rfind(')')]
    x_term_set = x_term.split(",")
    y_term_set = y_term.split(",")

    if Count_breaket(x) != 4 and Count_breaket(y) == 4:
        for i in range(0, len(x_term_set)):
            if x_term_set[i] in Variables:
                x = x.replace(x_term_set[i], y_term_set[i])
        return x, y
    if Count_breaket(x) == 4 and Count_breaket(y) != 4:
        for i in range(0, len(y_term_set)):
            if y_term_set[i] in Variables:
                y = y.replace(y_term_set[i], x_term_set[i])
        return x, y

    if Count_breaket(x) == 4 and Count_breaket(y) == 4:
        for i in range(0, len(x_term_set)):
            if x_term_set[i].find("(") != -1:
                x_function = x_term_set[i]
                y_function = y_term_set[i]
                if x_function.split("(")[0] in Functions:
                    x_var = x_function[x_function.find('(') + 1:x_function.rfind(')')]
                    y_var = y_function[y_function.find('(') + 1:y_function.rfind(')')]
                    if x_var in Variables:
                        x = x.replace(x_var, y_var)
                    elif y_var in Variables:
                        y = y.replace(y_var, x_var)

                return x, y

    return x, y


def Unify(x, y):
    if x.find(",") != -1 and y.find(",") != -1:
        if Count_breaket(x) == 4 or Count_breaket(y) == 4:
            x, y = Multiply_argv_function(x, y)
        x_var = x[x.find('(') + 1:x.rfind(')')]
        y_var = y[y.find('(') + 1:y.rfind(')')]
        x_var_set = x_var.split(",")
        y_var_set = y_var.split(",")
        remove_spot = []
        for i in range(0, len(x_var_set)):
            if x_var_set[i] in Variables:
                x = x.replace(x_var_set[i], y_var_set[i])
                remove_spot.append(y_var_set[i])
        for i in remove_spot:
            y_var_set.remove(i)
        for i in range(0, len(y_var_set)):
            if y_var_set[i] in Variables:
                y = y.replace(y_var_set[i], x_var_set[i])
        return x, y

    elif x.find(",") != -1:
        return x, y
    elif y.find(",") != -1:
        return x, y
    else:
        x_var = x[x.find('(') + 1:x.rfind(')')]
        y_var = y[y.find('(') + 1:y.rfind(')')]

        if Count_breaket(x) == 2 and Count_breaket(y) == 2:  # only one variable or const
            if x_var in Variables:
                x = x.replace(x_var, y_var)
            elif y_var in Variables:
                y = y.replace(y_var, x_var)
            return x, y

        else:
            if Count_breaket(x) == 4 and Count_breaket(y) == 4:
                x_function = x[x.find('(') + 1:x.rfind(')')]
                y_function = y[y.find('(') + 1:y.rfind(')')]
                if x_function.split("(")[0] in Functions:
                    x_var = x_function[x_function.find('(') + 1:x_function.rfind(')')]
                    y_var = y_function[y_function.find('(') + 1:y_function.rfind(')')]
                    if x_var in Variables:
                        x = x.replace(x_var, y_var)
                    elif y_var in Variables:
                        y = y.replace(y_var, x_var)
                return x, y

            elif Count_breaket(x) == 4 and Count_breaket(y) == 2:

                x_function = x[x.find('(') + 1:x.rfind(')')]
                if x_function.split("(")[0] in Functions:
                    y_var = y[y.find('(') + 1:y.rfind(')')]
                    if y_var in Variables:
                        y = y.replace(y_var, x_function)
                return x, y
            else:
                y_function = y[y.find('(') + 1:y.rfind(')')]
                if y_function.split("(")[0] in Functions:
                    x_var = x[x.find('(') + 1:x.rfind(')')]
                    if x_var in Variables:
                        x = x.replace(x_var, y_function)
                return x, y


def PLRESOLVER(C1, C2):  # retrun all possibility from two Clauses
    result = []
    c_set1 = C1.split(" ")
    c_set2 = C2.split(" ")
    for di in c_set1:
        for dj in c_set2:
            di_cp, dj_cp = Unify(di, dj)  # Unify two to see if it can be same
            if di_cp == Negate(dj_cp) or Negate(di_cp) == dj_cp:  #
                dinew = C1.split(" ")
                dinew.remove(di)
                djnew = C2.split(" ")
                djnew.remove(dj)
                itmp = ""
                jtmp = ""
                char_space = ""
                if (len(dinew) >= 2):
                    char_space = " "
                for i in dinew:
                    if itmp != "":
                        itmp = itmp + char_space + i
                    else:
                        itmp = itmp + i

                char_space = ""
                if (len(djnew) >= 2):
                    char_space = " "

                for j in djnew:
                    if jtmp != "":
                        jtmp = jtmp + char_space + j
                    else:
                        jtmp = jtmp + j

                if itmp == "" and jtmp == "":
                    result.append([])
                else:
                    if jtmp == "" or itmp == "":
                        result.append(itmp + jtmp)
                    else:
                        result.append(itmp + " " + jtmp)

    return result


def isSublist(l1, l2):
    for item in l1:
        if not item in l2:
            return False
    return True


def PLRESOLUTION(Clauses_set):  # resolution function return true or false
    # print(Clauses_set)
    new_list = []
    while True:
        pairs = [(Clauses_set[i], Clauses_set[j]) for i in range(len(Clauses_set)) for j in
                 range(i + 1, len(Clauses_set))]  # make pair from all possible Clauses
        for (ci, cj) in pairs:
            resolvents = PLRESOLVER(ci, cj)  # Call Resolver
            # print(resolvents)
            if [] in resolvents:  # if the empty Clauses we return T
                return True
            for temp in resolvents:
                if not temp in new_list:
                    new_list.append(temp)
        if isSublist(new_list, Clauses_set):  # check if the sublist we return false
            return False
        for i in new_list:
            if not i in Clauses_set:
                Clauses_set.append(i)


with open(sys.argv[1]) as f:  # read all the data from the file
    line_cnf = f.readline()
    while line_cnf:  # read line by line and store into the list
        if line_cnf.find("Predicates:") != (-1):
            line_cnf = line_cnf.replace("Predicates: ", "")
            Predicates = line_cnf.strip().split(" ")
            if Predicates[0] == "":
                Predicates = []
            line_cnf = ""
        if line_cnf.find("Variables:") != (-1):
            line_cnf = line_cnf.replace("Variables: ", "")
            Variables = line_cnf.strip().split(" ")
            if Variables[0] == "":
                Variables = []
            line_cnf = ""
        if line_cnf.find("Constants:") != (-1):
            line_cnf = line_cnf.replace("Constants: ", "")
            Constants = line_cnf.strip().split(" ")
            if Constants[0] == "":
                Constants = []
            line_cnf = ""
        if line_cnf.find("Functions:") != (-1):
            line_cnf = line_cnf.replace("Functions: ", "")
            Functions = line_cnf.strip().split(" ")
            if Functions[0] == "":
                Functions = []
            line_cnf = ""
        line_cnf = line_cnf.replace("Clauses:", "")
        line_cnf = line_cnf.strip()
        if line_cnf != "":
            Clauses.append(line_cnf)
        line_cnf = f.readline()

# result = []

# test  = ["loves(SKF0(x2),x2)","loves(SKF0(x1))"]
# # test1  = ["!dog(x0)","dog(Kim)"]
# result = Unify(test[0],test[1])
# print(result)
if PLRESOLUTION(Clauses):
    print("no")
else:
    print("yes")
