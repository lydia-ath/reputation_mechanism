import numpy
import matplotlib.pyplot as plt
import random
import seaborn as sns
import scipy.stats as st
from sci_analysis import analyze
import numpy as np
#from scipy.stats import uniform

thita = 0
#global variables, dictionairies, lists
subjective_metrics = {'accuracy': 0.0, 'availability': 0.0, 'validity':0.0}
subjective_metrics_weights1 = {'accuracy': 0.5, 'availability': 0.3, 'validity':0.2}
subjective_metrics_weights2 = {'accuracy': 0.1, 'availability': 0.1, 'validity':0.8}


#quality class metrics and target values
quality_class1 = {'availability':0.9, 'latency':0.2, 'noise':0.2}
quality_class2 = {'availability':0.5, 'latency':0.2, 'noise':0.3}
    
#quality class datasources
quality_class1_resources = ['datasource1', 'datasource2', 'datasource3', 'datasource4']
quality_class2_resources = ['datasource2', 'datasource3', 'datasource5', 'datasource6']

#quality class weights
quality_class1_weights = {'availability':0.5, 'latency':0.3, 'noise':0.2}
quality_class2_weights = {'availability':0.2, 'latency':0.7, 'noise':0.1}

#initialization of reputation scores 
objective_old = {'datasource1':0.5, 'datasource2':0.5, 'datasource3':0.5, 'datasource4':0.5, 'datasource5':0.5, 'datasource6':0.5}
subjective_old = {'datasource1':0.5, 'datasource2':0.5, 'datasource3':0.5, 'datasource4':0.5, 'datasource5':0.5, 'datasource6':0.5}

reputation_old_providers = {'provider1':0.5, 'provider2':0.5, 'provider3':0.5, 'provider4':0.5, 'provider5':0.5, 'provider6':0.5}
reputation_old_federations = {'federation1': 0.5, 'federation2': 0.5}
reputation_old_products = {'product1': 0.9, 'product2': 0.8, 'product3': 0.1, 'product4': 0.7}

final_reputation_scores = {'datasource1':0.0, 'datasource2':0.0, 'datasource3':0.0, 'datasource4':0.0, 'datasource5':0.0, 'datasource6':0.0}

#global variables
lamda = 0.8
weight = 0.8
thita = 0
#product 1 and porduct 2 belongs to service class 1 and have quality class 1
product1 = {'datasource1':0.8, 'datasource2':0.6}
product2= {'datasource3':0.7, 'datasource4':0.9}

#product 3 and porduct 4 belongs to service class 2 and have quality class 2
product3 = {'datasource2':0.7, 'datasource3':0.6}
product4 = {'datasource5':0.8, 'datasource6':0.8}
#datasource 2 and datasource 3 contribute in the formation of multiple products that belong to different service/quqlity classes
#so they will have multiple values in the same monitoring period based on those quality classes
datasources = ['datasource1', 'datasource2', 'datasource3', 'datasource4', 'datasource5', 'datasource6']


federation1 = {'datasource1': 0.7, 'datasource2': 0.5, 'datasource3': 0.7, 'datasource4':0.9}
federation2 = {'datasource2': 0.9, 'datasource3': 0.7, 'datasource5': 0.1, 'datasource6': 0.75}

#normalization works
def normalize(probs):
    prob_factor = 1 / sum(probs)
    return [prob_factor * p for p in probs]

#help function 
def contains(diction1, diction2, key):
    if (key in diction1) and (key in diction2):
        return True
    else: 
        return False

#help function
def add(self, key, value):
    self[key] = value

