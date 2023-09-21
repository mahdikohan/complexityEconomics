import networkx as nx
import random
import matplotlib.pyplot as plt
import math

plot_state = True
graph_state = False
report_state = True

# Create an empty graph
G = nx.Graph()
# Define the number of firms and households
num_firms = 100
num_households = 1000
num_steps = 800  # Number of simulation steps
_lambda = 3     # Fix of technology
phi = 0.25      # demand production relation production = phi * demand




# Initialize households with attributes and add them to the graph
for household_id in range(num_households):
    wage = random.uniform(2000, 6000)
    liquidity = random.uniform(50000, 300000)
    demand = random.uniform(20, 100)
    household_attrs = {
        "type": "household",
        "wage": wage,
        "liquidity": liquidity,
        "demand": demand,
        "labors":[]
    }
    G.add_node(f"Household_{household_id}", **household_attrs)

# Initialize firms with attributes and add them to the graph
for firm_id in range(num_firms):
    wage = random.uniform(30000, 70000)
    liquidity = random.uniform(10000000, 50000000)
    production = random.uniform(100, 500)
    price = random.uniform(10,20)
    low_production = random.randint(1, 100)
    low_price = random.randint(1,10)
    price_boundary = [low_price, random.randint(low_price + 1,25)]
    production_boundary = [low_production, random.randint(low_production + 1, 550)]
    recent_demand =random.uniform(20, 100)
    recent_production = random.uniform(100, 500)

    firm_attrs = {
        "type": "firm",
        "wage": wage,
        "liquidity": liquidity,
        "production": production,
        "recent_production": recent_production,
        "price_boundary": price_boundary,
        "production_boundary": production_boundary,
        "price": price,
        "recent_demand": recent_demand
    }
    G.add_node(f"Firm_{firm_id}", **firm_attrs)





# ============================ recruitment ==============================
j = 0
for firm_id in range(num_firms):
    # Randomly recruit a number of households
    i = random.randint(5,math.floor(num_households/num_firms)+1)
    if j<num_households:
        for recruit in range(j,j+i):
            G.add_edge(f"Firm_{firm_id}", f"Household_{recruit}")
    j = j+i


# set known employees
for households_id in range(num_households):
    connected_firm = random.sample(range(0, num_firms), math.floor(num_firms/2))
    G.nodes[f"Household_{recruit}"]["recent_demand"] = connected_firm


if plot_state==True and graph_state==True:
    pos = nx.spring_layout(G)
    node_colors = ['skyblue' if G.nodes[node]['type'] == "household" else 'red' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, font_color='black', node_size=800)
    plt.show()


wage_households_1 = []
production_firm_1 = []
unemployment_rate = []
Bankrupt_rate = []

