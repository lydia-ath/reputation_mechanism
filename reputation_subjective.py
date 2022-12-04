import numpy
import matplotlib.pyplot as plt
import random
import seaborn as sns
#from scipy.stats import uniform


#global variables, dictionairies, lists
subjective_metrics = {'accuracy': 0.0, 'availability': 0.0, 'validity':0.0}
subjective_metrics_weights1 = {'accuracy': 0.5, 'availability': 0.3, 'validity':0.2}
subjective_metrics_weights2 = {'accuracy': 0.1, 'availability': 0.1, 'validity':0.8}

    
#quality class datasources
quality_class1_resources = ['datasource1', 'datasource2', 'datasource3', 'datasource4']
quality_class2_resources = ['datasource2', 'datasource3', 'datasource5', 'datasource6']

#initialization of reputation scores 
subjective_old = {'datasource1':1.0, 'datasource2':1.0, 'datasource3':1.0, 'datasource4':1.0, 'datasource5':1.0, 'datasource6':1.0}

reputation_old_providers = {'provider1':1.0, 'provider2':1.0, 'provider3':1.0, 'provider4':1.0, 'provider5':1.0, 'provider6':1.0}
reputation_old_federations = {'federation1': 1.0, 'federation2': 1.0}
reputation_old_products = {'product1': 1.0, 'product2': 1.0, 'product3': 1.0, 'product4': 1.0}

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

#one subjective profile per application type
#products that belong to the same application type have same subjective vector 
#User specific --> per transaction --> use can select the weight and/or the subjective metrics,
def subjective_vector_choise(product):
    if (product == "product1"):
        for i in subjective_metrics:
            subjective_metric_value = random.uniform(0.8, 1)
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

def reputation_update_datasources(subjective_score, product):

    #update subjective score by taking into account the old values
    if(product == 'product1'):
        for i in product1:
            subjective_updated = lamda*subjective_old[i] + (1-lamda)*subjective_score
            add(subjective_old, i, subjective_updated)
            final_reputation = subjective_updated
            add(final_reputation_scores, i, final_reputation)

    if(product == 'product2'):
        for i in product2:
            subjective_updated = lamda*subjective_old[i] + (1-lamda)*subjective_score
            add(subjective_old, i, subjective_updated)
            final_reputation = subjective_updated
            add(final_reputation_scores, i, final_reputation)

    if(product == 'product3'):
        for i in product3:
            subjective_updated = lamda*subjective_old[i] + (1-lamda)*subjective_score
            add(subjective_old, i, subjective_updated)
            final_reputation = subjective_updated
            add(final_reputation_scores, i, final_reputation)

    if(product == 'product4'):
        for i in product4:
            subjective_updated = lamda*subjective_old[i] + (1-lamda)*subjective_score
            add(subjective_old, i, subjective_updated)
            final_reputation = subjective_updated
            add(final_reputation_scores, i, final_reputation)

    print ('final reputation scores: ', final_reputation_scores)
    return final_reputation_scores;


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
        subjective_metrics_per_transaction = subjective_vector_choise(i)
        subjective_values = []
        product_subjective = subjective(i, subjective_metrics_per_transaction)
        final_Reputation_per_datasource =reputation_update_datasources(product_subjective, i)
        reputation_update_providers(final_Reputation_per_datasource)
        reputation_update_federations(final_Reputation_per_datasource)
        reputation_update_products(final_Reputation_per_datasource)

        #Graphical representation of the subjective scores choises per transaction
        for j in subjective_metrics_per_transaction:
            subjective_values.append(subjective_metrics_per_transaction[j])
        plt.xlabel('subjective metrics')
        plt.ylabel('values of subjective metrics per transaction')
        plt.plot(subjective_metrics_names, subjective_values)
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