#each transaction = monitoring period, one product participates. One product is composed of 2 datasources
#each datasource may or may not follow the same distribution with the other datasource of the same product
#the distribution declares the random values that the objective metrics, of the same quality class, will take  
def choose_distribution(product, target_value, datasource, minmax):
    #all datasources follow uniform good distribution with low deviation(=low noise, values near to mean value)
    if (product == 'product1'): #first transaction = first monitoring period
        if (minmax == 'min'):
            actual_value = random.uniform(target_value-0.02, target_value +0.05) #good with low deviation
        if (minmax == 'max'):
            actual_value = random.uniform(target_value-0.05, target_value+0.01) #good with low deviation
    #datasources follow different uniform distributions 
    if (product == 'product2' or product == 'product3'): #second transaction = second monitoring period
        if (datasource == 'datasource1' or'datasource3' or'datasource5'):
            if (minmax == 'min'):
                actual_value = random.uniform(target_value-0.1, target_value + 0.1) #good with high deviation
            if (minmax == 'max'):
                actual_value = random.uniform(target_value-0.2, target_value+0.01) #good with high deviation
        if (datasource == 'datasource2' or'datasource4' or'datasource6'):
            if (minmax == 'min'):
                actual_value = random.uniform(target_value-0.5, target_value + 0.01) #bad with low deviation
            if (minmax == 'max'):
                actual_value = random.uniform(target_value-0.01, target_value+0.05) #bad with low deviation
    #all datasources follow uniform bad distribution with high deviation(=high noise, values dispare)
    if (product == 'product4'): #forth transaction = forth monitoring period
        if (minmax == 'min'):
            actual_value = random.uniform(target_value-0.2, target_value+0.01) #bad with low deviation
        if (minmax == 'max'):
            actual_value = random.uniform(target_value-0.01, target_value + 0.2) #bad with low deviation
    return actual_value;

#This function calculates the objective score of each resource of each quality class per monitoring period(=transaction period)
def objective(quality_class1, quality_class2, quality_class1_resources, quality_class2_resources, product):
    Objective_scores = {}
    
    #objective score of resources that belong to quality class 1
    objective_scores_qualityclass1 = {}
    for j in quality_class1_resources:
        #case of good values with low deviation(=low noise=values near to mean)
        temp_score_per_metric = []
        #for i in quality_Class1:
        for i in quality_class1:
            #same for both service classes 
            min_max = {'availability':'min', 'latency':'max', 'noise':'max'}
            target_value = quality_class1[i]
            minmax = min_max[i]
            actual_value = choose_distribution(product, target_value, j, minmax)
            print ('the objective metric is: ', i)
            print ('target value:', target_value)
            print ('actual value:', actual_value)
            print ('target is min or max? ', minmax)
            if ((actual_value<target_value and minmax == 'min')or (actual_value>target_value and minmax == 'max')):
                temp = 0;
                temp_score_per_metric.append(temp)
            else:
                temp = 1;
                temp_score_per_metric.append(temp)

        print (temp_score_per_metric) #3 values per datasource as many as the objective metrics

        #calculation of objective score per datasource
        objectivescore = temp_score_per_metric[0]*quality_class1_weights['availability'] + temp_score_per_metric[1]*quality_class1_weights['latency'] + temp_score_per_metric[2]*quality_class1_weights['noise']
        print ("The objective score for ", j, " is: ", objectivescore)
        add(objective_scores_qualityclass1, j, objectivescore)
        add(Objective_scores, j, objectivescore)

    #objective score of resources that belong to quality class 2
    objective_scores_qualityclass2 = {}
    for j in quality_class2_resources:
        #case of good values with low deviation(=low noise=values near to mean)
        temp_score_per_metric = []
        #for i in quality_Class2:
        for i in quality_class2:
            min_max = {'availability':'min', 'latency':'max', 'noise':'max'}
            target_value = quality_class2[i]
            minmax = min_max[i]
            actual_value = choose_distribution(product, target_value, j, minmax)
            print ('the objective metric is: ', i)
            print ('target value:', target_value)
            print ('actual value:', actual_value)
            print ('target is min or max? ', minmax)
            if ((actual_value<target_value and minmax == 'min')or (actual_value>target_value and minmax == 'max')):
                temp = 0;
                temp_score_per_metric.append(temp)
            else:
                temp = 1;
                temp_score_per_metric.append(temp)

        print (temp_score_per_metric) #3 values per datasource as many as the objective metrics

        #calculation of objective score per datasource   
        objectivescore = temp_score_per_metric[0]*quality_class2_weights['availability'] + temp_score_per_metric[1]*quality_class2_weights['latency'] + temp_score_per_metric[2]*quality_class2_weights['noise']
        print ("The objective score for ", j, " is: ", objectivescore)
        add(objective_scores_qualityclass2, j, objectivescore)
        add(Objective_scores, j, objectivescore)

    #combination of objective scores in case that a datasource belongs to multiple quality classes
    for n in datasources:
        print (n)
        if (contains(objective_scores_qualityclass1, objective_scores_qualityclass2, n)==True):
            final_objective_score = (objective_scores_qualityclass1[n]+objective_scores_qualityclass2[n])/2
            print (n, " belogns to multiple quality classes and its final reputation score is: ", final_objective_score)
            add(Objective_scores, n, final_objective_score)
    print ("objective scores for this monitoring period: ", Objective_scores)
    return Objective_scores;

