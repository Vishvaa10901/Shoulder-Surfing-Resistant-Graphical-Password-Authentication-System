import pandas as pd
import numpy as np
import random
from PIL import Image
import os
from django.conf import settings
import json

def my_fun(choice):

	totalClasses = 20
	classes = ['Ant', 'Binocular', 'Camera', 'Chair', 'Crocodile', 'Dinosour', 'Elephant', 'Fan', 'Fish', 'Flamingo', 'Flower', 'Flowerpot', 'Headphones', 'Laptop', 'Panda', 'Pizza', 'Rooster', 'Ship', 'Soccerball', 'Watch']
	ims = []
	label = []
	choiceIms = []
	choiceLabel = []

	print("choice = ", choice['choices'])
	imgChoices = choice['choices'].split(',')
	imgChoices.remove('')
	print(imgChoices)
	labelChoices = [classes.index(i) for i in imgChoices]
	print(labelChoices)

	for i in range(totalClasses):
		imgpath = "D:\\Object_images"
		imgpath = imgpath + "\\" + classes[i]
		path, dirs, files = next(os.walk(imgpath))
		flag = 0
		for ch in labelChoices:
			if ch == i:
				flag = 1
				print(i)
				break
		if flag != 1:
			for j in range(30):
				imgpath = path + "\\" + files[j]
				im = Image.open(imgpath)
				im = im.resize((200, 100))
				im = np.array(im)
				if im.shape==(100, 200, 3):
					ims.append(im)
					label.append(i)
					# print("img--",i, j, "--", im.shape)
		else:
			for j in range(30):
				imgpath = path + "\\" + files[j]
				im = Image.open(imgpath)
				im = im.resize((200, 100))
				im = np.array(im)
				if im.shape==(100, 200, 3):
					choiceIms.append(im)
					choiceLabel.append(i)


	# print("\n")
	ims = np.array([im for im in ims])
	label = np.array(label)
	choiceIms = np.array([im for im in choiceIms])
	choiceLabel = np.array(choiceLabel)
	# print("ims array shape: ", ims.shape)
	# print("Label shape: ", label.shape)
	# print("choice shape: ", choiceIms.shape)

	# print("\n")
	random_indices = random.sample(range(ims.shape[0]), 6)
	inputImgs = ims[random_indices]
	inputLabels = label[random_indices]
	# print("random indices = ", random_indices)

	random_indices.extend(random.sample(range(choiceIms.shape[0]), 3))
	print("random indices = ", random_indices)
	print(choiceIms[random_indices[6:9]].shape)
	inputImgs = np.append(inputImgs, choiceIms[random_indices[6:9]], axis=0)
	inputLabels = np.append(inputLabels, choiceLabel[random_indices[6:9]], axis=0)
	print("inputImgs shape: ", inputImgs.shape)
	print("inputLabels: ", inputLabels)

	random_index = [0, 1, 2, 3, 4, 5, 6, 7, 8]
	random.shuffle(random_index)
	# print("index ",random_index)
	
	inputImgs1 = inputImgs.copy()
	inputLabels1 = inputLabels.copy()
	# random_indices1 = random_indices.copy()
	for i in range(9):
		inputImgs[i] = inputImgs1[random_index[i]]
		inputLabels[i] = inputLabels1[random_index[i]]
		# random_indices[i] = random_indices1[random_index[i]]
	
	# print("random indices = ", random_indices)
	print("inputImgs shape: ", inputImgs.shape)
	print("inputLabels: ", inputLabels)

	# new_image = Image.new('RGB',(3 * inputImgs[0].shape[1], 3 * inputImgs[0].shape[0]), (250,250,250))
	# print("new image: ", new_image.size)
	image1 = Image.fromarray(inputImgs[0].astype('uint8'))
	st = "img_0.jpg"
	image1.save(settings.MEDIA_ROOT+ 'images/'+ st, 'JPEG')
	# new_image.paste(image1,(0,0))
	# j=1
	# k=0
	for i in range(1, 9):
		# print("Image ", inputImgs[i].shape[0], inputImgs[i].shape[1])
		image1 = Image.fromarray(inputImgs[i].astype('uint8'))
		st = "img_" + str(i) + ".jpg"
		image1.save(settings.MEDIA_ROOT+ 'images/'+ st, 'JPEG')
	# 	new_image.paste(image1,(j * inputImgs[i].shape[1], k * inputImgs[i].shape[0]))
	# 	j = j + 1
	# 	if(j>=3):
	# 		j=0
	# 		k = k + 1
	# new_image.show()

	with open(settings.MEDIA_ROOT+ 'inputLabels.txt', 'w') as filehandle:
		json.dump(inputLabels.tolist(), filehandle)
	
	with open(settings.MEDIA_ROOT+ 'labelChoices.txt', 'w') as filehandle:
		json.dump(labelChoices, filehandle)