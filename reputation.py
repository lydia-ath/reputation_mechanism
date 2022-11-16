import numpy
import matplotlib.pyplot as plt
import random

#global variables, dictionairies, lists

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
objective_old = {'datasource1':0.0, 'datasource2':0.0, 'datasource3':0.0, 'datasource4':0.0, 'datasource5':0.0, 'datasource6':0.0}
subjective_old = {'datasource1':0.0, 'datasource2':0.0, 'datasource3':0.0, 'datasource4':0.0, 'datasource5':0.0, 'datasource6':0.0}
reputation_old_providers = {'provider1':0.0, 'provider2':0.0, 'provider3':0.0, 'provider4':0.0, 'provider5':0.0, 'provider6':0.0}
reputation_old_federations = {'federation1': 0.0, 'federation2': 0.0}
reputation_old_products = {'product1': 0.0, 'product2': 0.0, 'product3': 0.0, 'product4': 0.0}
final_reputation_scores = {'datasource1':0.0, 'datasource2':0.0, 'datasource3':0.0, 'datasource4':0.0, 'datasource5':0.0, 'datasource6':0.0}

#global variables
lamda = 0.8
weight = 0.8

#product 1 and porduct 2 belongs to service class 1 and have quality class 1
product1 = ['datasource1', 'datasource2']
product2 = ['datasource3', 'datasource4']

#product 3 and porduct 4 belongs to service class 2 and have quality class 2
product3 = ['datasource2', 'datasource3']
product4 = ['datasource5', 'datasource6']
#datasource 2 and datasource 3 contribute in the formation of multiple products that belong to different service/quqlity classes
#so they will have multiple values in the same monitoring period based on those quality classes
datasources = ['datasource1', 'datasource2', 'datasource3', 'datasource4', 'datasource5', 'datasource6']


federation1 = ['datasource1', 'datasource2', 'datasource3', 'datasource4']
federation2 = ['datasource2', 'datasource3', 'datasource5', 'datasource6']

#check deviation
def deviation():
    speed = [86,87,88,86,87,85,86]
    x = numpy.std(speed)

    x = numpy.random.uniform(0.0, 5.0, 250)
    plt.hist(x, 5)
    plt.show()

    return print(x)

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
def choose_distribution(product, target_value, datasource):
    #all datasources follow uniform good distribution with low deviation(=low noise, values near to mean value)
    if (product == 'product1'): #first transaction = first monitoring period
        actual_value = random.uniform(target_value-0.25, 1.0) #good with low deviation
        deviation_actual_value = numpy.std(actual_value)
    #datasources follow different uniform distributions 
    #candidate_values = []
    if (product == 'product2' or product == 'product3'): #second transaction = second monitoring period
        if (datasource == 'datasource3'):
            actual_value = random.uniform(target_value-0.25, 1.0) #good with high deviation
            deviation_actual_value = numpy.std(actual_value)
        if (datasource == 'datasource2' or'datasource4'):
            actual_value = random.uniform(target_value-0.25, 1.0) #bad with high deviation
            deviation_actual_value = numpy.std(actual_value)
        #actual_value1 = random.uniform(target_value-0.25, 1.0) #bad with low deviation
        #candidate_values.append(actual_value1)
        #actual_value2 = random.uniform(target_value-0.25, 1.0) #good with low deviation
        #candidate_values.append(actual_value2)
        #actual_value3 = random.uniform(target_value-0.25, 1.0) #good with high deviation
        #candidate_values.append(actual_value3)
        #actual_value4 = random.uniform(target_value-0.25, 1.0) #bad with high deviation
        #candidate_values.append(actual_value4)
        #print ("the candidate values from the four kind of distributions are: ", candidate_values)
        #actual_value = candidate_values[random.randrange(len(candidate_values))]
        #print ("the selected distribution is: ", actual_value)
        #deviation_actual_value = numpy.std(actual_value)
    #all datasources follow uniform bad distribution with high deviation(=high noise, values dispare)
    if (product == 'product4'): #forth transaction = forth monitoring period
        actual_value = random.uniform(target_value-0.25, 1.0) #bad with low deviation
        deviation_actual_value = numpy.std(actual_value)
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
            actual_value = choose_distribution(product, target_value, j)
            deviation_actual_value = numpy.std(actual_value)
            minmax = min_max[i]
            print ('the objective metric is: ', i)
            print ('target value:', target_value)
            print ('actual value:', actual_value)
            print ('deviation for that set of values:', deviation_actual_value)
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
            actual_value = choose_distribution(product, target_value, j)
            deviation_actual_value = numpy.std(actual_value)
            minmax = min_max[i]
            print ('the objective metric is: ', i)
            print ('target value:', target_value)
            print ('actual value:', actual_value)
            print ('deviation for that set of values:', deviation_actual_value)
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
            print("mmmmmmmmmm", objective_scores_qualityclass1[n], objective_scores_qualityclass2[n])
            final_objective_score = (objective_scores_qualityclass1[n]+objective_scores_qualityclass2[n])/2
            print (n, " belogns to multiple quality classes and its final reputation score is: ", final_objective_score)
            add(Objective_scores, n, final_objective_score)
    
    print(Objective_scores)
    return Objective_scores;

def subjective():
    subjective_score = random.uniform(0.1, 1.0)
    deviation_actual_value = numpy.std(subjective_score)
    print (deviation_actual_value)
    return subjective_score;