#one subjective profile per application type
#products that belong to the same application type have same subjective vector 
#User specific --> per transaction --> use can select the weight and/or the subjective metrics 
#Suppose- that users are always submit truthfull evaluations
def subjective_vector_choise(product):
    if (product == "product1"):
        for i in subjective_metrics:
            subjective_metric_value = random.uniform(0, 0.2)
            add(subjective_metrics, i, subjective_metric_value)
    if (product == "product2" or product == "product3"):
        for i in subjective_metrics:
            subjective_metric_value = random.uniform(0.2, 0.8)
            add(subjective_metrics, i, subjective_metric_value)
    if (product == "product4"):
        for i in subjective_metrics:
            subjective_metric_value = random.uniform(0, 0.2)
            add(subjective_metrics, i, subjective_metric_value)
    print ("subjective metrics for transaction of product ", product, ":", subjective_metrics)
    return subjective_metrics;


def subjective(product, subjective_metrics):
    subjective_score = 0
    if(product == "product1" or product == "product2"):
        for i in subjective_metrics:
            subjective_score =  subjective_score + subjective_metrics[i]*subjective_metrics_weights1[i]
    if(product == "product3" or product == "product4"):
        for i in subjective_metrics:
            subjective_score = subjective_score + subjective_metrics[i]*subjective_metrics_weights2[i]
    print ("final subjective score of ", product, ":", subjective_score)
    return subjective_score;

