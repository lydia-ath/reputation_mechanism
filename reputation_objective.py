import numpy
import matplotlib.pyplot as plt
import random
import seaborn as sns
#from scipy.stats import uniform

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
datasources = ['datasource1', 'datasource2', 'datasource3', 'datasource4', 'datasource5', 'datasource6']


federation1 = {'datasource1': 0.7, 'datasource2': 0.5, 'datasource3': 0.7, 'datasource4':0.9}
federation2 = {'datasource2': 0.9, 'datasource3': 0.7, 'datasource5': 0.1, 'datasource6': 0.75}

#help function 
def contains(diction1, diction2, key):
    if (key in diction1) and (key in diction2):
        return True
    else: 
        return False

#help function
def add(self, key, value):
    self[key] = value
 
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
            actual_value = random.uniform(target_value-0.2, target_value+0.01) #bad with big deviation
        if (minmax == 'max'):
            actual_value = random.uniform(target_value-0.01, target_value + 0.2) #bad with big deviation
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
    
    return Objective_scores;

def reputation_update_datasources(objective_scores):
    #update objective score by taking into account the old values
    for i in objective_scores:
        objective_updated = lamda*objective_old[i] + (1-lamda)*objective_scores[i]
        add(objective_old, i, objective_updated)
   
    return objective_old;

def reputation_update_providers(final_reputation):
    for i in final_reputation:
        reputation_old_providers = final_reputation
    return reputation_old_providers;

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

def main():

    transactions = ['product1', 'product2', 'product3', 'product4']
    final_Reputation_products1 = []
    final_Reputation_products2 = []
    final_Reputation_products3 = []
    final_Reputation_products4 = []
    #4 transactions with 1 product per transaction, each product is composed of 2 datasources
    subjective_metrics_names = ['accuracy', 'validity', 'value for money']
    for i in transactions:
        print ("-----------------------------------------------Transaction for",i,"-------------------------------------------------------------------")
        #assumption: where monitoring period = transaction period
        objective_values = []
        objective_for_monitoring_period = objective(quality_class1, quality_class2, quality_class1_resources, quality_class2_resources, i)
        final_Reputation_per_datasource =reputation_update_datasources(objective_for_monitoring_period)
        reputation_update_providers(final_Reputation_per_datasource)
        reputation_update_federations(final_Reputation_per_datasource)
        reputation_update_products(final_Reputation_per_datasource)

        #Graphical representation of the objective scores per monitoring period
        for j in objective_for_monitoring_period:
            objective_values.append(objective_for_monitoring_period[j])
        plt.xlabel('objective metrics')
        plt.ylabel('values of objective metrics per monitoring period')
        plt.plot(datasources, objective_values)
        plt.show()

        #Graphical representation of the reputation scores per datasource (combination subjective and objective)
        final_Reputation_datasource = []
        for j in final_Reputation_per_datasource:
            final_Reputation_datasource.append(final_Reputation_per_datasource[j])
        sns.set_style("whitegrid")
        plt.figure(figsize=(12,6))
        plt.xlabel('datasources')
        plt.ylabel('reputation scores')
        plt.plot(datasources, final_Reputation_datasource)
        plt.show()

        #Graphical representation of the reputation scores per federation
        final_Reputation_feferations = []
        for j in reputation_old_federations:
            final_Reputation_feferations.append(reputation_old_federations[j])
        federation = ['federation1', 'federation2']
        plt.plot(federation, final_Reputation_feferations)
        plt.show()

        #Graphical representation of the reputation scores per product
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