def reputation_update_datasources(objective_scores, subjective_score, product):
    print("innnnnnnnnnn objectives", objective_scores)
    print("innnnnnnnnnn subjective", subjective_score)
    print("innnnnnnnnnn product", product)
    #datasource 2 and datasource 3 contribute in the formation of multiple products that belong to different service/quqlity classes
    #so they will have multiple values in the same monitoring period based on those quality classes
    
    #update objective score by taking into account the old values
    for i in objective_scores:
        objective_updated = lamda*objective_old[i] + (1-lamda)*objective_scores[i]
        add(objective_old, i, objective_updated)
    #print ("looooooolllllllllllllll", objective_old)

    #update subjective score by taking into account the old values
    if(product == 'product1'):
        for i in product1:
            print (i)
            print ('mplaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', subjective_score, subjective_old)
            subjective_updated = lamda*subjective_old[i] + (1-lamda)*subjective_score
            print (subjective_updated)
            add(subjective_old, i, subjective_updated)

            #final reputation score after the combination of subjective and objective for the datasources of product 1
            #where the objective_old and the subjective_old dictionaries are now updated 
            #print("OMGGGGGGGGGGGGGGG", objective_old[i])
            final_reputation = weight*objective_old[i] + (1-weight)*subjective_old[i]
            add(final_reputation_scores, i, final_reputation)

    if(product == 'product2'):
        for i in product2:
            print (i)
            print ('mplaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', subjective_score, subjective_old)
            subjective_updated = lamda*subjective_old[i] + (1-lamda)*subjective_score
            print (subjective_updated)
            add(subjective_old, i, subjective_updated)

            #final reputation score after the combination of subjective and objective
            final_reputation = weight*objective_old[i] + (1-weight)*subjective_old[i]
            add(final_reputation_scores, i, final_reputation)

    if(product == 'product3'):
        for i in product3:
            print (i)
            print ('mplaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', subjective_score, subjective_old)
            subjective_updated = lamda*subjective_old[i] + (1-lamda)*subjective_score
            print (subjective_updated)
            add(subjective_old, i, subjective_updated)

            #final reputation score after the combination of subjective and objective
            final_reputation = weight*objective_old[i] + (1-weight)*subjective_old[i]
            add(final_reputation_scores, i, final_reputation)

    if(product == 'product4'):
        for i in product4:
            print (i)
            print ('mplaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', subjective_score, subjective_old)
            subjective_updated = lamda*subjective_old[i] + (1-lamda)*subjective_score
            print (subjective_updated)
            add(subjective_old, i, subjective_updated)

            #final reputation score after the combination of subjective and objective
            final_reputation = weight*objective_old[i] + (1-weight)*subjective_old[i]
            add(final_reputation_scores, i, final_reputation)

    print ('final reputation scores: ', final_reputation_scores)
    return final_reputation_scores;


#provider 1 --> datasource1, provider2--> datasource2, etc
#so, in this case updated reputation  of datasource = updated reputation of provider
#datasources taking into account the previous old value so there is no need to taking into acount also here
def reputation_update_providers(final_reputation):
    for i in final_reputation:
        reputation_old_providers = final_reputation
    #print ("providersssssssssss", reputation_old_providers)
    return reputation_old_providers;

#federation 1 --> provider1,2,3,4 --> datasource1,2,3,4
#federation 2 --> provider2,3,5,6 --> datasource2,3,5,6
def reputation_update_federations(final_reputation):
    current_federation1 = 0
    current_federation2 = 0
    for i in final_reputation:
        if (contains(final_reputation, federation1, i) == True):
            #print ("OMGGGGGGGGGGG", final_reputation[i])
            current_federation1 = current_federation1 + final_reputation[i]
        if (final_reputation, federation2, i):
            current_federation2 = current_federation2 + final_reputation[i]
    #there is no need to see the old value of the federation as the datasources already taking into account the old values 
    final_federation1 = current_federation1 / len(federation1)
    reputation_old_federations['federation1'] = final_federation1
    final_federation2 = current_federation2 / len(federation2)
    reputation_old_federations['federation2'] = final_federation2
    print("OMGGGGGGGGGGGGGGGGG", reputation_old_federations)
    return reputation_old_federations;

#update current product of the traction and the affected ones that may have one or multiple common datasources
def reputation_update_products(final_reputation):
    
    final_product1 = (final_reputation['datasource1'] + final_reputation['datasource2'])/len(product1)
    reputation_old_products['product1']=final_product1

    final_product2 = (final_reputation['datasource3'] + final_reputation['datasource4'])/len(product2)
    reputation_old_products['product2']=final_product2

    final_product3 = (final_reputation['datasource2'] + final_reputation['datasource3'])/len(product3)
    reputation_old_products['product3']=final_product3

    final_product4 = (final_reputation['datasource5'] + final_reputation['datasource6'])/len(product4)
    reputation_old_products['product4']=final_product4

    print ("productsssssssssssssssssssssssssssss", reputation_old_products)
    return reputation_old_products;

def main():

    transactions = ['product1', 'product2', 'product3', 'product4']
    #4 transactions with 1 product per transaction, each product is composed of 2 datasources
    for i in transactions:
        print ("-----------------------------------------------Transaction for",i, "-------------------------------------------------------------------")
        product_subjective = subjective()
        #where monitoring period = transaction period
        objective_for_monitoring_period = objective(quality_class1, quality_class2, quality_class1_resources, quality_class2_resources, i)
        final_Reputation_per_datasource =reputation_update_datasources(objective_for_monitoring_period, product_subjective, i)
        reputation_update_providers(final_Reputation_per_datasource)
        reputation_update_federations(final_Reputation_per_datasource)
        reputation_update_products(final_Reputation_per_datasource)

if __name__ == "__main__":
    main()