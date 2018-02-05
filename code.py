import sys
import math

def parse_yfile(file):
    y_data = []
    for line in file:
        tokens = line.split()
        new = []
        for num in tokens:
            number = float(num)
            new.append(number)
        y_data.append(new)
    return y_data

def parse_gfile(file):
    g_data = []
    for line in file:
        tokens = line.split()
        new = []
        for num in tokens:
            number = float(num)
            new.append(number)
        g_data.append(new[1:])
    new_g_data = []
    for i in xrange(len(g_data)-1):
        new_r = (g_data[i][0]+g_data[i+1][0])/2
        new_g_11 = (g_data[i][1]+g_data[i+1][1])/2
        new_g_12 = (g_data[i][2]+g_data[i+1][2])/2
        new_g_22 = (g_data[i][3]+g_data[i+1][3])/2
        new_g_data.append([new_r,new_g_11,new_g_12,new_g_22])
    return new_g_data


y_filename = "yij.dat"
g_filename = "gofr.mdljmix"

temp = open(y_filename, "r")
y_file = temp.readlines()
temp.close()

temp = open(g_filename, "r")
g_file = temp.readlines()
temp.close()



y_data = parse_yfile(y_file)[2:]
g_data = parse_gfile(g_file)

#modify y_data
modified_y_data = []
for i in xrange(len(y_data)):
    new = []
    new.append(y_data[i][0])
    new.append(y_data[i][1])
    new.append((y_data[i][2]+y_data[i][3])/2)
    new.append(y_data[i][4])
    modified_y_data.append(new)
y_data = modified_y_data

sigma_11 = 1.0
k_B = 1.38064852E-23

input_file = open("input.txt","r").readlines()
epsilon_11 = float(input_file[0].split()[0])
epsilon_12 = epsilon_11*float(input_file[1].split()[0])
epsilon_22 = epsilon_11*float(input_file[2].split()[0])
temp_reduced = float(input_file[3].split()[0])
sigma_12 = sigma_11*float(input_file[4].split()[0])
sigma_22 = sigma_11*float(input_file[5].split()[0])

# Need to put in reduced units relative to epsilon_11 and sigma_11. 
# Modify for mixtures. 
#sigma = y_data[-1][0]


output = open("y_r_output","wa")
#compute beta
beta = 1.0/(epsilon_11*temp_reduced)

for i in xrange(len(g_data)):
    r = g_data[i][0]
    g_r_11 = g_data[i][1]
    g_r_12 = g_data[i][2]
    g_r_22 = g_data[i][3]
    y_r_11 = -1.0
# Need to change this for mixtures r < sigma_ij
    if (r<1.00*sigma_11):
        assert math.fabs(y_data[i][0] - r) < 0.0001
        y_r_11 = y_data[i][1]
        y_r_12 = y_data[i][2]
        y_r_22 = y_data[i][3]
    else:
        phi_11 = 4*epsilon_11*((sigma_11/r)**12-(sigma_11/r)**6)
        phi_12 = 4*epsilon_12*((sigma_12/r)**12-(sigma_12/r)**6)
        phi_22 = 4*epsilon_22*((sigma_22/r)**12-(sigma_22/r)**6)
        y_r_11 = math.exp(beta*phi_11)*g_r_11
        y_r_12 = math.exp(beta*phi_12)*g_r_12
        y_r_22 = math.exp(beta*phi_22)*g_r_22
    assert y_r_11>=0




    output.write(str(r)+" "+str(y_r_11)+" "+str(y_r_12)+" "+str(y_r_22)+"\n")

output.close()