def reputation_update_datasources(objective_scores, subjective_score, product, weight):
    #datasource 2 and datasource 3 contribute in the formation of multiple products that belong to different services/quality classes
    #so they will have multiple values in the same monitoring period based on those quality classes
    
    #update objective score by taking into account the old values
    for i in objective_scores:
        objective_updated = lamda*objective_old[i] + (1-lamda)*objective_scores[i]
        add(objective_old, i, objective_updated)

    #update subjective score by taking into account the old values
    print("mmmmmmmmmmmmmmmm", objective_scores)
    if(product == 'product1'):
        for i in product1:
            print("......................", i)
            subjective_updated = lamda*subjective_old[i] + (1-lamda)*subjective_score
            add(subjective_old, i, subjective_updated)
            #final reputation score after the combination of subjective and objective for the datasources of product 1
            #where the objective_old and the subjective_old dictionaries are now updated 
            if ((objective_scores[i] - subjective_score) > 0.5):
                print("iiiiiiiiiiiiiiiiiiiiiiiiiiii111111111111",objective_scores[i], "oooooooooooooooooooo", subjective_score)
                print ("weighttttttttttttttttttttttt", weight)
                if (weight>0.15):
                    weight -=0.1
                    print ("weighttttttttttttttttttttttt", weight)
                    final_reputation = weight*objective_old[i] + (1-weight)*subjective_old[i]
                    add(final_reputation_scores, i, final_reputation)
            if ((objective_scores[i] - subjective_score) < 0.2):
                if (weight<0.85):
                    print("iiiiiiiiiiiiiiiiiiiiiiiiiiii2222222222",objective_scores[i], "oooooooooooooooooooo", subjective_score)
                    weight +=0.1
                    print ("weighttttttttttttttttttttttt", weight)
                    final_reputation = weight*objective_old[i] + (1-weight)*subjective_old[i]
                    add(final_reputation_scores, i, final_reputation)
            if ((0.2 < (objective_scores[i] - subjective_score) < 0.5) or ((objective_scores[i] - subjective_score)<0)):
                print("iiiiiiiiiiiiiiiiiiiiiiiiiiii1111133333333333333",objective_scores[i], "oooooooooooooooooooo", subjective_score)
                final_reputation = weight*objective_old[i] + (1-weight)*subjective_old[i]
                add(final_reputation_scores, i, final_reputation)

    if(product == 'product2'):
        for i in product2:
            print("......................", i)
            subjective_updated = lamda*subjective_old[i] + (1-lamda)*subjective_score
            print (subjective_updated)
            add(subjective_old, i, subjective_updated)

            #final reputation score after the combination of subjective and objective
            if ((objective_scores[i] - subjective_score) > 0.5):
                print("iiiiiiiiiiiiiiiiiiiiiiiiiiii111111111111",objective_scores[i], "oooooooooooooooooooo", subjective_score)
                if (weight>0.15):
                    weight -=0.1
                    final_reputation = weight*objective_old[i] + (1-weight)*subjective_old[i]
                    add(final_reputation_scores, i, final_reputation)
            if ((objective_scores[i] - subjective_score) < 0.2):
                if (weight<0.85):
                    print("iiiiiiiiiiiiiiiiiiiiiiiiiiii2222222222",objective_scores[i], "oooooooooooooooooooo", subjective_score)
                    weight +=0.1
                    final_reputation = weight*objective_old[i] + (1-weight)*subjective_old[i]
                    add(final_reputation_scores, i, final_reputation)
            if ((0.2 < (objective_scores[i] - subjective_score) < 0.5) or ((objective_scores[i] - subjective_score)<0)):
                print("iiiiiiiiiiiiiiiiiiiiiiiiiiii1111133333333333333",objective_scores[i], "oooooooooooooooooooo", subjective_score)
                final_reputation = weight*objective_old[i] + (1-weight)*subjective_old[i]
                add(final_reputation_scores, i, final_reputation)

    if(product == 'product3'):
        for i in product3:
            print("......................", i)
            subjective_updated = lamda*subjective_old[i] + (1-lamda)*subjective_score
            print (subjective_updated)
            add(subjective_old, i, subjective_updated)

            #final reputation score after the combination of subjective and objective
            if ((objective_scores[i] - subjective_score) > 0.5):
                print("iiiiiiiiiiiiiiiiiiiiiiiiiiii111111111111",objective_scores[i], "oooooooooooooooooooo", subjective_score)
                if (weight>0.15):
                    weight -=0.1
                    final_reputation = weight*objective_old[i] + (1-weight)*subjective_old[i]
                    add(final_reputation_scores, i, final_reputation)
            if ((objective_scores[i] - subjective_score )< 0.2):
                if (weight<0.85):
                    print("iiiiiiiiiiiiiiiiiiiiiiiiiiii2222222222",objective_scores[i], "oooooooooooooooooooo", subjective_score)
                    weight +=0.1
                    final_reputation = weight*objective_old[i] + (1-weight)*subjective_old[i]
                    add(final_reputation_scores, i, final_reputation)
            if ((0.2 < (objective_scores[i] - subjective_score) < 0.5) or ((objective_scores[i] - subjective_score)<0)):
                print("iiiiiiiiiiiiiiiiiiiiiiiiiiii1111133333333333333",objective_scores[i], "oooooooooooooooooooo", subjective_score)
                final_reputation = weight*objective_old[i] + (1-weight)*subjective_old[i]
                add(final_reputation_scores, i, final_reputation)

    if(product == 'product4'):
        for i in product4:
            print("......................", i)
            subjective_updated = lamda*subjective_old[i] + (1-lamda)*subjective_score
            print (subjective_updated)
            add(subjective_old, i, subjective_updated)

            #final reputation score after the combination of subjective and objective
            if ((objective_scores[i] - subjective_score) > 0.5):
                print("iiiiiiiiiiiiiiiiiiiiiiiiiiii111111111111",objective_scores[i], "oooooooooooooooooooo", subjective_score)
                if (weight>0.15):
                    weight -=0.1
                    final_reputation = weight*objective_old[i] + (1-weight)*subjective_old[i]
                    add(final_reputation_scores, i, final_reputation)
            if ((objective_scores[i] - subjective_score) < 0.2):
                if (weight<0.85):
                    print("iiiiiiiiiiiiiiiiiiiiiiiiiiii2222222222",objective_scores[i], "oooooooooooooooooooo", subjective_score)
                    weight +=0.1
                    final_reputation = weight*objective_old[i] + (1-weight)*subjective_old[i]
                    add(final_reputation_scores, i, final_reputation)
            if ((0.2 < (objective_scores[i] - subjective_score) < 0.5) or ((objective_scores[i] - subjective_score)<0)):
                print("iiiiiiiiiiiiiiiiiiiiiiiiiiii1111133333333333333",objective_scores[i], "oooooooooooooooooooo", subjective_score)
                final_reputation = weight*objective_old[i] + (1-weight)*subjective_old[i]
                add(final_reputation_scores, i, final_reputation)

    print ('final reputation scores: ', final_reputation_scores)
    return final_reputation_scores, weight;


