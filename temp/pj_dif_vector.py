import numpy as np
from hmmlearn import hmm
import csv
import random
np.random.seed(42)
import math
import matplotlib.pyplot as plt

#normalizing and get angle difference vector,

x_train = open('x_train.csv', 'r', encoding='utf-8')
result = open('result.csv', 'w', encoding='utf-8')
train_reader = csv.reader(x_train)
result_writer = csv.writer(result)

train_size = 5000
test_size = 1000
model_list = []
components_size = 8

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_ylim([0,100])
ax.set_xlim([0, train_size])

for i in range(0, 10):
	temp = hmm.GaussianHMM(n_components = components_size, covariance_type="diag")
	temp.n_iter=100
	temp.tol=0.01
	model_list.append(temp)

num = 0

def data_process(li):
	ret = []
	length = int(len(li)/2)
	for i in range(0, length-1):
		ret.append(li[2*i+2]-li[2*i])
		ret.append(li[2*i+3]-li[2*i+1])
	return ret

def add_mid_vector(li):
	ret = []
	length = int(len(li)/2)
	for i in range(0, length):
		temp1 = (li[2*i]*0.9998-0.0174*li[2*i+1])/2
		temp2 = (0.0174*li[2*i]+0.9998*li[2*i+1])/2
		ret.append(temp1)
		ret.append(temp2)
		ret.append(li[2*i]-temp1)
		ret.append(li[2*i+1]-temp2)
	return ret

def add_mid_vector_uniform(li):
	ret = []
	length = int(len(li)/2)
	for i in range(0, length):
		temp1 = li[2*i]/2
		temp2 = li[2*i+1]/2
		ret.append(temp1)
		ret.append(temp2)
		ret.append(li[2*i]-temp1)
		ret.append(li[2*i+1]-temp2)
	return ret

def add_mid_vector_random(li):
	ret = []
	length = int(len(li)/2)
	for i in range(0, length):
		check = random.randint(0,10)
		if(check<5):
			temp1 = (li[2*i]*0.9998-0.0174*li[2*i+1])/2
			temp2 = (0.0174*li[2*i]+0.9998*li[2*i+1])/2
			ret.append(temp1)
			ret.append(temp2)
			ret.append(li[2*i]-temp1)
			ret.append(li[2*i+1]-temp2)
		else:
			temp1 = (li[2*i]*0.9998+0.0174*li[2*i+1])/2
			temp2 = (0.9998*li[2*i+1]-0.0174*li[2*i])/2
			ret.append(temp1)
			ret.append(temp2)
			ret.append(li[2*i]-temp1)
			ret.append(li[2*i+1]-temp2)
	return ret

def add_mid_point(li):
	ret = []
	length = int(len(li)/2)
	for i in range(0, length-1):
		ret.append(li[2*i])
		ret.append(li[2*i+1])
		ret.append((li[2*i]+li[2*i+2])/2)
		ret.append((li[2*i+1]+li[2*i+3])/2)
	ret.append(li[len(li)-2])
	ret.append(li[len(li)-1])
	return ret

def vector_duplicate(li):
	ret = []
	if(len(li)!=2):
		print("unexpected length : the number of vectors isn't 1(in vector_duplicate)")
		return li
	ret.append(li[0])
	ret.append(li[1])
	check = random.randint(0, 2)
	if(check==0):
		ret.append(0.9998*li[0]-0.0174*li[1])
		ret.append(0.0174*li[0]+0.9998*li[1])
	else:
		ret.append(0.9998*li[0]+0.0174*li[1])
		ret.append(0.9998*li[1]-0.0174*li[0])
	return ret
		

def zero_delete(li): #zero vector delete
	ret = []
	length = int(len(li)/2)
	for i in range(0, length):
		if(li[2*i] == 0.0 and li[2*i+1] == 0.0):
			continue
		else:
			ret.append(li[2*i])
			ret.append(li[2*i+1])
	return ret

def normalize(li): #normalizing, and zero vector delte
	ret = []
	length = int(len(li)/2)
	for i in range(0, length):
		temp = math.sqrt(li[2*i]*li[2*i] + li[2*i+1]*li[2*i+1])
		if(temp==0.0):
			continue
		else:
			ret.append(li[2*i]/temp)
			ret.append(li[2*i+1]/temp)
	return ret

print("train start")

def data_process2(li): #axis-transmation use, angle calculation, if (zero, zero):continue
	ret = []
	length = int(len(li)/2)
	for i in range(0, length-1):
		temp1 = li[2*i]*li[2*i+2] + li[2*i+1]*li[2*i+3]
		temp2 = li[2*i]*li[2*i+3] - li[2*i+1]*li[2*i+2]
		ret.append(temp1)
		ret.append(temp2)
	return ret

x = [0]
y = [0]

not_passed = 0
num = 0
for line in train_reader:
	if(num%50 == 0):
		print(num)
	if(num%1000 == 0 and num > 0):
		print("test start")
		x_test = open('x_test.csv', 'r', encoding='utf-8')
		test_reader = csv.reader(x_test)
		test_answer = 0
		n = 0
		for test_line in test_reader:
			if((n% 100) == 0):
				print(n)
			if(n == test_size):
				break
			length = int(test_line[0])
			test_sub_list = test_line[3:3+length*2]
			test_sub_list = list(map(lambda i: float(i), test_sub_list))
			if(len(test_sub_list)==2): #only one point : ignore
				not_passed = not_passed+1
				continue
			test_sub_list = data_process(test_sub_list) #vectorize
#			test_sub_list = zero_delete(test_sub_list) #zero-vector delete
#			if(len(test_sub_list)<2): #no vetor
#				not_passed = not_passed+1
#				continue
			while len(test_sub_list) < 30:
				test_sub_list = add_mid_vector(test_sub_list)
#				test_sub_list = add_mid_point(test_sub_list)
#			test_sub_list = normalize(test_sub_list)
#			test_sub_list = data_process2(test_sub_list)
			test_X = np.array(test_sub_list).reshape(-1, 1)
			test_lengths = [2] * int(len(test_sub_list)/2)
			Y = []
			for i in range(0, 10):
				Y.append(model_list[i].score(test_X, test_lengths)) #lengths
			inference = Y.index(max(Y))
			if(inference == int(test_line[2])):
				test_answer = test_answer + 1
			result_writer.writerow([inference, int(test_line[2])])
			n=n+1
		x_test.close()
		acculate = (test_answer / n)*100
		x.append(num)
		y.append(acculate)
	if(num == train_size):
		break
	answer = int(line[2])
	length = int(line[0])
	sub_list = line[3:3+length*2]
	sub_list = list(map(lambda i: float(i), sub_list))
	if(len(sub_list)==2): #only one point : ignore
		not_passed = not_passed+1
		continue
	sub_list = data_process(sub_list) #vectorize
#	sub_list = zero_delete(sub_list) #zero-vector delete
#	if(len(sub_list)<2): #no vetor
#		not_passed = not_passed+1
#		continue
	while len(sub_list) < 30:
		sub_list = add_mid_vector(sub_list)
#		sub_list = add_mid_point(sub_list)
#	sub_list = normalize(sub_list)
#	sub_list = data_process2(sub_list)
	X = np.array(sub_list).reshape(-1, 1)
	lengths = [2] * int(len(sub_list)/2)
	model_list[answer].fit(X,lengths) #lengths
	num = num+1

x_train.close()
plt.plot(x, y)
plt.xlabel('the number of train samples')
plt.ylabel('accurate')

plt.title('hmm')
plt.show()

