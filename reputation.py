import numpy
import matplotlib.pyplot as plt
import random
import seaborn as sns
#from scipy.stats import uniform


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
reputation_old_products = {'product1': 0.5, 'product2': 0.5, 'product3': 0.5, 'product4': 0.5}

final_reputation_scores = {'datasource1':0.0, 'datasource2':0.0, 'datasource3':0.0, 'datasource4':0.0, 'datasource5':0.0, 'datasource6':0.0}

#global variables
lamda = 0.8
weight = 0.8

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

#check deviation
def deviation():
    speed = [86,87,88,86,87,85,86]
    x = numpy.std(speed)

    x = numpy.random.uniform(0.0, 5.0, 250)
    plt.hist(x, 5)
    plt.show()

    return print(x)

#uniform distribution
def uniform_distribution():
    n = 10000
    start = 10
    width = 20
    data_uniform = uniform.rvs(size=n, loc = start, scale=width)
    ax = sns.distplot(data_uniform, bins=100, kde=True, color='skyblue', hist_kws={"linewidth": 15,'alpha':1})
    ax.set(xlabel='Uniform Distribution ', ylabel='Frequency')
    return ax

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
    print('ppppppppppppppppppp', minmax, product)
    if (product == 'product1'): #first transaction = first monitoring period
        if (minmax == 'min'):
            actual_value = random.uniform(target_value-0.02, target_value +0.05) #good with low deviation
            deviation_actual_value = numpy.std(actual_value)
        if (minmax == 'max'):
            actual_value = random.uniform(target_value-0.05, target_value+0.01) #good with low deviation
            deviation_actual_value = numpy.std(actual_value)
    #datasources follow different uniform distributions 
    #candidate_values = []
    if (product == 'product2' or product == 'product3'): #second transaction = second monitoring period
        if (datasource == 'datasource1' or'datasource3' or'datasource5'):
            print('ppppppppppppppppppp', minmax, datasource)
            if (minmax == 'min'):
                actual_value = random.uniform(target_value-0.1, target_value + 0.1) #good with high deviation
                deviation_actual_value = numpy.std(actual_value)
            if (minmax == 'max'):
                actual_value = random.uniform(target_value-0.2, target_value+0.01) #good with high deviation
                deviation_actual_value = numpy.std(actual_value)
        if (datasource == 'datasource2' or'datasource4' or'datasource6'):
            if (minmax == 'min'):
                actual_value = random.uniform(target_value-0.5, target_value + 0.01) #bad with low deviation
                deviation_actual_value = numpy.std(actual_value)
            if (minmax == 'max'):
                actual_value = random.uniform(target_value-0.01, target_value+0.05) #bad with low deviation
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
        if (minmax == 'min'):
            actual_value = random.uniform(target_value-0.2, target_value+0.01) #bad with big deviation
            deviation_actual_value = numpy.std(actual_value)
        if (minmax == 'max'):
            actual_value = random.uniform(target_value-0.01, target_value + 0.2) #bad with big deviation
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
            minmax = min_max[i]
            actual_value = choose_distribution(product, target_value, j, minmax)
            deviation_actual_value = numpy.std(actual_value)
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
            minmax = min_max[i]
            actual_value = choose_distribution(product, target_value, j, minmax)
            deviation_actual_value = numpy.std(actual_value)
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

#one subjective profile per application type
#products that belong to the same application type have same subjective vector 
#User specific --> per transaction --> use can select the weight and/or the subjective metrics,
def subjective_vector_choise(product):
    if (product == "product1"):
        for i in subjective_metrics:
            subjective_metric_value = random.uniform(0.8, 1)
            deviation_actual_value = numpy.std(subjective_metric_value)
            add(subjective_metrics, i, subjective_metric_value)
    if (product == "product2" or product == "product3"):
        for i in subjective_metrics:
            subjective_metric_value = random.uniform(0.2, 0.8)
            deviation_actual_value = numpy.std(subjective_metric_value)
            add(subjective_metrics, i, subjective_metric_value)
    if (product == "product4"):
        for i in subjective_metrics:
            subjective_metric_value = random.uniform(0, 0.2)
            deviation_actual_value = numpy.std(subjective_metric_value)
            add(subjective_metrics, i, subjective_metric_value)
            print (deviation_actual_value)
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

def reputation_update_datasources(objective_scores, subjective_score, product):
    print("innnnnnnnnnn objectives", objective_scores)
    print("innnnnnnnnnn subjective", subjective_score)
    print("innnnnnnnnnn product", product)
    #datasource 2 and datasource 3 contribute in the formation of multiple products that belong to different services/quality classes
    #so they will have multiple values in the same monitoring period based on those quality classes
    
    #update objective score by taking into account the old values
    for i in objective_scores:
        objective_updated = lamda*objective_old[i] + (1-lamda)*objective_scores[i]
        add(objective_old, i, objective_updated)
    print ("looooooolllllllllllllll", objective_old)

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
    print ("providersssssssssss", reputation_old_providers)
    return reputation_old_providers;