#provider 1 --> datasource1, provider2--> datasource2, etc
#so, in this case updated reputation  of datasource = updated reputation of provider
#datasources taking into account the previous old value so there is no need to taking into acount also here
def reputation_update_providers(final_reputation):
    for i in final_reputation:
        reputation_old_providers = final_reputation
    return reputation_old_providers;

#federation 1 --> provider1,2,3,4 --> datasource1,2,3,4
#federation 2 --> provider2,3,5,6 --> datasource2,3,5,6
def reputation_update_federations(final_reputation):
    current_federation1 = 0
    current_federation2 = 0
    for i in final_reputation:
        if (contains(final_reputation, federation1, i) == True):
            current_federation1 = current_federation1 + final_reputation[i]*federation1[i]
        if (contains(final_reputation, federation2, i) == True):
            current_federation2 = current_federation2 + final_reputation[i]*federation2[i]
    #there is no need to see the old value of the federation as the datasources already taking into account the old values 
    final_federation1 = current_federation1 / sum(federation1.values())
    reputation_old_federations['federation1'] = final_federation1
    final_federation2 = current_federation2 / sum(federation2.values())
    reputation_old_federations['federation2'] = final_federation2
    return reputation_old_federations;

#update current product of the traction and the affected ones that may have one or multiple common datasources
def reputation_update_products(final_reputation):
    current_product1 =0
    for i in final_reputation:
        if(contains(final_reputation, product1, i)== True):
            current_product1 = current_product1 + final_reputation[i]*product1[i]
    final_product1 = current_product1/sum(product1.values())
    reputation_old_products['product1']=final_product1

    current_product2=0
    for i in final_reputation:
        if(contains(final_reputation, product2, i)== True):
            current_product2 = current_product2 + final_reputation[i]*product2[i]
    final_product2 = current_product2/sum(product2.values())
    reputation_old_products['product2']=final_product2

    current_product3=0
    for i in final_reputation:
        if(contains(final_reputation, product3, i)== True):
            current_product3 = current_product3 + final_reputation[i]*product3[i]
    final_product3 = current_product3/sum(product3.values())
    reputation_old_products['product3']=final_product3

    current_product4=0
    for i in final_reputation:
        if(contains(final_reputation, product4, i)== True):
            current_product4 = current_product4 + final_reputation[i]*product4[i]
    final_product4 = current_product4/sum(product4.values())
    reputation_old_products['product4']=final_product4

    return reputation_old_products;

def reputation(product):
    weight = 0.8
    subjective_metrics_per_transaction = subjective_vector_choise(product)
    product_subjective = subjective(product, subjective_metrics_per_transaction)
    #assumption: where monitoring period = transaction period
    objective_for_monitoring_period = objective(quality_class1, quality_class2, quality_class1_resources, quality_class2_resources, product)
    final_Reputation_per_datasource,weight =reputation_update_datasources(objective_for_monitoring_period, product_subjective, product,weight)
    reputation_update_providers(final_Reputation_per_datasource)
    reputation_update_federations(final_Reputation_per_datasource)
    reputation_update_products(final_Reputation_per_datasource)

def main():
    product1_counter, product2_counter, product3_counter,product4_counter = 0, 0, 0, 0

    for i in range (0, 20):
        print ("-----------------------------------------------Transaction",i,"----------------------------------------------------------------------------")
        
        answer = input("Do you want a product of service class 1 or service class 2? ")
        print (reputation_old_products)
        if (answer == '1'):
            class1 = [reputation_old_products['product1'], reputation_old_products['product2']]
            class1_products = ['product1', 'product2']
            normalization_of_products_reputation = normalize(class1)
            print(normalization_of_products_reputation)
            choice = random.choices(class1_products, normalization_of_products_reputation)
            print(choice)
            if (choice[0] == "product1"): 
                product1_counter = product1_counter + 1
            if (choice[0] == "product2"): 
                product2_counter = product2_counter + 1
            reputation(choice[0])

        if (answer == '2'):
            class2 = [reputation_old_products['product3'], reputation_old_products['product4']]
            class2_products = ['product3', 'product4']
            normalization_of_products_reputation = normalize(class2)
            print(normalization_of_products_reputation)
            choice = random.choices(class2_products, normalization_of_products_reputation)
            print(choice)
            if (choice[0] == "product3"): 
                product3_counter = product3_counter + 1
            if (choice[0] == "product4"): 
                product4_counter = product4_counter + 1
            reputation(choice[0])
    print ("final counters", product1_counter, product2_counter, product3_counter,product4_counter)
        
if __name__ == "__main__":

    main()
    