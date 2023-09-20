import networkx as nx
import random
import matplotlib.pyplot as plt
import math

# Create an empty graph
G = nx.Graph()
# Define the number of firms and households
num_firms = 10
num_households = 100
num_steps = 6  # Number of simulation steps










# Initialize households with attributes and add them to the graph
for household_id in range(num_households):
    wage = random.uniform(2000, 6000)
    liquidity = random.uniform(5000, 30000)
    demand = random.uniform(200, 1000)
    household_attrs = {
        "type": "household",
        "wage": wage,
        "liquidity": liquidity,
        "demand": demand,
    }
    G.add_node(f"Household_{household_id}", **household_attrs)

# Initialize firms with attributes and add them to the graph
for firm_id in range(num_firms):
    wage = random.uniform(30000, 70000)
    liquidity = random.uniform(1000000, 5000000)
    production = random.uniform(100, 500)
    price = random.uniform(10,20)
    firm_attrs = {
        "type": "firm",
        "wage": wage,
        "liquidity": liquidity,
        "production": production,
        "price": price
    }
    G.add_node(f"Firm_{firm_id}", **firm_attrs)


# ============================ recruitment ==============================
j = 0
for firm_id in range(num_firms):
    # Randomly recruit a number of households
    i = random.randint(5,math.floor(num_households/num_firms)+1)
    
    if j<num_households:
        for recruit in range(j,j+i):
            # print(firm_id,recruit)
            G.add_edge(f"Firm_{firm_id}", f"Household_{recruit}")
    j = j+i

# # checking number of firms for each households
# for firm_id in range(num_firms):
#     print(G.degree(f"Firm_{firm_id}"))


pos = nx.spring_layout(G)
node_colors = ['skyblue' if G.nodes[node]['type'] == "household" else 'red' for node in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=node_colors, font_color='black', node_size=800)
plt.show()


wage_households_1 = []

# Simulation loop
for step in range(num_steps):
    print(f"Step {step + 1}: Done")
    print('===========================')

    # each households check some firms wage
    for household_id in range(num_households):

        # search a job position
        for firm_id in random.sample(range(0, num_firms), math.floor(num_firms/2)):
            if G.nodes[f"Firm_{firm_id}"]['liquidity'] < 0:
                G.remove_edges_from(list(G.edges(f"Firm_{firm_id}")))
                

            elif G.degree(f"Household_{household_id}") > 0 and (G.nodes[f"Firm_{firm_id}"]['wage']) > (G.nodes[f"Household_{household_id}"]['wage']):
                # print(f'new connection household_{household_id}, firm_{firm_id}')
                G.remove_edges_from(list(G.edges(f"Household_{household_id}")))
                G.add_edge(f"Household_{household_id}",f"Firm_{firm_id}")
                G.nodes[f"Firm_{firm_id}"]['wage'] = G.nodes[f"Household_{household_id}"]['wage']
                

            # print('*** Degree: '+str(G.degree(f"Household_{household_id}")))
            
            elif G.degree(f"Household_{household_id}") == 0:
                # print(f'unemployment new connection household_{household_id}, firm_{firm_id}')
                if G.nodes[f"Firm_{firm_id}"]['wage'] > 0:
                    G.add_edge(f"Household_{household_id}",f"Firm_{firm_id}")
                    G.nodes[f"Firm_{firm_id}"]['wage'] = G.nodes[f"Household_{household_id}"]['wage']

        

    # pay wage and adjust wage
    for firm_id in range(num_firms):
        liquidity = G.nodes[f"Firm_{firm_id}"]["liquidity"]
        print(f"liquidity of Firm_{firm_id}: {liquidity}")
        if liquidity > 0:
            labors = G.neighbors(f"Firm_{firm_id}")
            # wage = G.nodes[f"Firm_{firm_id}"]["liquidity"] / G.degree(f"Firm_{firm_id}") 

            G.nodes[f"Firm_{firm_id}"]['wage'] = wage
            
            for labor in labors:
                G.nodes[f"Firm_{firm_id}"]["liquidity"] -= wage
                G.nodes[labor]["liquidity"] += wage

                if labor=="Household_1":
                    # print(G.nodes[labor]["liquidity"])
                    wage_households_1.append(G.nodes[labor]["liquidity"])
        else:
            print(f'Firm_{firm_id} Bankrupt')


    # consumption
    for household_id in range(num_households):

        # search a job position
        for firm_id in random.sample(range(0, num_firms), math.floor(num_firms/2)):
            pass
            

# Visualize the graph to show recruitment
pos = nx.spring_layout(G)
node_colors = ['skyblue' if G.nodes[node]['type'] == "household" else 'yellow' for node in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=node_colors, font_color='black', node_size=800)
plt.show()