# Simulation loop
for step in range(num_steps):
    print(f"Step {step + 1}: Starting")
    print('====================================')

    # each households check some firms wage
    for household_id in range(num_households):
        # search a job position
        for firm_id in random.sample(range(0, num_firms), math.floor(num_firms/2)):
            if G.nodes[f"Firm_{firm_id}"]['liquidity'] < 0:
                G.remove_edges_from(list(G.edges(f"Firm_{firm_id}")))
            elif G.degree(f"Household_{household_id}") > 0 and \
                  (G.nodes[f"Firm_{firm_id}"]['wage']) > (G.nodes[f"Household_{household_id}"]['wage']):
                # print(f'new connection household_{household_id}, firm_{firm_id}')
                G.remove_edges_from(list(G.edges(f"Household_{household_id}")))
                G.add_edge(f"Household_{household_id}",f"Firm_{firm_id}")
                G.nodes[f"Firm_{firm_id}"]['wage'] = G.nodes[f"Household_{household_id}"]['wage']
            elif (G.nodes[f"Firm_{firm_id}"]['wage']) > (G.nodes[f"Household_{household_id}"]['wage']):
                G.add_edge(f"Household_{household_id}",f"Firm_{firm_id}")
                G.nodes[f"Firm_{firm_id}"]['wage'] = G.nodes[f"Household_{household_id}"]['wage']
        if G.degree(f"Household_{household_id}") == 0:
            if G.nodes[f"Household_{household_id}"]['wage'] > 0:
                G.nodes[f"Household_{household_id}"]['wage'] = 0.9 * G.nodes[f"Household_{household_id}"]['wage']
                # =============================================================================
                # print(f'unemployment new connection household_{household_id}, firm_{firm_id}')
                # if G.nodes[f"Firm_{firm_id}"]['wage'] > 0:
                #     G.add_edge(f"Household_{household_id}",f"Firm_{firm_id}")
                #     G.nodes[f"Firm_{firm_id}"]['wage'] = G.nodes[f"Household_{household_id}"]['wage']



    # production which is related to number of labor in firms
    for firm_id in range(num_firms):
        # adjust production
        G.nodes[f"Firm_{firm_id}"]["recent_production"] = phi * G.nodes[f"Firm_{firm_id}"]["recent_demand"]
        # new production
        recent_production = G.nodes[f"Firm_{firm_id}"]["recent_production"]
        G.nodes[f"Firm_{firm_id}"]['production'] = recent_production + _lambda*(G.degree(f"Firm_{firm_id}"))

        
        # labor adjustment with production status and price adjustment
        if type(recent_production) == complex:
            continue
        if G.degree(f"Firm_{firm_id}") > 1:
            # print(G.nodes[f"Firm_{firm_id}"])
            firm_production_adj_part = G.nodes[f"Firm_{firm_id}"]['production']
            firm_price_adj_part = G.nodes[f"Firm_{firm_id}"]['price']
            firm_low_production_adj_part = G.nodes[f"Firm_{firm_id}"]['production_boundary'][0]
            firm_high_production_adj_part = G.nodes[f"Firm_{firm_id}"]['production_boundary'][1]
            firm_high_price_adj_part = G.nodes[f"Firm_{firm_id}"]['price_boundary'][0]
            firm_low_price_adj_part = G.nodes[f"Firm_{firm_id}"]['price_boundary'][1]
            if firm_production_adj_part > firm_high_production_adj_part:
                fire_adj_part = random.choice(list(G.neighbors(f"Firm_{firm_id}")))
                G.remove_edge(f"Firm_{firm_id}", fire_adj_part)
                if firm_price_adj_part > firm_high_price_adj_part:
                    G.nodes[f"Firm_{firm_id}"]['price'] = firm_price_adj_part * (1+random.uniform(0.1,0.4))
                elif firm_price_adj_part < firm_low_price_adj_part:
                    G.nodes[f"Firm_{firm_id}"]['price'] = firm_price_adj_part * (1-random.uniform(0.1,0.4))
            elif firm_production_adj_part < firm_low_production_adj_part:
                # *temporary* is this we should add accurasy to it
                list_of_unmployed = [node for node in G.nodes() if G.degree(node) == 0 and G.nodes[node]['type'] == 'household']
                if list_of_unmployed:
                    hire_adj_part = random.choice(list_of_unmployed)
                G.add_edge(f"Firm_{firm_id}", hire_adj_part)
                G.nodes[hire_adj_part]['wage'] = G.nodes[f"Firm_{firm_id}"]['wage']
                if firm_price_adj_part > firm_high_price_adj_part:
                    G.nodes[f"Firm_{firm_id}"]['price'] = firm_price_adj_part * (1+random.uniform(0.1,0.4))
                elif firm_price_adj_part < firm_low_price_adj_part:
                    G.nodes[f"Firm_{firm_id}"]['price'] = firm_price_adj_part * (1-random.uniform(0.1,0.4))



    # pay wage and adjust wage households
    Bankrupt_c = 0
    for firm_id in range(num_firms):
        liquidity = G.nodes[f"Firm_{firm_id}"]["liquidity"]
        # print(f"liquidity of Firm_{firm_id}: {liquidity}")
        if liquidity > 0:
            labors = G.neighbors(f"Firm_{firm_id}")
            G.nodes[f"Firm_{firm_id}"]['wage'] = wage
            for labor in labors:
                G.nodes[f"Firm_{firm_id}"]["liquidity"] -= wage
                G.nodes[labor]["liquidity"] += wage

            # ===================collecting plot data=============================
                if labor=="Household_6":
                    wage_households_1.append(G.nodes[labor]["liquidity"])

            if firm_id == 6:
                production_firm_1.append(G.nodes[f"Firm_{firm_id}"]["production"])
            # ====================================================================

        else:
            Bankrupt_c += 1
            print(f'Firm_{firm_id} Bankrupt')
    Bankrupt_rate.append(Bankrupt_c/num_firms*100)




    # preparing for update recent demand
    for firm_id in connected_firm:
        G.nodes[f'Firm_{firm_id}']['recent_demand'] = 0

    # consumption
    for household_id in range(num_households):
        # random selection for connection
        connected_firm = random.sample(range(0, num_firms), math.floor(num_firms/2))
        total_price = 0
        for firm_id in connected_firm:
            total_price += G.nodes[f'Firm_{firm_id}']['price']
        avg_price = total_price/len(connected_firm)
        # buy things
        for firm_id in connected_firm:
            demand = ((G.nodes[f'Household_{household_id}']['liquidity'] / avg_price)**0.9)
            # print('==============demand of consumer==============')
            # print(G.nodes[f'Household_{household_id}'], f'price: {avg_price}')
            # input()
            consumption = demand * avg_price
            G.nodes[f'Firm_{firm_id}']['recent_demand'] += demand
            # if type(consumption)==complex:
                # print(f"consumprion is complex Household_{household_id}")
                # print(G.nodes[f'Household_{household_id}'])
                # input()
            if type(consumption)!= complex and consumption > 0:
                firm_production = G.nodes[f'Firm_{firm_id}']['production']
                if type(firm_production) != complex and firm_production > 0:
                    if G.nodes[f'Firm_{firm_id}']['production'] > demand:
                        G.nodes[f'Household_{household_id}']['liquidity'] -= consumption
                        G.nodes[f'Firm_{firm_id}']['liquidity'] += consumption
                    elif G.nodes[f'Firm_{firm_id}']['production'] < demand:
                        consumption -= G.nodes[f'Household_{household_id}']['liquidity'] 
                        G.nodes[f'Firm_{firm_id}']['liquidity'] += consumption
                        G.nodes[f'Firm_{firm_id}']['production'] = 0
                else:
                    break
                    print(f"Firm_{firm_id}: production is zero")
            else:
                break
                print(f"Household_{household_id}: consumption is zero")
                



    unem_c = 0
    for household_id in range(num_households):
        if G.degree(f"Household_{household_id}")==0:
            unem_c += 1
    
    u_r = unem_c / num_households * 100
    unemployment_rate.append(u_r)
    print(f'unemployment rate: {u_r} %')
    print('==============================')

    
if plot_state==True:
    plt.plot(wage_households_1)
    plt.title('Wage')
    plt.show()

    plt.plot(production_firm_1)
    plt.title('Production')
    plt.show()

    plt.plot(unemployment_rate)
    plt.title('unemployment rate')
    plt.show()

    plt.plot(Bankrupt_rate)
    plt.title('Bankrupt rate')
    plt.show()

if plot_state==True and graph_state==True:
    # Visualize the graph to show recruitment
    pos = nx.spring_layout(G)
    node_colors = ['skyblue' if G.nodes[node]['type'] == "household" else 'yellow' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, font_color='black', node_size=800)
    plt.show()


if report_state == True:  
    print(f'unemployment rate: {sum(unemployment_rate)/len(unemployment_rate)} %')
    print(f'Bankrupt rate: {sum(Bankrupt_rate)/len(Bankrupt_rate)} %')
