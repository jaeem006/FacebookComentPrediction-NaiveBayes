import csv
import random
import math

def cargaCsv(file):
	lineas = csv.reader(open(file, "rb"))
	dataset = list(lineas)
	for i in range(len(dataset)):
		dataset[i] = [float(x) for x in dataset[i]]
	return dataset

def dividirDatos(dataset, radio):
	trainSize = int(len(dataset) * radio)
	c = list(dataset)
	trainSet = []
	while len(trainSet) < trainSize:
		index = random.randrange(len(c))
		trainSet.append(c.pop(index))
	return [trainSet, c]

def separarClass(dataset):
	otros = {}
	for i in range(len(dataset)):
		vector = dataset[i]
		if (vector[-1] not in otros):
			otros[vector[-1]] = []
		otros[vector[-1]].append(vector)
	return otros

def media(numb):
	return sum(numb)/float(len(numb))
 
def desvStdr(numb):
	promedio = media(numb)
	varianza = sum([pow(x-promedio,2) for x in numb])/float(len(numb))
	return math.sqrt(varianza)

def resumir(dataset):
	res = [(media(atr), desvStdr(atr)) for atr in zip(*dataset)]
	del res[-1]
	return res

def resumenClass(dataset):
	res = {}
	otros = separarClass(dataset)
	for valor, instancia in otros.iteritems():
		res[valor] = resumir(instancia)
	return res

def proba(x, media, des):
	expo = math.exp(-(math.pow(x-media,2)/(2*math.pow(des,2))))
	return (1 / (math.sqrt(2*math.pi) * des)) *	expo

def classProba(res, vector):
	prob = {}
	for valor, res in res.iteritems():
		prob[valor] = 1
		for i in range(len(res)):
			media, des = res[i]
			x = vector[i]
			prob[valor] *= proba(x, media, des)
	return prob

def predecir(res, vector):
	prob = classProba(res, vector)
	etiqueta, mejor = None, -1
	for classValue, probability in prob.iteritems():
		if etiqueta is None or probability > mejor:
			mejor = probability
			etiqueta = classValue
	return etiqueta

def getPredicciones(res, conj):
	predicciones = []
	for i in range(len(conj)):
		ret = predecir(res, conj[i])
		predicciones.append(ret)
	return predicciones

def Accuracy(conj, predicciones):
	correct = 0
	for x in range(len(conj)):
		if conj[x][-1] == predicciones[x]:
			correct += 1
	return (correct/float(len(conj))) * 100.0

def main():
	#dataset = cargaCsv('Dataset/Training/Features_Variant_4.csv')
	dataset = cargaCsv('Dataset/Testing/Features_TestSet.csv')
	trainingSet, testSet = dividirDatos(dataset, 0.7)
	print('Cargados {0} train={1} test={2}').format(len(dataset), len(trainingSet), len(testSet))
	resu = resumenClass(trainingSet)
	print('Resumen: {0}%').format(resu)
	predicciones = getPredicciones(resu, testSet)
	print('predicciones: {0}').format(predicciones)
	acertadas = Accuracy(testSet, predicciones)
	print('Acertadas: {0}%').format(acertadas)

if __name__ == "__main__":
	main()