#federation 1 --> provider1,2,3,4 --> datasource1,2,3,4
#federation 2 --> provider2,3,5,6 --> datasource2,3,5,6
def reputation_update_federations(final_reputation):
    current_federation1 = 0
    current_federation2 = 0
    for i in final_reputation:
        if (contains(final_reputation, federation1, i) == True):
            #print ("OMGGGGGGGGGGG", final_reputation[i])
            current_federation1 = current_federation1 + final_reputation[i]*federation1[i]
        if (contains(final_reputation, federation2, i) == True):
            current_federation2 = current_federation2 + final_reputation[i]*federation2[i]
    #there is no need to see the old value of the federation as the datasources already taking into account the old values 
    final_federation1 = current_federation1 / sum(federation1.values())
    reputation_old_federations['federation1'] = final_federation1
    final_federation2 = current_federation2 / sum(federation2.values())
    reputation_old_federations['federation2'] = final_federation2
    print("OMGGGGGGGGGGGGGGGGG", reputation_old_federations)
    return reputation_old_federations;

#update current product of the traction and the affected ones that may have one or multiple common datasources
def reputation_update_products(final_reputation):
    current_product1 =0
    for i in final_reputation:
        if(contains(final_reputation, product1, i)== True):
            #print("FUCKKKKKKKKKKKKKKKKKKKKK", final_reputation[i], product1_weights[i])
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

    print ("productsssssssssssssssssssssssssssss", reputation_old_products)
    return reputation_old_products;

def main():

    transactions = ['product1', 'product2', 'product3', 'product4']
    final_Reputation_products1 = []
    final_Reputation_products2 = []
    final_Reputation_products3 = []
    final_Reputation_products4 = []
    #4 transactions with 1 product per transaction, each product is composed of 2 datasources
    for i in transactions:
        print ("-----------------------------------------------Transaction for",i,"-------------------------------------------------------------------")
        subjective_metrics_per_transaction = subjective_vector_choise(i)
        product_subjective = subjective(i, subjective_metrics_per_transaction)
        #assumption: where monitoring period = transaction period
        objective_for_monitoring_period = objective(quality_class1, quality_class2, quality_class1_resources, quality_class2_resources, i)
        final_Reputation_per_datasource =reputation_update_datasources(objective_for_monitoring_period, product_subjective, i)
        reputation_update_providers(final_Reputation_per_datasource)
        reputation_update_federations(final_Reputation_per_datasource)
        reputation_update_products(final_Reputation_per_datasource)
        final_Reputation_datasource = []
        for j in final_Reputation_per_datasource:
            final_Reputation_datasource.append(final_Reputation_per_datasource[j])
        sns.set_style("whitegrid")
        plt.figure(figsize=(12,6))
        plt.xlabel('datasources')
        plt.ylabel('reputation scores')
        plt.plot(datasources, final_Reputation_datasource)
        plt.show()

        final_Reputation_feferations = []
        for j in reputation_old_federations:
            final_Reputation_feferations.append(reputation_old_federations[j])
        federation = ['federation1', 'federation2']
        plt.plot(federation, final_Reputation_feferations)
        plt.show()

        if (i == 'product1'):
            for j in reputation_old_products:
                final_Reputation_products1.append(reputation_old_products[j])
            plt.xlabel('transactions - products')
            plt.ylabel('reputation scores of products')
            plt.plot(transactions, final_Reputation_products1)
            plt.show()
            plt.bar(transactions, final_Reputation_products1)
            plt.show()
        if (i == 'product2'):
            for j in reputation_old_products:
                final_Reputation_products2.append(reputation_old_products[j])
            plt.xlabel('transactions - products')
            plt.ylabel('reputation scores of products')
            plt.plot(transactions, final_Reputation_products2)
            plt.show()
            plt.bar(transactions, final_Reputation_products2)
            plt.show()
        if (i == 'product3'):
            for j in reputation_old_products:
                final_Reputation_products3.append(reputation_old_products[j])
            plt.xlabel('transactions - products')
            plt.ylabel('reputation scores of products')
            plt.plot(transactions, final_Reputation_products3)
            plt.show()
            plt.bar(transactions, final_Reputation_products3)
            plt.show()
        if (i == 'product4'):
            for j in reputation_old_products:
                final_Reputation_products4.append(reputation_old_products[j])
            plt.xlabel('transactions - products')
            plt.ylabel('reputation scores of products')
            plt.plot(transactions, final_Reputation_products4)
            plt.show()
            plt.bar(transactions, final_Reputation_products4)
            plt.show()
    sns.set_style("whitegrid")
    plt.figure(figsize=(12,6))
    plt.xlabel('transactions - products')
    plt.ylabel('reputation scores of products')
    plt.plot(transactions, final_Reputation_products1, marker = 'o')
    plt.plot(transactions, final_Reputation_products2, marker = 'o')
    plt.plot(transactions, final_Reputation_products3, marker = 'o')
    plt.plot(transactions, final_Reputation_products4, marker = 'o')
    plt.show()
    plt.bar(transactions, final_Reputation_products1)
    plt.bar(transactions, final_Reputation_products2)
    plt.bar(transactions, final_Reputation_products3)
    plt.bar(transactions, final_Reputation_products4)
    plt.show()
    plt.plot(federation, final_Reputation_feferations, marker = 'o')
    plt.show()
    plt.bar(federation, final_Reputation_feferations)
    plt.show()
if __name__ == "__main__":
    n=0
    #while (n<10):
    #    print ("-----------------------------------------------Round",n,"----------------------------------------------------------------------------")
    main()